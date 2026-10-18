from sqlalchemy import Column, Integer, String, Text , DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base
from sqlalchemy.sql import func



class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    tags: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    # Note owner
    owner = relationship(
        "User",
        back_populates="notes"
    )


    # Users who have access to this note
    shares = relationship(
        "NoteShare",
        back_populates="note",
        cascade="all, delete-orphan",
    )



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    # Notes created by this user
    notes = relationship(
        "Note",
        back_populates="owner"
    )


    # Conversation memory
    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    # Notes shared with this user
    shared_notes = relationship(
        "NoteShare",
        back_populates="user",
        cascade="all, delete-orphan",
    )



class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="conversations",
    )



class NoteShare(Base):
    __tablename__ = "note_shares"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    permission: Mapped[str] = mapped_column(
        String(20),
        default="read",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


    note: Mapped["Note"] = relationship(
        back_populates="shares",
    )


    user: Mapped["User"] = relationship(
        back_populates="shared_notes",
    )