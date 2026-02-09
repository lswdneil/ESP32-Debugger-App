@echo off
chcp 65001 >nul
echo ========================================
echo ESP32调试助手 - 完整自动构建系统
echo ========================================
echo.
echo 本脚本将自动完成以下步骤：
echo 1. 检查并安装Java JDK
echo 2. 下载Android命令行工具
echo 3. 配置Android SDK
echo 4. 构建APK
echo.
echo 预计总时间：30-60分钟（取决于网络速度）
echo.
pause

REM 创建工作目录
set WORK_DIR=%USERPROFILE%\AndroidBuildTools
if not exist "%WORK_DIR%" mkdir "%WORK_DIR%"
cd /d "%WORK_DIR%"

echo.
echo ========================================
echo [1/5] 检查Java环境
echo ========================================

REM 检查Java
java -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Java已安装
    java -version
    goto :android_sdk
)

echo Java未安装，准备下载安装...
echo.
echo 请选择安装方式：
echo 1. 自动下载安装JDK（推荐）
echo 2. 手动安装（需要您自己下载）
echo 3. 跳过（如果已安装但未配置环境变量）
echo.
set /p choice="请输入选择 (1/2/3): "

if "%choice%"=="1" goto :auto_install_jdk
if "%choice%"=="2" goto :manual_install_jdk
if "%choice%"=="3" goto :android_sdk

:auto_install_jdk
echo.
echo 正在下载JDK 17...
echo 下载地址: https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe
echo.
echo 由于Oracle JDK需要登录，建议使用OpenJDK
echo 正在下载 Microsoft OpenJDK 17...

REM 使用PowerShell下载
powershell -Command "& {Invoke-WebRequest -Uri 'https://aka.ms/download-jdk/microsoft-jdk-17.0.9-windows-x64.msi' -OutFile 'openjdk-17.msi'}"

if exist "openjdk-17.msi" (
    echo ✓ 下载完成
    echo 正在安装...
    msiexec /i openjdk-17.msi /qn
    echo ✓ 安装完成
    
    REM 设置JAVA_HOME
    setx JAVA_HOME "C:\Program Files\Microsoft\jdk-17.0.9-hotspot"
    setx PATH "%PATH%;%JAVA_HOME%\bin"
    
    echo 请关闭并重新打开命令提示符，然后重新运行此脚本
    pause
    exit
) else (
    echo ✗ 下载失败
    goto :manual_install_jdk
)

:manual_install_jdk
echo.
echo 请手动下载并安装JDK：
echo.
echo 选项1: Microsoft OpenJDK 17
echo https://learn.microsoft.com/zh-cn/java/openjdk/download
echo.
echo 选项2: Oracle JDK 17
echo https://www.oracle.com/java/technologies/downloads/
echo.
echo 安装完成后，请重新运行此脚本
pause
exit

:android_sdk
echo.
echo ========================================
echo [2/5] 检查Android SDK
echo ========================================

if defined ANDROID_HOME (
    echo ✓ ANDROID_HOME已设置: %ANDROID_HOME%
    goto :download_gradle
)

echo Android SDK未配置
echo 正在下载Android命令行工具...

set SDK_DIR=%WORK_DIR%\android-sdk
if not exist "%SDK_DIR%" mkdir "%SDK_DIR%"

REM 下载Android命令行工具
echo 下载 Android Command Line Tools...
powershell -Command "& {Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/commandlinetools-win-9477386_latest.zip' -OutFile 'cmdline-tools.zip'}"

if exist "cmdline-tools.zip" (
    echo ✓ 下载完成
    echo 正在解压...
    powershell -Command "Expand-Archive -Path 'cmdline-tools.zip' -DestinationPath '%SDK_DIR%' -Force"
    
    REM 重命名目录
    if not exist "%SDK_DIR%\cmdline-tools" mkdir "%SDK_DIR%\cmdline-tools"
    move "%SDK_DIR%\cmdline-tools" "%SDK_DIR%\cmdline-tools\latest"
    
    REM 设置环境变量
    setx ANDROID_HOME "%SDK_DIR%"
    setx PATH "%PATH%;%SDK_DIR%\cmdline-tools\latest\bin;%SDK_DIR%\platform-tools"
    
    echo ✓ Android SDK配置完成
) else (
    echo ✗ 下载失败，请检查网络连接
    pause
    exit /b 1
)

:download_gradle
echo.
echo ========================================
echo [3/5] 准备Gradle
echo ========================================

cd /d "C:\Users\wd_al\Desktop\ESP32_Debugger_App"

REM 创建Gradle Wrapper
if not exist "gradlew.bat" (
    echo 创建Gradle Wrapper...
    
    REM 创建gradle wrapper配置
    if not exist "gradle\wrapper" mkdir "gradle\wrapper"
    
    echo distributionUrl=https\://services.gradle.org/distributions/gradle-8.0-bin.zip > gradle\wrapper\gradle-wrapper.properties
    
    REM 下载gradlew文件
    powershell -Command "& {Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/gradle/gradle/master/gradlew.bat' -OutFile 'gradlew.bat'}"
    powershell -Command "& {Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/gradle/gradle/master/gradlew' -OutFile 'gradlew'}"
)

echo ✓ Gradle准备完成

:install_sdk_packages
echo.
echo ========================================
echo [4/5] 安装Android SDK组件
echo ========================================

REM 接受许可
echo y | %ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager --licenses

REM 安装必要的SDK组件
echo 安装SDK组件（这可能需要10-20分钟）...
%ANDROID_HOME%\cmdline-tools\latest\bin\sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"

echo ✓ SDK组件安装完成

:build_apk
echo.
echo ========================================
echo [5/5] 构建APK
echo ========================================

cd /d "C:\Users\wd_al\Desktop\ESP32_Debugger_App"

echo 清理旧构建...
if exist "app\build" rmdir /s /q "app\build"

echo.
echo 开始构建APK...
echo 这可能需要5-10分钟，请耐心等待...
echo.

call gradlew.bat assembleDebug

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✓✓✓ 构建成功！✓✓✓
    echo ========================================
    echo.
    
    set APK_PATH=app\build\outputs\apk\debug\app-debug.apk
    
    if exist "%APK_PATH%" (
        echo APK文件位置:
        echo %CD%\%APK_PATH%
        echo.
        
        REM 复制到桌面
        copy "%APK_PATH%" "%USERPROFILE%\Desktop\ESP32_Debugger.apk"
        echo ✓ APK已复制到桌面: ESP32_Debugger.apk
        echo.
        
        REM 显示文件信息
        dir "%USERPROFILE%\Desktop\ESP32_Debugger.apk"
        echo.
        echo ========================================
        echo 安装说明:
        echo ========================================
        echo.
        echo 方法1: 通过USB安装
        echo   1. 手机连接电脑
        echo   2. 启用USB调试
        echo   3. 运行: adb install ESP32_Debugger.apk
        echo.
        echo 方法2: 手动安装
        echo   1. 将APK传输到手机
        echo   2. 在手机上点击APK文件
        echo   3. 允许安装未知来源应用
        echo.
        echo ========================================
    ) else (
        echo ✗ 未找到APK文件
    )
) else (
    echo.
    echo ✗ 构建失败
    echo 请检查上面的错误信息
)

echo.
pause
