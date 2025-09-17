import json
import datetime
import os
import time
from printer import send_to_printer, format_task  # Import format_task from printer.py

# Add these counter functions from your Flask app
def load_task_counter():
    today = datetime.datetime.now().date()
    TICKET_COUNTER_FILE = "ticket_counter.json"

    if os.path.exists(TICKET_COUNTER_FILE):
        with open(TICKET_COUNTER_FILE, "r") as f:
            try:
                data = json.load(f)
                last_date_str = data.get("date")
                count = data.get("count", 0)

                if last_date_str:
                    last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d").date()
                    if last_date == today:
                        return count
            except (json.JSONDecodeError, ValueError):
                pass  # corrupted file or bad format — start fresh

    return 0

def save_task_counter(count):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    TICKET_COUNTER_FILE = "ticket_counter.json"
    with open(TICKET_COUNTER_FILE, "w") as f:
        json.dump({"date": today, "count": count}, f)

def load_tasks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_last_run():
    if os.path.exists('last_run.json'):
        with open('last_run.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"daily": None, "weekly": None}

def save_last_run(daily_date=None, weekly_date=None):
    last_run = load_last_run()
    if daily_date:
        last_run["daily"] = daily_date.isoformat()
    if weekly_date:
        last_run["weekly"] = weekly_date.isoformat()
    with open('last_run.json', 'w', encoding='utf-8') as f:
        json.dump(last_run, f, indent=2)

def print_tasks_from_file(file_path, delay_seconds=4):
    tasks = load_tasks(file_path)
    counter = load_task_counter()  # Load current counter
    
    for i, task in enumerate(tasks, 1):
        ticket_number = counter + i  # Calculate actual ticket number
        # FIXED: Added subtasks parameter to pass subtasks from JSON
        ticket_text = format_task(task, 
                                 subtasks=task.get('subtasks'), 
                                 notes=task.get('notes'), 
                                 ticket_number=ticket_number)
        send_to_printer(ticket_text)
        time.sleep(delay_seconds)
    
    # Update the counter after printing all tasks
    save_task_counter(counter + len(tasks))

def should_print_daily():
    last_run = load_last_run()
    last_daily = datetime.datetime.fromisoformat(last_run["daily"]).date() if last_run["daily"] else None
    current_date = datetime.datetime.now().date()
    return last_daily != current_date if last_daily else True

def should_print_weekly():
    last_run = load_last_run()
    last_weekly = datetime.datetime.fromisoformat(last_run["weekly"]).date() if last_run["weekly"] else None
    current_week = datetime.datetime.now().isocalendar()[1]
    last_week = last_weekly.isocalendar()[1] if last_weekly else None
    return datetime.datetime.now().weekday() == 4 and (last_week != current_week if last_weekly else True)

def daily_print():
    if not should_print_daily():
        print(" [P] Daily tasks already printed today, exiting.")
        return False
    response = input("Ready to print Daily Tasks (y/n): ").lower()
    if response == 'y':
        print(" > Printing Daily Auto Tasks:")
        print_tasks_from_file("auto_daily.json")
        save_last_run(daily_date=datetime.datetime.now())
    else:
        print(" [P] Daily tasks skipped.")
    return True

def weekly_print():
    if not should_print_weekly():
        print(" [P] Weekly tasks not scheduled or already printed this week, exiting.")
        return False
    response = input("Ready to print Weekly Tasks (y/n): ").lower()
    if response == 'y':
        print(" > Printing Weekly Auto Tasks:")
        print_tasks_from_file("auto_weekly.json")
        save_last_run(weekly_date=datetime.datetime.now())
    else:
        print(" [P] Weekly tasks skipped.")
    return True

if __name__ == "__main__":
    print(rf""" 
  ______           __      ____                            
 /_  __/___ ______/ /__   / __ \___  ____ _____  ___  _____
  / / / __ `/ ___/ //_/  / /_/ / _ \/ __ `/ __ \/ _ \/ ___/
 / / / /_/ (__  ) ,<    / _, _/  __/ /_/ / /_/ /  __/ /    
/_/  \__,_/____/_/|_|  /_/ |_|\___/\__,_/ .___/\___/_/   V1
                                       /_/
    Task Reaper: Manual Cutting @ {datetime.datetime.now().strftime('%H:%M %d/%m/%y')}""")
    
    daily_result = daily_print()
    if daily_result and datetime.datetime.now().weekday() == 4:
        weekly_result = weekly_print()
    
    print(" [OK] Done, exiting.")
    
    # Auto-close after 3 seconds instead of waiting for key press
    time.sleep(5)