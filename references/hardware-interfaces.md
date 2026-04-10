# Hardware Interface Standards

详细的硬件接口配置规范和代码模板。

---

## SPI接口规范

### 时序模式

| 模式 | CPOL | CPHA | 适用设备 |
|------|------|------|----------|
| **Mode 0** | 0 | 0 | ST7789 LCD、多数传感器 |
| **Mode 1** | 0 | 1 | 特殊传感器 |
| **Mode 2** | 1 | 0 | 特殊应用 |
| **Mode 3** | 1 | 1 | 特殊应用 |

### SPI初始化模板

```c
#include "driver/spi_master.h"

typedef struct {
    spi_host_device_t host;
    uint32_t clock_speed_hz;
    uint8_t mode;
    bool use_dma;
    gpio_num_t mosi_pin;
    gpio_num_t miso_pin;
    gpio_num_t sclk_pin;
    gpio_num_t cs_pin;
} spi_config_t;

esp_err_t spi_master_init(const spi_config_t *config) {
    spi_bus_config_t buscfg = {
        .mosi_io_num     = config->mosi_pin,
        .miso_io_num     = config->miso_pin,
        .sclk_io_num     = config->sclk_pin,
        .max_transfer_sz = config->use_dma ? 4092 : 0,  // ESP32-S3限制
    };
    
    spi_device_interface_config_t devcfg = {
        .clock_speed_hz = config->clock_speed_hz,
        .mode           = config->mode,
        .spics_io_num   = config->cs_pin,
        .queue_size     = 7,
    };
    
    spi_bus_initialize(config->host, &buscfg, SPI_DMA_CH_AUTO);
    spi_bus_add_device(config->host, &devcfg, &handle);
    return ESP_OK;
}
```

### DMA分块传输（突破4092字节限制）

```c
esp_err_t spi_chunked_transmit(spi_device_handle_t handle,
                                const uint8_t *data,
                                size_t total_len) {
    size_t chunk_size = 4092;  // ESP32-S3 DMA限制
    size_t offset = 0;
    
    while (offset < total_len) {
        size_t len = MIN(chunk_size, total_len - offset);
        spi_transaction_t t = {
            .length    = len * 8,
            .tx_buffer = data + offset,
            .flags     = SPI_TRANS_USE_DMA,
        };
        spi_device_transmit(handle, &t);
        offset += len;
    }
    return ESP_OK;
}
```

---

## I2C接口规范

### 配置参数

| 参数 | 典型值 |
|------|------|
| **时钟** | 100kHz (标准), 400kHz (快速) |
| **地址** | 7-bit (常用), 10-bit (特殊) |
| **上拉电阻** | 4.7kΩ (标准), 2.2kΩ (快速) |

### I2C初始化模板

```c
#include "driver/i2c.h"

esp_err_t i2c_master_init(i2c_port_t port, gpio_num_t sda, gpio_num_t scl) {
    i2c_config_t conf = {
        .mode             = I2C_MODE_MASTER,
        .sda_io_num       = sda,
        .scl_io_num       = scl,
        .sda_pullup_en    = GPIO_PULLUP_ENABLE,
        .scl_pullup_en    = GPIO_PULLUP_ENABLE,
        .master.clk_speed = 400000,
    };
    
    i2c_param_config(port, &conf);
    return i2c_driver_install(port, conf.mode, 0, 0, 0);
}

// 读取寄存器
esp_err_t i2c_read_reg(uint8_t addr, uint8_t reg, uint8_t *data) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg, true);
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_READ, true);
    i2c_master_read_byte(cmd, data, I2C_MASTER_NACK);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, 100);
    i2c_cmd_link_delete(cmd);
    return ret;
}
```

---

## UART接口规范

### 标准配置

| 参数 | 典型值 |
|------|------|
| **波特率** | 115200 (调试), 9600-5Mbps (通信) |
| **数据位** | 8 |
| **停止位** | 1 |
| **校验** | 无 |

