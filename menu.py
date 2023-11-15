import re
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
        if not Student.select().where(nickname=nickname):
            student = Student.create(
                nickname=nickname,
                role=role,
            )
        


    def parse_schedule(self, text: str):
        self.schedule = {}
        current_day = None
        pattern = re.compile(r'(\w+):$|([\w\s]+), (\d+), (\d+\.\d+);')

        for line in text.split('\n'):
            match = pattern.match(line)
            if match:
                # если строка день недели
                if match.group(1):
                    current_day = match.group(1)
                    self.schedule[current_day] = []
                # если строка инфа о предмете                    
                elif match.group(2):
                    subject = match.group(2)
                    auditorium = int(match.group(3))
                    time = float(match.group(4))
                    self.schedule[current_day].append([subject, auditorium, time])
    
    def format_schedule(self, group: str) -> str:
        formatted_schedule = f'Расписание для {group}:'

        for day, subjects in self.schedule.items():
            formatted_schedule += f'\n{day}:\n'
            for subject_info in subjects:
                subject, auditorium, time = subject_info
                formatted_subject = f"{subject} | {time:.2f} | {auditorium} каб\n"
                formatted_schedule += formatted_subject
            formatted_schedule += '_' * 30

        return formatted_schedule
    
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
