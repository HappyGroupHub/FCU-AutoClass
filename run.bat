:Start

@echo off
title FCU-AutoClass
chcp 65001
set currentDate=%date:~-4,4%-%date:~4,2%-%date:~7,2%-%time:~0,2%%time:~3,2%%time:~6,2%
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