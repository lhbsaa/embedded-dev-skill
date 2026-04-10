# Programming Languages & Code Standards

编程语言支持、代码规范和模块化架构设计。

---

## 支持的编程语言

| 语言 | 特点 | 适用场景 |
|------|------|----------|
| **C** | 高效、底层控制 | 驱动开发、RTOS |
| **C++** | OOP、模板、RAII | 复杂应用、框架 |
| **C++17/20** | 现代特性、constexpr | 高效抽象 |
| **Rust** | 内存安全、零成本 | ESP32-C3、STM32 |
| **MicroPython** | Python语法、快速原型 | ESP32、RP2040 |
| **TinyGo** | Go语言嵌入式版 | ESP32、nRF52 |

---

## MISRA C 编程规范

### 核心规则

| 规则类型 | 示例 |
|----------|------|
| **强制** | 禁止`goto`、禁止递归 |
| **必要** | 函数必须有原型声明 |
| **建议** | 避免使用全局变量 |

### 安全编码原则

```c
// 1. 参数检查
esp_err_t function(void *param) {
    if (param == NULL) {
        return ESP_ERR_INVALID_ARG;
    }
    // ...
}

// 2. 边界检查
void array_access(int *arr, int index, int size) {
    if (index >= 0 && index < size) {
        arr[index] = value;
    }
}

// 3. 避免魔法数字
#define MAX_BUFFER_SIZE 256
uint8_t buffer[MAX_BUFFER_SIZE];

// 4. 使用const正确性
void read_only_function(const uint8_t *data);

// 5. 明确的类型
uint32_t counter = 0;  // 而非 int
```

---

## 模块化架构设计

### 三层架构模型

```
┌─────────────────────────────────────┐
│     Application Layer               │  ← 业务逻辑
│   (业务功能、用户交互)                │
├─────────────────────────────────────┤
│     HAL/Driver Layer               │  ← 硬件抽象
│   (硬件接口抽象、驱动封装)             │
├─────────────────────────────────────┤
│     Platform Layer                 │  ← 平台SDK
│   (ESP-IDF、STM32 HAL、Pico SDK)     │
└─────────────────────────────────────┘
```

### 标准模块结构

```c
// driver_xxx.h - 头文件
#ifndef DRIVER_XXX_H
#define DRIVER_XXX_H

#include "esp_err.h"

// 初始化函数
esp_err_t xxx_init(const xxx_config_t *config);

// 操作函数
esp_err_t xxx_write(const uint8_t *data, size_t len);
esp_err_t xxx_read(uint8_t *data, size_t len);

// 状态查询
bool xxx_is_ready(void);

#endif // DRIVER_XXX_H

// driver_xxx.c - 实现文件
#include "driver_xxx.h"
#include "driver/spi_master.h"  // 平台依赖

static xxx_handle_t g_handle;   // 模块内部状态

esp_err_t xxx_init(const xxx_config_t *config) {
    // 参数检查
    if (config == NULL) return ESP_ERR_INVALID_ARG;
    
    // 初始化底层硬件
    spi_master_init(&config->spi);
    
    // 设备特定初始化序列
    xxx_write_cmd(RESET_CMD);
    vTaskDelay(100);
    
    return ESP_OK;
}
```

---

## 文件组织规范

### 目录结构模板

```
project/
├── src/
│   ├── main/
│   │   ├── main.c              # 入口
│   │   ├── app_task.c          # 应用任务
│   │   └── config.h            # 配置定义
│   ├── drivers/
│   │   ├── driver_lcd.c        # LCD驱动
│   │   ├── driver_lcd.h
│   │   ├── driver_imu.c        # IMU驱动
│   │   └── driver_imu.h
│   ├── hal/
│   │   ├── hal_spi.c           # SPI HAL
│   │   ├── hal_i2c.c           # I2C HAL
│   │   └── hal_gpio.c          # GPIO HAL
│   └── services/
│       ├── service_display.c   # 显示服务
│       └── service_sensor.c    # 传感器服务
├── include/
│   ├── app_config.h
│   └── error_codes.h
├── CMakeLists.txt
└── sdkconfig
```

### 文件命名规范

| 类型 | 前缀 | 示例 |
|------|------|------|
| 驱动 | driver_ | driver_lcd.c |
| HAL | hal_ | hal_spi.c |
| 服务 | service_ | service_display.c |
| 应用 | app_ | app_main.c |
| 配置 | config_ | config_board.h |

---

## 代码注释规范

### 文件头注释

```c
/**
 * @file driver_lcd.c
 * @brief ST7789 LCD驱动实现
 * @author [作者]
 * @date 2026-04-09
 * 
 * @details
 * 本文件实现ST7789 LCD驱动，支持SPI接口通信。
 * 主要功能：
 * - LCD初始化和配置
 * - 图形绘制（点、线、矩形）
 * - 文字显示
 * - DMA加速传输
 */
```

### 函数注释

```c
/**
 * @brief 初始化LCD显示
 * @param config LCD配置参数
 * @return ESP_OK成功，其他失败
 * 
 * @note 必须在使用其他LCD函数前调用
 */
esp_err_t lcd_init(const lcd_config_t *config);
```

---

## Rust嵌入式编程

### Embedded Rust优势

| 特性 | 说明 |
|------|------|
| **内存安全** | 无GC，编译期检查 |
| **无畏并发** | 无数据竞争 |
| **零成本抽象** | 高性能 |

### Rust嵌入式架构示例

```rust
// embassy-rs 异步框架
use embassy_executor::Spawner;
use embassy_rp::spi::{Spi, Config};

#[embassy_executor::main]
async fn main(_spawner: Spawner) {
    let p = embassy_rp::init(Default::default());
    
    let spi = Spi::new(p.SPI0, p.PIN_16, p.PIN_17, p.PIN_18, Config::default());
    
    // 驱动LCD
    let mut lcd = LcdDriver::new(spi);
    lcd.init().await;
    lcd.fill_screen(Color::BLACK).await;
}
```

---

## 代码质量检查工具

### 静态分析工具

| 工具 | 功能 |
|------|------|
| **clang-tidy** | C++静态分析 |
| **cppcheck** | C/C++错误检测 |
| **clang-format** | 代码格式化 |

### clang-format配置

```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 120
AllowShortFunctionsOnASingleLine: Empty
BreakBeforeBraces: Attach
```

---
Version: 2.0
Updated: 2026-04-09