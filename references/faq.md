# Frequently Asked Questions (FAQ)

嵌入式开发常见问题快速解答。

---

## 编译相关 FAQ

### Q1: 编译提示 `uint32_t` 格式字符串错误？

**错误示例**:
```
error: format '%d' expects argument of type 'int', 
but argument 6 has type 'long unsigned int' [-Werror=format=]
ESP_LOGD(TAG, "Value: %d", value);  // value is uint32_t
```

**原因**:
- ESP32平台 `uint32_t` 定义为 `unsigned long`
- `%d` 用于 `int`，类型不匹配

**解决方案**:

```c
// 方案1: 使用 %lu + 类型转换 (推荐)
ESP_LOGD(TAG, "Value: %lu", (unsigned long)value);

// 方案2: 使用 PRIu32 宏 (跨平台)
#include <inttypes.h>
ESP_LOGD(TAG, "Value: %" PRIu32, value);

// 方案3: 使用 %u 并强制转换
ESP_LOGD(TAG, "Value: %u", (unsigned int)value);
```

**类型格式对照表**:

| 类型 | ESP32定义 | 正确格式 |
|------|-----------|----------|
| `int` | 4 bytes | `%d` |
| `unsigned int` | 4 bytes | `%u` |
| `uint32_t` | `unsigned long` | `%lu` 或 `PRIu32` |
| `size_t` | `unsigned int` | `%zu` |
| `int64_t` | `long long` | `%lld` 或 `PRId64` |

---

### Q2: 编译时出现 `undefined reference to xxx` 错误？

**错误示例**:
```
undefined reference to `lcd_init'
```

**原因分析**:
1. 函数声明但未实现
2. CMakeLists.txt未包含源文件
3. 链接顺序问题
4. 条件编译排除

**解决方案**:

```yaml
# 检查1: 确认函数实现
# main.c
void lcd_init(void) {
    // 实现
}

# 检查2: 确认CMakeLists.txt
# main/CMakeLists.txt
idf_component_register(
    SRCS "main.c" "lcd_driver.c"  # ← 确保包含所有源文件
    INCLUDE_DIRS "."
)

# 检查3: 确认头文件包含
# main.c
#include "lcd_driver.h"  # ← 包含函数声明

# 检查4: 检查条件编译
#ifndef CONFIG_DISABLE_LCD
void lcd_init(void) { ... }
#endif
```

---

### Q3: 编译警告 `unused variable` 或 `unused function`？

**警告示例**:
```
warning: 'debug_buffer' defined but not used [-Wunused-variable]
warning: 'helper_function' defined but not used [-Wunused-function]
```

**解决方案**:

```c
// 方案1: 添加 unused 属性
static void helper_function(void) __attribute__((unused));
static uint8_t debug_buffer[256] __attribute__((unused));

// 方案2: 使用 (void) 避免警告
void function(void) {
    int unused_var = 0;
    (void)unused_var;  // 明确标记未使用
}

// 方案3: 使用 UNUSED 宏
#define UNUSED(x) (void)(x)
UNUSED(unused_var);

// 方案4: 条件编译
#ifdef DEBUG
static void debug_function(void) { ... }
#endif
```

---

### Q4: 编译错误 `section .text will not fit in region iram`？

**错误示例**:
```
region `iram0_0_seg' overflowed by 12345 bytes
```

**原因**: 代码段超出IRAM容量

**解决方案**:

```c
// 方案1: 使用Flash存储常量
const char large_data[] = "...";  // 存储在Flash

// 方案2: 移除IRAM属性
// sdkconfig中检查
// CONFIG_SPI_FLASH_ROM_DRIVER_PATCH = n
// CONFIG_ESP_TIMER_INTERRUPT_LEVEL = 1

// 方案3: 优化代码大小
// CMakeLists.txt
set(COMPONENT_OPTIMIZATION_LEVEL "-Os")  # 优化大小

// 方案4: 使用PSRAM存储大对象
uint8_t *large_buffer = heap_caps_malloc(size, MALLOC_CAP_SPIRAM);
```

