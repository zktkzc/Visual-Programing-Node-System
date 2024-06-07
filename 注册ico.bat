@echo off
REM 提示用户输入文件扩展名、文件类型名称、描述和ICO文件路径
set extension=.vgf
set fileTypeName=Visual Graph File
set description=Visual Graph File
set current_dir=%cd%
set iconPath=%current_dir%\assets\file.ico

REM 检查ICO文件是否存在
if not exist "%iconPath%" (
    echo Icon file not found: %iconPath%
    exit /b 1
)

REM 创建文件类型的注册表项
reg add "HKEY_CLASSES_ROOT\%extension%" /ve /d "%fileTypeName%" /f
reg add "HKEY_CLASSES_ROOT\%fileTypeName%" /ve /d "%description%" /f
reg add "HKEY_CLASSES_ROOT\%fileTypeName%\DefaultIcon" /ve /d "%iconPath%" /f

REM 刷新图标缓存
echo Refreshing icon cache...
ie4uinit.exe -ClearIconCache
taskkill /IM explorer.exe /F
start explorer.exe

echo Registration completed successfully.
pause
