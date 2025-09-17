@echo off
cd /d "C:\Users\const\taskprinter"
call venv\Scripts\activate
start /B pythonw app.py
exit