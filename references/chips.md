# Supported Chip Families

详细的芯片系列规格、开发框架和配置参数。

---

## 1. ESP32 系列 (Espressif)

### 芯片规格对比

| 芯片 | CPU | 主频 | RAM | Wi-Fi | 蓝牙 | USB | 典型应用 |
|------|-----|------|-----|-------|------|-----|----------|
| **ESP32** | Xtensa LX6 双核 | 240MHz | 520KB | 802.11 b/g/n | BT 4.2+BLE | 无 | 智能家居 |
| **ESP32-S2** | Xtensa LX7 单核 | 240MHz | 320KB | 802.11 b/g/n | 无 | USB OTG | 安全IoT |
| **ESP32-S3** | Xtensa LX7 双核 | 240MHz | 512KB+8MB PSRAM | 802.11 b/g/n | BT 5.0+BLE | USB OTG | AI IoT、LCD |
| **ESP32-C3** | RISC-V 单核 | 160MHz | 400KB | 802.11 b/g/n | BT 5.0+BLE | USB Serial | 低成本IoT |
| **ESP32-C6** | RISC-V 单核 | 160MHz | 320KB | 802.11 ax | BT 5.0+BLE | USB Serial | Wi-Fi 6 |
| **ESP32-H2** | RISC-V 单核 | 96MHz | 256KB | 无 | BLE+Zigbee | USB Serial | 多协议 |

### ESP32-S3 特色功能（重点支持）
- **AI加速**: 8MB PSRAM支持大内存
- **LCD接口**: SPI/QSPI/RGB接口
- **USB OTG**: 主机和设备模式
- **摄像头**: DVP接口支持

### ESP32 开发框架

| 框架 | 语言 | 特点 |
|------|------|------|
| **ESP-IDF** | C/C++ | 官方SDK，功能完整 |
| **Arduino-ESP32** | C/C++ | 简单易用 |
| **MicroPython** | Python | 快速原型 |
| **PlatformIO** | C/C++ | 集成开发环境 |

### ESP32-S3 LCD配置示例

```yaml
lcd:
  controller: ST7789/SH8601
  interface: SPI/QSPI
  resolution: 240x240
  dma_buffer: 4092 bytes  # 单次传输限制
  psram_framebuffer: true
  
# MimiClaw-1.3-LCD正确配置
display:
  driver: SH8601
  y_gap: 0
  x_gap: 0
  madctl_val: 0x00
  gui_flush: Y轴翻转 + 行顺序翻转
  
# 全屏显示方案
fullscreen:
  y_gap: 80
  madctl_val: 0xC0 或 0x80
  flush: 仅保留行顺序翻转
```

---

## 2. STM32 系列 (STMicroelectronics)

### 芯片分类

| 系列 | 内核 | 主频 | 定位 |
|------|------|------|------|
| **STM32F0** | Cortex-M0 | 48MHz | 入门级 |
| **STM32F1** | Cortex-M3 | 72MHz | 主流型 |
| **STM32F4** | Cortex-M4F | 168MHz | 高性能DSP |
| **STM32F7** | Cortex-M7 | 216MHz | LCD显示 |
| **STM32H7** | Cortex-M7/M4 | 480MHz | 边缘AI |
| **STM32L4** | Cortex-M4F | 80MHz | 低功耗 |
| **STM32U5** | Cortex-M33 | 160MHz | IoT安全 |

### 开发框架

| 框架 | 特点 |
|------|------|
| **STM32CubeIDE** | 官方IDE |
| **HAL库** | 高级抽象，易移植 |
| **LL库** | 底层轻量，高效 |
| **Arduino STM32** | 快速原型 |

### STM32 LCD接口

```yaml
# STM32F7/H7 LTDC配置
lcd:
  interface: LTDC (RGB)
  framebuffer: SDRAM
  resolution: 800x480
  graphics_accel: Chrom-ART
```

---

## 3. RP2040 (Raspberry Pi Pico)

### 芯片规格

| 特性 | 规格 |
|------|------|
| **处理器** | 双核 Cortex-M0+ @ 133MHz |
| **SRAM** | 264KB (6个独立银行) |
| **PIO** | 8个状态机，可编程I/O |

### 独特功能
- **PIO**: 自定义通信协议，无需硬件外设
- **UF2启动**: USB大容量存储启动
- **低成本**: 芯片价格极低

### 开发框架

| 框架 | 语言 |
|------|------|
| **Pico SDK** | C/C++ |
| **MicroPython** | Python |
| **Arduino-Pico** | C/C++ |
| **Rust (rp-rs)** | Rust |

---

## 4. nRF52 系列 (Nordic)

### 芯片对比

| 特性 | nRF52832 | nRF52840 |
|------|----------|----------|
| **处理器** | Cortex-M4F @ 64MHz | Cortex-M4F @ 64MHz |
| **Flash** | 512KB | 1MB |
| **RAM** | 64KB | 256KB |
| **蓝牙** | BLE 5.4 | BLE+Thread+Zigbee |
| **USB** | 无 | USB 2.0 |

### 低功耗配置

```yaml
power:
  sleep_mode: system_off
  wakeup: GPIO/timer
  deep_sleep: ~2μA
```

---

## 芯片选择矩阵

| 需求 | ESP32-S3 | STM32H7 | RP2040 | nRF52840 |
|------|----------|---------|--------|----------|
| **Wi-Fi** | ✓优秀 | 外扩 | 外扩 | 外扩 |
| **蓝牙** | ✓BLE5.0 | 外扩 | 外扩 | ✓内置 |
| **LCD** | ✓SPI/RGB | ✓LTDC | SPI | SPI |
| **AI** | ✓向量扩展 | ✓高算力 | 无 | 无 |
| **成本** | 中等 | 较高 | ✓极低 | 中等 |

---

## 多芯片项目适配

```yaml
project:
  target_chip:
    family: ESP32
    model: ESP32-S3
    framework: ESP-IDF
    
  # 备选方案
  supported_chips:
    - ESP32-S3 (主力)
    - STM32F4 (备选)
    - RP2040 (原型)
```

---
Version: 2.0
Updated: 2026-04-09