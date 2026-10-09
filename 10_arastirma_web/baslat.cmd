@echo off
setlocal
where py >nul 2>&1
if not errorlevel 1 (
  py -3 "%~dp0serve.py" %*
  exit /b
)
where python >nul 2>&1
if not errorlevel 1 (
  python "%~dp0serve.py" %*
  exit /b
)
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
  "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "%~dp0serve.py" %*
  exit /b
)
echo Python 3.10+ bulunamadi. Python kurup bu komutu tekrar calistirin.
exit /b 1
