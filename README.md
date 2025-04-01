# 🌐 Self-Hosted IP API

A lightweight API that returns the client IP, hostname (reverse DNS), and Unix timestamp. Supports **IPv4/IPv6** via separate endpoints with a reverse proxy.

## 📜 Response Example

```json
{
  "hostname": "dns9.quad9.net",
  "ip": "9.9.9.9",
  "timestamp": 1743250659
}
```

## 🚀 Quick Start

### 📥 Clone & Setup

```bash
git clone https://github.com/xFanexx/ip-api.git
cd ip-api
python -m venv venv
source venv/bin/activate  # Linux/macOS
# On Windows use: venv\Scripts\activate
pip install flask
```

### ⚙️ Systemd Service Configuration

Create systemd service files for both IPv4 and IPv6:

#### IPv4 Service

```bash
sudo nano /etc/systemd/system/ipv4-api.service
```

Paste the following configuration:

```ini
[Unit]
Description=IPv4 API Service
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/ip-api
Environment="PATH=/path/to/ip-api/venv/bin"
ExecStart=/path/to/ip-api/venv/bin/python ip_api.py --port 7111
Restart=always

[Install]
WantedBy=multi-user.target
```

#### IPv6 Service

Create a similar file for IPv6 but change the port to **7112**:

```bash
sudo nano /etc/systemd/system/ipv6-api.service
```

Modify the port in the configuration:

```ini
[Unit]
Description=IPv6 API Service
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/ip-api
Environment="PATH=/path/to/ip-api/venv/bin"
ExecStart=/path/to/ip-api/venv/bin/python ip_api.py --port 7112
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Enable and Start the Services

```bash
sudo systemctl daemon-reload

# For IPv4
sudo systemctl enable ipv4-api
sudo systemctl start ipv4-api
sudo systemctl status ipv4-api

# For IPv6
sudo systemctl enable ipv6-api
sudo systemctl start ipv6-api
sudo systemctl status ipv6-api
```

## 🔧 Apache Configuration

### IPv4 Virtual Host

Create a virtual host configuration:

```bash
sudo nano /etc/apache2/sites-available/4.example.com.conf
```

Paste the following configuration:

```apache
<VirtualHost *:443>
    ServerName 4.example.com
    
    # Proxy configuration
    ProxyPass / http://127.0.0.1:7111/
    ProxyPassReverse / http://127.0.0.1:7111/
    
    # ⚠️ IMPORTANT: X-Forwarded-For header configuration
    # This ensures the client's real IP is passed to the API
    RequestHeader set X-Forwarded-For expr=%{REMOTE_ADDR}
    
    # ⚠️ IMPORTANT: CORS headers for external access
    # Required if you're building a "What's My IP" website
    Header always set Access-Control-Allow-Origin "https://example.com"
    Header always set Access-Control-Allow-Methods "GET"
    Header always set Access-Control-Allow-Headers "X-Requested-With"
    
    # SSL configuration
    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
</VirtualHost>
```

### IPv6 Virtual Host

Create a similar configuration for IPv6:

```bash
sudo nano /etc/apache2/sites-available/6.example.com.conf
```

Use the following configuration (note the IPv6 localhost address):

```apache
<VirtualHost *:443>
    ServerName 6.example.com
    
    # Proxy configuration with IPv6 localhost
    ProxyPass / http://[::1]:7112/
    ProxyPassReverse / http://[::1]:7112/
    
    # ⚠️ IMPORTANT: X-Forwarded-For header configuration
    # This ensures the client's real IP is passed to the API
    RequestHeader set X-Forwarded-For expr=%{REMOTE_ADDR}
    
    # ⚠️ IMPORTANT: CORS headers for external access
    # Required if you're building a "What's My IP" website
    Header always set Access-Control-Allow-Origin "https://example.com"
    Header always set Access-Control-Allow-Methods "GET"
    Header always set Access-Control-Allow-Headers "X-Requested-With"
    
    # SSL configuration
    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
</VirtualHost>
```

### Enable Apache Modules and Sites

```bash
# Enable required Apache modules
sudo a2enmod proxy proxy_http headers ssl

# Enable sites
sudo a2ensite 4.example.com.conf
sudo a2ensite 6.example.com.conf

# Apply changes
sudo systemctl reload apache2
```

## 📡 DNS Setup

Configure your DNS records:

- **A record:** `4.example.com` → Your server's IPv4 address
- **AAAA record:** `6.example.com` → Your server's IPv6 address

## ⚠️ Important Configuration Notes

### X-Forwarded-For Header

The `X-Forwarded-For` header is crucial for this API to work correctly behind a reverse proxy:

```apache
RequestHeader set X-Forwarded-For expr=%{REMOTE_ADDR}
```

This ensures the API receives the client's real IP address instead of the proxy's address (127.0.0.1).

### CORS Headers

If you're building a frontend website that needs to access this API, you must configure CORS headers:

```apache
Header always set Access-Control-Allow-Origin "https://example.com"
Header always set Access-Control-Allow-Methods "GET"
Header always set Access-Control-Allow-Headers "X-Requested-With"
```

Replace `https://example.com` with your frontend domain. For multiple domains, you can use:

```apache
# For multiple specific domains
Header always set Access-Control-Allow-Origin "https://example.com https://app.example.com"

# Or for any domain (not recommended for production)
# Header always set Access-Control-Allow-Origin "*"
```

## 🛠️ Troubleshooting

### Service Status

Check systemd logs:

```bash
# For IPv4 service
journalctl -u ipv4-api -f

# For IPv6 service
journalctl -u ipv6-api -f
```

### API Testing

Test API directly:

```bash
# Test IPv4 endpoint
curl -v http://localhost:7111

# Test IPv6 endpoint
curl -v http://localhost:7112
```

### Apache Configuration

Verify Apache configuration syntax:

```bash
sudo apachectl configtest
```

Check Apache error logs:

```bash
sudo tail -f /var/log/apache2/error.log
```

## 📝 Common Customizations

- Change the listening ports (7111/7112) if they conflict with other services
- Add rate limiting in Apache configuration to prevent abuse
- Implement additional security headers as needed

---

✅ Your IP API is now up and running! 🎉
