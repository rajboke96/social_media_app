from sqlalchemy import Column, Integer, Boolean, String, Date, Table
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from typing import List, Optional
import logging
import enum

from database import engine
# from database import engine

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# Then create your engine as usual (echo=False or omit)

# url_object = URL.create(
#     'sqlite',
#     database='database.db',
# )

class Base(DeclarativeBase):
    pass

class AccountType(enum.Enum):
        PRIVATE="private"
        PUBLIC="public"

class AccountStatus(enum.Enum):
        ACTIVE="active"
        SUSPENDED="suspended"
        INACTIVE="inactive"

class Visibility(enum.Enum):
        PRIVATE="private"
        FRIENDS="friends"
        PUBLIC="public"

class Gender(enum.Enum):
        MALE="male"
        FEMALE="female"
        OTHER="other"

class MediaType(enum.Enum):
    IMAGE="image"
    VIDEO="video"

class Theme(enum.Enum):
    LIGHT="light"
    DARK="dark"

class UserRole(enum.Enum):
    ADMIN="admin"
    CUSTOMER="customer"

# Friend - u1 fk User, u2 fk User, friends_at
friends = Table(
    'friends', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('friend_id', ForeignKey('users.id'), primary_key=True),
    Column('friends_at', Date),
)

post_media = Table(
     'post_media', Base.metadata,
     Column('post_id', ForeignKey('posts.id'), primary_key=True),
     Column('media_id', ForeignKey('media.id'), primary_key=True),
)

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True)
    firstname=Column(String(50))
    middlename=Column(String(50))
    Lastname=Column(String(50))
    dob=Column(Date)
    gender: Mapped[Optional[Gender]]
    username=Column(String(50), unique=True, nullable=False)
    email_address=Column(String(100), unique=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    hashed_password=Column(String(200), nullable=False)
    account_type: Mapped[AccountType]=mapped_column(default=AccountType.PRIVATE)
    account_status: Mapped[AccountStatus]=mapped_column(default=AccountStatus.ACTIVE)
    created_at=Column(DateTime)
    role: Mapped[UserRole]=mapped_column(default=UserRole.CUSTOMER)
    # -------------Relationships-------------
    user_friends: Mapped[List["User"]]=relationship(secondary="friends", primaryjoin=friends.c.user_id == id, secondaryjoin=friends.c.friend_id == id, back_populates="friend_req_by")
    friend_req_by: Mapped[List["User"]]=relationship(secondary="friends", primaryjoin=friends.c.friend_id == id, secondaryjoin=friends.c.user_id == id, back_populates="user_friends")
    posts: Mapped[List["Post"]]=relationship(back_populates="user")
    media: Mapped[List["Media"]]=relationship(back_populates="user")
    setting: Mapped["UserSetting"]=relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User({self.firstname}, {self.username}, {self.dob})"

class UserProfile(Base):
    __tablename__="users_profile"
    id=Column(Integer, primary_key=True)
    user_id=Column(ForeignKey("users.id"))
    profile_bio=Column(String(300))
    profile_pic_img=Column(ForeignKey("media.id"))
    cover_pic_img=Column(ForeignKey("media.id"))
    city_id=Column(ForeignKey("cities.id"))
    # -------------Relationships-------------
    city: Mapped["City"]=relationship(back_populates="user_profiles")

class UserSetting(Base):
    __tablename__="users_setting"
    id=Column(Integer, primary_key=True)
    user_id=Column(ForeignKey("users.id"))
    theme: Mapped[Theme]=mapped_column(default=Theme.LIGHT)
    # -------------Relationships-------------
    user: Mapped[User]=relationship(back_populates="setting")

class Post(Base):
     __tablename__="posts"
     id: Mapped[int]=mapped_column(primary_key=True)
     title=Column(String(30), nullable=False)
     description=Column(String(300))
     created_by=Column(ForeignKey("users.id"), nullable=False)
     created_at=Column(DateTime, nullable=False)
     visibility: Mapped[Visibility]=mapped_column(default=Visibility.PUBLIC)
     # -------------Relationships-------------
     user: Mapped[User]=relationship(back_populates="posts")
     media: Mapped[List["Media"]]=relationship(secondary="post_media", back_populates="posts")

class Media(Base):
     __tablename__="media"
     id: Mapped[int]=mapped_column(primary_key=True)
     name=Column(String(30), nullable=False)
     alt=Column(String(30))
     type: Mapped[MediaType]
     visibility: Mapped[Visibility]=mapped_column(default=Visibility.PUBLIC)
     uploaded_by=Column(ForeignKey("users.id"), nullable=False)
     user: Mapped[User]=relationship(back_populates="media")
     uploaded_at=Column(DateTime, nullable=False)
     uploaded_to=Column(String(300), nullable=False)
     # -------------Relationships-------------
     posts: Mapped[List["Post"]]=relationship(secondary="post_media", back_populates="media")

class Country(Base):
    __tablename__="countries"
    id=Column(Integer, primary_key=True)
    country=Column(String(30))
    country_code=Column(String(5))
    # -------------Relationships-------------
    states: Mapped[List["State"]]=relationship(back_populates="country")

class State(Base):
    __tablename__="states"
    id=Column(Integer, primary_key=True)
    state=Column(String(30))
    state_code=Column(String(5))
    country_id=Column(ForeignKey("countries.id"))
    # -------------Relationships-------------
    cities: Mapped[List["City"]]=relationship(back_populates="state")
    country: Mapped[Country]=relationship(back_populates="states")

class City(Base):
    __tablename__="cities"
    id=Column(Integer, primary_key=True)
    city=Column(String(30))
    city_code=Column(String(5))
    state_id=Column(ForeignKey("states.id"))
    # -------------Relationships-------------
    state: Mapped[State]=relationship(back_populates="cities")
    user_profiles: Mapped[List["UserProfile"]]=relationship(back_populates="city")

if __name__=="__main__":
    Base.metadata.create_all(engine)