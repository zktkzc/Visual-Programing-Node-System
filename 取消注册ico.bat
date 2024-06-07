@echo off
REM 提示用户输入文件扩展名和文件类型名称
set extension=.vgf
set fileTypeName=Visual Graph File

REM 删除文件类型的注册表项
reg delete "HKEY_CLASSES_ROOT\%extension%" /f
reg delete "HKEY_CLASSES_ROOT\%fileTypeName%" /f

REM 刷新图标缓存
echo Refreshing icon cache...
ie4uinit.exe -ClearIconCache
taskkill /IM explorer.exe /F
start explorer.exe

echo Unregistration completed successfully.
pause
