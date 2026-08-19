@echo off
chcp 65001 >nul
rem `tia` 命令入口（V21）。把本交付包根目录加入 PATH 后，可直接：tia gen spec.yaml
rem V20 用户请改用同目录的 tia-v20.cmd。所有参数原样透传给引擎 exe。
rem 交付 zip 布局在 tools\...\bin\Release\net48；git 克隆布局在 runtime\v21。两处都找。
set "EXE=%~dp0tools\tiaportal-mcp\src\TiaMcpServer\bin\Release\net48\TiaMcpServer.exe"
if not exist "%EXE%" set "EXE=%~dp0runtime\v21\TiaMcpServer.exe"
if not exist "%EXE%" (
  echo [错误] 找不到引擎 exe（tools\...\bin\Release\net48 和 runtime\v21 均不存在）。
  exit /b 2
)
"%EXE%" %*
exit /b %ERRORLEVEL%
