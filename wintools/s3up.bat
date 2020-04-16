@echo off

py %~dp0\s3.py --mode upload --bucket magarimame --dir test --profile home %1
pause
