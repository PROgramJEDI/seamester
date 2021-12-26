from program import Group, Course

# 1. ADD THE COURSES BELOW THIS LINE
# ----------------------------------

linear_algebra_2 = Course(
		number=91492, 
		title='Linear Algebra 2', 
		description='fjdiojfds', 
		must=True, 
		points=5, 
		difficulty=7,
		link='.com',
		took=False,
		summer=False,
		degree='computer-science')

linear_algebra_1 = Course(
		number=93432, 
		title='Linear Algebra 1', 
		description='fjdiojfds', 
		must=True, 
		points=7, 
		difficulty=10,
		link='.com',
		took=False,
		summer=False,
		degree='computer-science')

infy_1 = Course(
		number=91532, 
		title='Infy 1', 
		description='fjdiojfds', 
		must=True, 
		points=7, 
		difficulty=8,
		link='.com',
		took=False,
		summer=False,
		degree='computer-science')


infy_2 = Course(
		number=91732, 
		title='Infy 2', 
		description='fjdiojfds', 
		must=True, 
		points=7, 
		difficulty=9,
		link='.com',
		took=False,
		summer=False,
		degree='computer-science')

# 2. ADD THE GROUPS BELOW THIS LINE
# ----------------------------------


# 3. ADD THE PREREQUISITES OF THE COURSES BELOW THE LINE
# ------------------------------------------------------

linear_algebra_2.prerequisites = [linear_algebra_1, infy_1]
infy_2.prerequisites = [infy_1]

# 4. ADD THE GROUPS OF THE COURSES BELOW THIS LINE
# ------------------------------------------------

linear_algebra_1.groups = []
linear_algebra_2.groups = []

infy_1.groups = []

# 5. ADD THE COURSES OBJECTS TO THE LIST BELOW
# --------------------------------------------

COURSES = [
	linear_algebra_1,
	linear_algebra_2,
	infy_1,
	infy_2,
]

# 6. ADD THE GROUPS OBJECTS TO THE LIST BELOW
# --------------------------------------------

GROUPS = [

]
