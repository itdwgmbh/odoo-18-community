# Odoo 18 Community Docker Image

```bash
docker pull ghcr.io/itdwgmbh/odoo-18-community:latest
```

## Usage

```bash
docker run -d \
  -p 8069:8069 \
  -e DB_HOST=your-postgres-host \
  -e DB_PASSWORD=your-password \
  ghcr.io/itdwgmbh/odoo-18-community:latest
```

See `examples/` for Docker Compose setup.

## Tags

- `latest`
- `18.0.YYYYMMDD` (Odoo nightly version)

## Documentation

See [wiki](https://github.com/itdwgmbh/odoo-18-community/wiki) for configuration options.
