@echo off
echo Copying SafeOps AI datasets to your Downloads folder...
if not exist "%USERPROFILE%\Downloads\SafeOps_Datasets" mkdir "%USERPROFILE%\Downloads\SafeOps_Datasets"
copy /Y "%~dp0datasets\*.*" "%USERPROFILE%\Downloads\SafeOps_Datasets\"
echo.
echo ============================================================
echo All 12 datasets copied successfully to:
echo %USERPROFILE%\Downloads\SafeOps_Datasets
echo ============================================================
explorer.exe "%USERPROFILE%\Downloads\SafeOps_Datasets"
pause
