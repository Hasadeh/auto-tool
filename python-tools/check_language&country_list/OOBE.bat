chcp 65001
@echo off
setlocal enabledelayedexpansion
adb devices

:: 获取连接的设备列表
for /f "skip=1 tokens=1" %%i in ('adb devices') do (
    if "%%i" NEQ "List" (
        set device=%%i
        ECHO 正在处理: !device!
        
        adb -s !device! root
        
        adb -s !device! shell settings put secure user_setup_complete 1
        adb -s !device! shell settings put global device_provisioned 1
        adb -s !device! shell settings put system system_locales en-US
        adb -s !device! shell input keyevent 4
        adb -s !device! shell am start -a android.intent.action.MAIN -c android.intent.category.HOME
        adb -s !device! shell getprop ro.build.display.id
    )
)

endlocal
pause
