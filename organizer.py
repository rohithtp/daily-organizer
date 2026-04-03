import os
from typing import List
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# --- Schema Definitions ---
class Task(BaseModel):
    time: str = Field(description="Specific time or logical slot")
    activity: str = Field(description="Task description")
    priority: str = Field(description="High, Medium, or Low")

class DailySchedule(BaseModel):
    tasks: List[Task] = Field(description="Chronological list of tasks")

# --- AI Setup ---
def get_organizer_chain():
    llm = ChatMistralAI(model="mistral-large-latest", temperature=0.1)
    structured_llm = llm.with_structured_output(DailySchedule)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional organizer. Convert the provided notes into a structured daily plan."),
        ("human", "Here are my notes: {notes}")
    ])
    return prompt | structured_llm

# --- Main Application Logic ---
def main():
    notes_list = []
    chain = get_organizer_chain()

    while True:
        print("\n--- 📅 AI DAILY ORGANIZER ---")
        print("1. Add Note/Activity")
        print("2. View Current Notes")
        print("3. Generate & View AI Schedule")
        print("4. Clear All Notes")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")

        if choice == '1':
            note = input("Enter activity or thought: ")
            notes_list.append(note)
            print("✅ Note added.")

        elif choice == '2':
            print("\n--- Current Raw Notes ---")
            for i, n in enumerate(notes_list, 1):
                print(f"{i}. {n}")
            if not notes_list: print("(Empty)")

        elif choice == '3':
            if not notes_list:
                print("❌ No notes to organize! Add some first.")
                continue
            
            print("\n🤖 Mistral is organizing your day...")
            combined_notes = " ".join(notes_list)
            try:
                result = chain.invoke({"notes": combined_notes})
                print("\n--- ✨ YOUR STRUCTURED SCHEDULE ---")
                print(f"{'TIME':<12} | {'ACTIVITY':<35} | {'PRIORITY'}")
                print("-" * 60)
                for task in result.tasks:
                    print(f"{task.time:<12} | {task.activity:<35} | {task.priority}")
            except Exception as e:
                print(f"Error connecting to Mistral: {e}")

        elif choice == '4':
            notes_list = []
            print("🗑️ Notes cleared.")

        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()