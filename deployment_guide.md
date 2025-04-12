# Solar Lead Generation System - Deployment Guide

## Overview

This guide provides instructions for deploying the Solar Lead Generation System in both development and production environments. Follow these steps to set up and configure the system for your organization.

## System Requirements

### Development Environment
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.10 or higher
- **Database**: SQLite (included)
- **Web Server**: Flask development server
- **Storage**: Minimum 1GB free disk space
- **Memory**: Minimum 4GB RAM

### Production Environment
- **Operating System**: Linux (Ubuntu 20.04 LTS or higher recommended)
- **Python**: 3.10 or higher
- **Database**: PostgreSQL 13 or higher
- **Web Server**: Nginx + Gunicorn
- **Storage**: Minimum 10GB free disk space (scales with data volume)
- **Memory**: Minimum 8GB RAM
- **CPU**: 2+ cores recommended

## Development Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/your-organization/solar-leads-project.git
cd solar-leads-project
```

### 2. Set Up Python Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory:

```
# Database Configuration
DATABASE_URL=sqlite:///solar_leads.db

# API Keys
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
SKIP_TRACE_API_KEY=your_skip_trace_api_key
PROPERTY_DATA_API_KEY=your_property_data_api_key

# Application Settings
DEBUG=True
SECRET_KEY=your_secret_key
LOG_LEVEL=DEBUG
```

### 4. Initialize the Database

```bash
# Create database tables
python -m src.database create_tables

# Generate sample data (optional)
python -m src.test_data_generator
```

### 5. Start the Development Server

```bash
python -m src.main
```

The application will be available at http://localhost:5000

## Production Deployment

### 1. Prepare the Server

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib
```

### 2. Create Database

```bash
# Create PostgreSQL user and database
sudo -u postgres psql -c "CREATE USER solar_leads WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "CREATE DATABASE solar_leads_db OWNER solar_leads;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE solar_leads_db TO solar_leads;"
```

### 3. Clone and Configure the Application

```bash
# Clone the repository
git clone https://github.com/your-organization/solar-leads-project.git /opt/solar-leads
cd /opt/solar-leads

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory:

```
# Database Configuration
DATABASE_URL=postgresql://solar_leads:your_secure_password@localhost/solar_leads_db

# API Keys
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
SKIP_TRACE_API_KEY=your_skip_trace_api_key
PROPERTY_DATA_API_KEY=your_property_data_api_key

