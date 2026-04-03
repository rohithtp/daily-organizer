import os
from typing import List
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# 1. Define the Data Structure
class Task(BaseModel):
    time: str = Field(description="Specific time or 'Flexible'")
    activity: str = Field(description="Task description")
    priority: str = Field(description="High, Medium, or Low")

class DailySchedule(BaseModel):
    tasks: List[Task] = Field(description="Chronological list of tasks")

# 2. Setup Mistral (Ensure MISTRAL_API_KEY is in your env)
llm = ChatMistralAI(model="mistral-large-latest", temperature=0.1)
structured_llm = llm.with_structured_output(DailySchedule)

# 3. Define the Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI Daily Organizer. Transform messy notes into a structured schedule."),
    ("human", "Organize these tasks for today: {user_input}")
])

# 4. Chain & Execution
chain = prompt | structured_llm

def parse_tasks(raw_notes: str):
    clean = raw_notes.rstrip(".").replace(" and ", ", ")
    return [t.strip().capitalize() for t in clean.split(",") if t.strip()]


def run_organizer():
    raw_notes = input("Enter your tasks (comma or 'and' separated): ")
    tasks = parse_tasks(raw_notes)
    print(tasks)
    result = chain.invoke({"user_input": raw_notes})

    print("\n--- Your Organized Day ---")
    for task in result.tasks:
        print(f"{task.time: <10} | {task.activity: <30} | Priority: {task.priority}")

if __name__ == "__main__":
    run_organizer()
