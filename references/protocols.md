# Communication Protocol Standards

详细的通信协议配置规范和代码模板。

---

## Wi-Fi网络协议

### 工作模式

| 模式 | 用途 |
|------|------|
| **STA** | 连接AP热点，作为客户端 |
| **AP** | 创建热点，作为服务端 |
| **AP+STA** | 双角色应用 |

### Wi-Fi初始化模板

```c
#include "esp_wifi.h"

void wifi_init_sta(const char *ssid, const char *password) {
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();
    
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    
    wifi_config_t wifi_cfg = {
        .sta = {
            .ssid = ssid,
            .password = password,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };
    
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_cfg);
    esp_wifi_start();
    esp_wifi_connect();
}
```

---

## TCP/IP Socket编程

### TCP客户端模板

```c
#include "lwip/sockets.h"

int tcp_connect(const char *host, int port) {
    struct sockaddr_in dest_addr;
    dest_addr.sin_addr.s_addr = inet_addr(host);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(port);
    
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
    return sock;
}

int tcp_send(int sock, const char *data, int len) {
    return send(sock, data, len, 0);
}

int tcp_recv(int sock, char *buf, int len) {
    return recv(sock, buf, len, 0);
}
```

---

## HTTP客户端

### HTTP GET请求模板

```c
#include "esp_http_client.h"

esp_err_t http_get(const char *url) {
    esp_http_client_config_t config = {
        .url = url,
        .method = HTTP_METHOD_GET,
        .timeout_ms = 5000,
    };
    
    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_err_t err = esp_http_client_perform(client);
    
    if (err == ESP_OK) {
        int content_length = esp_http_client_get_content_length(client);
        int status_code = esp_http_client_get_status_code(client);
    }
    
    esp_http_client_cleanup(client);
    return err;
}
```

---

## MQTT协议

### QoS等级

| QoS | 说明 |
|------|------|
| **0** | 最多一次，不保证送达 |
| **1** | 至少一次，保证送达 |
| **2** | 只有一次，精确送达 |

### MQTT客户端模板

```c
#include "mqtt_client.h"

esp_mqtt_client_handle_t mqtt_init(const char *uri) {
    esp_mqtt_client_config_t cfg = {
        .uri = uri,
        .qos = 1,
        .retain = false,
    };
    
    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&cfg);
    esp_mqtt_client_start(client);
    return client;
}

void mqtt_publish(esp_mqtt_client_handle_t client, 
                  const char *topic, const char *data) {
    esp_mqtt_client_publish(client, topic, data, 0, 1, 0);
}
```

---

## Bluetooth BLE协议

### GATT服务结构

```
Service
├── Characteristic 1 (Read)
├── Characteristic 2 (Write)
└── Characteristic 3 (Notify)
```

### BLE初始化模板

```c
#include "esp_bt.h"
#include "esp_gap_ble_api.h"

void ble_init(void) {
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    esp_bt_controller_init(&bt_cfg);
    esp_bt_controller_enable(ESP_BT_MODE_BLE);
    esp_bluedroid_init();
    esp_bluedroid_enable();
}
```

---

## JSON数据序列化

### JSON生成模板

```c
#include "cJSON.h"

char *json_create_object(void) {
    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "device", "ESP32-S3");
    cJSON_AddNumberToObject(root, "temperature", 25.5);
    cJSON_AddBoolToObject(root, "status", true);
    
    char *json_str = cJSON_Print(root);
    cJSON_Delete(root);
    return json_str;
}

cJSON *json_parse(const char *json_str) {
    return cJSON_Parse(json_str);
}
```

---

## TLS/SSL安全通信

### TLS配置模板

```c
#include "esp_tls.h"

esp_tls_t *tls_connect(const char *host, int port) {
    esp_tls_cfg_t cfg = {
        .cacert_pem_buf = server_cert_pem_start,
        .cacert_pem_bytes = server_cert_pem_end - server_cert_pem_start,
    };
    
    return esp_tls_conn_new_sync(host, strlen(host), port, &cfg);
}
```

---

## WebSocket协议

### WebSocket连接模板

```c
#include "esp_websocket_client.h"

esp_websocket_client_handle_t ws_connect(const char *uri) {
    esp_websocket_client_config_t cfg = {
        .uri = uri,
        .reconnect_timeout_ms = 5000,
    };
    
    return esp_websocket_client_init(&cfg);
}

void ws_send(esp_websocket_client_handle_t client, const char *data) {
    esp_websocket_client_send(client, data, strlen(data), portMAX_DELAY);
}
```

---

## Modbus协议

### 功能码

| 功能码 | 名称 |
|--------|------|
| **03** | Read Holding Registers |
| **06** | Write Single Register |
| **16** | Write Multiple Registers |

### Modbus主站模板

```c
#include "esp_modbus.h"

void modbus_master_init(void) {
    mb_communication_info_t comm_info = {
        .port = UART_NUM_1,
        .mode = MB_MODE_RTU,
        .baudrate = 9600,
    };
    mbc_master_init(MB_PORT_SERIAL_MASTER, &comm_info);
}

esp_err_t modbus_read_reg(uint8_t slave, uint16_t addr, uint16_t *value) {
    mb_param_request_t request = {
        .slave_addr = slave,
        .command = 3,  // Read Holding
        .reg_addr = addr,
        .reg_count = 1,
    };
    return mbc_master_send_request(&request, value);
}
```

---

## 协议选择指南

| 场景 | 推荐协议 | 理由 |
|------|----------|------|
| IoT消息推送 | MQTT | 轻量，支持QoS |
| 实时通信 | WebSocket | 双向，低延迟 |
| REST API | HTTP | 标准化，兼容性好 |
| 近场通信 | BLE | 低功耗，便捷 |
| 工业控制 | Modbus | 标准，可靠 |

---
Version: 2.0
Updated: 2026-04-09