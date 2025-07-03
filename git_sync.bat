@echo off
setlocal enabledelayedexpansion

echo 🔍 当前 Git 状态：
git status

set /p confirm=是否继续提交并推送？(Y/N): 
if /I "%confirm%" NEQ "Y" (
    echo ❌ 已取消操作。
    exit /b
)

:: 设置 commit 信息（带时间）
for /f %%i in ('powershell -command "Get-Date -Format \"yyyy-MM-dd HH:mm:ss\""') do set now=%%i
set msg=自动同步提交：!now!

echo 🕒 当前时间：!now!
git add .
git commit -m "!msg!"
git push

echo ✅ 同步完成！
pause
