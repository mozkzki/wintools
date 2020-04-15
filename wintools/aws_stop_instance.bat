@echo off

REM https://dev.classmethod.jp/articles/awscli-tips-ec2-start-stop/
REM https://dev.classmethod.jp/articles/awscli-wait-instance-status-ok-include-all-instances/

set instanceid=%1

aws ec2 stop-instances --profile home --instance-ids %instanceid%

echo "ok."
