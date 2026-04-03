# Daily Organizer

An AI-powered daily planner that uses LangChain and MistralAI to convert your scattered notes into a structured daily schedule.

## Features

- **AI-Powered Organization**: Uses MistralAI through LangChain to intelligently structure your daily activities
- **Structured Output**: Generates organized schedules with time slots, activities, and priority levels
- **Simple CLI Interface**: Easy-to-use command-line interface for adding notes and generating schedules
- **Pydantic Models**: Type-safe data structures for tasks and schedules

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rohithtp/daily-organizer.git
cd daily-organizer
```

2. Install dependencies using pip:
```bash
pip install -e .
```

Or using uv (recommended for faster installation):
```bash
uv pip install -e .
```

3. Set up your MistralAI API key:
```bash
export MISTRAL_API_KEY="your-api-key-here"
```

## Usage

Run the application:
```bash
python main.py
```

Or run the organizer directly:
```bash
python organizer.py
```

Using uv run (automatically manages dependencies):
```bash
uv run python main.py
```

Or:
```bash
uv run python organizer.py
```

### CLI Options

1. **Add Note/Activity**: Add your thoughts, tasks, or activities
2. **View Current Notes**: See all your raw notes
3. **Generate & View AI Schedule**: Let AI organize your notes into a structured schedule
4. **Clear All Notes**: Reset your notes
5. **Exit**: Close the application

## Project Structure

```
daily-organizer/
├── main.py              # Entry point
├── organizer.py         # Main application logic
├── pyproject.toml       # Project configuration and dependencies
└── README.md           # This file
```

## Dependencies

- `langchain-core`: Core LangChain functionality
- `langchain-mistralai`: MistralAI integration for LangChain
- `pydantic`: Data validation and serialization

## How It Works

1. **Input Collection**: Users add notes and activities through the CLI
2. **AI Processing**: LangChain sends combined notes to MistralAI with structured output instructions
3. **Schedule Generation**: MistralAI returns a structured `DailySchedule` with `Task` objects
4. **Display**: Formatted schedule is displayed with time, activity, and priority columns

## License

MIT License