---

## 内存相关 FAQ

### Q5: 如何选择 PSRAM vs SRAM？

**ESP32-S3 内存配置**:
```
内部SRAM: 512KB (快速，有限)
外部PSRAM: 8MB (较慢，充足)
```

**分配策略**:

| 对象类型 | 推荐内存 | 原因 |
|----------|----------|------|
| Framebuffer (>100KB) | PSRAM | 大对象，节省内部RAM |
| DMA缓冲区 | SRAM或PSRAM | 看具体需求 |
| 频繁访问数据 | SRAM | 速度快 |
| 任务堆栈 | SRAM | 默认配置 |
| 大型数组 | PSRAM | 节省内部RAM |
| 临时缓冲区 | PSRAM | 用完释放 |

**示例代码**:

```c
// ✅ 正确: 大对象使用PSRAM
uint16_t *framebuffer = heap_caps_malloc(257 * 1024, MALLOC_CAP_SPIRAM);

// ✅ 正确: Fallback机制
uint16_t *buffer = heap_caps_malloc(size, MALLOC_CAP_SPIRAM);
if (!buffer) {
    buffer = heap_caps_malloc(size, MALLOC_CAP_DMA | MALLOC_CAP_INTERNAL);
}

// ❌ 错误: 大对象使用内部RAM
uint16_t framebuffer[128640];  // 占用257KB内部RAM！

// ✅ 正确: 频繁访问数据用SRAM
uint32_t *lookup_table = heap_caps_malloc(4 * 1024, MALLOC_CAP_INTERNAL);
```

---

### Q6: PSRAM 分配失败怎么办？

**错误现象**:
```c
uint8_t *buffer = heap_caps_malloc(size, MALLOC_CAP_SPIRAM);
// buffer == NULL
```

**诊断步骤**:

```bash
# 1. 检查sdkconfig配置
idf.py menuconfig
# → Component config → ESP PSRAM
#   → [*] Enable PSRAM
#   → SPI RAM Type (Octal PSRAM)
#   → [*] Initialize PSRAM during startup

# 2. 检查PSRAM大小
# 预期: 8MB
```

**代码检查**:

```c
// 3. 检查PSRAM初始化
void app_main(void)
{
    // 查看启动日志
    // 应该看到: "Detected octal PSRAM" 或类似信息
    
    // 打印内存信息
    ESP_LOGI("MEM", "Free heap: %lu", esp_get_free_heap_size());
    ESP_LOGI("MEM", "Free PSRAM: %lu", heap_caps_get_free_size(MALLOC_CAP_SPIRAM));
}

// 4. 检查分配大小
size_t required_size = 1024 * 1024;  // 1MB
size_t free_psram = heap_caps_get_free_size(MALLOC_CAP_SPIRAM);
if (free_psram < required_size) {
    ESP_LOGE("MEM", "Not enough PSRAM: need %lu, have %lu",
             (unsigned long)required_size, (unsigned long)free_psram);
}
```

**常见原因与解决**:

| 原因 | 解决方案 |
|------|----------|
| sdkconfig未启用PSRAM | `CONFIG_SPIRAM=y` |
| 引脚配置错误 | 检查硬件连接 |
| 分配大小过大 | 减小分配大小或分段分配 |
| PSRAM碎片化 | 重启系统或整理碎片 |
| 初始化失败 | 检查电源和硬件 |

---

### Q7: 如何检测内存泄漏？

**方法1: 定期检查堆内存**

```c
void monitor_memory(void)
{
    static uint32_t last_free = 0;
    uint32_t current_free = esp_get_free_heap_size();
    
    if (last_free > 0 && current_free < last_free) {
        ESP_LOGW("MEM", "Possible memory leak: %lu bytes lost",
                 (unsigned long)(last_free - current_free));
    }
    
    last_free = current_free;
}

// 定期调用
void app_main(void)
{
    while (1) {
        monitor_memory();
        vTaskDelay(pdMS_TO_TICKS(60000));  // 每分钟检查
    }
}
```

**方法2: 使用堆跟踪功能**

