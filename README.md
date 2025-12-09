# Odoo 18 Community Docker Image

[![Docker Build](https://github.com/itdwgmbh/odoo-18-community/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/itdwgmbh/odoo-18-community/actions/workflows/docker-publish.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Optimized Odoo 18 Community Docker image with dynamic configuration, multi-architecture support, and production-ready features.

## Features

- **Odoo 18** installed from official GitHub source
- **Python 3.13** on Debian Trixie (slim)
- **Multi-architecture** support (amd64/arm64)
- **Dynamic configuration** via environment variables
- **Production-ready** with WebSocket support
- **Built-in health checks** for reliable deployments
- **Security scanning** with Trivy vulnerability detection
- **Automated builds** with retention policy (last 3 versions)

## Quick Start

```bash
# Pull the image
docker pull ghcr.io/itdwgmbh/odoo-18-community:latest

# Clone for examples
git clone https://github.com/itdwgmbh/odoo-18-community.git
cd odoo-18-community/examples

# Configure environment
cp .env.example .env
# Edit .env to set your passwords

# Start services
docker compose up -d

# Access services
# Odoo: http://odoo.localhost
# Mail: http://mail.localhost
```

## Basic Usage

### Docker Run
```bash
docker run -d \
  --name odoo18 \
  -p 8069:8069 \
  -e DB_HOST=your-postgres-host \
  -e DB_PASSWORD=your-password \
  -e ODOO_MASTER_PASSWORD=admin-password \
  ghcr.io/itdwgmbh/odoo-18-community:latest
```

### Docker Compose
See `examples/docker-compose.yaml` for a complete setup with:
- Nginx reverse proxy with WebSocket support
- PostgreSQL 17 database
- MailDev for email testing

## Available Tags

- `latest` - Latest stable build
- `YYYY-MM` - Monthly releases (e.g., `2025-01`)
- `YYYYMMDDHHMMSS` - Timestamp-based tags
- `sha-XXXXXXX` - Git commit SHA

## Documentation

For detailed documentation, visit our [GitHub Wiki](https://github.com/itdwgmbh/odoo-18-community/wiki):

- [Environment Variables](https://github.com/itdwgmbh/odoo-18-community/wiki/Environment-Variables)
- [Development Guide](https://github.com/itdwgmbh/odoo-18-community/wiki/Development-Guide)
- [Production Deployment](https://github.com/itdwgmbh/odoo-18-community/wiki/Production-Deployment)
- [Troubleshooting](https://github.com/itdwgmbh/odoo-18-community/wiki/Troubleshooting)

## License

This Docker image setup is licensed under the MIT License. See [LICENSE](LICENSE) file.

Note: Odoo Community Edition itself is licensed under LGPL-3.0.

## Support

- **Issues**: [GitHub Issues](https://github.com/itdwgmbh/odoo-18-community/issues)
- **Odoo Documentation**: [Official Docs](https://www.odoo.com/documentation/18.0/)

---

Built with ❤️ by IT-DW GmbH