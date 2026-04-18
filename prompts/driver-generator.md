# Driver Code Generator Prompt

## Task Description

Generate embedded driver code for specified hardware.

## Required Inputs

| Parameter | Description | Example |
|-----------|-------------|---------|
| chip_family | Target MCU family | ESP32-S3, STM32F4, RP2040 |
| interface | Communication interface | SPI, I2C, UART, GPIO |
| controller | Device controller/model | ST7789, SH8601, BME280 |
| resolution/config | Hardware configuration | 240x240, Mode 0, 40MHz |

## Required Outputs

1. **driver.h**: Header file with function declarations and constants
2. **driver.c**: Implementation with init/write/read functions

## Hard Constraints (Iron Law)

- **DMA buffer <= 4092 bytes** (ESP32-S3 SPI DMA)
- Follow MISRA C guidelines
- Include error handling for all paths
- Use initialization sequence from datasheet (not guessed)
- Chunk handling for data > DMA limit

## Verification Required

```bash
# Windows PowerShell
idf.py build

# Linux/macOS
idf.py build
```

Expected: Exit code 0, no errors or warnings

## Status Report Format

After implementation, report ONE of:

| Status | Meaning | Next Action |
|--------|---------|-------------|
| `DONE` | Code generated, build verified | Proceed to hardware validator |
| `DONE_WITH_CONCERNS` | Completed but flagged doubts | Review concerns before proceeding |
| `NEEDS_DATASHEET` | Missing controller specification | Provide datasheet initialization sequence |
| `BLOCKED` | Cannot proceed | Explain blocker, await resolution |

## Template Structure

### driver.h Template

```c
#ifndef {CONTROLLER}_H
#define {CONTROLLER}_H

#include <stdint.h>
#include "esp_err.h"  // For ESP32, adjust for other platforms

// Configuration constants
#define {CONTROLLER}_WIDTH     {width}
#define {CONTROLLER}_HEIGHT    {height}
#define {CONTROLLER}_SPI_MODE  {mode}
#define {CONTROLLER}_SPI_CLK   {clock_hz}

// DMA constraint (ESP32-S3)
#define {CONTROLLER}_DMA_MAX   4092

// Function declarations
esp_err_t {controller}_init(void);
esp_err_t {controller}_write(const uint8_t *data, size_t len);
esp_err_t {controller}_read(uint8_t *data, size_t len);
void {controller}__deinit(void);

#endif // {CONTROLLER}_H
```

### driver.c Template

```c
#include "{controller}.h"
#include "esp_log.h"
#include "driver/spi_master.h"  // Adjust for interface type

static const char *TAG = "{CONTROLLER}";

// Initialization sequence from datasheet
// Format: {command, delay_ms, data_len, data...}
static const uint8_t init_sequence[] = {
    // Example for ST7789:
    // 0x01, 0, 0,           // Software reset, 120ms delay
    // 0x11, 120, 0,         // Sleep out
    // 0x3A, 0, 1, 0x55,     // Color mode: 16-bit
    // ... (from datasheet, not guessed)
};

// DMA chunk buffer
static uint8_t dma_buffer[{CONTROLLER}_DMA_MAX];

esp_err_t {controller}_init(void) {
    ESP_LOGI(TAG, "Initializing {controller}");
    
    // 1. Configure interface (SPI/I2C/UART)
    // 2. Send initialization sequence from datasheet
    // 3. Verify device response (if applicable)
    
    return ESP_OK;
}

esp_err_t {controller}_write(const uint8_t *data, size_t len) {
    // Handle DMA chunking for data > 4092 bytes
    size_t remaining = len;
    size_t offset = 0;
    
    while (remaining > 0) {
        size_t chunk = (remaining > {CONTROLLER}_DMA_MAX) ? 
                       {CONTROLLER}_DMA_MAX : remaining;
        
        // Copy to DMA-safe buffer
        memcpy(dma_buffer, data + offset, chunk);
        
        // Send chunk
        // spi_device_transmit(...) or equivalent
        
        offset += chunk;
        remaining -= chunk;
    }
    
    return ESP_OK;
}

esp_err_t {controller}_read(uint8_t *data, size_t len) {
    // Implement read if device supports
    return ESP_OK;
}

void {controller}_deinit(void) {
    // Clean up resources
}
```

## Anti-Patterns (DO NOT)

| Bad Practice | Correct Approach |
|--------------|------------------|
| Guess initialization sequence | Use datasheet values exactly |
| Skip DMA chunking for large data | Always chunk > 4092 bytes |
| No error handling | Check every esp_err_t return |
| Hardcoded delays from memory | Verify delays match datasheet |
| Single large DMA transfer | Chunk with proper boundaries |

## Platform-Specific Notes

### Windows PowerShell
```powershell
idf.py build; if($?) {echo "Build successful"} else {echo "Build failed"}
```

### Linux/macOS Bash
```bash
idf.py build && echo "Build successful"
```

## Self-Check Before Reporting DONE

- [ ] All functions have error handling
- [ ] DMA chunking implemented if needed
- [ ] Init sequence matches datasheet
- [ ] Constants defined in header
- [ ] Build verified with `idf.py build`
- [ ] No warnings in build output