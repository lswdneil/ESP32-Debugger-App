#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ESP32 S3 ZERO 调试助手 - Android项目生成器
自动生成完整的Android Studio项目结构和源代码
"""

import os
import shutil

# 项目根目录
PROJECT_ROOT = r"C:\Users\wd_al\Desktop\ESP32_Debugger_App"
APP_DIR = os.path.join(PROJECT_ROOT, "app")
SRC_DIR = os.path.join(APP_DIR, "src", "main")
JAVA_DIR = os.path.join(SRC_DIR, "java", "com", "weidao", "esp32debugger")
RES_DIR = os.path.join(SRC_DIR, "res")

def create_directories():
    """创建项目目录结构"""
    dirs = [
        JAVA_DIR,
        os.path.join(JAVA_DIR, "utils"),
        os.path.join(JAVA_DIR, "wifi"),
        os.path.join(JAVA_DIR, "bluetooth"),
        os.path.join(RES_DIR, "layout"),
        os.path.join(RES_DIR, "values"),
        os.path.join(RES_DIR, "drawable"),
        os.path.join(RES_DIR, "mipmap-hdpi"),
        os.path.join(RES_DIR, "mipmap-mdpi"),
        os.path.join(RES_DIR, "mipmap-xhdpi"),
        os.path.join(RES_DIR, "mipmap-xxhdpi"),
        os.path.join(RES_DIR, "mipmap-xxxhdpi"),
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("✓ 目录结构创建完成")

def create_main_activity():
    """创建MainActivity.java"""
    code = '''package com.weidao.esp32debugger;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.viewpager2.widget.ViewPager2;

import com.google.android.material.tabs.TabLayout;
import com.google.android.material.tabs.TabLayoutMediator;
import com.weidao.esp32debugger.utils.ViewPagerAdapter;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    
    private static final int PERMISSION_REQUEST_CODE = 1001;
    private TabLayout tabLayout;
    private ViewPager2 viewPager;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initViews();
        checkPermissions();
    }
    
    private void initViews() {
        tabLayout = findViewById(R.id.tabLayout);
        viewPager = findViewById(R.id.viewPager);
        
        ViewPagerAdapter adapter = new ViewPagerAdapter(this);
        viewPager.setAdapter(adapter);
        
        new TabLayoutMediator(tabLayout, viewPager,
                (tab, position) -> {
                    switch (position) {
                        case 0:
                            tab.setText("WiFi调试");
                            break;
                        case 1:
                            tab.setText("蓝牙调试");
                            break;
                        case 2:
                            tab.setText("设置");
                            break;
                    }
                }).attach();
    }
    
    private void checkPermissions() {
        List<String> permissions = new ArrayList<>();
        
        // 位置权限
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Manifest.permission.ACCESS_FINE_LOCATION);
        }
        
        // Android 12+ 蓝牙权限
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_SCAN)
                    != PackageManager.PERMISSION_GRANTED) {
                permissions.add(Manifest.permission.BLUETOOTH_SCAN);
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT)
                    != PackageManager.PERMISSION_GRANTED) {
                permissions.add(Manifest.permission.BLUETOOTH_CONNECT);
            }
        }
        
        if (!permissions.isEmpty()) {
            ActivityCompat.requestPermissions(this,
                    permissions.toArray(new String[0]),
                    PERMISSION_REQUEST_CODE);
        }
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                          @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            boolean allGranted = true;
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false;
                    break;
                }
            }
            
            if (!allGranted) {
                Toast.makeText(this, "需要授予所有权限才能正常使用", Toast.LENGTH_LONG).show();
            }
        }
    }
}
'''
    
    with open(os.path.join(JAVA_DIR, "MainActivity.java"), 'w', encoding='utf-8') as f:
        f.write(code)
    
    print("✓ MainActivity.java 创建完成")

def create_wifi_fragment():
    """创建WiFi调试Fragment"""
    code = '''package com.weidao.esp32debugger.wifi;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.weidao.esp32debugger.R;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class WiFiFragment extends Fragment {
    
    private EditText etIpAddress, etPort, etCommand;
    private Button btnConnect, btnDisconnect, btnSend, btnClear;
    private TextView tvLog;
    private ScrollView scrollView;
    
    private Socket socket;
    private PrintWriter writer;
    private BufferedReader reader;
    private boolean isConnected = false;
    private Handler mainHandler;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                           @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_wifi, container, false);
        
        initViews(view);
        mainHandler = new Handler(Looper.getMainLooper());
        
        return view;
    }
    
    private void initViews(View view) {
        etIpAddress = view.findViewById(R.id.etIpAddress);
        etPort = view.findViewById(R.id.etPort);
        etCommand = view.findViewById(R.id.etCommand);
        btnConnect = view.findViewById(R.id.btnConnect);
        btnDisconnect = view.findViewById(R.id.btnDisconnect);
        btnSend = view.findViewById(R.id.btnSend);
        btnClear = view.findViewById(R.id.btnClear);
        tvLog = view.findViewById(R.id.tvLog);
        scrollView = view.findViewById(R.id.scrollView);
        
        // 设置默认值
        etIpAddress.setText("192.168.1.100");
        etPort.setText("8888");
        
        btnConnect.setOnClickListener(v -> connectToESP32());
        btnDisconnect.setOnClickListener(v -> disconnect());
        btnSend.setOnClickListener(v -> sendCommand());
        btnClear.setOnClickListener(v -> tvLog.setText(""));
        
        updateButtonStates();
    }
    
    private void connectToESP32() {
        String ip = etIpAddress.getText().toString().trim();
        String portStr = etPort.getText().toString().trim();
        
        if (ip.isEmpty() || portStr.isEmpty()) {
            Toast.makeText(getContext(), "请输入IP地址和端口", Toast.LENGTH_SHORT).show();
            return;
        }
        
        int port = Integer.parseInt(portStr);
        
        new Thread(() -> {
            try {
                socket = new Socket(ip, port);
                writer = new PrintWriter(socket.getOutputStream(), true);
                reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                isConnected = true;
                
                mainHandler.post(() -> {
                    addLog("已连接到 " + ip + ":" + port);
                    updateButtonStates();
                    Toast.makeText(getContext(), "连接成功", Toast.LENGTH_SHORT).show();
                });
                
                // 启动接收线程
                startReceiving();
                
            } catch (IOException e) {
                mainHandler.post(() -> {
                    addLog("连接失败: " + e.getMessage());
                    Toast.makeText(getContext(), "连接失败", Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }
    
    private void disconnect() {
        new Thread(() -> {
            try {
                isConnected = false;
                if (writer != null) writer.close();
                if (reader != null) reader.close();
                if (socket != null) socket.close();
                
                mainHandler.post(() -> {
                    addLog("已断开连接");
                    updateButtonStates();
                    Toast.makeText(getContext(), "已断开连接", Toast.LENGTH_SHORT).show();
                });
                
            } catch (IOException e) {
                mainHandler.post(() -> addLog("断开连接出错: " + e.getMessage()));
            }
        }).start();
    }
    
    private void sendCommand() {
        String command = etCommand.getText().toString();
        
        if (command.isEmpty()) {
            Toast.makeText(getContext(), "请输入命令", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (!isConnected) {
            Toast.makeText(getContext(), "请先连接设备", Toast.LENGTH_SHORT).show();
            return;
        }
        
        new Thread(() -> {
            try {
                writer.println(command);
                mainHandler.post(() -> {
                    addLog("发送: " + command);
                    etCommand.setText("");
                });
            } catch (Exception e) {
                mainHandler.post(() -> addLog("发送失败: " + e.getMessage()));
            }
        }).start();
    }
    
    private void startReceiving() {
        new Thread(() -> {
            try {
                String line;
                while (isConnected && (line = reader.readLine()) != null) {
                    String finalLine = line;
                    mainHandler.post(() -> addLog("接收: " + finalLine));
                }
            } catch (IOException e) {
                if (isConnected) {
                    mainHandler.post(() -> addLog("接收数据出错: " + e.getMessage()));
                }
            }
        }).start();
    }
    
    private void addLog(String message) {
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss", Locale.getDefault());
        String timestamp = sdf.format(new Date());
        String log = "[" + timestamp + "] " + message + "\\n";
        tvLog.append(log);
        
        // 自动滚动到底部
        scrollView.post(() -> scrollView.fullScroll(View.FOCUS_DOWN));
    }
    
    private void updateButtonStates() {
        btnConnect.setEnabled(!isConnected);
        btnDisconnect.setEnabled(isConnected);
        btnSend.setEnabled(isConnected);
    }
    
    @Override
    public void onDestroyView() {
        super.onDestroyView();
        disconnect();
    }
}
'''
    
    wifi_dir = os.path.join(JAVA_DIR, "wifi")
    with open(os.path.join(wifi_dir, "WiFiFragment.java"), 'w', encoding='utf-8') as f:
        f.write(code)
    
    print("✓ WiFiFragment.java 创建完成")

def create_bluetooth_fragment():
    """创建蓝牙调试Fragment"""
    code = '''package com.weidao.esp32debugger.bluetooth;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;

import com.weidao.esp32debugger.R;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.UUID;

public class BluetoothFragment extends Fragment {
    
    private static final UUID SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    
    private ListView lvDevices;
    private EditText etCommand;
    private Button btnScan, btnSend, btnClear;
    private TextView tvLog;
    private ScrollView scrollView;
    
    private BluetoothAdapter bluetoothAdapter;
    private ArrayAdapter<String> deviceAdapter;
    private List<BluetoothDevice> deviceList;
    private BluetoothSocket socket;
    private OutputStream outputStream;
    private InputStream inputStream;
    private boolean isConnected = false;
    private Handler mainHandler;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                           @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_bluetooth, container, false);
        
        initViews(view);
        initBluetooth();
        mainHandler = new Handler(Looper.getMainLooper());
        
        return view;
    }
    
    private void initViews(View view) {
        lvDevices = view.findViewById(R.id.lvDevices);
        etCommand = view.findViewById(R.id.etCommand);
        btnScan = view.findViewById(R.id.btnScan);
        btnSend = view.findViewById(R.id.btnSend);
        btnClear = view.findViewById(R.id.btnClear);
        tvLog = view.findViewById(R.id.tvLog);
        scrollView = view.findViewById(R.id.scrollView);
        
        deviceList = new ArrayList<>();
        deviceAdapter = new ArrayAdapter<>(requireContext(),
                android.R.layout.simple_list_item_1, new ArrayList<>());
        lvDevices.setAdapter(deviceAdapter);
        
        btnScan.setOnClickListener(v -> scanDevices());
        btnSend.setOnClickListener(v -> sendCommand());
        btnClear.setOnClickListener(v -> tvLog.setText(""));
        
        lvDevices.setOnItemClickListener((parent, view1, position, id) -> {
            BluetoothDevice device = deviceList.get(position);
            connectToDevice(device);
        });
    }
    
    private void initBluetooth() {
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        
        if (bluetoothAdapter == null) {
            Toast.makeText(getContext(), "设备不支持蓝牙", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (!bluetoothAdapter.isEnabled()) {
            Toast.makeText(getContext(), "请先打开蓝牙", Toast.LENGTH_SHORT).show();
        }
    }
    
    private void scanDevices() {
        if (ActivityCompat.checkSelfPermission(requireContext(),
                Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(getContext(), "需要蓝牙权限", Toast.LENGTH_SHORT).show();
            return;
        }
        
        deviceList.clear();
        deviceAdapter.clear();
        
        // 获取已配对设备
        Set<BluetoothDevice> pairedDevices = bluetoothAdapter.getBondedDevices();
        
        if (pairedDevices.size() > 0) {
            for (BluetoothDevice device : pairedDevices) {
                deviceList.add(device);
                deviceAdapter.add(device.getName() + "\\n" + device.getAddress());
            }
            addLog("找到 " + pairedDevices.size() + " 个已配对设备");
        } else {
            addLog("未找到已配对设备");
        }
    }
    
    private void connectToDevice(BluetoothDevice device) {
        if (ActivityCompat.checkSelfPermission(requireContext(),
                Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        
        addLog("正在连接到 " + device.getName() + "...");
        
        new Thread(() -> {
            try {
                socket = device.createRfcommSocketToServiceRecord(SPP_UUID);
                socket.connect();
                outputStream = socket.getOutputStream();
                inputStream = socket.getInputStream();
                isConnected = true;
                
                mainHandler.post(() -> {
                    addLog("已连接到 " + device.getName());
                    Toast.makeText(getContext(), "连接成功", Toast.LENGTH_SHORT).show();
                });
                
                // 启动接收线程
                startReceiving();
                
            } catch (IOException e) {
                mainHandler.post(() -> {
                    addLog("连接失败: " + e.getMessage());
                    Toast.makeText(getContext(), "连接失败", Toast.LENGTH_SHORT).show();
                });
            }
        }).start();
    }
    
    private void sendCommand() {
        String command = etCommand.getText().toString();
        
        if (command.isEmpty()) {
            Toast.makeText(getContext(), "请输入命令", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (!isConnected) {
            Toast.makeText(getContext(), "请先连接设备", Toast.LENGTH_SHORT).show();
            return;
        }
        
        new Thread(() -> {
            try {
                outputStream.write((command + "\\n").getBytes());
                outputStream.flush();
                mainHandler.post(() -> {
                    addLog("发送: " + command);
                    etCommand.setText("");
                });
            } catch (IOException e) {
                mainHandler.post(() -> addLog("发送失败: " + e.getMessage()));
            }
        }).start();
    }
    
    private void startReceiving() {
        new Thread(() -> {
            byte[] buffer = new byte[1024];
            int bytes;
            
            try {
                while (isConnected) {
                    bytes = inputStream.read(buffer);
                    if (bytes > 0) {
                        String data = new String(buffer, 0, bytes);
                        mainHandler.post(() -> addLog("接收: " + data.trim()));
                    }
                }
            } catch (IOException e) {
                if (isConnected) {
                    mainHandler.post(() -> addLog("接收数据出错: " + e.getMessage()));
                }
            }
        }).start();
    }
    
    private void addLog(String message) {
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss", Locale.getDefault());
        String timestamp = sdf.format(new Date());
        String log = "[" + timestamp + "] " + message + "\\n";
        tvLog.append(log);
        
        scrollView.post(() -> scrollView.fullScroll(View.FOCUS_DOWN));
    }
    
    @Override
    public void onDestroyView() {
        super.onDestroyView();
        disconnect();
    }
    
    private void disconnect() {
        isConnected = false;
        try {
            if (outputStream != null) outputStream.close();
            if (inputStream != null) inputStream.close();
            if (socket != null) socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
'''
    
    bt_dir = os.path.join(JAVA_DIR, "bluetooth")
    with open(os.path.join(bt_dir, "BluetoothFragment.java"), 'w', encoding='utf-8') as f:
        f.write(code)
    
    print("✓ BluetoothFragment.java 创建完成")

def create_settings_fragment():
    """创建设置Fragment"""
    code = '''package com.weidao.esp32debugger;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class SettingsFragment extends Fragment {
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                           @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_settings, container, false);
        
        TextView tvVersion = view.findViewById(R.id.tvVersion);
        tvVersion.setText("版本: 1.0.0\\n\\n开发者: 惟道机器人技术（重庆）有限公司\\n\\n" +
                "本应用用于调试ESP32 S3 ZERO开发板\\n支持WiFi和蓝牙通信");
        
        return view;
    }
}
'''
    
    with open(os.path.join(JAVA_DIR, "SettingsFragment.java"), 'w', encoding='utf-8') as f:
        f.write(code)
    
    print("✓ SettingsFragment.java 创建完成")

def create_viewpager_adapter():
    """创建ViewPager适配器"""
    code = '''package com.weidao.esp32debugger.utils;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.viewpager2.adapter.FragmentStateAdapter;

import com.weidao.esp32debugger.SettingsFragment;
import com.weidao.esp32debugger.bluetooth.BluetoothFragment;
import com.weidao.esp32debugger.wifi.WiFiFragment;

public class ViewPagerAdapter extends FragmentStateAdapter {
    
    public ViewPagerAdapter(@NonNull FragmentActivity fragmentActivity) {
        super(fragmentActivity);
    }
    
    @NonNull
    @Override
    public Fragment createFragment(int position) {
        switch (position) {
            case 0:
                return new WiFiFragment();
            case 1:
                return new BluetoothFragment();
            case 2:
                return new SettingsFragment();
            default:
                return new WiFiFragment();
        }
    }
    
    @Override
    public int getItemCount() {
        return 3;
    }
}
'''
    
    utils_dir = os.path.join(JAVA_DIR, "utils")
    with open(os.path.join(utils_dir, "ViewPagerAdapter.java"), 'w', encoding='utf-8') as f:
        f.write(code)
    
    print("✓ ViewPagerAdapter.java 创建完成")

def create_layouts():
    """创建布局文件"""
    
    # activity_main.xml
    main_layout = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:theme="@style/ThemeOverlay.AppCompat.Dark.ActionBar">

        <androidx.appcompat.widget.Toolbar
            android:id="@+id/toolbar"
            android:layout_width="match_parent"
            android:layout_height="?attr/actionBarSize"
            android:background="?attr/colorPrimary"
            app:title="ESP32 S3 调试助手"
            app:titleTextColor="@android:color/white" />

        <com.google.android.material.tabs.TabLayout
            android:id="@+id/tabLayout"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            app:tabMode="fixed"
            app:tabGravity="fill" />

    </com.google.android.material.appbar.AppBarLayout>

    <androidx.viewpager2.widget.ViewPager2
        android:id="@+id/viewPager"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />

</LinearLayout>
'''
    
    with open(os.path.join(RES_DIR, "layout", "activity_main.xml"), 'w', encoding='utf-8') as f:
        f.write(main_layout)
    
    # fragment_wifi.xml
    wifi_layout = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="IP地址">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/etIpAddress"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="text" />
    </com.google.android.material.textfield.TextInputLayout>

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="端口"
        android:layout_marginTop="8dp">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/etPort"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="number" />
    </com.google.android.material.textfield.TextInputLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:layout_marginTop="8dp">

        <Button
            android:id="@+id/btnConnect"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="连接"
            android:layout_marginEnd="4dp" />

        <Button
            android:id="@+id/btnDisconnect"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="断开"
            android:layout_marginStart="4dp" />
    </LinearLayout>

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="命令"
        android:layout_marginTop="16dp">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/etCommand"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="text" />
    </com.google.android.material.textfield.TextInputLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:layout_marginTop="8dp">

        <Button
            android:id="@+id/btnSend"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="发送"
            android:layout_marginEnd="4dp" />

        <Button
            android:id="@+id/btnClear"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="清空日志"
            android:layout_marginStart="4dp" />
    </LinearLayout>

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="通信日志:"
        android:textStyle="bold"
        android:layout_marginTop="16dp"
        android:layout_marginBottom="8dp" />

    <ScrollView
        android:id="@+id/scrollView"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:background="#F5F5F5"
        android:padding="8dp">

        <TextView
            android:id="@+id/tvLog"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:textSize="12sp"
            android:fontFamily="monospace" />
    </ScrollView>

</LinearLayout>
'''
    
    with open(os.path.join(RES_DIR, "layout", "fragment_wifi.xml"), 'w', encoding='utf-8') as f:
        f.write(wifi_layout)
    
    # fragment_bluetooth.xml
    bt_layout = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <Button
        android:id="@+id/btnScan"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="扫描蓝牙设备" />

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="可用设备:"
        android:textStyle="bold"
        android:layout_marginTop="16dp"
        android:layout_marginBottom="8dp" />

    <ListView
        android:id="@+id/lvDevices"
        android:layout_width="match_parent"
        android:layout_height="150dp"
        android:background="#F5F5F5" />

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="命令"
        android:layout_marginTop="16dp">

        <com.google.android.material.textfield.TextInputEditText
            android:id="@+id/etCommand"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:inputType="text" />
    </com.google.android.material.textfield.TextInputLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:layout_marginTop="8dp">

        <Button
            android:id="@+id/btnSend"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="发送"
            android:layout_marginEnd="4dp" />

        <Button
            android:id="@+id/btnClear"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="清空日志"
            android:layout_marginStart="4dp" />
    </LinearLayout>

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="通信日志:"
        android:textStyle="bold"
        android:layout_marginTop="16dp"
        android:layout_marginBottom="8dp" />

    <ScrollView
        android:id="@+id/scrollView"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:background="#F5F5F5"
        android:padding="8dp">

        <TextView
            android:id="@+id/tvLog"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:textSize="12sp"
            android:fontFamily="monospace" />
    </ScrollView>

</LinearLayout>
'''
    
    with open(os.path.join(RES_DIR, "layout", "fragment_bluetooth.xml"), 'w', encoding='utf-8') as f:
        f.write(bt_layout)
    
    # fragment_settings.xml
    settings_layout = '''<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:gravity="center_horizontal">

        <ImageView
            android:layout_width="120dp"
            android:layout_height="120dp"
            android:src="@mipmap/ic_launcher"
            android:layout_marginTop="32dp" />

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="ESP32 S3 调试助手"
            android:textSize="20sp"
            android:textStyle="bold"
            android:layout_marginTop="16dp" />

        <TextView
            android:id="@+id/tvVersion"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="版本: 1.0.0"
            android:textSize="14sp"
            android:layout_marginTop="32dp"
            android:gravity="center"
            android:lineSpacingExtra="4dp" />

    </LinearLayout>

</ScrollView>
'''
    
    with open(os.path.join(RES_DIR, "layout", "fragment_settings.xml"), 'w', encoding='utf-8') as f:
        f.write(settings_layout)
    
    print("✓ 布局文件创建完成")

def create_values():
    """创建values资源文件"""
    
    # strings.xml
    strings = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">ESP32 S3 调试助手</string>
</resources>
'''
    
    with open(os.path.join(RES_DIR, "values", "strings.xml"), 'w', encoding='utf-8') as f:
        f.write(strings)
    
    # colors.xml
    colors = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
'''
    
    with open(os.path.join(RES_DIR, "values", "colors.xml"), 'w', encoding='utf-8') as f:
        f.write(colors)
    
    # themes.xml
    themes = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.ESP32Debugger" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
        <item name="colorSecondary">@color/teal_200</item>
        <item name="colorSecondaryVariant">@color/teal_700</item>
        <item name="colorOnSecondary">@color/black</item>
        <item name="android:statusBarColor">?attr/colorPrimaryVariant</item>
    </style>
</resources>
'''
    
    with open(os.path.join(RES_DIR, "values", "themes.xml"), 'w', encoding='utf-8') as f:
        f.write(themes)
    
    print("✓ Values资源文件创建完成")

def create_build_script():
    """创建构建说明"""
    content = '''# Android项目构建说明

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
'''
    
    with open(os.path.join(PROJECT_ROOT, "BUILD.md"), 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ 构建说明创建完成")

def main():
    """主函数"""
    print("=" * 50)
    print("ESP32 S3 ZERO 调试助手 - Android项目生成器")
    print("=" * 50)
    print()
    
    try:
        create_directories()
        create_main_activity()
        create_wifi_fragment()
        create_bluetooth_fragment()
        create_settings_fragment()
        create_viewpager_adapter()
        create_layouts()
        create_values()
        create_build_script()
        
        print()
        print("=" * 50)
        print("✓ 项目生成完成！")
        print("=" * 50)
        print()
        print("项目位置:", PROJECT_ROOT)
        print()
        print("下一步:")
        print("1. 使用Android Studio打开项目文件夹")
        print("2. 等待Gradle同步完成")
        print("3. 连接Android设备")
        print("4. 点击Run按钮构建并安装APK")
        print()
        print("详细说明请查看 BUILD.md 文件")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
