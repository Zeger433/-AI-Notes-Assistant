from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import logging

from sqlalchemy.orm import Session

from app.models import Conversation

from app.mcp.tools import (
    list_notes,
    search_notes,
    get_note,
    create_note,
    update_note,
    delete_note,
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

logger = logging.getLogger(__name__)


TOOLS = {
    "list_notes": list_notes,
    "search_notes": search_notes,
    "get_note": get_note,
    "create_note": create_note,
    "update_note": update_note,
    "delete_note": delete_note,
}


OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List all notes belonging to the authenticated user.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search notes by title or content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_note",
            "description": "Get a note by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "integer"
                    }
                },
                "required": ["note_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_note",
            "description": "Create a new note.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "content": {
                        "type": "string"
                    }
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_note",
            "description": "Update an existing note.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "integer"
                    },
                    "title": {
                        "type": "string"
                    },
                    "content": {
                        "type": "string"
                    }
                },
                "required": [
                    "note_id",
                    "title",
                    "content"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_note",
            "description": "Delete a note.",
            "parameters": {
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "integer"
                    }
                },
                "required": ["note_id"]
            }
        }
    }
]


def chat(prompt: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content



def load_conversation_history(
    db: Session,
    user_id: int,
):

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.created_at.asc()
        )
        .limit(20)
        .all()
    )

    messages = []

    for conversation in conversations:
        messages.append(
            {
                "role": conversation.role,
                "content": conversation.content,
            }
        )

    return messages



def save_message(
    db: Session,
    user_id: int,
    role: str,
    content: str,
):

    message = Conversation(
        user_id=user_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()



def run_agent(
    db: Session,
    user_id: int,
    prompt: str,
):

    messages = [
        {
            "role": "system",
            "content": (
    "You are an AI Notes Assistant.\n"
    "\n"
    "The authenticated user's ID is automatically provided by the backend.\n"
    "Never ask for the user ID.\n"
    "\n"
    "Important rules:\n"
    "1. Do not create notes unless the user explicitly asks you to create, save, add, or write a note.\n"
    "2. Normal conversation, preferences, facts about the user, and temporary information should only be remembered through conversation memory.\n"
    "3. Use note tools only when the user requests note management actions.\n"
    "4. You may call multiple tools when needed.\n"
)
        }
    ]

    history = load_conversation_history(
        db,
        user_id,
    )

    messages.extend(history)


    user_message = {
        "role": "user",
        "content": prompt,
    }

    messages.append(user_message)


    save_message(
        db,
        user_id,
        "user",
        prompt,
    )


    MAX_ITERATIONS = 10


    for step in range(MAX_ITERATIONS):

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=messages,
            tools=OPENAI_TOOLS,
        )


        message = response.choices[0].message


        print("=" * 60)
        print(message)
        print("=" * 60)


        # Final answer
        if not message.tool_calls:

            messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                }
            )


            save_message(
                db,
                user_id,
                "assistant",
                message.content,
            )


            return message.content



        # Save tool call message in memory
        messages.append(
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ],
            }
        )


        # Execute tools

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name


            arguments = json.loads(
                tool_call.function.arguments
            )


            arguments["user_id"] = user_id


            tool = TOOLS.get(tool_name)


            if tool is None:
                raise ValueError(
                    f"Unknown tool: {tool_name}"
                )


            logger.info(
                "Executing tool %s with arguments %s",
                tool_name,
                arguments,
            )


            try:
                result = tool(**arguments)

            except Exception as e:

                logger.exception(
                    "Tool execution failed"
                )

                result = {
                    "error": str(e)
                }


            logger.info(
                "Tool %s completed",
                tool_name,
            )


            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )


    raise RuntimeError(
        "Agent exceeded the maximum number of reasoning steps."
    )