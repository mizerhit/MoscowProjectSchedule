from peewee import *


db = SqliteDatabase('data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    class Meta:
        db_table = 'Students'

    nickname = CharField(unique=True)
    role = CharField(max_length='20')
    Group = ManyToManyField('Group')


class Group(BaseModel):
    class Meta:
        db_table = 'Groups'

    name = CharField(unique=True)
    # schedule = ForeignKeyField('Schedule', unique=True, blank=True, backref='schedule')
    schedule = CharField()
    homeworks = ForeignKeyField('Homework', blank=True)


# class Schedule(BaseModel):
#     class Meta:
#         db_table = 'Schedules'


class Subject(BaseModel):
    class Meta:
        db_table = 'Subjects'

    name = CharField()
    week_day = CharField()
    auditorium = CharField()
    group = ForeignKeyField('Group')
    homework = CharField()
    deadline = DateTimeField()
