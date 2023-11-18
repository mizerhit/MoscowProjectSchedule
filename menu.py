import re
from datetime import datetime
import models as md


class Menu:
    def __init__(self, group_name: str):
        if not md.Group.select().where(md.Group.name == group_name).exists():
            self.__group = md.Group.create(
                name=group_name
            )
        else:
            self.__group = md.Group.get(name=group_name)

    def get_or_add_student(self, nickname: str):
        student = md.Student.get_or_none(nickname=nickname)
        if not student:
            student = md.Student.create(
                nickname=nickname,
                group=self.__group,
            )
        return student

    def get_group(self, student_nickname: str):
        student = md.Student.get(nickname=student_nickname)
        group = student.group
        return group

    def add_schedule(self, input_schedule: str):
        schedule = {}
        current_day = None
        pattern = re.compile(r'(\w+):$|([\w\s]+), (\d+), (\d+\.\d+);')

        for line in input_schedule.split('\n'):
            match = pattern.match(line)
            if match:
                # если строка это день недели
                if match.group(1):
                    current_day = match.group(1)
                    schedule[current_day] = []
                # если строка это инфа о предмете
                elif match.group(2):
                    subject = match.group(2)
                    auditorium = int(match.group(3))
                    time = float(match.group(4))
                    time_str = f'{int(time):02d}:{int((time % 1) * 60):02d}'
                    formatted_time = datetime.strptime(time_str, "%H:%M")
                    md.Subject.create(
                        name=subject,
                        week_day=current_day,
                        auditorium=auditorium,
                        time=formatted_time,
                        group=self.__group
                    )
                    schedule[current_day].append([subject, auditorium, time])
        return schedule

    def format_schedule(self, schedule):
        formatted_schedule = f'Расписание для {self.__group.name}:'

        for day, subjects in schedule.items():
            formatted_schedule += f'\n{day}:\n'
            for subject_info in subjects:
                subject, auditorium, time = subject_info
                formatted_subject = f"{subject} | {time:.2f} | {auditorium} каб\n"
                formatted_schedule += formatted_subject
            formatted_schedule += '_' * 30

        self.__group.schedule = formatted_schedule
        self.__group.save()

    def show_schedule(self):
        if self.__group.schedule is not None:
            return self.__group.schedule
        else:
            return "Расписание отсутствует"

    def add_homework(self, text: str):
        pattern = re.compile(r'(.+): (\d{4}\.\d{2}\.\d{2});\n(.+)')
        match = pattern.match(text)
        parsed_data = match.groups()
        subject_name = parsed_data[0]
        date = parsed_data[1]
        task = parsed_data[2]
        date_deadline = datetime.strptime(date, '%Y.%m.%d')
        weekday_number = date_deadline.weekday()
        weekdays = ['Понедельник', 'Вторник', 'Среда',
                    'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        weekday = weekdays[weekday_number]
        subject = md.Subject.get_or_none(
            name=subject_name, group=self.__group)
        # if not subject:
        #     return 0
        time_deadline = subject.time
        datetime_deadline = datetime.combine(
            date_deadline.date(), time_deadline)
        homework = md.Homework.create(
            group=self.__group,
            task=task,
            deadline=datetime_deadline,
            subject=subject
        )

        return parsed_data

    def show_homework(self):
        today = datetime.now().date()
        homeworks = (
            md.Homework.select()
            .join(md.Subject)
            .join(md.Group)
            .where(md.Group.id == self.__group.id)
            .where((md.Homework.deadline > today) |
                   ((md.Homework.deadline == today) & (md.Homework.deadline > datetime.now().time())))
            .order_by(md.Homework.deadline)
        )

        if not homeworks:
            return 'Домашнего задания пока что нет'

        formatted_homeworks = []
        for homework in homeworks:
            subject_name = homework.subject.name
            deadline = homework.deadline.strftime('%Y.%m.%d')
            task = homework.task
            formatted_homeworks.append(f"{subject_name}: {deadline};\n{task}")

        return "\n".join(formatted_homeworks)

    def show_students(self):
        for student in self.__group.students:
            yield student
