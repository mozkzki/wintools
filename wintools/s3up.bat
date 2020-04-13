@echo off

py %~dp0\s3up.py --bucket magarimame --dir test --profile home %1
pause
