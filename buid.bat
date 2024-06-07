@echo off
echo 切换环境
call conda activate python38
echo 开始执行pyintaller打包命令
pyinstaller editorWnd\main.py -n 编程可视化编辑器 --add-data editorWnd:editorWnd --add-data assets:assets --add-data 注册ico.bat:. --add-data 取消注册ico.bat:. -y --clean -D -i icon.ico --contents-directory . 
echo 复制打包后的文件夹
xcopy /S /Y dist ..
echo 删除打包创建的临时文件和文件夹
del /Q *.spec
rmdir /Q /S dist
rmdir /Q /S build 2> nul
timeout /t 1 /nobreak > nul
rmdir /Q /S build > nul