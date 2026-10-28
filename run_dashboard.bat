@echo off
title SafeOps AI Platform - Team Idea Ignitors (XH-23)
echo ========================================================
echo Starting SafeOps AI Autonomous Remediation Platform...
echo Cynefian Hackathon - AI-Ops Track | Team Idea Ignitors
echo ========================================================
echo.
cd /d "%~dp0"
echo Starting web server on http://localhost:8080 ...
start "" "http://localhost:8080"
python app.py
pause
