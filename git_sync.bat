@echo off

setlocal enabledelayedexpansion

echo ?? ��ǰ Git ״̬��
git status

set /p confirm=�Ƿ�����ύ�����ͣ�(Y/N): 
if /I "%confirm%" NEQ "Y" (
    echo ? ��ȡ��������
    exit /b
)

:: ���� commit ��Ϣ����ʱ�䣩
for /f %%i in ('powershell -command "Get-Date -Format \"yyyy-MM-dd HH:mm:ss\""') do set now=%%i
set msg=�Զ�ͬ���ύ��!now!

echo ?? ��ǰʱ�䣺!now!
git add .
git commit -m "!msg!"
git push

echo ? ͬ����ɣ�
pause
