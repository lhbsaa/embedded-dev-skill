# Remote Connection & Monitoring Tools

远程连接、监控和管理工具规范。

---

## WiFi远程烧录

### ESP32 OTA配置

```c
#include "esp_ota_ops.h"
#include "esp_https_ota.h"

esp_err_t ota_update(const char *url) {
    esp_http_client_config_t config = {
        .url = url,
        .cert_pem = server_cert_pem_start,
    };
    
    esp_err_t ret = esp_https_ota(&config);
    if (ret == ESP_OK) {
        esp_restart();
    }
    return ret;
}
```

### OTA API服务器

```c
// 简单的OTA HTTP服务器
void ota_server_start(void) {
    httpd_handle_t server = NULL;
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    
    httpd_start(&server, &config);
    
    httpd_uri_t ota_uri = {
        .uri = "/ota",
        .method = HTTP_POST,
        .handler = ota_handler,
    };
    httpd_register_uri_handler(server, &ota_uri);
}
```

---

## 串口远程监控

### ser2net配置

```yaml
# /etc/ser2net.conf
# 端口 设备  选项
2001:raw:0:/dev/ttyUSB0:115200 8DATABITS NONE 1STOPBIT
2002:raw:0:/dev/ttyUSB1:115200 8DATABITS NONE 1STOPBIT
```

### socat串口转发

```bash
# 转发本地串口到TCP端口
socat TCP-LISTEN:2001,fork,reuseaddr FILE:/dev/ttyUSB0,b115200,raw

# 客户端连接
socat TCP:192.168.1.100:2001 STDIO
```

### Python串口转发脚本

```python
import socket
import serial

def serial_to_tcp(ser_port, tcp_port):
    ser = serial.Serial(ser_port, 115200)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', tcp_port))
    sock.listen(1)
    
    while True:
        conn, addr = sock.accept()
        while True:
            if ser.in_waiting:
                conn.send(ser.read(ser.in_waiting))
```

---

## Web远程管理

### ESP32 Web服务器

```c
#include "esp_http_server.h"

httpd_handle_t start_webserver(void) {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    httpd_handle_t server = NULL;
    httpd_start(&server, &config);
    
    // 设备状态API
    httpd_uri_t status_uri = {
        .uri = "/api/status",
        .method = HTTP_GET,
        .handler = status_handler,
    };
    httpd_register_uri_handler(server, &status_uri);
    
    // 控制API
    httpd_uri_t control_uri = {
        .uri = "/api/control",
        .method = HTTP_POST,
        .handler = control_handler,
    };
    httpd_register_uri_handler(server, &control_uri);
    
    return server;
}
```

---

## 云平台集成

### AWS IoT Core

```c
#include "aws_iot_mqtt_client.h"

void aws_iot_connect(const char *endpoint, const char *thing_name) {
    IoT_Client_Init_Params init_params = {
        .pHostURL = endpoint,
        .port = 8883,
        .pRootCALocation = "/cert/root-ca.pem",
        .pDeviceCertLocation = "/cert/cert.pem",
        .pDevicePrivateKeyLocation = "/cert/key.pem",
    };
    
    aws_iot_mqtt_init(&client, &init_params);
    aws_iot_mqtt_connect(&client, &connect_params);
}
```

### MQTT消息发布

```c
void publish_sensor_data(float temperature, float humidity) {
    char payload[128];
    snprintf(payload, sizeof(payload), 
             "{\"temperature\":%.1f,\"humidity\":%.1f}", 
             temperature, humidity);
    
    IoT_Publish_Message_Params params = {
        .qos = 1,
        .payload = payload,
        .payloadlen = strlen(payload),
    };
    aws_iot_mqtt_publish(&client, "device/sensors", payload, strlen(payload), 1, NULL);
}
```

---

## 远程日志采集

### 日志上报服务

```c
void log_upload_task(void *arg) {
    while (1) {
        char *log_data = get_log_buffer();
        
        esp_http_client_config_t config = {
            .url = "https://log-server/api/logs",
            .method = HTTP_METHOD_POST,
        };
        
        esp_http_client_handle_t client = esp_http_client_init(&config);
        esp_http_client_set_post_field(client, log_data, strlen(log_data));
        esp_http_client_perform(client);
        esp_http_client_cleanup(client);
        
        vTaskDelay(60000);  // 每分钟上报一次
    }
}
```

---

## 安全访问规范

### Token认证

```c
typedef struct {
    char token[32];
    uint32_t expiry;
} auth_token_t;

bool validate_token(const char *token) {
    auth_token_t stored_token;
    nvs_get_token(&stored_token);
    
    if (strcmp(token, stored_token.token) != 0) {
        return false;
    }
    
    if (time(NULL) > stored_token.expiry) {
        return false;
    }
    
    return true;
}
```

### API安全中间件

```c
esp_err_t auth_middleware(httpd_req_t *req) {
    char token[32];
    if (httpd_req_get_hdr_value_str(req, "Authorization", token, sizeof(token)) != ESP_OK) {
        httpd_resp_send_err(req, HTTPD_401_UNAUTHORIZED, "Missing token");
        return ESP_FAIL;
    }
    
    if (!validate_token(token)) {
        httpd_resp_send_err(req, HTTPD_401_UNAUTHORIZED, "Invalid token");
        return ESP_FAIL;
    }
    
    return ESP_OK;
}
```

---

## 监控仪表板

### InfluxDB数据存储

```c
void influxdb_write(const char *measurement, float value) {
    char payload[128];
    snprintf(payload, sizeof(payload), "%s value=%.2f", measurement, value);
    
    esp_http_client_config_t config = {
        .url = "http://influxdb:8086/write?db=iot",
        .method = HTTP_METHOD_POST,
    };
    
    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_http_client_set_post_field(client, payload, strlen(payload));
    esp_http_client_perform(client);
    esp_http_client_cleanup(client);
}
```

---

## 远程工具对比

| 工具 | 协议 | 安全性 | 适用场景 |
|------|------|--------|----------|
| **OTA** | HTTPS | 高 | 固件升级 |
| **串口转发** | TCP | 低 | 调试日志 |
| **Web API** | HTTP/HTTPS | 中 | 设备控制 |
| **MQTT** | TCP/TLS | 中 | IoT消息 |
| **WebSocket** | WS/WSS | 中 | 实时通信 |

---
Version: 2.0
Updated: 2026-04-09