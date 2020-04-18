@echo off

REM "http://www.lancarse.co.jp/blog/?p=1076"
REM jenkins マルチ構成プロジェクトで実行する

mkdir .\git_barnch_test
pushd .\git_barnch_test

set repogitory=git@github.com:yukkun007/tmp.git
set branch_name=support/V9.0.0



REM %[元の文字列]:[置き換え前の文字列]=[置き換え後の文字列]%
set repo_name_tmp=%repogitory:git@github.com:yukkun007/=%
set repo_name=%repo_name_tmp:.git=%
echo %repo_name%

rmdir /s /q .\%repo_name%
git clone %repogitory%
pushd .\%repo_name%

git checkout -b %branch_name% origin/master
git branch -a
git push -u origin %branch_name%

popd
popd
