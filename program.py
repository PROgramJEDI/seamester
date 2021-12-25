import itertools
import numpy as np
import pandas as pd

from typing import Iterable, Optional
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from collections.abc import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# to display each course/semester/
# the .exe file can read a DB file that will contain the courses, such that the user will have to download the DB only.

Base = declarative_base()
engine = create_engine(f'sqlite:///seamester.db')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def populate():
	from groups import GROUPS
	from courses import COURSES

	session.add_all(GROUPS + COURSES)



class Group(Base):
	__tablename__ = 'groups'

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey('courses.id'))

	title = Column(String)
	platform = Column(String)
	link = Column(String)
	description = Column(String)

	def __init__(self, 
		title: str, 
		platform: str,  
		link: str,
		description: Optional[str] = None) -> None:

		self.title = title
		self.platform = platform
		self.link = link
		self.description = description



class Course(Base):
	__tablename__ = 'courses'

	id = Column(Integer, primary_key=True)
	parent_id = Column(Integer, ForeignKey('courses.id'))
	semester_id = Column(Integer, ForeignKey('semesters.id'))

	number = Column(Integer)
	title = Column(String)
	description = Column(String)
	degree = Column(String)

	must = Column(Boolean)
	points = Column(Integer)
	difficulty = Column(Float)
	link = Column(String)

	summer = Column(Boolean)
	took = Column(Boolean)
	cost = Column(Integer)

	_groups = relationship('Group')
	_prerequisites = relationship('Course')

	def __init__(
		self, 
		number: int, 
		title: str, 
		description: str, 
		degree: str,
		must: bool,
		points: int,
		difficulty: float, 
		link: str,
		summer: bool,
		took: bool = False,
		cost: Optional[int] = None,
		groups: Optional[Iterable[Group]] = None, 
		prerequisites: Optional[Iterable] = None) -> None:

		self.number = number
		self.title = title
		self.description = description
		self.degree = degree

		self.must = must
		self.points = points
		self.difficulty = difficulty
		self.link = link

		self.summer = summer
		self.took = took
		self.cost = cost

		self.groups = groups if groups else []
		self.prerequisites = prerequisites if prerequisites else []

	def __repr__(self):
		return f'Course(title={self.title}, summer={self.summer}, took={self.took})'

	def __enter__(self): pass