```bash
# sdkconfig配置
CONFIG_HEAP_TASK_TRACKING=y
CONFIG_HEAP_TRACING=y
CONFIG_HEAP_TRACING_STACK_DEPTH=2
```

```c
#include "esp_heap_trace.h"

void app_main(void)
{
    // 启动堆跟踪
    heap_trace_start(HEAP_TRACE_LEAKS);
    
    // ... 应用代码 ...
    
    // 停止并打印结果
    heap_trace_stop();
    heap_trace_dump();
}
```

**方法3: 使用Task List**

```c
#include "esp_task_wdt.h"

void print_task_list(void)
{
    char *task_list = (char *)malloc(2048);
    if (task_list) {
        vTaskList(task_list);
        ESP_LOGI("TASK", "Task List:\n%s", task_list);
        free(task_list);
    }
}
```

---

## LCD显示相关 FAQ

### Q8: LCD不显示或显示异常？

**诊断流程**:

```
LCD不显示
    ├─ 硬件检查
    │   ├─ 电源连接
    │   ├─ 背光控制
    │   └─ 引脚连接
    │
    ├─ 初始化检查
    │   ├─ SPI/QSPI配置
    │   ├─ 初始化序列
    │   └─ 复位时序
    │
    └─ 数据传输检查
        ├─ 地址设置
        ├─ 数据格式
        └─ DMA配置
```

**诊断代码**:

```c
void diagnose_lcd(void)
{
    // 1. 检查背光
    gpio_set_level(LCD_BL_PIN, 1);
    ESP_LOGI("LCD", "Backlight ON");
    
    // 2. 检查复位
    gpio_set_level(LCD_RST_PIN, 0);
    vTaskDelay(pdMS_TO_TICKS(100));
    gpio_set_level(LCD_RST_PIN, 1);
    vTaskDelay(pdMS_TO_TICKS(100));
    ESP_LOGI("LCD", "Reset complete");
    
    // 3. 检查SPI传输
    uint8_t test_cmd = 0x0C;  // Read ID
    lcd_send_cmd(test_cmd, NULL, 0);
    ESP_LOGI("LCD", "Test command sent");
    
    // 4. 填充测试颜色
    lcd_fill_screen(0xF800);  // 红色
    ESP_LOGI("LCD", "Screen filled with RED");
    vTaskDelay(pdMS_TO_TICKS(1000));
    
    lcd_fill_screen(0x07E0);  // 绿色
    ESP_LOGI("LCD", "Screen filled with GREEN");
}
```

**常见问题与解决**:

| 现象 | 原因 | 解决方案 |
|------|------|----------|
| 完全黑屏 | 背光未开启 | 检查BL引脚 |
| 白屏/花屏 | 初始化序列错误 | 检查驱动IC和序列 |
| 显示模糊 | SPI速度过高 | 降低SPI时钟 |
| 颜色异常 | RGB/BGR设置 | 修改MADCTL寄存器 |
| 部分显示 | 窗口设置错误 | 检查地址设置 |
| 闪烁严重 | 刷新频率低 | 增加帧率或使用双缓冲 |

---

### Q9: SPI DMA传输失败？

**错误现象**:
```c
esp_err_t ret = spi_device_transmit(spi_handle, &trans);
// ret == ESP_ERR_INVALID_SIZE
```

**原因**: ESP32 SPI DMA单次传输限制

**DMA限制**:
```
ESP32:  最大 4092 bytes (4096 - 4)
ESP32-S3: 最大 32768 bytes (32KB)
```

**解决方案**:

```c
// ✅ 正确: 分块传输
void lcd_push_colors(uint16_t *data, size_t len)
{
    const size_t CHUNK_SIZE = 4092;  // ESP32
    
    while (len > 0) {
        size_t chunk = (len > CHUNK_SIZE) ? CHUNK_SIZE : len;
        
        spi_transaction_t t = {
            .length = chunk * 8,  // bits
            .tx_buffer = data,
        };
        
        spi_device_transmit(spi_handle, &t);
        
        data += chunk;
        len -= chunk;
    }
}

// ✅ 正确: 使用PSRAM绕过限制
uint16_t *buffer = heap_caps_malloc(size, MALLOC_CAP_SPIRAM);
// PSRAM DMA传输在ESP32-S3支持更大缓冲区
```

