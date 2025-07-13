#!/bin/bash
set -e

# Set database connection parameters early for root access
: ${DB_HOST:=${DB_PORT_5432_TCP_ADDR:='db'}}
: ${DB_PORT:=${DB_PORT_5432_TCP_PORT:=5432}}
: ${DB_USER:=${DB_ENV_POSTGRES_USER:=${POSTGRES_USER:='odoo'}}}
: ${DB_PASSWORD:=${DB_ENV_POSTGRES_PASSWORD:=${POSTGRES_PASSWORD:='odoo'}}}
: ${UPDATE_BASE:='true'} # Simplified variable assignment, always true
: ${ODOO_MASTER_PASSWORD:=''} # Master password environment variable

# Run initial setup as root
if [ "$(id -u)" = "0" ]; then
    # Generate odoo.conf from environment variables
    echo "Generating odoo.conf from environment variables..."
    python3 /usr/local/bin/generate_odoo_conf.py "$ODOO_RC"
    
    # Set ownership for critical directories
    chown odoo /etc/odoo/odoo.conf
    chown -R odoo /mnt/extra-addons /var/lib/odoo /opt/odoo-customer-addons /tmp

    # Create secure .pgpass file for root
    echo "${DB_HOST}:${DB_PORT}:*:${DB_USER}:${DB_PASSWORD}" > /root/.pgpass
    chmod 600 /root/.pgpass

    # Switch to odoo user
    exec gosu odoo "$0" "$@"
fi

# Using system Python3 directly
# Rest of original script remains unchanged below
if [ -v PASSWORD_FILE ]; then
    PASSWORD="$(< $PASSWORD_FILE)"
fi

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

# Add database name check - this is critical for update to work
DB_NAME=""
if grep -q -E "^\s*\bdatabase\b\s*=" "$ODOO_RC"; then
    DB_NAME=$(grep -E "^\s*\bdatabase\b\s*=" "$ODOO_RC" | cut -d " " -f3 | sed 's/["\n\r]//g')
    DB_ARGS+=("--database")
    DB_ARGS+=("${DB_NAME}")
fi

case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]] ; then
            exec python3 /opt/odoo/src/odoo-bin "$@"
        else
            python3 /usr/local/bin/wait-for-psql.py ${DB_ARGS[@]} --timeout=60

            # Directly include -u base in the command
            exec python3 /opt/odoo/src/odoo-bin "$@" "${DB_ARGS[@]}"
        fi
        ;;
    -*)
        python3 /usr/local/bin/wait-for-psql.py ${DB_ARGS[@]} --timeout=60

        # Directly include -u base in the command
        exec python3 /opt/odoo/src/odoo-bin "$@" "${DB_ARGS[@]}"
        ;;
    *)
        exec "$@"
esac

exit 1
