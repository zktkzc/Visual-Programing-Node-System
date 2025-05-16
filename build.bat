@echo off
for /f %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"
chcp 65001

echo %ESC%[38;5;42m========================[1.切换python环境]========================%ESC%[0m
call .venv\Scripts\activate.bat

echo %ESC%[38;5;42m========================[2.开始执行pyintaller打包命令]========================%ESC%[0m
pyinstaller editorWnd\main.py -n 编程可视化编辑器 --add-data editorWnd:editorWnd --add-data assets:assets --add-data 注册ico.bat:. --add-data 取消注册ico.bat:. -y --clean -D -i assets\app.ico --contents-directory .
echo %ESC%[38;5;42m================================================================================%ESC%[0m

echo %ESC%[38;5;42m========================[3.复制打包后的文件夹]========================%ESC%[0m
xcopy /S /Y dist ..
echo %ESC%[38;5;42m================================================================================%ESC%[0m

echo %ESC%[38;5;42m========================[4.删除打包创建的临时文件和文件夹]========================%ESC%[0m
del /Q *.spec
rmdir /Q /S dist
rmdir /Q /S build 2
timeout /t 1 /nobreak > nul
rmdir /Q /S build
echo %ESC%[38;5;42m================================================================================%ESC%[0m

pause