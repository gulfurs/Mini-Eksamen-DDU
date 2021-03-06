from flask_login import UserMixin
from main import login_manager
from peewee import *

USER = 'nejjyigpsyjcqc'
PASSWORD = 'f7345217f875c8a617f3aff8f2812e35a6f55ef9178bf177a9c1247978b2f223'
HOST = 'ec2-52-208-175-161.eu-west-1.compute.amazonaws.com'
PORT = 5432

DB = PostgresqlDatabase('dae8653ftqev6r', 
                                   user=USER, 
                                   password=PASSWORD, 
                                   host=HOST, 
                                   port=PORT)


class Class(Model):
    name = CharField(unique=True)

    class Meta:
        database = DB


class simpleQuestion(Model):
    clazz = ForeignKeyField(model=Class, backref="questions")
    questionText = CharField()
    answer1 = CharField()
    answer2 = CharField()
    # If this boolean field contains the value True then it means that answer1 is the correct answer/value
    yesOrNo = BooleanField()

    class Meta:
        database = DB


class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique=True)
    password = CharField()
    teacher = BooleanField()

    class Meta:
        database = DB


class userQuestionRel(Model):
    user = ForeignKeyField(model=User, backref="questions")
    question = ForeignKeyField(model=simpleQuestion, backref="users")
    correctAnswer = BooleanField()

    class Meta:
        database = DB


class userClassRel(Model):
    user = ForeignKeyField(model=User, backref="classes")
    clazz = ForeignKeyField(model=Class, backref="users")

    class Meta:
        database = DB


# Det her sørger for at login manager'en kan finde brugeren på en specifik måde
# så vi ikke altid har behov for at gøre det selv
@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)


if __name__ == '__main__':
    DB.connect()
    DB.create_tables([Class, simpleQuestion, User, userQuestionRel, userClassRel], safe=True)
    DB.close()

