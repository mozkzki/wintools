@echo off

REM "http://www.lancarse.co.jp/blog/?p=1076"
REM jenkins �}���`�\���v���W�F�N�g�Ŏ��s����

mkdir .\git_barnch_test
pushd .\git_barnch_test

set repogitory=git@github.com:yukkun007/tmp.git
set branch_name=support/V9.0.0



REM %[���̕�����]:[�u�������O�̕�����]=[�u��������̕�����]%
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
