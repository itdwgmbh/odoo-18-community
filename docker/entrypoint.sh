#!/bin/bash
set -e

# Database connection parameters with fallback values
: ${DB_HOST:=${DB_PORT_5432_TCP_ADDR:='db'}}
: ${DB_PORT:=${DB_PORT_5432_TCP_PORT:=5432}}
: ${DB_USER:=${DB_ENV_POSTGRES_USER:=${POSTGRES_USER:='odoo'}}}
: ${DB_PASSWORD:=${DB_ENV_POSTGRES_PASSWORD:=${POSTGRES_PASSWORD:='odoo'}}}
: ${ODOO_MASTER_PASSWORD:=''}

# Initial setup when running as root
if [ "$(id -u)" = "0" ]; then
    # Generate configuration from environment variables
    echo "Generating odoo.conf from environment variables..."
    python3 /usr/local/bin/generate_odoo_conf.py "$ODOO_RC"
    
    # Ensure odoo user owns required directories
    chown odoo /etc/odoo/odoo.conf
    chown -R odoo /mnt/extra-addons /var/lib/odoo /opt/odoo-customer-addons /tmp

    # Create PostgreSQL authentication file
    echo "${DB_HOST}:${DB_PORT}:*:${DB_USER}:${DB_PASSWORD}" > /root/.pgpass
    chmod 600 /root/.pgpass

    # Re-execute as odoo user
    exec gosu odoo "$0" "$@"
fi

# Handle password file if provided
if [ -v PASSWORD_FILE ]; then
    PASSWORD="$(< $PASSWORD_FILE)"
fi

# Build database connection arguments, preferring config file values
DB_ARGS=()
function check_config() {
    param="$1"
    value="$2"
    if grep -q -E "^\s*\b${param}\b\s*=" "$ODOO_RC" ; then       
        value=$(grep -E "^\s*\b${param}\b\s*=" "$ODOO_RC" |cut -d " " -f3|sed 's/["\n\r]//g')
    fi;
    DB_ARGS+=("--${param}")
    DB_ARGS+=("${value}")
}
check_config "db_host" "$DB_HOST"
check_config "db_port" "$DB_PORT"
check_config "db_user" "$DB_USER"
check_config "db_password" "$DB_PASSWORD"

# Add database name if specified in configuration
DB_NAME=""
if grep -q -E "^\s*\bdatabase\b\s*=" "$ODOO_RC"; then
    DB_NAME=$(grep -E "^\s*\bdatabase\b\s*=" "$ODOO_RC" | cut -d " " -f3 | sed 's/["\n\r]//g')
    DB_ARGS+=("--database")
    DB_ARGS+=("${DB_NAME}")
fi

# Handle different command invocation patterns
case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]] ; then
            # Scaffold command doesn't need database connection
            exec python3 /opt/odoo/src/odoo-bin "$@"
        else
            # Wait for PostgreSQL to be ready
            python3 /usr/local/bin/wait-for-psql.py ${DB_ARGS[@]} --timeout=60
            # Start Odoo with database arguments
            exec python3 /opt/odoo/src/odoo-bin "$@" "${DB_ARGS[@]}"
        fi
        ;;
    -*)
        # Direct option flags - wait for database and start Odoo
        python3 /usr/local/bin/wait-for-psql.py ${DB_ARGS[@]} --timeout=60
        exec python3 /opt/odoo/src/odoo-bin "$@" "${DB_ARGS[@]}"
        ;;
    *)
        # Pass through any other command
        exec "$@"
esac

exit 1
