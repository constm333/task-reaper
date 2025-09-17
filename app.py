from flask import Flask, request, render_template, redirect
import json
import os
from datetime import datetime
from printer import format_task, send_to_printer

# Add system tray imports
import threading
import pystray
from PIL import Image, ImageDraw
import webbrowser
import sys

app = Flask(__name__)
TASK_FILE = "tasks.json"
TICKET_COUNTER_FILE = "ticket_counter.json"

# System Tray Functions
def create_tray_icon():
    # Create a simple icon for the system tray
    try:
        # Create a 64x64 image with a white background
        image = Image.new('RGB', (64, 64), 'white')
        dc = ImageDraw.Draw(image)
        # Draw a black rectangle in the center
        dc.rectangle((16, 16, 48, 48), fill='black')
        
        # Tray menu items
        menu = pystray.Menu(
            pystray.MenuItem('Open Task Reaper', open_web_interface),
            pystray.MenuItem('Exit', exit_app)
        )
        
        # Create and run the tray icon
        icon = pystray.Icon("task_reaper", image, "Task Reaper", menu)
        icon.run()
    except Exception as e:
        print(f"Error creating tray icon: {e}")

def open_web_interface():
    """Open the web interface in default browser"""
    webbrowser.open('http://localhost:5000')

def exit_app():
    """Clean exit from the application"""
    print("Shutting down Task Reaper...")
    os._exit(0)

def load_task_counter():
    today = datetime.now().date()

    if os.path.exists(TICKET_COUNTER_FILE):
        with open(TICKET_COUNTER_FILE, "r") as f:
            try:
                data = json.load(f)
                last_date_str = data.get("date")
                count = data.get("count", 0)

                if last_date_str:
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                    if last_date == today:
                        return count
            except (json.JSONDecodeError, ValueError):
                pass  # corrupted file or bad format — start fresh

    return 0

def save_task_counter(count):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(TICKET_COUNTER_FILE, "w") as f:
        json.dump({"date": today, "count": count}, f)

@app.route("/", methods=["GET", "POST"])
def task_form():
    if request.method == "POST":
        task = {
            "title": request.form["title"],
            "subtasks": [s.strip() for s in request.form["subtasks"].split(",") if s.strip()],
            "notes": request.form["notes"],
            "print_now": True
        }

        # Load existing tasks
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(task)

        with open(TASK_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"✅ Task saved: {task['title']}")

        if task["print_now"]:
            # Load and update counter
            counter = load_task_counter()
            counter += 1
            save_task_counter(counter)

            # Format task with current ticket number
            print_text = format_task(task, task.get("subtasks"), task.get("notes"), ticket_number=counter)
            send_to_printer(print_text)

        return redirect("/")

    return render_template("form.html")

if __name__ == "__main__":
    # Start system tray icon in a separate thread
    # Only start if not running in debug mode or frozen (pyinstaller)
    if not hasattr(sys, 'frozen') and not os.environ.get('DEBUG'):
        tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
        tray_thread.start()
        print("System tray icon started")
    
    # Run the Flask app
    app.run(debug=False)