---

### Q10: LCD显示颜色不对？

**问题现象**:
- 红色显示为蓝色
- 绿色显示为红色
- 颜色整体偏移

**原因**: RGB/BGR顺序配置错误

**解决方案**:

```c
// 检查MADCTL寄存器 (Memory Access Control)
#define TFT_MADCTL  0x36
#define TFT_MAD_RGB 0x00   // RGB顺序
#define TFT_MAD_BGR 0x08   // BGR顺序

// 方案1: 修改驱动配置
void lcd_set_color_order(bool bgr)
{
    uint8_t madctl = bgr ? TFT_MAD_BGR : TFT_MAD_RGB;
    lcd_send_cmd(TFT_MADCTL, &madctl, 1);
}

// 方案2: 修改颜色数据
uint16_t swap_rb(uint16_t color)
{
    uint16_t r = (color >> 11) & 0x1F;
    uint16_t g = (color >> 5) & 0x3F;
    uint16_t b = color & 0x1F;
    return (b << 11) | (g << 5) | r;
}

// 方案3: 检查初始化序列
const lcd_cmd_t init_seq[] = {
    {0x36, {0x08}, 1},  // ← BGR order
    // ...
};
```

---

## 通信协议相关 FAQ

### Q11: UART接收数据丢失或错误？

**问题诊断**:

```c
// 检查UART配置
void diagnose_uart(void)
{
    // 1. 检查波特率
    ESP_LOGI("UART", "Baud rate: %d", UART_BAUD);
    
    // 2. 检查缓冲区
    uart_flush_input(UART_NUM);
    ESP_LOGI("UART", "Buffer flushed");
    
    // 3. 检查接收状态
    size_t buffered_len;
    uart_get_buffered_data_len(UART_NUM, &buffered_len);
    ESP_LOGI("UART", "Buffered data: %d bytes", buffered_len);
    
    // 4. 检查错误状态
    uart_err_status_t err_status;
    uart_get_err_status(UART_NUM, &err_status);
    if (err_status.parity_err) ESP_LOGW("UART", "Parity error");
    if (err_status.frame_err) ESP_LOGW("UART", "Frame error");
    if (err_status.overrun_err) ESP_LOGW("UART", "Overrun error");
}
```

**常见问题与解决**:

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 数据丢失 | 缓冲区太小 | 增大UART缓冲区 |
| 数据乱码 | 波特率不匹配 | 检查波特率设置 |
| 帧错误 | 时钟偏差 | 调整波特率或时钟 |
| 接收不完整 | 读取超时太短 | 增加超时时间 |
| 数据重复 | 缓冲区未清空 | 定期flush缓冲区 |

**优化配置**:

```c
// 增加缓冲区
uart_driver_install(UART_NUM_2, 2048, 0, 0, NULL, 0);  // 2KB RX buffer

// 调整超时
int len = uart_read_bytes(UART_NUM, data, len, pdMS_TO_TICKS(1000));  // 1s timeout

// 使用DMA
uart_driver_install(UART_NUM, 2048, 2048, 0, NULL, ESP_INTR_FLAG_IRAM);
```

---

### Q12: I2C设备通信失败？

**错误现象**:
```
I2C: ACK not received
I2C: Timeout
```

**诊断步骤**:

```c
// 1. I2C总线扫描
void i2c_scan(void)
{
    ESP_LOGI("I2C", "Scanning bus...");
    
    for (uint8_t addr = 0x08; addr < 0x78; addr++) {
        i2c_cmd_handle_t cmd = i2c_cmd_link_create();
        i2c_master_start(cmd);
        i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
        i2c_master_stop(cmd);
        
        esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, pdMS_TO_TICKS(100));
        i2c_cmd_link_delete(cmd);
        
        if (ret == ESP_OK) {
            ESP_LOGI("I2C", "Device found at 0x%02X", addr);
        }
    }
}

// 2. 检查上拉电阻
// I2C需要外部上拉电阻 (通常4.7K)
// 使用万用表测量SDA/SCL空闲时为高电平

// 3. 检查信号质量
// 使用逻辑分析仪查看波形
```

