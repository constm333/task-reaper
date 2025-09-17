# 💀 Task Reaper

A productivity system for printing tasks from your PC using a 58mm thermal receipt printer. Features a web-based task submission form, automated daily/weekly task printing, and system tray integration for background operation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)](https://flask.palletsprojects.com/)

## 🌟 Features

- **Web Interface**: Web-based task submission form.
- **Automatic Scheduling**: Prints daily and weekly tasks automatically.
- **Ticket Numbering**: Sequential numbering with daily reset.
- **System Tray Integration**: Runs in the background with a tray icon (Windows).
- **Thermal Printer Support**: Optimized for 58mm receipt printers.
- **Cross-Platform**: Windows native, Linux with CUPS adjustments.

## 📁 Project Structure

```
taskprinter/
├── app.py                # Flask web app with system tray integration
├── scheduler.py          # Automated daily/weekly task printing
├── printer.py            # Thermal printer formatting and communication
├── run_taskreaper.bat    # Windows launcher for web app
├── run_scheduler.bat     # Windows launcher for scheduler
├── tasks.json            # Stores one-off tasks from web interface
├── auto_daily.json       # Repeating daily tasks
├── auto_weekly.json      # Repeating weekly tasks (Friday)
├── ticket_counter.json   # Tracks daily ticket numbers
├── last_run.json         # Tracks scheduler execution history
├── requirements.txt      # Python dependencies
├── static/
│   └── styles.css        # Web interface styling
└── templates/
    └── form.html         # Web form for task submission
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- 58mm thermal receipt printer (connected and configured)
- Windows (for `pywin32`) or Linux (with CUPS for printing)
- Virtual environment recommended

### 1. Clone and Setup
```bash
git clone https://github.com/constm333/task-reaper.git
cd task-reaper
python -m venv venv
# Windows: venv\Scripts\activate
# Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Tasks
Edit JSON files to define tasks:

**auto_daily.json** (prints daily):
```json
[
  {
    "title": "Morning Routine",
    "notes": "Daily auto task",
    "subtasks": ["Check emails", "Plan day"]
  }
]
```

**auto_weekly.json** (prints every Friday):
```json
[
  {
    "title": "Weekly Review",
    "notes": "Friday auto task",
    "subtasks": ["Review goals", "Update reports"]
  }
]
```

### 3. Printer Configuration
- Ensure your thermal printer is set as the default or specified in `printer.py` (modify `printer_name = "58M Thermal Printer"`).
- For Linux, install CUPS and update `printer.py` to use `python-escpos` or `cups` libraries.

### 4. Run the Application
```bash
# Start web interface (http://localhost:5000)
python app.py
# Run scheduler manually
python scheduler.py
```

### 5. Automated Startup (Windows)
- **Web Interface**:
  1. Open Task Scheduler → Create Basic Task.
  2. Trigger: "At log on".
  3. Action: Start `run_taskreaper.bat`.
- **Scheduler**:
  1. Open Task Scheduler → Create Basic Task.
  2. Trigger: "At startup".
  3. Action: Start `run_scheduler.bat`.

### 6. System Tray Controls
Right-click the Task Reaper tray icon (Windows):
- **Open Task Reaper**: Opens web interface in browser.
- **Exit**: Shuts down the app.

## ▶️ Usage
- **Web Interface**: Visit `http://localhost:5000` to submit tasks with a title, subtasks (comma-separated), and notes. Tasks print automatically.
- **Scheduler**: Run `scheduler.py` to print daily tasks or weekly tasks (on Fridays).
- **Task Format**: Tasks are printed with a ticket number, date, title, subtasks, and notes.

## ⚙️ Configuration
- **Task Files**: `tasks.json` (web tasks), `auto_daily.json` (daily), `auto_weekly.json` (weekly).
- **Ticket Counter**: `ticket_counter.json` resets daily.
- **Scheduler History**: `last_run.json` tracks last print times.
- **Print Format**: Customize in `printer.py` (`format_task` function).

## 🔧 Portability
- **Windows to Windows**: Copy folder, update `.bat` file paths, reconfigure Task Scheduler.
- **Windows to Linux**:
  - Convert `.bat` to `.sh` scripts.
  - Replace Task Scheduler with `cron` or `systemd`.
  - Update `printer.py` to use CUPS or `python-escpos`.

## 🐛 Troubleshooting
- **Printer Not Found**: Verify printer name in `printer.py` and ensure it’s connected.
- **JSON Errors**: Validate JSON syntax in task files.
- **Web Interface Inaccessible**: Check firewall settings for port 5000.
- **Scheduler Issues**: Ensure Task Scheduler or cron jobs are configured correctly.

**Task JSON Structure**:
```json
{
  "title": "Task name",
  "subtasks": ["subtask1", "subtask2"],
  "notes": "Additional information",
  "print_now": true
}
```

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Credits
**Made by C.M. - Braila, 2025**

### Acknowledgments
- Flask team for the web framework.
- pystray for system tray integration.
- Python community for thermal printer libraries.

## 🔮 Future Enhancements
- Mobile app interface.
- Cloud sync for tasks.
- Support for multiple printers.
- Advanced scheduling options.
- Task statistics and reporting.

**Happy Printing!** 🐱