# Application Settings
DEBUG=False
SECRET_KEY=your_production_secret_key
LOG_LEVEL=INFO
```

### 5. Initialize the Database

```bash
# Create database tables
python -m src.database create_tables
```

### 6. Configure Gunicorn

Create a systemd service file at `/etc/systemd/system/solar-leads.service`:

```
[Unit]
Description=Solar Lead Generation System
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/solar-leads
Environment="PATH=/opt/solar-leads/venv/bin"
EnvironmentFile=/opt/solar-leads/.env
ExecStart=/opt/solar-leads/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 src.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable solar-leads
sudo systemctl start solar-leads
```

### 7. Configure Nginx

Create an Nginx configuration file at `/etc/nginx/sites-available/solar-leads`:

```
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/solar-leads/src/web;
        expires 30d;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/solar-leads /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 8. Set Up SSL (Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain and configure SSL certificate
sudo certbot --nginx -d your-domain.com
```

## Docker Deployment

### 1. Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher

### 2. Create Docker Compose File

Create a `docker-compose.yml` file in the project root:

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=solar_leads
      - POSTGRES_PASSWORD=your_secure_password
      - POSTGRES_DB=solar_leads_db
    restart: always

  web:
    build: .
    restart: always
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://solar_leads:your_secure_password@db/solar_leads_db
      - GOOGLE_MAPS_API_KEY=your_google_maps_api_key
      - SKIP_TRACE_API_KEY=your_skip_trace_api_key
      - PROPERTY_DATA_API_KEY=your_property_data_api_key
      - DEBUG=False
      - SECRET_KEY=your_production_secret_key
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./src/web:/usr/share/nginx/html/static
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
```

### 3. Create Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

COPY . .

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "src.main:app"]
```

### 4. Create Nginx Configuration

Create a `nginx.conf` file in the project root:

```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /usr/share/nginx/html/static;
        expires 30d;
    }
}
```

### 5. Build and Start the Containers

```bash
docker-compose up -d
```

### 6. Initialize the Database

```bash
docker-compose exec web python -m src.database create_tables
```

## Cloud Deployment (AWS)

### 1. Set Up AWS Resources

- Create an EC2 instance (t3.medium or larger recommended)
- Set up an RDS PostgreSQL database
- Configure a security group allowing traffic on ports 22, 80, and 443
- Allocate an Elastic IP and associate it with the EC2 instance

### 2. Deploy the Application

Follow the Production Deployment steps above, with these modifications:

- Use the RDS endpoint in your DATABASE_URL
- Configure the security group to allow traffic from the EC2 instance to the RDS database

### 3. Set Up Load Balancing (Optional)

For high-availability deployments:

1. Create an AMI from your configured EC2 instance
2. Set up an Auto Scaling Group using the AMI
3. Configure an Application Load Balancer
4. Update your DNS records to point to the load balancer

## Maintenance and Updates

### Backup Strategy

1. **Database Backups**:
   - For SQLite: `sqlite3 solar_leads.db .dump > backup.sql`
   - For PostgreSQL: `pg_dump -U solar_leads solar_leads_db > backup.sql`

2. **Automated Backups**:
   - Set up a cron job to run daily backups
   - Rotate backups to maintain the last 7 daily, 4 weekly, and 12 monthly backups

### Updating the Application

```bash
# Pull the latest changes
git pull

# Activate the virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Apply database migrations (if any)
python -m src.database migrate

# Restart the application
sudo systemctl restart solar-leads
```

### Monitoring

1. **Log Monitoring**:
   - Application logs: `/var/log/solar-leads/app.log`
   - Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
   - System logs: `journalctl -u solar-leads`

2. **Performance Monitoring**:
   - Set up Prometheus and Grafana for comprehensive monitoring
   - Monitor CPU, memory, disk usage, and database performance

## Troubleshooting

### Common Issues

1. **Application Won't Start**:
   - Check the application logs: `journalctl -u solar-leads`
   - Verify environment variables are correctly set
   - Ensure the database is accessible

2. **Database Connection Issues**:
   - Verify database credentials
   - Check network connectivity to the database server
   - Ensure the database service is running

3. **Web Interface Not Accessible**:
   - Check Nginx configuration
   - Verify Nginx is running: `systemctl status nginx`
   - Check firewall settings: `sudo ufw status`

4. **Slow Performance**:
   - Check database query performance
   - Monitor system resources for bottlenecks
   - Consider scaling up resources if consistently at high utilization

## Security Considerations

1. **API Keys**:
   - Store API keys securely in environment variables
   - Rotate keys periodically
   - Use different keys for development and production

2. **Database Security**:
   - Use strong passwords
   - Limit database access to the application server
   - Enable SSL for database connections

3. **Web Security**:
   - Always use HTTPS in production
   - Implement proper authentication and authorization
   - Keep all software components updated

## Scaling Considerations

1. **Vertical Scaling**:
   - Increase resources (CPU, memory) on the application server
   - Upgrade the database instance

2. **Horizontal Scaling**:
   - Deploy multiple application servers behind a load balancer
   - Implement database read replicas
   - Use a distributed cache like Redis

## Support and Resources

- **Documentation**: Refer to the user guide and API reference
- **Source Code**: Available in the repository
- **Issue Tracking**: Report issues through the project's issue tracker
- **Contact**: Reach out to the development team at support@example.com
