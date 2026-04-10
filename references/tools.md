# Development Tools & Environment Standards

编译工具链、构建系统、调试工具配置规范。

---

## 编译工具链

### GCC ARM选项

```makefile
# 目标架构
ARCH = -mcpu=cortex-m4 -mthumb -mfloat-abi=hard

# 优化选项
OPT = -Og          # 调试版本（推荐）
# OPT = -O2        # 发布版本

# 警告选项
WARNINGS = -Wall -Wextra -Werror -Wshadow

# C标准
C_STD = -std=c11

# 完整标志
CFLAGS = $(ARCH) $(OPT) $(WARNINGS) $(C_STD) \
         -ffunction-sections -fdata-sections
```

---

## 构建系统

### CMake配置

```cmake
cmake_minimum_required(VERSION 3.16)
project(embedded_project C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "-Wall -Wextra -Og")

# 添加源文件
add_executable(firmware
    src/main.c
    src/driver_lcd.c
    src/hal_spi.c
)

# 链接脚本
set_target_properties(firmware PROPERTIES
    LINK_FLAGS "-T${CMAKE_SOURCE_DIR}/linker.ld"
)
```

### ESP-IDF构建

```bash
# 编译
idf.py build

# 烧录
idf.py flash

# 监控
idf.py monitor

# 全流程
idf.py build flash monitor
```

---

## 调试工具

### OpenOCD配置

```bash
# ESP32-S3 JTAG调试
openocd -f board/esp32s3-builtin.cfg

# STM32调试
openocd -f board/st_nucleo_f4.cfg
```

### GDB调试脚本

```gdb
# .gdbinit
target remote localhost:3333
monitor reset halt
load
break main
continue
```

---

## IDE配置

### VSCode配置

```json
// .vscode/tasks.json
{
    "tasks": [
        {
            "label": "Build",
            "type": "shell",
            "command": "idf.py build"
        },
        {
            "label": "Flash",
            "type": "shell",
            "command": "idf.py flash"
        }
    ]
}
```

### PlatformIO配置

```yaml
# platformio.ini
[env:esp32-s3]
platform = espressif32
board = esp32-s3-devkitc-1
framework = espidf
monitor_speed = 115200
```

---

## 版本控制

### Git工作流

```
main (稳定发布)
  │
  └─ develop (开发主分支)
       │
       ├─ feature/* (新功能)
       ├─ hotfix/* (紧急修复)
       └─ release/* (发布准备)
```

### 提交规范

```
格式: <type>(<scope>): <subject>

类型:
  feat:     新功能
  fix:      Bug修复
  docs:     文档更新
  refactor: 重构
  test:     测试相关

示例:
  feat(driver): add ST7789 LCD driver
  fix(spi): resolve DMA buffer overflow
```

---

## OTA固件升级

### ESP32 OTA流程

```c
#include "esp_ota_ops.h"

esp_err_t ota_update(const char *url) {
    esp_http_client_config_t config = { .url = url };
    esp_https_ota(&config);
    
    esp_ota_mark_app_valid_cancel_rollback();
    esp_restart();
    return ESP_OK;
}
```

---
Version: 2.0
Updated: 2026-04-09