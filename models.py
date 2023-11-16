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


class Group(BaseModel):
    class Meta:
        db_table = 'Groups'

    name = CharField(unique=True)
    schedule = CharField(black=True)
    students = ManyToManyField('Student', backref='groups')


class Subject(BaseModel):
    class Meta:
        db_table = 'Subjects'

    name = CharField()
    week_day = CharField()
    auditorium = CharField()
    time=DateTimeField()
    group = ForeignKeyField('Group')


class Homework(BaseModel):
    class Meta:
        db_table = 'Homeworks'
    
    text = CharField()
    deadline = DateTimeField()
    subject = ForeignKeyField('Subject', backref='homework')
