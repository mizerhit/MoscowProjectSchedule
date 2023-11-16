import re
from datetime import datetime, time
from models import *

class Menu:
    def __init__(self, group_name: str):
        if not Group.select().where(name=group_name):
            self.group = Group.create(
                name=group_name
            )
        else:
            self.group = Group.get(name=group_name)
        

    def add_student(self, nickname: str, role: str):
        try:
            student = Student.get(nickname=nickname)
        except Student.DoesNotExists:
            student = None
        if not student:
            student = Student.create(
                nickname=nickname,
                role=role,
            )
        if not student in self.group.students:
            self.group.students.add(student)


    def parse_schedule(self, input_schedule: str):
        schedule = {}
        current_day = None
        pattern = re.compile(r'(\w+):$|([\w\s]+), (\d+), (\d+\.\d+);')

        for line in input_schedule.split('\n'):
            match = pattern.match(line)
            if match:
                # если строка день недели
                if match.group(1):
                    current_day = match.group(1)
                    schedule[current_day] = []
                # если строка инфа о предмете                    
                elif match.group(2):
                    subject = match.group(2)
                    auditorium = int(match.group(3))
                    time = float(match.group(4))
                    Subject.create(
                        name=subject,
                        week_day=current_day,
                        auditorium=auditorium,
                        group=self.group
                    )
                    schedule[current_day].append([subject, auditorium, time])
        return schedule
    
    def format_schedule(self, schedule):
        formatted_schedule = f'Расписание для {self.group}:'

        for day, subjects in self.schedule.items():
            formatted_schedule += f'\n{day}:\n'
            for subject_info in subjects:
                subject, auditorium, time = subject_info
                formatted_subject = f"{subject} | {time:.2f} | {auditorium} каб\n"
                formatted_schedule += formatted_subject
            formatted_schedule += '_' * 30

        self.group(schedule=formatted_schedule)

    def __format_deadline(input_time: float):
        hours, minutes = divmod(int(input_time * 60), 60)
        converted_time = time(hours, minutes)
        current_year = datetime.now().year
        combined_datetime = datetime(current_year, 1, 1, hours, minutes)
    
    def add_homework(self, text: str):
        pattern = re.compile(r'(.+): (\d{4}\.\d{2}\.\d{2});\n(.+)')
        match = pattern.match(text)
        parsed_data = match.groups()
        return parsed_data
        
    
    def show_homework(self):
        pass
    
    def send_allert(self):
        pass





text = """Понедельник:
Математика, 100, 14.00;
Английский язык, 200, 15.35;
Теория вероятностей, 300, 16.00;

Вторник:
Физика, 101, 10.00;
Критическое мышление, 201, 11.00;
ЭВМ, 301, 12.00;"""

menu = Menu(text)
schedule = menu.parse_schedule(text)
formatted_schedule = menu.format_schedule('ИСИБ 22-1')
print(formatted_schedule)
