from sqlalchemy import Column, Integer, Boolean, String, Date, Table
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from typing import List, Optional
import logging
import enum
from datetime import date, datetime
from src.logger import get_logger
logger = get_logger(__name__)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

class Base(DeclarativeBase):
    pass

class FriendRequestStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class AccountType(enum.Enum):
    PRIVATE = "private"
    PUBLIC = "public"

class AccountStatus(enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"

class Visibility(enum.Enum):
    PRIVATE = "private"
    FRIENDS = "friends"
    PUBLIC = "public"

class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class Theme(enum.Enum):
    LIGHT = "light"
    DARK = "dark"

class UserRole(enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class OauthProviderType(enum.Enum):
    GOOGLE="google"

class Friend(Base):
    __tablename__ = "friends"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    
    # The extra values you want to set
    status: Mapped[FriendRequestStatus] = mapped_column(default=FriendRequestStatus.PENDING)
    friends_at: Mapped[date] = mapped_column(nullable=True)

    # Back-populates link back to User
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id], back_populates="user_friends"
    )

post_media = Table(
    "post_media",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("media_id", ForeignKey("media.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    middlename = Column(String(50))
    Lastname = Column(String(50))
    dob = Column(Date)
    gender: Mapped[Optional[Gender]]
    username = Column(String(50), unique=True, nullable=False)
    email_address = Column(String(100), unique=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    hashed_password = Column(String(200))
    oauth_provider: Mapped[Optional[OauthProviderType]]
    oauth_id=Column(String(200))
    account_type: Mapped[AccountType] = mapped_column(default=AccountType.PRIVATE)
    account_status: Mapped[AccountStatus] = mapped_column(default=AccountStatus.ACTIVE)
    created_at = Column(DateTime)
    role: Mapped[UserRole] = mapped_column(default=UserRole.CUSTOMER)
    # -------------Relationships-------------
    user_friends: Mapped[list["Friend"]] = relationship(
        primaryjoin="User.id == Friend.user_id",
        back_populates="user"
    )
    user_profile: Mapped["UserProfile"]=relationship(back_populates="user")
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    seen_posts: Mapped[List["PostView"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    media: Mapped[List["Media"]] = relationship(back_populates="user")
    setting: Mapped["UserSetting"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        logger.info('exit')
        return f"User({self.firstname}, {self.username}, {self.dob})"

class UserProfile(Base):
    __tablename__ = "users_profile"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    profile_bio = Column(String(300))
    profile_pic_img = Column(ForeignKey("media.id"))
    cover_pic_img = Column(ForeignKey("media.id"))
    city_id = Column(ForeignKey("cities.id"))
    # -------------Relationships-------------
    # Explicitly specify foreign_keys to resolve target ambiguity
    profile_picture: Mapped["Media"] = relationship(
        "Media", foreign_keys=[profile_pic_img]
    )
    cover_picture: Mapped["Media"] = relationship(
        "Media", foreign_keys=[cover_pic_img]
    )
    user: Mapped["User"]=relationship(back_populates="user_profile")
    city: Mapped["City"] = relationship(back_populates="user_profiles")

class UserSetting(Base):
    __tablename__ = "users_setting"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    theme: Mapped[Theme] = mapped_column(default=Theme.LIGHT)
    # -------------Relationships-------------
    user: Mapped[User] = relationship(back_populates="setting")

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title = Column(String(30), nullable=False)
    description = Column(String(300))
    created_by = Column(ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    visibility: Mapped[Visibility] = mapped_column(default=Visibility.PUBLIC)
    # -------------Relationships-------------
    user: Mapped[User] = relationship(back_populates="posts")
    media: Mapped[List["Media"]] = relationship(
        secondary="post_media", back_populates="posts"
    )
    likes: Mapped[List["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    views: Mapped[List["PostView"]] = relationship(back_populates="post", cascade="all, delete-orphan")

class PostView(Base):
    __tablename__ = "post_views"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    seen_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="seen_posts")
    post: Mapped["Post"] = relationship(back_populates="views")

class Like(Base):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    
    # Relationships
    post: Mapped["Post"] = relationship(back_populates="likes")
    user: Mapped["User"] = relationship()

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    
    # Relationships
    post: Mapped["Post"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship()

class Media(Base):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(200), nullable=False)
    alt = Column(String(30))
    type: Mapped[MediaType]
    visibility: Mapped[Visibility] = mapped_column(default=Visibility.PUBLIC)
    uploaded_by = Column(ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, nullable=False)
    uploaded_to = Column(String(300), nullable=False)
    # public_image_url=Column(String(300), nullable=False)
    # -------------Relationships-------------
    user: Mapped[User] = relationship(back_populates="media")
    posts: Mapped[List["Post"]] = relationship(
        secondary="post_media", back_populates="media"
    )

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    country = Column(String(30))
    country_code = Column(String(5))
    # -------------Relationships-------------
    states: Mapped[List["State"]] = relationship(back_populates="country")

class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True)
    state = Column(String(30))
    state_code = Column(String(5))
    country_id = Column(ForeignKey("countries.id"))
    # -------------Relationships-------------
    cities: Mapped[List["City"]] = relationship(back_populates="state")
    country: Mapped[Country] = relationship(back_populates="states")

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    city = Column(String(30))
    city_code = Column(String(5))
    state_id = Column(ForeignKey("states.id"))
    # -------------Relationships-------------
    state: Mapped[State] = relationship(back_populates="cities")
    user_profiles: Mapped[List["UserProfile"]] = relationship(back_populates="city")

# Base.metadata.create_all(engine)
