<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architecture Dashboard</title>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen p-4 md:p-8">

    <div class="max-w-4xl mx-auto">
        
        <header class="mb-8 text-center">
            <h1 class="text-3xl font-bold text-slate-800 mb-2">Architecture Comparison Dashboard</h1>
            <p class="text-slate-500">Real-time latency metrics: HTTP vs MQTT</p>
        </header>

        <div class="bg-white rounded-xl shadow-md p-4 md:p-6 border border-slate-100">
            <h2 class="text-lg font-semibold mb-4 text-slate-700">Latency (ms)</h2>
            
            <div class="relative h-72 md:h-96 w-full">
                <canvas id="latencyChart"></canvas>
            </div>
            
            <div class="mt-4 flex items-center justify-end text-sm">
                <span class="flex items-center gap-2">
                    <span id="statusIndicator" class="w-3 h-3 rounded-full bg-gray-400"></span>
                    <span id="statusText" class="text-slate-500">Connecting...</span>
                </span>
            </div>
        </div>

    </div>

    <script>
        // Cấu hình UI cho biểu đồ
        const ctx = document.getElementById('latencyChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Current Latency'],
                datasets: [
                    {
                        label: 'HTTP',
                        data: [0],
                        backgroundColor: 'rgba(59, 130, 246, 0.8)', // Màu xanh dương (Tailwind blue-500)
                        borderColor: 'rgb(37, 99, 235)',
                        borderWidth: 1,
                        borderRadius: 6, // Bo góc cột
                        barPercentage: 0.5 // Thu gọn bề ngang của cột
                    },
                    {
                        label: 'MQTT',
                        data: [0],
                        backgroundColor: 'rgba(16, 185, 129, 0.8)', // Màu xanh lá (Tailwind emerald-500)
                        borderColor: 'rgb(5, 150, 105)',
                        borderWidth: 1,
                        borderRadius: 6,
                        barPercentage: 0.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Bắt buộc false để thẻ div cha kiểm soát chiều cao
                animation: {
                    duration: 400 // Giảm thời gian animation để update mỗi giây nhìn mượt hơn, không bị giật
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Milliseconds (ms)'
                        },
                        grid: {
                            color: '#f1f5f9' // Màu lưới nhạt hơn
                        }
                    },
                    x: {
                        grid: {
                            display: false // Ẩn lưới trục X cho gọn
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true, // Chuyển icon chú thích thành hình tròn
                            padding: 20
                        }
                    }
                }
            }
        });

        // DOM Elements cho trạng thái kết nối
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');

        // Hàm lấy dữ liệu
        async function loadMetrics() {
            try {
                let res = await fetch("http://localhost:8000/metrics");
                
                if (!res.ok) throw new Error("Network response was not ok");
                
                let data = await res.json();

                // Cập nhật dữ liệu biểu đồ
                chart.data.datasets[0].data = [data.http.http_latency];
                chart.data.datasets[1].data = [data.mqtt.mqtt_latency];
                chart.update();

                // Cập nhật UI trạng thái: Xanh (Online)
                statusIndicator.classList.replace('bg-gray-400', 'bg-green-500');
                statusIndicator.classList.replace('bg-red-500', 'bg-green-500');
                statusText.innerText = "Live / Connected";

            } catch (error) {
                console.error("Error fetching metrics:", error);
                
                // Cập nhật UI trạng thái: Đỏ (Offline/Lỗi)
                statusIndicator.classList.replace('bg-gray-400', 'bg-red-500');
                statusIndicator.classList.replace('bg-green-500', 'bg-red-500');
                statusText.innerText = "Connection lost";
            }
        }

        // Gọi ngay lần đầu tiên để không phải chờ 1 giây
        loadMetrics();

        // Lặp lại mỗi giây
        setInterval(loadMetrics, 1000);
    </script>
</body>
</html>