**常见问题**:

| 问题 | 检查项 |
|------|--------|
| 无ACK | 设备地址错误、设备未上电、上拉电阻缺失 |
| 被超时 | 速率过高、线路过长、电容过大 |
| 数据错误 | 上拉电阻不合适、干扰、地线问题 |
| 锁死 | 时钟拉伸、设备故障 |

---

### Q13: SPI通信不稳定？

**问题现象**:
- 偶尔数据错误
- 传输失败
- CRC错误

**优化配置**:

```c
// 1. 降低时钟频率
#define SPI_FREQUENCY  10000000  // 10MHz (原来是20MHz)

// 2. 增加CS保持时间
spi_device_interface_config_t devcfg = {
    .clock_speed_hz = SPI_FREQUENCY,
    .mode = 0,
    .spics_io_num = CS_PIN,
    .cs_ena_pretrans = 16,   // CS激活前延时
    .cs_ena_posttrans = 16,  // CS释放后延时
};

// 3. 使用DMA提高稳定性
#define SPI_MAX_TRANSFER_SIZE  4092
spi_bus_config_t buscfg = {
    .mosi_io_num = MOSI_PIN,
    .miso_io_num = MISO_PIN,
    .sclk_io_num = SCK_PIN,
    .max_transfer_sz = SPI_MAX_TRANSFER_SIZE,
};

// 4. 添加错误重试
esp_err_t spi_transmit_with_retry(spi_device_handle_t handle, spi_transaction_t *trans)
{
    for (int retry = 0; retry < 3; retry++) {
        esp_err_t ret = spi_device_transmit(handle, trans);
        if (ret == ESP_OK) {
            return ESP_OK;
        }
        ESP_LOGW("SPI", "Transmit failed (retry %d): %s", retry, esp_err_to_name(ret));
        vTaskDelay(pdMS_TO_TICKS(10));
    }
    return ESP_FAIL;
}
```

---

## 调试相关 FAQ

### Q14: 如何查看日志输出？

**方法1: 串口监控**

```bash
# 启动监控
idf.py monitor

# 或指定端口
idf.py -p COM3 monitor

# 退出监控
Ctrl + ]
```

**方法2: 设置日志级别**

```c
// 全局设置
esp_log_level_set("*", ESP_LOG_INFO);

// 模块设置
esp_log_level_set("LCD", ESP_LOG_DEBUG);
esp_log_level_set("SPI", ESP_LOG_VERBOSE);

// sdkconfig配置
CONFIG_LOG_DEFAULT_LEVEL_INFO=y
CONFIG_LOG_DEFAULT_LEVEL=3
```

**方法3: 条件日志**

```c
// 使用TAG便于过滤
static const char *TAG = "MAIN";

ESP_LOGE(TAG, "Error message");    // 错误
ESP_LOGW(TAG, "Warning message");  // 警告
ESP_LOGI(TAG, "Info message");     // 信息
ESP_LOGD(TAG, "Debug message");    // 调试
ESP_LOGV(TAG, "Verbose message");  // 详细
```

---

### Q15: 如何调试崩溃问题？

**崩溃信息分析**:

```bash
# 典型崩溃输出
Guru Meditation Error: Core  0 panic'ed (LoadProhibited)
. Exception was unhandled.
Core  0 register dump:
PC      : 0x400d1234  PS      : 0x00060433  A0      : 0x800d1250  A1      : 0x3ffc1234
...

# 解析步骤:
1. PC (Program Counter): 崩溃地址
2. 使用 addr2line 定位源码
```

**定位崩溃位置**:

