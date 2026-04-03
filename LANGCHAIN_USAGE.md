# LangChain Usage and Project Organization

This document outlines how LangChain is integrated into the Daily Organizer project and describes the overall project organization.

## LangChain Integration Overview

The Daily Organizer uses LangChain to create an AI-powered scheduling assistant that converts unstructured notes into structured daily plans. The integration focuses on:

- **LLM Provider**: MistralAI via `langchain-mistralai`
- **Structured Output**: Pydantic models for type-safe AI responses
- **Prompt Engineering**: ChatPromptTemplate for consistent AI interactions

## Core LangChain Components

### 1. LLM Configuration
```python
from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(model="mistral-large-latest", temperature=0.1)
```

- **Model**: `mistral-large-latest` for high-quality reasoning
- **Temperature**: 0.1 for consistent, focused responses
- **Provider**: MistralAI for cost-effective, capable AI

### 2. Structured Output with Pydantic
```python
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Task(BaseModel):
    time: str = Field(description="Specific time or logical slot")
    activity: str = Field(description="Task description")
    priority: str = Field(description="High, Medium, or Low")

class DailySchedule(BaseModel):
    tasks: List[Task] = Field(description="Chronological list of tasks")

structured_llm = llm.with_structured_output(DailySchedule)
```

- **Type Safety**: Pydantic models ensure structured, validated responses
- **Schema Definition**: Clear field descriptions guide AI output
- **Nested Structures**: `DailySchedule` contains multiple `Task` objects

### 3. Prompt Template
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional organizer. Convert the provided notes into a structured daily plan."),
    ("human", "Here are my notes: {notes}")
])
```

- **System Message**: Sets AI role and behavior
- **Human Message**: Provides user input with variable substitution
- **Template Format**: Consistent prompt structure for reliable results

### 4. Chain Composition
```python
chain = prompt | structured_llm
result = chain.invoke({"notes": combined_notes})
```

- **Pipeline Pattern**: LangChain's `|` operator creates processing pipelines
- **Invocation**: Single method call processes input through entire chain
- **Structured Results**: Output automatically parsed into Pydantic models

## Project Organization

### Architecture Pattern
The project follows a simple, modular architecture:

1. **Entry Point** (`main.py`): Basic launcher
2. **Core Logic** (`organizer.py`): Main application with LangChain integration
3. **Configuration** (`pyproject.toml`): Dependencies and project metadata

### Code Organization Principles

- **Separation of Concerns**: AI logic separated from UI logic
- **Type Safety**: Pydantic models for all data structures
- **Error Handling**: Try-catch blocks for API failures
- **User Experience**: Clear CLI interface with numbered options

### Data Flow

```
User Input → Notes Collection → LangChain Processing → Structured Output → Formatted Display
     ↓             ↓                ↓                     ↓              ↓
   CLI        List Storage     MistralAI API        Pydantic Models   Console Table
```

### Dependencies Management

- **Minimal Dependencies**: Only essential packages
- **Version Pinning**: Specific versions for reproducibility
- **Package Managers**: Supports both pip and uv for installation
- **Core Libraries**:
  - `langchain-core`: Base LangChain functionality
  - `langchain-mistralai`: MistralAI integration
  - `pydantic`: Data validation

## LangChain Best Practices Implemented

1. **Structured Output**: Ensures consistent, parseable AI responses
2. **Prompt Engineering**: Clear system instructions for reliable behavior
3. **Error Handling**: Graceful degradation when API calls fail
4. **Type Safety**: Pydantic integration prevents runtime errors
5. **Modular Design**: Reusable chain components

## Future Extensibility

The current architecture supports easy extension:

- **Alternative LLMs**: Swap MistralAI for other providers
- **Enhanced Schemas**: Add more fields to Task/DailySchedule models
- **Multiple Prompts**: Different prompt templates for various use cases
- **Output Formats**: Additional structured output destinations (JSON, database, etc.)

## Performance Considerations

- **Temperature Setting**: Low temperature (0.1) for consistent results
- **Batch Processing**: Single API call per schedule generation
- **Caching**: No caching implemented (could be added for repeated inputs)
- **Rate Limiting**: No explicit rate limiting (rely on MistralAI limits)