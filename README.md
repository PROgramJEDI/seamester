# Seamester📖

## Installation
In order to install Seamester📖, you must first install Python and the 'pip' package manager. Right after, you can open the command-prompt and type the following command, corresponding to your operating system:

* Windows: ```pip install seamester```
* Unix/Linux: ```pip3 install seamester```

## Getting Started
The core of the Seamester📖 library, is the Course class. The course class contains the base definition of a course, and provides us with a stable ground to create a new Semester or a Degree. Semester is a collection of courses that belong to a summer/not summer semester. With the Semester class we can see what courses Seamester📖 has to recommend, based on rules that we apply, such as the average difficulty of the semester, the faculty of the courses, the average price of the courses and more:
```python
>>> from seamester import COURSES
>>> mycourses = [41542, 41531] # the courses we know we'll take this semester.
>>> semester = Semester([course for course in COURSES if course.number in mycourses], summer=False)
>>> semester.recommend(2, avg_difficulty=6.5, degree_treshold=['computer-science']) # a recommendation of 2 more 
                                              # courses based on an average difficulty of 6.5 or less.

```

## Add Groups & Courses
Seamester📖 provides you with the most simple way to add courses to the library. All you need in order to do so, is to create a new Group/Course object in their corresponding  file, and add them to the lists:
1. Navigate to ```objects.py```.
2. Create a ```Course``` object in the right location: 
```python 
>>> linear_algebra_2 = Course(...)
```
3. Add the Course object to its prerequisites list: 
```python
>>> linear_algebra_2.prerequisites = [linear_algebra_1, java_programming_2]
```
4. Add the Course object to the ```COURSES``` list: 
```python
>>> COURSES = [..., linear_algebra_2]
```

1. Navigate to ```objects.py```.
2. Create a ```Group``` object in the right location:
```python
>>> linear_algebra_2_discord = Group(...)
```
3. Add the Group object to the groups list of the course: 
```python
>>> linear_algebra_2.groups = [linear_algebra_2_discord, linear_algebra_2_whatsapp]
```
4. Add the Group object to the ```GROUPS``` list: 
```python
>>> GROUPS = [linear_algebra_2_discord, ...]
```
