# 🤖 AI Notes Assistant

An AI-powered Notes Assistant built with Python and OpenRouter that enables users to manage their notes through natural language. Using an LLM agent with function calling, the application can create, search, retrieve, update, and delete notes while maintaining conversation history in a database.

## ✨ Features

- **AI Chat Assistant:** Interact with an AI assistant using natural language.
- **Create Notes:** Save notes with titles and content.
- **Search Notes:** Find notes by title or content.
- **Retrieve Notes:** Access individual notes by ID.
- **Update Notes:** Modify existing note titles and content.
- **Delete Notes:** Remove unwanted notes.
- **Conversation Memory:** Store and retrieve chat history.
- **Tool Calling:** Automatically select and execute note-management functions.
- **User-Specific Data:** Pass the authenticated user's ID to note-management tools.
- **Error Handling:** Capture tool execution errors and log agent activity.
- **Multi-Step Execution:** Allow multiple tool calls within a single request.

## 🛠️ Technologies Used

- Python
- OpenRouter API
- OpenAI Python SDK
- GPT-OSS 20B model
- SQLAlchemy ORM
- Python-dotenv
- JSON
- Logging

## 📁 Project Structure

```text
ai-notes-assistant/
├── app/
│   ├── models.py
│   └── mcp/
│       └── tools.py
├── .env
├── requirements.txt
└── README.md
```

*Note: This is a suggested structure based on the provided code. Adjust it to match your actual project.*

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd ai-notes-assistant
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

**3. Install dependencies**

Create a `requirements.txt` file:

```text
openai
python-dotenv
sqlalchemy
```

Install the packages:

```bash
pip install -r requirements.txt
```

Install your database driver and any additional framework dependencies required by your application.

## 🔑 Environment Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Replace the placeholder with your actual OpenRouter API key. Never commit your `.env` file or expose your API key in public repositories.

## 🚀 How It Works

1. The user submits a prompt to the `run_agent()` function.
2. The application loads the user's previous conversation history from the database.
3. The LLM analyzes the prompt and decides whether a note-management tool is required.
4. The application executes the selected tool and supplies the authenticated user ID.
5. Tool results are returned to the LLM for further processing.
6. The agent generates a final response and saves it to the conversation database.

## 🔧 Available Tools

| Tool | Description |
|---|---|
| `list_notes` | Lists the user's notes. |
| `search_notes` | Searches notes by title or content. |
| `get_note` | Retrieves a note by ID. |
| `create_note` | Creates a new note. |
| `update_note` | Updates an existing note. |
| `delete_note` | Deletes a note. |

## 🧠 Conversation Memory

The application uses SQLAlchemy to store conversation messages in the `Conversation` model. Previous messages are loaded to provide context for subsequent interactions, allowing the assistant to maintain conversational continuity.

The agent also limits execution to 10 iterations per request to prevent endless tool-calling loops.

## 🔒 Security Considerations

- Store API credentials in environment variables.
- Authenticate users before calling `run_agent()`.
- Ensure every note operation verifies ownership using the authenticated user ID.
- Validate tool arguments before database operations.
- Avoid logging sensitive note content or credentials.
- Restrict access to conversation history by user.

## 🔮 Future Improvements

- Develop a web-based chat interface.
- Add streaming AI responses.
- Implement note categories, tags, and reminders.
- Add conversation deletion and memory-management options.
- Improve tool-call validation and structured error handling.
- Support document attachments and semantic note search.

## 📄 License

Add an appropriate open-source license before distributing the project.
