@echo off

REM �p�����[�^���p�����[�^�Œu������T���v��

set recipi=aaaaaaaaaaaa $VARG1$ test recipi $VARG2$ this is test
set varg1_value=hogehoge
set varg2_value=foobar

REM %[���̕�����]:[�u�������O�̕�����]=[�u��������̕�����]%
call set recipi=%%recipi:$VARG1$=%varg1_value%%%
call set recipi=%%recipi:$VARG2$=%varg2_value%%%

echo %recipi%
