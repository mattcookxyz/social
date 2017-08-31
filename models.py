from datetime import datetime
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash


db = SqliteDatabase('social.db')


class BaseModel(Model):
    '''Set database information in each table.'''

    class Meta:
        database = db


class User(UserMixin, BaseModel):
    '''User table.'''

    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()
    joindate = DateTimeField(default=datetime.now)
    isadmin = BooleanField(default=False)

    @classmethod
    def create_user(cls, email, username, password,
                                joindate=datetime.now, admin=False):
        '''Constructor method for a row in the User table.'''

        try:
            cls.create(
                email = email,
                username = username,
                password = generate_password_hash(password),
                isadmin = admin)

        except IntegrityError:
            raise ValueError("User already exists.")


class Profile(BaseModel):
    '''Profile table.'''

    user = ForeignKeyField(User)
    about = CharField(null = True)
    twitter = CharField(null = True)
    facebook = CharField(null = True)
    instagram = CharField(null = True)


def initialize():
    '''Connect to database, safely create tables, and close connection.'''

    db.get_conn()
    db.create_tables([User, Profile], safe=True)
    db.close()
