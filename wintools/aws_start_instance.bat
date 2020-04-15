@echo off

REM https://dev.classmethod.jp/articles/awscli-tips-ec2-start-stop/
REM https://dev.classmethod.jp/articles/awscli-wait-instance-status-ok-include-all-instances/

set instanceid=%1

rem 既に起動している場合、エラーにならずすぐ返ってくる→このまま呼べば良い
aws ec2 start-instances --profile home --instance-ids %instanceid%
aws ec2 wait instance-status-ok --profile home --include-all-instances --instance-ids %instanceid%
aws ec2 describe-instances --profile home --instance-ids %instanceid% --query Reservations[].Instances[].[InstanceId,State.Name] --output text

echo "ok."
