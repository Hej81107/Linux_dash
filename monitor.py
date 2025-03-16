from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = {
        'cpu_usage': psutil.cpu_percent(interval=1),  # CPU Load
        'memory_usage': psutil.virtual_memory().percent,  # Memory Usage
        'disk_usage': psutil.disk_usage('/').percent,  # Disk Usage
        'io_counters': psutil.disk_io_counters().write_bytes + psutil.disk_io_counters().read_bytes,  # Disk I/O
        'network_io': psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,  # Network Traffic
    }
    return jsonify(metrics)

if __name__ == '__main__':
    print(f"Running on http://34.136.205.1:3939/metrics")
    app.run(host='0.0.0.0', port=3939, debug=True)
