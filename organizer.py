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

# --- Export Functions ---
def get_priority_emoji(priority):
    """Return emoji for priority level"""
    priority = priority.lower()
    if "high" in priority:
        return "🔴"
    elif "medium" in priority:
        return "🟡"
    else:
        return "🟢"

def export_schedule_to_markdown(schedule):
    """Export AI-generated schedule to Markdown format"""
    if not schedule or not schedule.tasks:
        print("❌ No schedule to export!")
        return
    
    filename = "daily-schedule.md"
    with open(filename, "w") as f:
        f.write("# 📅 Daily Schedule\n\n")
        f.write(f"**Generated:** {os.popen('date').read().strip()}\n\n")
        f.write("| Time | Activity | Priority |\n")
        f.write("|------|----------|----------|\n")
        for task in schedule.tasks:
            emoji = get_priority_emoji(task.priority)
            f.write(f"| {task.time} | {task.activity} | {emoji} {task.priority} |\n")
    print(f"✅ Exported to Markdown: {filename}")

def export_schedule_to_logseq(schedule):
    """Export AI-generated schedule to Logseq format"""
    if not schedule or not schedule.tasks:
        print("❌ No schedule to export!")
        return
    
    filename = "daily-schedule.md"
    with open(filename, "w") as f:
        f.write("- Daily Schedule\n")
        f.write("  collapsed:: false\n")
        for task in schedule.tasks:
            emoji = get_priority_emoji(task.priority)
            f.write(f"  - {task.time}\n")
            f.write(f"    - {task.activity}\n")
            f.write(f"      #priority:: {task.priority}\n")
            f.write(f"      #status:: TODO\n")
    print(f"✅ Exported to Logseq format: {filename}")

# --- Main Application Logic ---
def main():
    notes_list = []
    generated_schedule = None
    chain = get_organizer_chain()

    while True:
        print("\n--- 📅 AI DAILY ORGANIZER ---")
        print("1. Add Note/Activity")
        print("2. View Current Notes")
        print("3. Edit Note")
        print("4. Delete Note")
        print("5. Generate & View AI Schedule")
        print("6. Export Schedule to Markdown")
        print("7. Export Schedule to Logseq Format")
        print("8. Clear All Notes")
        print("9. Exit")
        
        choice = input("\nSelect an option (1-9): ")

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
                print("❌ No notes to edit!")
                continue
            print("\n--- Current Notes ---")
            for i, n in enumerate(notes_list, 1):
                print(f"{i}. {n}")
            index = int(input("\nEnter note number to edit: ")) - 1
            if 0 <= index < len(notes_list):
                notes_list[index] = input(f"Edit note (current: {notes_list[index]}): ")
                print("✅ Note updated.")
            else:
                print("❌ Invalid note number.")

        elif choice == '4':
            if not notes_list:
                print("❌ No notes to delete!")
                continue
            print("\n--- Current Notes ---")
            for i, n in enumerate(notes_list, 1):
                print(f"{i}. {n}")
            index = int(input("\nEnter note number to delete: ")) - 1
            if 0 <= index < len(notes_list):
                deleted = notes_list.pop(index)
                print(f"🗑️ Deleted: {deleted}")
            else:
                print("❌ Invalid note number.")

        elif choice == '5':
            if not notes_list:
                print("❌ No notes to organize! Add some first.")
                continue
            
            print("\n🤖 Mistral is organizing your day...")
            combined_notes = " ".join(notes_list)
            try:
                result = chain.invoke({"notes": combined_notes})
                generated_schedule = result
                print("\n--- ✨ YOUR STRUCTURED SCHEDULE ---")
                print(f"{'TIME':<12} | {'ACTIVITY':<35} | {'PRIORITY'}")
                print("-" * 60)
                for task in result.tasks:
                    print(f"{task.time:<12} | {task.activity:<35} | {task.priority}")
                print("\n💡 You can now export this schedule to Markdown (option 6) or Logseq (option 7)")
            except Exception as e:
                print(f"Error connecting to Mistral: {e}")

        elif choice == '6':
            if not generated_schedule:
                print("❌ No schedule to export! Generate one first (option 5).")
                continue
            export_schedule_to_markdown(generated_schedule)

        elif choice == '7':
            if not generated_schedule:
                print("❌ No schedule to export! Generate one first (option 5).")
                continue
            export_schedule_to_logseq(generated_schedule)

        elif choice == '8':
            notes_list = []
            print("🗑️ Notes cleared.")

        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()