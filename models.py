from peewee import *


db = SqliteDatabase('data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Group(BaseModel):
    class Meta:
        db_table = 'Groups'

    name = CharField(unique=True)
    schedule = CharField(null=True)


class Student(BaseModel):
    class Meta:
        db_table = 'Students'

    nickname = CharField(unique=True)
    group = ForeignKeyField(Group, backref='students')


class Subject(BaseModel):
    class Meta:
        db_table = 'Subjects'

    name = CharField()
    week_day = CharField()
    auditorium = CharField(null=True)
    time = TimeField()
    group = ForeignKeyField(Group)


class Homework(BaseModel):
    class Meta:
        db_table = 'Homeworks'

    group = ForeignKeyField(Group, backref='homeworks')
    task = CharField()
    deadline = DateTimeField()
    subject = ForeignKeyField(Subject, backref='homeworks')


if __name__ == '__main__':
    db.connect()
    db.create_tables([Group, Student, Subject, Homework], safe=True)
    db.close()
