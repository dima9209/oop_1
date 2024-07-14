# Создадим класс для реализации подсчет баллов и условий сравнения классов
class Grade:
    def __init__(self):
        self.grades = {}

    def avg_grade_total(self):
        return 0 if len(self.grades) == 0 else sum(map(lambda x: sum(x) / len(x), self.grades.values())) / len(
            self.grades)

    def avg_grade_course(self, course):
        return 0 if not self.grades.get(course, 0) else sum(self.grades[course]) / len(self.grades[course])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.avg_grade_total() == other.avg_grade_total()

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.avg_grade_total() < other.avg_grade_total()

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.avg_grade_total() <= other.avg_grade_total()


class Student(Grade):
    def __init__(self, name, surname, gender):
        super().__init__()
        self.name = name
        self.surname = surname
        self.gender = gender
        self._finished_courses = []
        self._courses_in_progress = []

    @property
    def finished_courses(self):
        """ The function returns the name of completed courses"""
        return ' ' if len(self._finished_courses) else ', '.join(self._finished_courses)

    def add_finished_courses(self, courses):
        if isinstance(courses, str):
            self._finished_courses.append(courses)
        elif isinstance(courses, list):
            self._finished_courses.extend(courses)
        else:
            print('Назание курсов должны быть в формате строки или списка!')

    def deleted_finish_course(self, courses, deleted_all=False):
        if deleted_all:
            self._finished_courses.clear()
        else:
            if isinstance(courses, list):
                for course in courses:
                    self._finished_courses.remove(course)
            elif isinstance(courses, str):
                self._finished_courses.remove(courses)
            else:
                print('Назание курсов должны быть в формате строки или списка!')

    @property
    def courses_in_progress(self):
        """The function returns the name of the current course courses"""
        return '' if self._courses_in_progress else ', '.join(self._courses_in_progress)

    def add_courses_in_progress(self, courses):
        if isinstance(courses, str):
            self._courses_in_progress.append(courses)
        elif isinstance(courses, list):
            self._courses_in_progress.extend(courses)
            print(self._courses_in_progress)
        else:
            print('Назание курсов должны быть в формате строки или списка!')

    def deleted_courses_in_progress(self, courses, deleted_all=False):
        if deleted_all:
            self._courses_in_progress.clear()
        else:
            if isinstance(courses, list):
                for course in courses:
                    self._courses_in_progress.remove(course)
            elif isinstance(courses, str):
                self._courses_in_progress.remove(courses)
            else:
                print('Назание курсов должны быть в формате строки или списка!')

    def lecturer_evaluation(self, lecturer, course, grade):
        """Function for grading a teacher"""
        if not isinstance(lecturer, Lecturer):
            print("Лектор не найден.")
        elif grade < 0 or grade > 10:
            print(" Оценка должна быть в диапозоне от 0 до 10")
        elif course in self._courses_in_progress and course in lecturer._courses_attached:
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            print("Оценку проставить невозможно, так как, либо лектор не является преподавателем на указанном курсе, "
                  "либо студент не учится на указанном курсе.")

    def __str__(self):
        return \
            f"""Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за домашнее задание: {round(self.avg_grade_total(), 1)}
Курсы в процессе изучения: {', '.join(self._courses_in_progress)}
Завершенные курсы: {', '.join(self._finished_courses)}"""


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self._courses_attached = []

    @property
    def courses_attached(self):
        """Returns the name of the courses to which the mentor is assigned"""
        return ', '.join(self._courses_attached)

    def add_courses_attached(self, courses):
        if isinstance(courses, str):
            self._courses_attached.append(courses)
        elif isinstance(courses, list):
            self._courses_attached.extend(courses)
        else:
            print('Назание курсов должны быть в формате строки или списка!')

    def deleted_courses_attached(self, courses, deleted_all=False):
        if deleted_all:
            self._courses_attached.clear()
        else:
            if isinstance(courses, list):
                for course in courses:
                    self._courses_attached.remove(course)
            elif isinstance(courses, str):
                self._courses_attached.remove(courses)
            else:
                print('Назание курсов должны быть в формате строки или списка!')


