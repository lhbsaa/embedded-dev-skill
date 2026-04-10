# Debugging Guide

调试策略、日志分析和问题诊断指南。

---

## 调试策略

### 编译错误调试流程

```
编译失败 → 分析错误信息
    ├─ 语法错误 → 检查代码语法
    ├─ 链接错误 → 检查依赖和链接脚本
    ├─ 类型错误 → 检查类型匹配
    └─ 内存不足 → 检查分区配置
```

### 运行错误调试流程

```
运行异常 → 分析日志输出
    ├─ 崩溃 → 检查栈溢出、指针错误
    ├─ 死锁 → 检查资源竞争
    ├─ 内存泄漏 → 检查分配释放配对
    └─ 时序问题 → 检查中断优先级
```

---

## 日志分析

### ESP-IDF日志级别

| 级别 | 宏 | 用途 |
|------|------|------|
| **Error** | ESP_LOGE | 错误信息 |
| **Warning** | ESP_LOGW | 警告信息 |
| **Info** | ESP_LOGI | 重要信息 |
| **Debug** | ESP_LOGD | 调试信息 |
| **Verbose** | ESP_LOGV | 详细信息 |

### 日志配置

```c
// 设置日志级别
esp_log_level_set("LCD", ESP_LOG_DEBUG);
esp_log_level_set("*", ESP_LOG_INFO);  // 全局

// 添加日志
ESP_LOGI(TAG, "LCD initialized: width=%d, height=%d", width, height);
ESP_LOGE(TAG, "SPI transmit failed: %s", esp_err_to_name(ret));
```

---

## 常见问题诊断

### 1. LCD不显示

```yaml
检查清单:
  - SPI初始化是否成功
  - 引脚配置是否正确
  - LCD背光是否开启
  - 初始化序列是否完整
  - DMA缓冲区是否正确对齐
  
常见原因:
  - CS引脚未正确控制
  - 时钟频率过高
  - DMA缓冲超过4092字节
  - madctl配置方向错误
```

### 2. IMU数据异常

```yaml
检查清单:
  - I2C地址是否正确
  - 传感器是否正常供电
  - 数据解析是否正确
  - 采样率是否合适
  
常见原因:
  - I2C地址错误（不同型号地址不同）
  - 传感器未校准
  - 数据格式解析错误
```

### 3. Wi-Fi连接失败

```yaml
检查清单:
  - SSID和密码是否正确
  - AP是否存在
  - 信号强度是否足够
  - 认证模式是否匹配
  
常见原因:
  - 密码错误
  - 路由器MAC过滤
  - DHCP问题
  - 超时设置过短
```

### 4. 内存不足

```yaml
检查清单:
  - 静态内存使用情况
  - 动态内存分配
  - DMA缓冲区大小
  - 任务栈大小
  
解决方案:
  - 启用PSRAM（ESP32-S3）
  - 优化缓冲区大小
  - 减少任务栈深度
  - 使用内存池管理
```

---

## 硬件调试技巧

### GPIO测试

```c
// 简单GPIO测试
gpio_set_direction(TEST_PIN, GPIO_MODE_OUTPUT);
gpio_set_level(TEST_PIN, 1);  // 高电平
gpio_set_level(TEST_PIN, 0);  // 低电平
// 用示波器或万用表验证
```

### SPI时序验证

```c
// 发送测试数据
uint8_t test_data[] = {0xAA, 0x55, 0xF0, 0x0F};
spi_transmit(handle, test_data, 4);
// 用逻辑分析仪验证时序
```

---

## 断点调试

### GDB常用命令

```
break main          # 在main函数设置断点
break file.c:50     # 在file.c第50行设置断点
continue            # 继续执行
step                # 单步执行（进入函数）
next                # 单步执行（不进入函数）
print variable      # 打印变量值
backtrace           # 显示调用栈
info registers      # 显示寄存器
```

---

## 性能分析

### CPU使用率分析

```c
#include "esp_freertos_hooks.h"

void cpu_usage_task(void *arg) {
    while (1) {
        printf("CPU usage: %d%%\n", get_cpu_usage());
        vTaskDelay(1000);
    }
}
```

### 内存使用分析

```c
#include "esp_system.h"

void print_memory_info(void) {
    printf("Free heap: %d bytes\n", esp_get_free_heap_size());
    printf("Min free heap: %d bytes\n", esp_get_minimum_free_heap_size());
    printf Largest free block: %d bytes\n", heap_caps_get_largest_free_block(MALLOC_CAP_8BIT));
}
```

---
Version: 2.0
Updated: 2026-04-09