### UART初始化模板

```c
#include "driver/uart.h"

esp_err_t uart_init(uart_port_t port, int baud, gpio_num_t tx, gpio_num_t rx) {
    uart_config_t config = {
        .baud_rate = baud,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    };
    
    uart_param_config(port, &config);
    uart_set_pin(port, tx, rx, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    return uart_driver_install(port, 2048, 2048, 0, NULL, 0);
}
```

---

## GPIO接口规范

### 配置模式

| 模式 | 用途 |
|------|------|
| **INPUT** | 读取状态 |
| **OUTPUT** | 控制输出 |
| **INPUT_PULLUP** | 按键、传感器 |
| **INPUT_PULLDOWN** | 低电平触发 |
| **OUTPUT_OD** | 开漏输出 |

### GPIO中断处理

```c
#include "driver/gpio.h"

void gpio_isr_handler(void *arg) {
    uint32_t gpio_num = (uint32_t)arg;
    // 处理中断
}

esp_err_t gpio_interrupt_init(gpio_num_t pin, gpio_int_type_t type) {
    gpio_config_t io_conf = {
        .intr_type = type,
        .pin_bit_mask = (1ULL << pin),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
    };
    gpio_config(&io_conf);
    
    gpio_install_isr_service(0);
    gpio_isr_handler_add(pin, gpio_isr_handler, (void *)pin);
    return ESP_OK;
}
```

---

## ADC接口规范

### 配置参数

| 参数 | ESP32-S3 | STM32F4 |
|------|----------|----------|
| **分辨率** | 12-bit | 12-bit |
| **通道** | 10 | 16 |
| **采样率** | 83kHz | 1MHz |

### ADC读取模板

```c
#include "esp_adc_cal.h"

static esp_adc_cal_characteristics_t *adc_chars;

void adc_init(adc1_channel_t channel) {
    adc1_config_width(ADC_WIDTH_BIT_12);
    adc1_config_channel_atten(channel, ADC_ATTEN_DB_11);
    
    adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));
    esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_11, 
                             ADC_WIDTH_BIT_12, 1100, adc_chars);
}

uint32_t adc_read_voltage(adc1_channel_t channel) {
    int raw = adc1_get_raw(channel);
    return esp_adc_cal_raw_to_voltage(raw, adc_chars);
}
```

---

## LCD显示接口规范

### 接口类型

| 类型 | 速度 | 适用场景 |
|------|------|----------|
| **SPI** | 低 | 小屏，简单应用 |
| **QSPI** | 中 | 240x240等 |
| **RGB** | 高 | 大屏，视频 |
| **MIPI DSI** | 极高 | 高端手机屏 |

### LCD初始化序列

```c
// ST7789初始化示例
void lcd_st7789_init(void) {
    lcd_write_cmd(0x11);  // Sleep Out
    vTaskDelay(120 / portTICK_PERIOD_MS);
    
    lcd_write_cmd(0x36);  // MADCTL
    lcd_write_data(0x00); // 正常方向
    
    lcd_write_cmd(0x3A);  // COLMOD
    lcd_write_data(0x05); // 16-bit color
    
    lcd_write_cmd(0x29);  // Display ON
}

// SH8601配置（MimiClaw项目）
void lcd_sh8601_init(void) {
    // y_gap = 0, x_gap = 0
    // madctl_val = 0x00
    // GUI刷新: Y轴翻转 + 行顺序翻转
}
```

---

## DMA限制汇总

| 芯片 | SPI DMA | UART DMA | I2C DMA |
|------|----------|----------|----------|
| **ESP32-S3** | 4092字节 | 支持 | 支持 |
| **STM32F4** | 可配置 | 支持 | 不支持 |
| **RP2040** | PIO替代 | 支持 | PIO |

---
Version: 2.0
Updated: 2026-04-09