class Lecturer(Mentor, Grade):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return \
            f"""Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за лекции: {round(self.avg_grade_total(), 1)}"""


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self._courses_attached and course in student._courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print('Ошибка')

    def __str__(self):
        return \
            f'''Имя: {self.name}
Фамилия: {self.surname}'''


# Функция для подсчета средней  оценки за лекции всех лекторов в рамках курса
def evaluate_all_lecturers(course, *args):
    lecturers = filter(lambda x: isinstance(x, Lecturer) and course in x._courses_attached, args)
    list_evaluate = list(map(lambda y: y.avg_grade_course(course), lecturers))
    return f'Средняя оценка преподавателей препадающих на курсе {course} составляет {round(sum(list_evaluate) / len(list_evaluate), 1)}'


# Функция для подсчета средней  оценки за дз  всех студентов курса
def evakuate_all_students(course, *args):
    students = filter(lambda x: isinstance(x, Student) and course in x._courses_in_progress, args)
    list_evaluate = list(map(lambda y: y.avg_grade_course(course), students))
    return f'Средняя оценка домашних задания студентов обучающихся на курсе {course} составляет {round((sum(list_evaluate) / len(list_evaluate)), 1)}'

# Проверка


# Реализуем 2 экземпляра класса Reviewer
reviewer1 = Reviewer('Bob', 'Martin')
reviewer2 = Reviewer('Liza', 'Parcker')
print(reviewer1)
print()

# Добавим им курсы
reviewer1.add_courses_attached(['Django', 'Python', 'JavaScript'])
reviewer2.add_courses_attached('Java')
print(reviewer1.courses_attached)
print(reviewer2.courses_attached)

# Удалим один курс reviewer1
reviewer1.deleted_courses_attached('JavaScript', deleted_all=False)
print(reviewer1.courses_attached)
print()

# Создадим 2 экземпляра класса Student
student1 = Student('Martin', 'Back', 'M')
student2 = Student('Kate', 'Luis', 'F')

# Добавим им курсов:
student1.add_finished_courses(['Java', 'Python'])
student2.add_finished_courses('Python')
student1.add_courses_in_progress('Django')
student2.add_courses_in_progress('Java')
print(student1)
print()

# Попробуем сравнить 2 студентов
print(student1 == student2)
print()

# Добавим им оценок по курсу:
reviewer1.rate_hw(student1, 'Java', 10)  # Должна быть ошибка
reviewer1.rate_hw(student1, 'Django', 8)
reviewer1.rate_hw(student1, 'Django', 9)
reviewer2.rate_hw(student2, 'Java', 8)
reviewer2.rate_hw(student2, 'Java', 9)

print(student2)
print()
print(student2 == student1)  # Должно быть True
print()

student2.add_courses_in_progress('Django')
reviewer1.rate_hw(student2, 'Django', 10)
reviewer1.rate_hw(student2, 'Django', 10)

print(student2 == student1)  # False
print(student2 >= student1)  # True
print()
print(evakuate_all_students('Django', student1, student2))
print()

# Добавим 2 лекторов

lecturer1 = Lecturer('Kevin', 'Smit')
lecturer2 = Lecturer('Jack', 'Kaje')

# Добавим лекторам курсы, на которых они являются преподавателями
lecturer2.add_courses_attached(['Java', 'Django'])
lecturer1.add_courses_attached('Django')

#Добавим оценку преподавателям

student2.lecturer_evaluation(lecturer2, 'Java', 8)
student2.lecturer_evaluation(lecturer2, 'Java', 10)
student2.lecturer_evaluation(lecturer2, 'Java', 6)
student2.lecturer_evaluation(lecturer2, 'Python', 8) # Оценку поставить не возможно
print()
print(lecturer2)

student1.lecturer_evaluation(lecturer2, 'Django', 6)
student1.lecturer_evaluation(lecturer2, 'Django', 4)
student1.lecturer_evaluation(lecturer2, 'Django', 9)
student2.lecturer_evaluation(lecturer1, 'Django', 7)
student2.lecturer_evaluation(lecturer1, 'Django', 9)
student2.lecturer_evaluation(lecturer1, 'Django', 9)
print()
print(lecturer1)
print(evaluate_all_lecturers('Django', lecturer1, lecturer2))