```bash
# 方法1: 使用 addr2line
xtensa-esp32s3-elf-addr2line -pf -C -e build/project.elf 0x400d1234

# 方法2: 使用 gdb
xtensa-esp32s3-elf-gdb build/project.elf
(gdb) info line *0x400d1234

# 方法3: 查看反汇编
xtensa-esp32s3-elf-objdump -d build/project.elf | grep -A 20 "400d1234"
```

**常见崩溃原因**:

| 错误类型 | 原因 | 排查方向 |
|----------|------|----------|
| LoadProhibited | 空指针解引用 | 检查指针是否NULL |
| StoreProhibited | 写入非法地址 | 检查数组越界、野指针 |
| InstrLoadProhibited | 执行非法指令 | 函数指针错误、栈溢出 |
| IntegerDivideByZero | 除零错误 | 检查除数是否为0 |
| StackGuard | 栈溢出 | 增大任务堆栈 |

**防护措施**:

```c
// 1. 指针检查
if (ptr != NULL) {
    *ptr = value;
}

// 2. 数组边界检查
if (index < ARRAY_SIZE(array)) {
    array[index] = value;
}

// 3. 除零检查
if (divisor != 0) {
    result = dividend / divisor;
}

// 4. 看门狗保护
esp_task_wdt_init(10, true);  // 10秒超时
```

---

### Q16: 任务堆栈溢出怎么检测？

**方法1: 运行时检测**

```c
#include "esp_task.h"

void task_function(void *pvParameters)
{
    while (1) {
        // 检查堆栈水位
        UBaseType_t stack_remaining = uxTaskGetStackHighWaterMark(NULL);
        uint32_t bytes_remaining = stack_remaining * sizeof(StackType_t);
        
        if (bytes_remaining < 512) {
            ESP_LOGW("TASK", "Stack low: %u bytes remaining", bytes_remaining);
        }
        
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
```

**方法2: 启动时检查所有任务**

```c
void print_all_tasks_stack(void)
{
    TaskStatus_t *task_array;
    UBaseType_t task_count = uxTaskGetNumberOfTasks();
    
    task_array = pvPortMalloc(task_count * sizeof(TaskStatus_t));
    if (task_array) {
        uxTaskGetSystemState(task_array, task_count, NULL);
        
        ESP_LOGI("TASK", "Task Stack Usage:");
        for (int i = 0; i < task_count; i++) {
            ESP_LOGI("TASK", "  %-16s: %u bytes free",
                     task_array[i].pcTaskName,
                     task_array[i].usStackHighWaterMark * 4);
        }
        
        vPortFree(task_array);
    }
}
```

**方法3: 配置栈溢出检测**

```bash
# sdkconfig
CONFIG_FREERTOS_CHECK_STACKOVERFLOW_CANARY=y
```

---

## 硬件相关 FAQ

### Q17: GPIO电平不稳定？

**问题现象**:
- 读取值随机跳变
- 输出不稳定

**解决方案**:

```c
// 1. 配置上拉/下拉
gpio_config_t io_conf = {
    .pin_bit_mask = (1ULL << GPIO_NUM),
    .mode = GPIO_MODE_INPUT,
    .pull_up_en = GPIO_PULLUP_ENABLE,     // 上拉
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .intr_type = GPIO_INTR_DISABLE,
};

// 2. 添加硬件滤波
gpio_pulldown_en(GPIO_NUM);
gpio_pullup_dis(GPIO_NUM);

// 3. 软件消抖
int stable_read(uint32_t gpio_num, int samples, int delay_ms)
{
    int high_count = 0;
    for (int i = 0; i < samples; i++) {
        if (gpio_get_level(gpio_num) == 1) {
            high_count++;
        }
        vTaskDelay(pdMS_TO_TICKS(delay_ms));
    }
    return (high_count > samples / 2) ? 1 : 0;
}
```

---

### Q18: ADC读数不准确？

**问题现象**:
- ADC值波动大
- 与实际电压不符

**优化方法**:

