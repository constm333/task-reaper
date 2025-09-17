@echo off
cd /d "Your install location here"
call venv\Scripts\activate
start /B pythonw app.py

exit
