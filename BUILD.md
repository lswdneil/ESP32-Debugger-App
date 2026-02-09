# Android项目构建说明

## 前提条件
1. 安装Android Studio (最新版本)
2. 安装JDK 8或更高版本
3. 配置Android SDK

## 构建步骤

### 方法一：使用Android Studio（推荐）
1. 打开Android Studio
2. 选择 File -> Open
3. 选择 ESP32_Debugger_App 文件夹
4. 等待Gradle同步完成
5. 连接Android设备或启动模拟器
6. 点击 Run 按钮（绿色三角形）
7. APK会自动安装到设备上

### 方法二：使用命令行
1. 打开命令行，进入项目目录
2. 运行: gradlew assembleDebug
3. APK位置: app/build/outputs/apk/debug/app-debug.apk

## 项目结构说明

由于完整的Android项目需要Gradle构建系统和Android SDK，
本项目提供了核心源代码文件。

要完整构建项目，请按以下步骤操作：

1. 使用Android Studio创建新项目
   - 选择 "Empty Activity"
   - 包名: com.weidao.esp32debugger
   - 最低SDK: API 26 (Android 8.0)

2. 替换生成的文件
   - 将提供的Java源文件复制到对应目录
   - 将布局文件复制到res/layout目录
   - 将AndroidManifest.xml替换
   - 将build.gradle替换

3. 同步Gradle并构建

## 注意事项

- 确保手机已开启开发者选项和USB调试
- 首次运行需要授予位置、蓝牙等权限
- 建议使用真实设备测试蓝牙功能
- OnePlus 8T运行Android 11或更高版本

## 生成APK

### Debug版本
gradlew assembleDebug

### Release版本（需要签名）
1. 生成签名密钥
2. 配置build.gradle中的签名信息
3. 运行: gradlew assembleRelease

## 常见问题

Q: Gradle同步失败？
A: 检查网络连接，可能需要配置代理

Q: 编译错误？
A: 确保Android SDK版本正确，检查依赖库版本

Q: 无法安装APK？
A: 检查手机设置中是否允许安装未知来源应用
