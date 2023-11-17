import menu as mn
import models as md

schedule = '''Понедельник:
Математика, 100, 14.00;
Английский язык, 200, 15.00;
Теория вероянтостей, 300, 16.00;

Вторник:
Физика, 101, 10.00;
Критическое мышление, 201, 11.00;
ЭВМ, 301, 12.00;'''

menu = mn.Menu(group_name='ИСИБ')
# menu.add_student(nickname='Саша')
# menu.add_student(nickname='Петя')

# sch = menu.add_schedule(schedule)
# menu.format_schedule(sch)
print(menu.show_schedule())

print()

for student in menu.show_students():
    print(student.nickname)
print()

hw1 = '''Математика: 2023.11.20;
Сделать дз'''

hw2 = '''Физика: 2023.11.21;
прочитать параграф'''

# menu.add_homework(hw1)
# menu.add_homework(hw2)
print(menu.show_homework())




# for i in md.Subject.select():
#     print(f'{i.name} | {i.week_day} | {i.auditorium} | {i.time} | {i.group.name}')

# for i in md.Group.select():
#     print(i.name)

