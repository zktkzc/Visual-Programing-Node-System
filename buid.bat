@echo off
echo �л�����
call conda activate python38
echo ��ʼִ��pyintaller�������
pyinstaller editorWnd\main.py -n ��̿��ӻ��༭�� --add-data editorWnd:editorWnd --add-data assets:assets --add-data ע��ico.bat:. --add-data ȡ��ע��ico.bat:. -y --clean -D -i icon.ico --contents-directory . 
echo ���ƴ������ļ���
xcopy /S /Y dist ..
echo ɾ�������������ʱ�ļ����ļ���
del /Q *.spec
rmdir /Q /S dist
rmdir /Q /S build 2> nul
timeout /t 1 /nobreak > nul
rmdir /Q /S build > nul