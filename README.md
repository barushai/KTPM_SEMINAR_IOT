# Demo So Sánh Kiến Trúc IoT

## Tổng quan

Dự án này trình bày sự khác biệt về kiến trúc giữa mô hình **Yêu cầu – Phản hồi (Request–Response)** truyền thống (**HTTP**) và kiến trúc **Hướng sự kiện (Event-Driven)** dành cho **IoT (MQTT)**.

Mục tiêu của thử nghiệm là so sánh đặc tính hiệu suất của hai phương pháp này khi xử lý dữ liệu đo lường (**telemetry**) từ nhiều cảm biến.

Hệ thống mô phỏng nhiều thiết bị IoT gửi dữ liệu và đo lường các chỉ số kiến trúc then chốt như:

- **Latency (Độ trễ)**
- **Throughput (Thông lượng)**
- **Message Volume (Số lượng tin nhắn)**

Kết quả được trực quan hóa thông qua một **dashboard thời gian thực**.

---

# Tổng quan về Kiến trúc

Thử nghiệm so sánh hai mô hình hệ thống sau:

---

# 1. Kiến trúc Truyền thống (HTTP Request–Response)

Trong mô hình này, mỗi cảm biến gửi dữ liệu trực tiếp đến máy chủ bằng các yêu cầu **HTTP POST**.

## Luồng dữ liệu

```
Sensor → HTTP POST → HTTP Server → Processing → Metrics
```

## Đặc điểm

- Giao tiếp **không trạng thái (Stateless)**
- Mỗi tin nhắn yêu cầu một chu kỳ **request–response đầy đủ**
- **Protocol overhead cao hơn**
- Không tối ưu cho hệ thống có **hàng nghìn thiết bị IoT**

---

# 2. Kiến trúc IoT (MQTT Event-Driven)

Trong mô hình này, các cảm biến **publish** tin nhắn tới một **MQTT Broker**. Các dịch vụ xử lý sẽ **subscribe** vào các **topics** liên quan.

## Luồng dữ liệu

```
Sensor → MQTT Publish → MQTT Broker → Processing Service → Metrics
```

## Đặc điểm

- **Persistent connections**
- **Lightweight protocol**
- **Event-driven communication**
- **Scalable cho số lượng lớn thiết bị**

---

# Thành phần Hệ thống

| Thành phần | Mô tả |
|---|---|
| `sensor.py` | Trình mô phỏng cảm biến MQTT |
| `sensor_http.py` | Trình mô phỏng cảm biến HTTP |
| `server_http.py` | HTTP Server nhận dữ liệu cảm biến |
| `processor_iot.py` | Dịch vụ xử lý MQTT |
| `sensor_dashboard.py` | API cung cấp số liệu cho dashboard |
| `index.html` | Dashboard web trực quan hóa |

---

# Các Chỉ số Đo lường (Metrics)

## 1. Độ trễ (Latency)

Độ trễ đại diện cho **thời gian cần thiết để một tin nhắn từ cảm biến đến được hệ thống xử lý**.

### Công thức

```
Latency = Current_Time - Sensor_Timestamp
```

### Độ trễ trung bình

```
Average Latency = Σ(Latency) / N
```

Trong đó:

- **N** là số lượng tin nhắn đã xử lý.

---

## 2. Thông lượng (Throughput)

Thông lượng đại diện cho **số lượng tin nhắn mà hệ thống xử lý được trong một khoảng thời gian nhất định**.

### Công thức

```
Throughput = Total Messages / Time Interval
```

### Ví dụ

```
200 messages / 10 seconds = 20 messages/second
```

Thông lượng càng cao cho thấy **khả năng mở rộng của hệ thống càng tốt**.

---

# Dashboard

Dashboard hiển thị các chỉ số thực tế của thử nghiệm.

| Chỉ số | Mô tả |
|---|---|
| HTTP Latency | Độ trễ trung bình của kiến trúc HTTP |
| MQTT Latency | Độ trễ trung bình của kiến trúc MQTT |
| HTTP Messages | Tổng số tin nhắn HTTP đã xử lý |
| MQTT Messages | Tổng số tin nhắn MQTT đã xử lý |

---

# Cấu trúc Dự án

```
iot-demo
│
├── sensor.py           # Giả lập MQTT
├── sensor_http.py      # Giả lập HTTP
├── processor_iot.py    # Xử lý dữ liệu MQTT
├── server_http.py      # Server HTTP
├── sensor_dashboard.py # API Dashboard
├── index.html          # Giao diện dashboard
│
├── metrics.json        # Lưu trữ số liệu MQTT
└── metrics_http.json   # Lưu trữ số liệu HTTP
```

---

# Hướng dẫn Chạy Thử nghiệm

## 1. Cài đặt thư viện

```bash
pip install flask paho-mqtt requests
```

---

# 2. Các bước thực hiện

Mở **nhiều terminal riêng biệt**.

---

## Chạy HTTP Server

```bash
python server_http.py
```

Server chạy tại:

```
http://localhost:5000
```

---

## Chạy MQTT Processor

```bash
python processor_iot.py
```

---

## Chạy các cảm biến HTTP

```bash
python sensor_http.py 1
python sensor_http.py 2
```

---

## Chạy các cảm biến MQTT

```bash
python sensor.py 1
python sensor.py 2
```

---

## Khởi chạy Dashboard API

```bash
python sensor_dashboard.py
```

---

## Truy cập Dashboard

Mở trình duyệt tại:

```
http://localhost:8000
```

---

# Kết quả Ví dụ

| Chỉ số | HTTP | MQTT |
|---|---|---|
| Latency | 2.03 s | 0.66 s |
| Messages | 251 | 230 |

### Nhận xét

Kiến trúc **MQTT** thường đạt được:

- **Độ trễ thấp hơn**
- **Thông lượng cao hơn**
- **Khả năng mở rộng tốt hơn**

---

# Kết luận

Thử nghiệm chứng minh rằng kiến trúc **IoT hướng sự kiện (MQTT)** vượt trội so với mô hình **Request–Response (HTTP)** khi xử lý khối lượng lớn dữ liệu cảm biến.

Các yếu tố chính:

### 1. Persistent Connection

Giảm chi phí thiết lập kết nối lại cho mỗi yêu cầu.

### 2. Lightweight Protocol

Header nhỏ, giảm **network overhead**.

### 3. Pub/Sub Architecture

Tách biệt **producer** và **consumer**, giúp hệ thống **dễ mở rộng và linh hoạt hơn**.
