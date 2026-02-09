#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目文件检查和总结
"""

import os

PROJECT_ROOT = r"C:\Users\wd_al\Desktop\ESP32_Debugger_App"

print("=" * 60)
print("ESP32 S3 ZERO 调试助手 - 项目文件检查")
print("=" * 60)
print()

# 检查关键文件
files_to_check = {
    "源代码": [
        "app/src/main/java/com/weidao/esp32debugger/MainActivity.java",
        "app/src/main/java/com/weidao/esp32debugger/wifi/WiFiFragment.java",
        "app/src/main/java/com/weidao/esp32debugger/bluetooth/BluetoothFragment.java",
        "app/src/main/java/com/weidao/esp32debugger/SettingsFragment.java",
        "app/src/main/java/com/weidao/esp32debugger/utils/ViewPagerAdapter.java",
    ],
    "布局文件": [
        "app/src/main/res/layout/activity_main.xml",
        "app/src/main/res/layout/fragment_wifi.xml",
        "app/src/main/res/layout/fragment_bluetooth.xml",
        "app/src/main/res/layout/fragment_settings.xml",
    ],
    "资源文件": [
        "app/src/main/res/values/strings.xml",
        "app/src/main/res/values/colors.xml",
        "app/src/main/res/values/themes.xml",
        "app/src/main/AndroidManifest.xml",
    ],
    "构建配置": [
        "build.gradle",
        "settings.gradle",
        "app/build.gradle",
    ],
    "文档": [
        "README.md",
        "BUILD.md",
        "如何构建APK.md",
        "项目完成报告.txt",
    ],
    "脚本": [
        "generate_project.py",
        "build_apk.bat",
    ]
}

total_files = 0
found_files = 0

for category, files in files_to_check.items():
    print(f"【{category}】")
    for file_path in files:
        full_path = os.path.join(PROJECT_ROOT, file_path)
        total_files += 1
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  ✓ {file_path} ({size:,} bytes)")
            found_files += 1
        else:
            print(f"  ✗ {file_path} (未找到)")
    print()

print("=" * 60)
print(f"文件检查完成: {found_files}/{total_files} 个文件")
print("=" * 60)
print()

if found_files == total_files:
    print("✓ 所有文件已生成！")
    print()
    print("下一步:")
    print("1. 使用Android Studio打开项目")
    print("2. 或运行 build_apk.bat 自动构建")
    print("3. 查看'如何构建APK.md'了解详细步骤")
else:
    print(f"⚠ 缺少 {total_files - found_files} 个文件")
    print("请检查项目生成过程")

print()
print("=" * 60)
