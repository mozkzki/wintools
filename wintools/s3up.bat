@echo off

python s3up.py %1

REM echo %1 -----^> s3://magarimame

REM rem アップロード
REM @echo on
REM rem aws s3 cp s3://magarimame --recursive --human-readable --summarize --profile home
REM @echo off
REM echo done.

REM rem アップロード後の確認
REM @echo on
REM aws s3 ls s3://magarimame --recursive --human-readable --summarize --profile home
REM @echo off

pause