class Semester(Base):
	__tablename__ = 'semesters'

	id = Column(Integer, primary_key=True)
	degree_id = Column(Integer, ForeignKey('degrees.id'))

	number = Column(Integer)
	summer = Column(Boolean)

	_courses = relationship('Course')

	def __init__(
		self, 
		courses: Iterable[Course],
		summer: bool,
		check: bool = True) -> None:

		self._courses = courses
		self._summer = summer

		if check: 
			self.courses; self.summer

	def __repr__(self):
		f = lambda course: {
				'Title': course.title,
				'Summer': course.summer,
				'Took': course.took,
				'Difficulty': course.difficulty
			}
		return pd.DataFrame.from_records(f(x) for x in self.courses).to_string()

	def __getitem__(self, index):
		return self.courses[index]

	def _courses_types(self):
		is_summer, is_summer2 = itertools.tee(map(lambda x: x.summer, self._courses), 2)
		return (all(is_summer), not any(is_summer2))

	def _are_valid_courses(self):
		f = self._courses_types()
		return (f[0] or f[1]) and \
		all(map(lambda course: Semester._fulfilled_prerequisites(course.prerequisites), self._courses))

	@staticmethod
	def _fulfilled_prerequisites(courses):
		return all(map(lambda course: course.took, courses))

	@property
	def courses(self):
		if self._are_valid_courses():
			return np.array(self._courses)
		raise ValueError('+ All the given courses must be of the same semester type (summer / not summer)!')
			
	@property
	def summer(self):
		f = self._courses_types()
		if (f[0] and self._summer) or (f[1] and not self._summer):
			return self._summer
		raise ValueError('+ self.summer must be True if the given courses are summer courses, and the opposite!')

	def take(self):
		for x in self.courses:
			x.took = True

	@classmethod
	def recommend(
		self, 
		n_courses: int, 
		n_points: int = None,
		n_musts: int = None,
		
		avg_difficulty: float = None, # selection based on an diff average difficulty.
		avg_cost: float = None,
		
		difficulty_treshold: float = None,
		cost_treshold: float = None,
		degree_treshold: Iterable[str] = None): # selection based on a diff treshold for each course.

		def n_recommender(iterable, prop, func):
			return func([x.__dict__[prop] for x in iterable])

		def treshold_recommender(iterable, prop, tresh):
			return filter(lambda x: x.__dict__[prop] <= tresh, iterable)

		def avg_recommender(iterable: Iterable, prop: str, average: float, n_courses: int):
			'''
			if 2 courses were given with difficulties [3, 7] - for a semester with 4
			courses, what is the combination that it's average is 5?
			[3, 7, 5, 5] / 4 = 5, ... -> avg * len(total_number_of_courses) - sum_of_given_difficulties = 
			'''

			from itertools import combinations
			sigma = average * (len(self.courses) + n_courses) - sum(map(lambda x: x.__dict__[prop], iterable))
			
			# check if the degree of the course is in the threshold list.
			courses = filter(lambda x: x.degree in degree_treshold, iterable) if len(degree_treshold) >= 1 else iterable
			
			# verifies that the recommended course are not self.took=True in the DB.
			return filter(lambda comb: not any(map(lambda course: course.took, comb)), combinations(courses, n_courses))			

		def filters_func(filters, func, initial, *args, **kwargs):
			for f in filters:
				if f[1]:
					initial = func(initial, f[0], f[1], *args, **kwargs)

		degree_treshold = degree_treshold if degree_treshold else []
		current_courses = session.query(Course).all()

		# n_points & n_musts filter
		n_filter = filter(lambda comb: n_recommender(comb, 'points', sum) <= n_points, current_courses) if n_points else current_courses
		n_filter = filter(lambda comb: n_recommender(comb, 'must', len) >= n_musts, n_filter) if n_musts else n_filter
		
		# treshold filter
		tresh_filter = n_filter
		treshs = [('difficulty', difficulty_treshold), ('cost', cost_treshold)]
		filters_func(treshs, treshold_recommender, tresh_filter)

		# verify that all the prerequisites are fulfilled.
		current_courses = filter(lambda course: self._fulfilled_prerequisites(course.prerequisites), tresh_filter)

		# average filter
		filters = [('difficulty', avg_difficulty), ('cost', avg_cost)]
		filters_func(filters, avg_recommender, current_courses, n_courses)
		
		return np.array(list(current_courses))


class Degree(Base):
	__tablename__ = 'degrees'

	id = Column(Integer, primary_key=True)
	title = Column(String)

	_semesters = relationship('Semester')

	def __init__(self, 
		title: str,
		semesters: Iterable[Semester] = None) -> None:

		self.title = title
		self.semesters = semesters if semesters else []

	@property
	def courses(self):
		return np.array(session.query(Course).filter(Course.degree == self.title).all())

	def recommend(self, 
		n_semesters: int, 
		start_summer: bool, # start/not with summer semester. 
		with_summer: bool, # recommend/not summer semesters.

		avg_difficulty: float = None, # the average diff of the degree.
		avg_cost: float = None, # the average cost of the degree.
		
		difficulty_treshold: float = None, # each semester below certain difficulty.
		cost_treshold: float = None, # each semester below certain cost.

		semester_params: dict = None # semester parameters - Semester(...).recommend(semester_params) 

		):

		'''
		0. Check which courses the user took.
		1. Create a first semester, then used Semester.recommend(semester_params) to estimate
			the second one based on the first, and on the rules of the degree -
			such as the number of semesters, the difficulty function, and more.

		
		'''
		pass


populate()
