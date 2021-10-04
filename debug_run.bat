@echo off
title BotCLI(Debug RUN)
py main.py
echo プログラムの処理が終了しました。何かキーを押すと閉じます。
pause > nul
echo 本当に終了しますか?何かキーを押すと本当に閉じます。
pause > nul
exit