```c
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"

// 1. 多次采样平均
float read_adc_average(adc_oneshot_unit_handle_t handle, adc_channel_t channel, int samples)
{
    int total = 0;
    for (int i = 0; i < samples; i++) {
        int raw;
        adc_oneshot_read(handle, channel, &raw);
        total += raw;
        vTaskDelay(pdMS_TO_TICKS(10));
    }
    return (float)total / samples;
}

// 2. 使用ADC校准
adc_cali_handle_t cali_handle = NULL;
adc_cali_line_fitting_config_t cali_config = {
    .unit_id = ADC_UNIT_1,
    .atten = ADC_ATTEN_DB_12,
    .bitwidth = ADC_BITWIDTH_12,
};
adc_cali_create_scheme_line_fitting(&cali_config, &cali_handle);

// 读取校准后的电压
int voltage_mv;
adc_cali_raw_to_voltage(cali_handle, raw_value, &voltage_mv);

// 3. 使用过采样提高精度
// sdkconfig
CONFIG_ADC_ONESHOT_CTRL_ONESHOT_REGULAR_DATA_NUM=16
```

---

## 性能优化 FAQ

### Q19: 如何提高系统性能？

**优化策略**:

```c
// 1. 使用DMA减少CPU占用
spi_bus_config_t buscfg = {
    .max_transfer_sz = 4092,  // 启用DMA
};

// 2. 优化任务优先级
xTaskCreate(high_priority_task, "high", 4096, NULL, 10, NULL);  // 高优先级
xTaskCreate(low_priority_task, "low", 4096, NULL, 1, NULL);     // 低优先级

// 3. 使用PSRAM减少内存拷贝
uint8_t *buffer = heap_caps_malloc(size, MALLOC_CAP_SPIRAM);

// 4. 优化循环
// 避免在循环中调用函数
for (int i = 0; i < ARRAY_SIZE; i++) {
    // 内联小函数
    array[i] = inline_function(array[i]);
}

// 5. 使用查表代替计算
const uint16_t sin_table[360] = { ... };  // 预计算正弦表
uint16_t fast_sin(int angle) {
    return sin_table[angle % 360];
}

// 6. 编译器优化
// CMakeLists.txt
set(COMPONENT_OPTIMIZATION_LEVEL "-O3")  # 最高优化
```

---

### Q20: 如何降低功耗？

**低功耗策略**:

```c
// 1. 降低CPU频率
// sdkconfig
CONFIG_ESP_DEFAULT_CPU_FREQ_80=y  // 80MHz (原来是240MHz)

// 2. 使用Light Sleep
esp_sleep_enable_timer_wakeup(60 * 1000000);  // 60秒唤醒
esp_light_sleep_start();

// 3. 使用Deep Sleep
esp_sleep_enable_timer_wakeup(3600 * 1000000);  // 1小时唤醒
esp_deep_sleep_start();

// 4. 关闭外设
gpio_set_level(LCD_BL_PIN, 0);  // 关闭背光
uart_driver_delete(UART_NUM_2);  // 释放UART

// 5. 降低WiFi功率
esp_wifi_set_max_tx_power(8);  // 最小发射功率

// 6. 使用低功耗模式
// sdkconfig
CONFIG_PM_ENABLE=y
CONFIG_FREERTOS_USE_TICKLESS_IDLE=y
```

**功耗对比**:

| 模式 | 典型功耗 | 说明 |
|------|----------|------|
| Active | 160mA | 全速运行 |
| Modem Sleep | 40mA | WiFi关闭 |
| Light Sleep | 0.8mA | CPU暂停 |
| Deep Sleep | 10μA | 仅RTC运行 |

---

## 总结

以上FAQ覆盖了嵌入式开发中最常见的问题。遇到问题时，建议按照以下流程排查:

1. **明确问题**: 准确描述问题现象
2. **检查日志**: 查看串口输出和错误信息
3. **逐步定位**: 使用诊断代码缩小问题范围
4. **验证假设**: 逐一验证可能的原因
5. **查找资料**: 查阅数据手册和应用笔记
6. **寻求帮助**: 在论坛或社区提问

记住: **详细的日志和诊断信息是解决问题的关键！**

---
Version: 1.0
Updated: 2026-04-10