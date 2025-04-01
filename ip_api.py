from flask import Flask, request, jsonify
import socket
import time

app = Flask(__name__)

@app.route('/')
def get_ip_info():
    # Client-IP from X-Forwarded-For
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    # Reverse-DNS
    hostname = None
    if client_ip and client_ip not in ('(null)', '::1', '127.0.0.1'):
        try:
            hostname = socket.gethostbyaddr(client_ip)[0]
        except (socket.herror, socket.gaierror):
            pass
    
    return jsonify({
        'ip': client_ip,
        'hostname': hostname,
        'timestamp': int(time.time())
    })

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    
    app.run(
        host='::' if args.port == 7112 else '0.0.0.0',
        port=args.port
    )
