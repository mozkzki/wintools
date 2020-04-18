@echo off

REM パラメータをパラメータで置換するサンプル

set recipi=aaaaaaaaaaaa $VARG1$ test recipi $VARG2$ this is test
set varg1_value=hogehoge
set varg2_value=foobar

REM %[元の文字列]:[置き換え前の文字列]=[置き換え後の文字列]%
call set recipi=%%recipi:$VARG1$=%varg1_value%%%
call set recipi=%%recipi:$VARG2$=%varg2_value%%%

echo %recipi%
