:Start

@echo off
title FCU-AutoClass
chcp 65001

for /F "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do set datetime=%%I
set currentDate=%datetime:~0,8%-%datetime:~8,6%
FCU-AutoClass.exe 2> "logs\logs-%currentDate%.txt"

for /f "delims=" %%a in ("logs\logs-%currentDate%.txt") do (
    if "%%a"=="All classes joined." (
        goto :End
    )
)

echo 現在可按視窗右上角的 X 關閉程式 否則將於5sec後自動重新啟動
timeout /t 5 > nul
goto Start

:End