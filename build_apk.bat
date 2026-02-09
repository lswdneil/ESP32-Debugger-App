@echo off
chcp 65001 >nul
echo ========================================
echo ESP32调试助手 - 自动构建脚本
echo ========================================
echo.

REM 检查是否安装了Android SDK
echo [1/5] 检查Android SDK...
if not defined ANDROID_HOME (
    echo ✗ 未找到ANDROID_HOME环境变量
    echo.
    echo 请先安装Android Studio或Android SDK
    echo 下载地址: https://developer.android.com/studio
    echo.
    echo 安装后设置环境变量:
    echo ANDROID_HOME=你的Android SDK路径
    echo 例如: C:\Users\%USERNAME%\AppData\Local\Android\Sdk
    echo.
    pause
    exit /b 1
)

echo ✓ Android SDK: %ANDROID_HOME%
echo.

REM 检查Java
echo [2/5] 检查Java环境...
java -version >nul 2>&1
if errorlevel 1 (
    echo ✗ 未找到Java
    echo 请安装JDK 11或更高版本
    pause
    exit /b 1
)

echo ✓ Java环境正常
echo.

REM 进入项目目录
cd /d "%~dp0"

REM 检查Gradle Wrapper
echo [3/5] 检查Gradle...
if not exist "gradlew.bat" (
    echo ✗ 未找到gradlew.bat
    echo 正在创建Gradle Wrapper...
    
    REM 创建gradle wrapper
    gradle wrapper --gradle-version 8.0
)

echo ✓ Gradle准备就绪
echo.

REM 清理旧的构建
echo [4/5] 清理旧构建...
if exist "app\build" (
    rmdir /s /q "app\build"
)
echo ✓ 清理完成
echo.

REM 构建APK
echo [5/5] 开始构建APK...
echo 这可能需要几分钟时间，请耐心等待...
echo.

call gradlew.bat assembleDebug

if errorlevel 1 (
    echo.
    echo ✗ 构建失败
    echo 请检查错误信息
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ 构建成功！
echo ========================================
echo.

REM 查找生成的APK
set APK_PATH=app\build\outputs\apk\debug\app-debug.apk

if exist "%APK_PATH%" (
    echo APK位置: %APK_PATH%
    echo 文件大小: 
    dir "%APK_PATH%" | find "app-debug.apk"
    echo.
    
    REM 复制到桌面
    echo 正在复制APK到桌面...
    copy "%APK_PATH%" "%USERPROFILE%\Desktop\ESP32_Debugger.apk" >nul
    if errorlevel 0 (
        echo ✓ APK已复制到桌面: ESP32_Debugger.apk
    )
) else (
    echo ✗ 未找到生成的APK文件
)

echo.
echo ========================================
echo 安装说明:
echo ========================================
echo 1. 将ESP32_Debugger.apk传输到手机
echo 2. 在手机上启用"未知来源"安装
echo 3. 点击APK文件安装
echo 4. 授予必要的权限
echo.
echo 或使用ADB安装:
echo adb install ESP32_Debugger.apk
echo ========================================
echo.

pause
