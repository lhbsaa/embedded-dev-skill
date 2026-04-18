# Embedded Development Examples

本文档包含嵌入式开发的实战案例。核心 Skill 见 `SKILL.md`。

---

## Example 1: LCD Driver (ST7789)

**场景:** Configure ST7789 LCD, 240×240, SPI on ESP32-S3

### Steps

```
1. read AGENTS.md → check constraints
2. Load references/chips.md → ESP32-S3 SPI config
3. Generate driver code:
   write src/lcd_st7789.c
   write include/lcd_st7789.h
4. bash: idf.py build
5. bash: idf.py -p COM3 flash monitor
6. Visual feedback:
   bash: python scripts/camera_capture.py --session
   image_read screenshots/capture_xxx.png (Pi)
   # 或直接 read screenshots/capture_xxx.png (OpenCode)
7. Adjust if needed → Re-verify
```

### Key Points

| 步骤 | 关键检查 |
|------|----------|
| 驱动生成 | DMA buffer ≤4092 bytes |
| 编译 | 检查 exit code，无错误 |
| 烧录 | Flash success message |
| 监控 | 无 crash/panic/assertion |
| 视觉验证 | 布局、字体、颜色正确 |

### Common Issues

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 屏幕空白 | Init sequence错误 | 检查 reset 和 MADCTL |
| 部分显示 | MADCTL值不对 | 调整 0x00/0xC0/0x80 |
| 颜色错误 | 颜色格式不匹配 | RGB565/RGB666 |
| 显示偏移 | y_gap/x_gap 错误 | 调整 gap 参数 |
| 镜像/翻转 | MADCTL rotation bits | 检查 bit 5,6,7 |

---

## Example 2: Wi-Fi Setup

**场景:** Connect to Wi-Fi AP on ESP32

### Steps

```
1. Load references/protocols.md → Wi-Fi section
2. Configure STA mode, SSID, password:
   read main/wifi_config.c
   edit main/wifi_config.c
3. Add event handlers for connection
4. bash: idf.py build flash monitor
5. Test connectivity
```

### Wi-Fi Config Template

```c
// wifi_config.c
#define WIFI_SSID "YOUR_SSID"
#define WIFI_PASS "YOUR_PASSWORD"

void wifi_init_sta(void) {
    esp_netif_init();
    esp_event_loop_create_default();
    
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    
    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
        },
    };
    
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
}
```

### Key Points

| 步骤 | 关键检查 |
|------|----------|
| 配置 | SSID/password正确 |
| 编译 | 无错误 |
| 监控 | "Connected to AP" 日志 |

---

## Example 3: Debugging LCD Blank Screen

**场景:** LCD shows nothing after flash

### Steps

```
1. Analyze monitor output from bash command
2. Check SPI initialization logs
3. Verify pin assignments: read src/lcd.c
4. Check backlight control
5. Apply fix: edit src/lcd.c
6. Verify: bash: idf.py build flash monitor
7. If still broken, use Pi's session tree:
   - Press Escape twice → /tree
   - Navigate to earlier working version
   - /fork to create new branch
   - Try different fix approach
```

### Debug Checklist

| 检查项 | 命令/方法 |
|--------|-----------|
| 编译输出 | 检查 errors/warnings |
| SPI初始化 | Monitor 日志 |
| GPIO配置 | read driver.c |
| Backlight | GPIO电平检查 |
| DMA配置 | buffer size ≤4092 |

### Pi Session Tree

Pi Coding Agent 的 Session Tree 是嵌入式调试的重要工具：
- `/tree` - 打开 session navigator
- Navigate - 回到之前的 working state
- `/fork` - 创建新分支尝试不同修复方案

---

## Example 4: Compilation Format String Error

**场景:** 编译提示 uint32_t 格式字符串错误

### Steps

```
1. read references/faq.md → Q1: uint32_t 格式字符串错误
2. 检查类型定义差异
3. 使用 %lu 或 PRIu32 宏
4. bash: idf.py build
5. Verify compilation success
```

### Solution

```c
// 错误
printf("Value: %d\n", (uint32_t)value);

// 正确
printf("Value: %lu\n", (unsigned long)value);

// 或使用 PRIu32
#include <inttypes.h>
printf("Value: %" PRIu32 "\n", value);
```

---

## Example 5: DMA Overflow Fix

**场景:** 大数据传输时 LCD 显示异常

### Steps

```
1. read references/hardware-interfaces.md → DMA section
2. 检查 buffer size 是否超过 4092
3. 实现分块传输
4. bash: idf.py build flash monitor
5. Verify no overflow
```

### DMA Chunked Transfer

```c
#define DMA_MAX_SIZE 4092

esp_err_t lcd_write_chunked(const uint8_t *data, size_t len) {
    size_t remaining = len;
    size_t offset = 0;
    
    while (remaining > 0) {
        size_t chunk = (remaining > DMA_MAX_SIZE) ? DMA_MAX_SIZE : remaining;
        
        esp_err_t ret = spi_device_transmit(spi, &trans_desc);
        if (ret != ESP_OK) return ret;
        
        offset += chunk;
        remaining -= chunk;
    }
    
    return ESP_OK;
}
```

---

## Example 6: Sensor Reading (IMU)

**场景:** Read IMU sensor via I2C

### Steps

```
1. read references/hardware-interfaces.md → I2C section
2. Configure I2C master:
   write src/i2c_driver.c
3. Implement sensor read function
4. bash: idf.py build flash monitor
5. Verify sensor data in log
```

### I2C Read Template

```c
esp_err_t imu_read(uint8_t addr, uint8_t *data, size_t len) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (IMU_ADDR << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, addr, true);
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (IMU_ADDR << 1) | I2C_MASTER_READ, true);
    i2c_master_read(cmd, data, len, I2C_MASTER_LAST_NACK);
    i2c_master_stop(cmd);
    
    esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000 / portTICK_RATE_MS);
    i2c_cmd_link_delete(cmd);
    
    return ret;
}
```

---

## Example 7: MQTT Integration

**场景:** Publish sensor data via MQTT

### Steps

```
1. read references/protocols.md → MQTT section
2. Configure MQTT client
3. Implement publish/subscribe
4. bash: idf.py build flash monitor
5. Verify message delivery
```

### MQTT Publish Template

```c
void mqtt_publish_sensor_data(void) {
    char payload[64];
    snprintf(payload, sizeof(payload), 
             "{\"temp\":%.2f,\"humidity\":%.2f}", 
             temperature, humidity);
    
    esp_mqtt_client_publish(client, 
                            "sensor/data", 
                            payload, 
                            0,  // len (auto-detect)
                            1,  // qos
                            0); // retain
}
```

---

## Quick Reference

更多案例见 `references/cases.md`。