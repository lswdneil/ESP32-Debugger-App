# ESP32 S3 ZERO 调试助手

一款用于通过WiFi和蓝牙调试ESP32 S3 ZERO开发板的Android应用

## 功能特性

### WiFi功能
- 扫描ESP32设备
- TCP/UDP通信
- HTTP请求测试
- WebSocket连接
- 实时数据监控

### 蓝牙功能
- 扫描蓝牙设备
- BLE连接
- 经典蓝牙连接
- 数据收发
- 特征值读写

### 调试功能
- 串口监视器
- 命令发送
- 数据日志
- 十六进制/文本切换
- 数据保存

## 系统要求

- Android 8.0 (API 26) 及以上
- 支持WiFi和蓝牙
- 已测试设备：OnePlus 8T

## 安装说明

1. 在手机设置中启用"未知来源"应用安装
2. 将ESP32_Debugger.apk传输到手机
3. 点击APK文件安装
4. 授予必要的权限（位置、蓝牙、WiFi）

## 使用说明

### WiFi调试
1. 确保手机和ESP32连接到同一WiFi网络
2. 点击"WiFi"标签
3. 点击"扫描设备"
4. 选择ESP32设备
5. 输入命令或数据发送

### 蓝牙调试
1. 打开手机蓝牙
2. 点击"蓝牙"标签
3. 点击"扫描设备"
4. 选择ESP32设备
5. 连接并开始通信

## ESP32端配置

### WiFi模式
```cpp
#include <WiFi.h>

const char* ssid = "your_ssid";
const char* password = "your_password";

WiFiServer server(8888);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  server.begin();
  Serial.println("Server started");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        String data = client.readStringUntil('\n');
        Serial.println(data);
        client.println("Received: " + data);
      }
    }
    client.stop();
  }
}
```

### 蓝牙模式
```cpp
#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_S3_ZERO");
  Serial.println("Bluetooth started");
}

void loop() {
  if (SerialBT.available()) {
    String data = SerialBT.readString();
    Serial.println(data);
    SerialBT.println("Received: " + data);
  }
  
  if (Serial.available()) {
    String data = Serial.readString();
    SerialBT.println(data);
  }
}
```

## 开发说明

### 项目结构
```
ESP32_Debugger_App/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/weidao/esp32debugger/
│   │       │   ├── MainActivity.java
│   │       │   ├── WiFiFragment.java
│   │       │   ├── BluetoothFragment.java
│   │       │   └── utils/
│   │       ├── res/
│   │       │   ├── layout/
│   │       │   ├── values/
│   │       │   └── drawable/
│   │       └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
└── settings.gradle
```

### 构建说明
1. 安装Android Studio
2. 打开项目
3. 同步Gradle
4. 连接设备或启动模拟器
5. 点击Run构建APK

### 权限说明
应用需要以下权限：
- ACCESS_FINE_LOCATION：扫描WiFi和蓝牙设备
- BLUETOOTH：蓝牙通信
- BLUETOOTH_ADMIN：蓝牙管理
- BLUETOOTH_CONNECT：蓝牙连接（Android 12+）
- BLUETOOTH_SCAN：蓝牙扫描（Android 12+）
- INTERNET：网络通信
- ACCESS_WIFI_STATE：WiFi状态
- CHANGE_WIFI_STATE：WiFi控制

## 技术栈

- 语言：Java
- 最低SDK：26 (Android 8.0)
- 目标SDK：33 (Android 13)
- UI框架：Material Design
- 网络：OkHttp3
- 蓝牙：Android Bluetooth API

## 更新日志

### v1.0.0 (2026-02-09)
- 初始版本
- WiFi TCP/UDP通信
- 蓝牙BLE/经典蓝牙
- 基础调试功能

## 许可证

MIT License

## 联系方式

开发者：惟道机器人技术（重庆）有限公司
