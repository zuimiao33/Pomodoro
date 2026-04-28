@echo off
set "ROOT=%~dp0"
start "todo-backend" cmd /k "cd /d "%ROOT%backend" && call start-dev.cmd"
start "todo-frontend" cmd /k "cd /d "%ROOT%frontend" && call start-dev.cmd"
