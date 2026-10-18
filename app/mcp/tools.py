from .server import mcp
from app.database import SessionLocal
from app.models import Note


# ----------------------------
# TEST TOOL
# ----------------------------

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello {name}, MCP is working!"


# ----------------------------
# READ TOOLS
# ----------------------------

@mcp.tool()
def list_notes(user_id: int):
    """
    Return all notes belonging to a user.
    """

    db = SessionLocal()

    try:
        notes = (
            db.query(Note)
            .filter(Note.user_id == user_id)
            .all()
        )

        return [
            {
                "id": note.id,
                "title": note.title,
                "summary": note.summary,
                "category": note.category,
            }
            for note in notes
        ]

    finally:
        db.close()


@mcp.tool()
def search_notes(user_id: int, query: str):
    """
    Search a user's notes by title or content.
    """

    db = SessionLocal()

    try:
        notes = (
            db.query(Note)
            .filter(
                Note.user_id == user_id,
                (
                    Note.title.ilike(f"%{query}%")
                    | Note.content.ilike(f"%{query}%")
                ),
            )
            .all()
        )

        return [
            {
                "id": note.id,
                "title": note.title,
                "summary": note.summary,
                "category": note.category,
            }
            for note in notes
        ]

    finally:
        db.close()


@mcp.tool()
def get_note(user_id: int, note_id: int):
    """
    Get one note belonging to a user.
    """

    db = SessionLocal()

    try:
        note = (
            db.query(Note)
            .filter(
                Note.id == note_id,
                Note.user_id == user_id,
            )
            .first()
        )

        if note is None:
            return {"error": "Note not found"}

        return {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "summary": note.summary,
            "category": note.category,
            "tags": note.tags,
            "created_at": str(note.created_at),
            "updated_at": str(note.updated_at),
        }

    finally:
        db.close()


# ----------------------------
# WRITE TOOLS
# ----------------------------

@mcp.tool()
def create_note(
    user_id: int,
    title: str,
    content: str,
):
    """
    Create a note for a user.
    """

    db = SessionLocal()

    try:
        note = Note(
            title=title,
            content=content,
            user_id=user_id,
        )

        db.add(note)
        db.commit()
        db.refresh(note)

        return {
            "message": "Note created successfully",
            "id": note.id,
            "title": note.title,
        }

    finally:
        db.close()


@mcp.tool()
def update_note(
    user_id: int,
    note_id: int,
    title: str,
    content: str,
):
    """
    Update one of the user's notes.
    """

    db = SessionLocal()

    try:
        note = (
            db.query(Note)
            .filter(
                Note.id == note_id,
                Note.user_id == user_id,
            )
            .first()
        )

        if note is None:
            return {"error": "Note not found"}

        note.title = title
        note.content = content

        db.commit()
        db.refresh(note)

        return {
            "message": "Note updated successfully",
            "id": note.id,
            "title": note.title,
        }

    finally:
        db.close()


@mcp.tool()
def delete_note(
    user_id: int,
    note_id: int,
):
    """
    Delete one of the user's notes.
    """

    db = SessionLocal()

    try:
        note = (
            db.query(Note)
            .filter(
                Note.id == note_id,
                Note.user_id == user_id,
            )
            .first()
        )

        if note is None:
            return {"error": "Note not found"}

        db.delete(note)
        db.commit()

        return {
            "message": "Note deleted successfully",
            "id": note_id,
        }

    finally:
        db.close()