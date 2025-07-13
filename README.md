# Odoo 18 Community Docker Image

[![Docker Build](https://github.com/itdwgmbh/odoo-18-community/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/itdwgmbh/odoo-18-community/actions/workflows/docker-publish.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Optimized Odoo 18 Community Docker image with dynamic configuration, multi-architecture support, and production-ready features.

## Features

- **Odoo 18** installed from official GitHub source
- **Optimized multi-stage Docker build** for smaller image size
- **Dynamic configuration** via environment variables
- **PostgreSQL 17 client** for better compatibility
- **Health check** endpoint included
- **Support for custom addons** with multiple addon paths
- **Automatic database initialization**
- **Master password configuration** via environment variable

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Using the pre-built image from GitHub Container Registry
docker pull ghcr.io/itdwgmbh/odoo-18-community:latest

# Clone the repository
git clone https://github.com/itdwgmbh/odoo-18-community.git
cd odoo-18-community/examples

# Copy environment template
cp .env.example .env
# Edit .env to set your passwords

# Start the containers
docker compose up -d

# View logs
docker compose logs -f

# Access Odoo at http://odoo.localhost
# Access MailDev at http://mail.localhost
```

### Using Docker directly

```bash
# Pull the image from GitHub Container Registry
docker pull ghcr.io/itdwgmbh/odoo-18-community:latest

# Run with PostgreSQL
docker run -d \
  --name odoo18 \
  -p 8069:8069 \
  -e DB_HOST=your-db-host \
  -e DB_USER=odoo \
  -e DB_PASSWORD=odoo \
  -e ODOO_MASTER_PASSWORD=admin123 \
  -v odoo-data:/var/lib/odoo \
  -v ./addons:/mnt/extra-addons \
  ghcr.io/itdwgmbh/odoo-18-community:latest
```

### Available Tags

- `latest` - Latest stable build from main branch
- `YYYY-MM` - Monthly releases (e.g., `2025-01`)
- `YYYYMMDDHHMMSS` - Timestamp-based tags for specific builds
- `sha-XXXXXXX` - Git commit SHA for reproducible builds

## Repository Structure

```
odoo-18-community/
├── docker/                 # Docker image build files
│   ├── Dockerfile         # Multi-stage Dockerfile
│   ├── entrypoint.sh      # Container entrypoint script
│   ├── generate_odoo_conf.py  # Dynamic config generator
│   ├── wait-for-psql.py  # PostgreSQL readiness check
│   └── requirements.txt   # Python dependencies
├── examples/              # Usage examples
│   ├── docker-compose.yaml  # Full example with nginx, websockets, mail
│   ├── nginx.conf         # Nginx reverse proxy configuration
│   └── .env.example       # Environment template
├── .github/workflows/     # GitHub Actions
│   └── docker-publish.yml # Multi-arch build & publish
├── LICENSE               # MIT License
└── README.md            # This file
```

## Container Directory Structure

```
/opt/odoo/
├── src/                    # Odoo source code from GitHub
│   ├── addons/            # Core Odoo addons
│   └── odoo-bin           # Main executable
├── pip-packages/          # Python packages installed via pip
/opt/odoo-customer-addons/ # Customer-specific addons (volume)
/mnt/extra-addons/         # Additional addons (volume)
/etc/odoo/                 # Configuration files
├── odoo.conf             # Generated configuration
/var/lib/odoo/            # Data directory (filestore, sessions)
```

## Environment Variables

All Odoo configuration options can be set via environment variables. The configuration file is automatically generated at container startup.

### Database Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `db` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_USER` | `odoo` | PostgreSQL user |
| `DB_PASSWORD` | `odoo` | PostgreSQL password |
| `ODOO_DB_NAME` | - | Single database name (if set, disables database manager) |
| `ODOO_DB_TEMPLATE` | `template1` | Template database for new databases |
| `ODOO_DBFILTER` | `.*` | Database filter regex |
| `ODOO_DB_MAXCONN` | `32` | Maximum database connections |
| `ODOO_DB_SSLMODE` | `prefer` | PostgreSQL SSL mode |

### Security

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_MASTER_PASSWORD` | - | Master password for database operations |
| `ODOO_LIST_DB` | `True` | Show database list |

### Server Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_PROXY_MODE` | `True` | Enable proxy mode (X-Forwarded headers) |
| `ODOO_XMLRPC` | `True` | Enable XML-RPC |
| `ODOO_XMLRPC_PORT` | `8069` | XML-RPC port |
| `ODOO_GEVENT_PORT` | `8072` | Gevent/WebSocket port |

### Performance

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_WORKERS` | `4` | Number of worker processes |
| `ODOO_MAX_CRON_THREADS` | `2` | Maximum cron threads |
| `ODOO_LIMIT_MEMORY_HARD` | `4294967296` | Hard memory limit (4GB) |
| `ODOO_LIMIT_MEMORY_SOFT` | `3221225472` | Soft memory limit (3GB) |
| `ODOO_LIMIT_REQUEST` | `8192` | Request limit per worker |
| `ODOO_LIMIT_TIME_CPU` | `600` | CPU time limit in seconds |
| `ODOO_LIMIT_TIME_REAL` | `1200` | Real time limit in seconds |
| `ODOO_LIMIT_TIME_REAL_CRON` | `3600` | Real time limit for cron |

### Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_LOG_LEVEL` | `info` | Log level (debug, info, warning, error, critical) |
| `ODOO_LOG_HANDLER` | `['werkzeug:CRITICAL','odoo:WARNING']` | Log handlers configuration |
| `ODOO_LOG_DB` | `False` | Enable database logging |
| `ODOO_LOG_DB_LEVEL` | `warning` | Database log level |

### Email

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_EMAIL_FROM` | - | Default email sender |
| `ODOO_SMTP_SERVER` | `localhost` | SMTP server |
| `ODOO_SMTP_PORT` | `25` | SMTP port |
| `ODOO_SMTP_SSL` | `False` | Use SSL for SMTP |
| `ODOO_SMTP_USER` | - | SMTP username |
| `ODOO_SMTP_PASSWORD` | - | SMTP password |

### Module Options

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_WITHOUT_DEMO` | `all` | Disable demo data |

### Paths

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_ADDONS_PATH` | `/opt/odoo/src/addons,`<br>`/mnt/extra-addons,`<br>`/opt/odoo-customer-addons` | Addon directories |
| `ODOO_DATA_DIR` | `/var/lib/odoo` | Data directory for filestore |

### Other

| Variable | Default | Description |
|----------|---------|-------------|
| `ODOO_UNACCENT` | `True` | Enable unaccent search (requires PostgreSQL unaccent extension) |
| `ODOO_CONFIG_DEBUG` | `False` | Print generated config for debugging |

## Volumes

| Volume | Purpose |
|--------|---------|
| `/etc/odoo/` | Configuration files |
| `/var/lib/odoo` | Odoo data files (filestore, sessions) |
| `/mnt/extra-addons` | Additional addons directory |
| `/opt/odoo-customer-addons` | Customer-specific addons |

## Ports

| Port | Purpose |
|------|---------|
| `8069` | HTTP/XML-RPC |
| `8072` | Gevent/WebSocket |

## Customization

### Adding Custom Addons

1. Place your addons in one of the addon directories:
   - `./addons` → mounted to `/mnt/extra-addons`
   - Customer addons → `/opt/odoo-customer-addons`

2. The addon paths are automatically included in the configuration

### Adding Python Dependencies

1. Edit `requirements.txt` to add new Python packages
2. Rebuild the image:
   ```bash
   docker compose build
   docker compose up -d
   ```

### Custom Configuration

For advanced configuration options, you can:

1. Use environment variables (recommended)
2. Mount a custom `odoo.conf` file to `/etc/odoo/odoo.conf`
3. Pass command-line arguments to the container

## Building from Source

```bash
# Clone the repository
git clone https://github.com/itdwgmbh/odoo-18-community.git
cd odoo-18-community

# Build the image locally
docker build -t odoo18-custom ./docker

# Or use docker compose to build
docker compose -f examples/docker compose.yaml build
```

## Development & Operations

### Working Directory
All commands below assume you're in the `examples/` directory:
```bash
cd odoo-18-community/examples
```

### Access Odoo Shell

```bash
# Interactive shell with database access
docker compose exec web odoo shell -d your-database

# Python shell without database
docker compose exec web odoo shell --no-database

# Execute Python code directly
docker compose exec web odoo shell -d your-database --no-http -c "print(self.env['res.users'].search_count([]))"
```

### Database Management

```bash
# Create a new database
docker compose exec web odoo -d new_db --init base

# List databases
docker compose exec db psql -U odoo -c "\l"

# Backup database
docker compose exec db pg_dump -U odoo your_database > backup.sql

# Restore database
docker compose exec -T db psql -U odoo -c "CREATE DATABASE restored_db;"
docker compose exec -T db psql -U odoo restored_db < backup.sql
```

### Module Management

```bash
# Update module list
docker compose exec web odoo -d your_db -u base --stop-after-init

# Install a module
docker compose exec web odoo -d your_db -i module_name --stop-after-init

# Update a module
docker compose exec web odoo -d your_db -u module_name --stop-after-init

# Update all modules
docker compose exec web odoo -d your_db -u all --stop-after-init

# Run tests for a module
docker compose exec web odoo -d test_db -i your_module --test-enable --stop-after-init
```

### Debugging & Logs

```bash
# Follow all logs
docker compose logs -f

# Follow specific service logs
docker compose logs -f web
docker compose logs -f nginx

# View last 100 lines
docker compose logs --tail=100 web

# Check generated configuration
docker compose exec web cat /etc/odoo/odoo.conf

# Debug configuration generation
docker compose exec web bash -c "ODOO_CONFIG_DEBUG=True python3 /usr/local/bin/generate_odoo_conf.py"

# Access container shell
docker compose exec web bash
docker compose exec db psql -U odoo
```

### Development Workflow

```bash
# Create a custom addons directory
mkdir -p addons/my_module

# Scaffold a new module
docker compose exec web odoo scaffold my_module /mnt/extra-addons/

# Restart Odoo to reload Python code
docker compose restart web

# Update module and restart
docker compose exec web odoo -d your_db -u my_module --stop-after-init && docker compose restart web
```

### Performance Monitoring

```bash
# Check container resources
docker stats

# View running processes in Odoo container
docker compose exec web ps aux

# Check database connections
docker compose exec db psql -U odoo -c "SELECT count(*) FROM pg_stat_activity;"

# View slow queries (requires pg_stat_statements extension)
docker compose exec db psql -U odoo -c "SELECT query, calls, total_time, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

## Example Configurations

### Basic configuration with external database

```bash
docker run -d \
  -e DB_HOST=postgres.example.com \
  -e DB_USER=myuser \
  -e DB_PASSWORD=mypassword \
  -e ODOO_MASTER_PASSWORD=admin123 \
  ghcr.io/itdwgmbh/odoo-18-community:latest
```

### Development configuration

```bash
docker run -d \
  -e ODOO_LOG_LEVEL=debug \
  -e ODOO_WORKERS=0 \
  -e ODOO_WITHOUT_DEMO=False \
  ghcr.io/itdwgmbh/odoo-18-community:latest
```

### Production configuration with email

```bash
docker run -d \
  -e ODOO_WORKERS=8 \
  -e ODOO_LIMIT_MEMORY_HARD=8589934592 \
  -e ODOO_SMTP_SERVER=smtp.gmail.com \
  -e ODOO_SMTP_PORT=587 \
  -e ODOO_SMTP_SSL=True \
  -e ODOO_EMAIL_FROM=noreply@example.com \
  ghcr.io/itdwgmbh/odoo-18-community:latest
```

## Production Deployment

### With Nginx Reverse Proxy

The `examples/` directory includes a complete nginx configuration with WebSocket support. See `examples/nginx.conf` for the full configuration.

Key features:
- Virtual hosts: `odoo.localhost` for Odoo, `mail.localhost` for MailDev
- WebSocket routing to gevent port (8072)
- Proper headers for proxy mode
- Static file caching
- Gzip compression

**Note**: Add these entries to your `/etc/hosts` file:
```
127.0.0.1 odoo.localhost
127.0.0.1 mail.localhost
```

### Performance Tuning

For production, adjust these environment variables based on your server capacity:

```yaml
environment:
  - ODOO_WORKERS=8              # 2 * CPU cores + 1
  - ODOO_LIMIT_MEMORY_HARD=8589934592  # 8GB
  - ODOO_LIMIT_MEMORY_SOFT=6442450944  # 6GB
  - ODOO_DB_MAXCONN=64
```

## Troubleshooting

### Container Won't Start

1. Check logs: `docker compose logs web`
2. Verify database connection: `docker compose exec web python3 /usr/local/bin/wait-for-psql.py`
3. Check generated configuration: `docker compose exec web cat /etc/odoo/odoo.conf`

### Database Connection Issues

```bash
# Test database connection
docker compose exec web psql -h $DB_HOST -U $DB_USER -d postgres -c "SELECT 1"
```

### Module Not Found

1. Verify addon path is correct
2. Check file permissions: `docker compose exec web ls -la /mnt/extra-addons`
3. Update module list in Odoo: Apps → Update Apps List

## Health Check

The container includes a health check endpoint:

```bash
curl http://localhost:8069/web/health
```

## Notes

- All environment variables are optional and have sensible defaults
- Database connection variables (`DB_*`) also support Docker link aliases
- The configuration is generated dynamically at container startup - no static `odoo.conf` needed
- For production deployments with real-time features, ensure your reverse proxy routes `/websocket` paths to the gevent port
- The examples setup includes everything needed for production: nginx, websockets, and email

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This Docker image setup is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

Note: Odoo Community Edition itself is licensed under LGPL-3.0. The Odoo source code and its license can be found at https://github.com/odoo/odoo.

## Support

For issues specific to this Docker setup, please open an issue on GitHub.
For Odoo-related questions, refer to the [official Odoo documentation](https://www.odoo.com/documentation/18.0/).

---

Built with ❤️ by IT-DW GmbH