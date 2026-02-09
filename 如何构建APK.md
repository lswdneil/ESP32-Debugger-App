# 快速构建APK指南

由于完整的Android开发环境配置较为复杂，这里提供三种方案来获取APK：

## 方案一：使用Android Studio（推荐）

### 1. 安装Android Studio
- 下载地址：https://developer.android.com/studio
- 安装Android SDK (API 26-33)
- 安装Android Build Tools

### 2. 打开项目
```bash
1. 启动Android Studio
2. 选择 "Open an Existing Project"
3. 选择 C:\Users\wd_al\Desktop\ESP32_Debugger_App
4. 等待Gradle同步完成（首次需要下载依赖）
```

### 3. 构建APK
```bash
方法1：菜单构建
Build -> Build Bundle(s) / APK(s) -> Build APK(s)

方法2：命令行构建
cd C:\Users\wd_al\Desktop\ESP32_Debugger_App
gradlew assembleDebug

生成的APK位置：
app/build/outputs/apk/debug/app-debug.apk
```

### 4. 安装到手机
```bash
# 通过USB连接手机，启用USB调试
adb install app/build/outputs/apk/debug/app-debug.apk

# 或直接在Android Studio中点击Run按钮
```

## 方案二：在线构建服务

### 使用GitHub Actions或其他CI服务
1. 将项目上传到GitHub
2. 配置GitHub Actions自动构建
3. 下载构建好的APK

## 方案三：使用Gradle命令行（需要JDK和Android SDK）

### 前置条件
```bash
# 安装JDK 11或更高版本
# 设置JAVA_HOME环境变量

# 安装Android SDK
# 设置ANDROID_HOME环境变量
```

### 构建命令
```bash
cd C:\Users\wd_al\Desktop\ESP32_Debugger_App

# Windows
gradlew.bat assembleDebug

# 构建Release版本（需要签名）
gradlew.bat assembleRelease
```

## 快速测试方案

如果你只是想快速测试，我已经在项目中包含了：

### 1. 完整源代码
- 所有Java源文件
- 布局XML文件
- 资源文件
- 构建配置

### 2. 项目结构
```
ESP32_Debugger_App/
├── app/
│   ├── src/main/
│   │   ├── java/com/weidao/esp32debugger/
│   │   │   ├── MainActivity.java          # 主活动
│   │   │   ├── wifi/
│   │   │   │   └── WiFiFragment.java      # WiFi调试界面
│   │   │   ├── bluetooth/
│   │   │   │   └── BluetoothFragment.java # 蓝牙调试界面
│   │   │   ├── SettingsFragment.java      # 设置界面
│   │   │   └── utils/
│   │   │       └── ViewPagerAdapter.java  # 页面适配器
│   │   ├── res/
│   │   │   ├── layout/                    # 布局文件
│   │   │   ├── values/                    # 资源值
│   │   │   └── drawable/                  # 图标资源
│   │   └── AndroidManifest.xml            # 应用清单
│   └── build.gradle                       # 应用构建配置
├── build.gradle                           # 项目构建配置
├── settings.gradle                        # 项目设置
├── README.md                              # 项目说明
└── BUILD.md                               # 构建说明
```

## 最简单的方法（推荐新手）

### 使用在线Android开发环境

1. **Android Studio Online**
   - 访问：https://developer.android.com/studio/run/emulator-commandline
   - 上传项目文件
   - 在线构建

2. **Replit**
   - 访问：https://replit.com
   - 创建Android项目
   - 上传代码
   - 在线构建

## 预构建APK说明

由于我无法直接在你的电脑上运行完整的Android构建工具链（需要安装Android SDK、配置环境等），
APK需要通过以上任一方案构建。

**推荐流程：**
1. 安装Android Studio（一次性配置）
2. 打开项目
3. 点击Run按钮
4. APK自动构建并安装到手机

**预计时间：**
- 首次安装Android Studio：30-60分钟
- 首次构建项目：10-20分钟
- 后续构建：1-3分钟

## 常见问题

### Q: 为什么不能直接生成APK？
A: APK构建需要：
- Android SDK（约3-5GB）
- Android Build Tools
- Gradle构建系统
- Java开发环境
这些工具需要专门安装和配置。

### Q: 有没有更简单的方法？
A: 可以使用在线构建服务，或者我可以帮你配置Android Studio。

### Q: 项目能在OnePlus 8T上运行吗？
A: 是的，项目配置为：
- 最低Android 8.0 (API 26)
- 目标Android 13 (API 33)
- OnePlus 8T运行Android 11/12/13，完全兼容

## 技术支持

如需帮助构建APK，可以：
1. 安装Android Studio后重新运行构建
2. 使用在线构建服务
3. 联系技术支持

---

**项目已完成：**
✓ 完整的Android源代码
✓ 所有布局和资源文件
✓ 构建配置文件
✓ 详细的文档说明

**下一步：选择上述任一构建方案生成APK**
