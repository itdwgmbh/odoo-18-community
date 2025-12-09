#!/usr/bin/env python3
"""
Generate odoo.conf file from environment variables.
Configuration options use the pattern: ODOO_<KEY>
"""

import os
import sys
from configparser import ConfigParser

# Default configuration for containerized Odoo
ODOO_CONFIG = {
    'options': {
        # Database connection
        'db_host': os.environ.get('DB_HOST', os.environ.get('DB_PORT_5432_TCP_ADDR', 'db')),
        'db_port': os.environ.get('DB_PORT', os.environ.get('DB_PORT_5432_TCP_PORT', '5432')),
        'db_user': os.environ.get('DB_USER', os.environ.get('DB_ENV_POSTGRES_USER', os.environ.get('POSTGRES_USER', 'odoo'))),
        'db_password': os.environ.get('DB_PASSWORD', os.environ.get('DB_ENV_POSTGRES_PASSWORD', os.environ.get('POSTGRES_PASSWORD', 'odoo'))),
        'db_name': os.environ.get('ODOO_DB_NAME', ''),
        'db_template': os.environ.get('ODOO_DB_TEMPLATE', 'template1'),
        'dbfilter': os.environ.get('ODOO_DBFILTER', '.*'),
        'db_maxconn': os.environ.get('ODOO_DB_MAXCONN', '32'),
        'db_sslmode': os.environ.get('ODOO_DB_SSLMODE', 'prefer'),
        
        # Master password
        'admin_passwd': os.environ.get('ODOO_MASTER_PASSWORD', os.environ.get('ODOO_ADMIN_PASSWD', '')),
        
        # Module and data paths
        'addons_path': os.environ.get('ODOO_ADDONS_PATH', '/opt/odoo/src/addons,/mnt/extra-addons,/opt/odoo-customer-addons'),
        'data_dir': os.environ.get('ODOO_DATA_DIR', '/var/lib/odoo'),
        
        # Server configuration
        'proxy_mode': os.environ.get('ODOO_PROXY_MODE', 'True'),
        
        # Worker processes
        'workers': os.environ.get('ODOO_WORKERS', '4'),
        'max_cron_threads': os.environ.get('ODOO_MAX_CRON_THREADS', '2'),
        
        # Memory limits
        'limit_memory_hard': os.environ.get('ODOO_LIMIT_MEMORY_HARD', '4294967296'),  # 4GB
        'limit_memory_soft': os.environ.get('ODOO_LIMIT_MEMORY_SOFT', '3221225472'),  # 3GB
        'limit_request': os.environ.get('ODOO_LIMIT_REQUEST', '8192'),
        
        # Request timeouts
        'limit_time_cpu': os.environ.get('ODOO_LIMIT_TIME_CPU', '600'),
        'limit_time_real': os.environ.get('ODOO_LIMIT_TIME_REAL', '1200'),
        'limit_time_real_cron': os.environ.get('ODOO_LIMIT_TIME_REAL_CRON', '3600'),
        
        # Logging
        'log_handler': os.environ.get('ODOO_LOG_HANDLER', "['werkzeug:CRITICAL','odoo:WARNING']"),
        'log_level': os.environ.get('ODOO_LOG_LEVEL', 'info'),
        'log_db': os.environ.get('ODOO_LOG_DB', 'False'),
        'log_db_level': os.environ.get('ODOO_LOG_DB_LEVEL', 'warning'),
        
        # Email configuration
        'email_from': os.environ.get('ODOO_EMAIL_FROM', 'no-reply@example.org'),
        'smtp_server': os.environ.get('ODOO_SMTP_SERVER', 'mail'),
        'smtp_port': os.environ.get('ODOO_SMTP_PORT', '1025'),
        'smtp_ssl': os.environ.get('ODOO_SMTP_SSL', 'False'),
        'smtp_user': os.environ.get('ODOO_SMTP_USER', ''),
        'smtp_password': os.environ.get('ODOO_SMTP_PASSWORD', ''),
        
        # Security
        'list_db': os.environ.get('ODOO_LIST_DB', 'True'),
        
        # Performance
        'unaccent': os.environ.get('ODOO_UNACCENT', 'True'),
        'without_demo': os.environ.get('ODOO_WITHOUT_DEMO', 'all'),
        
        # Network ports
        'xmlrpc': os.environ.get('ODOO_XMLRPC', 'True'),
        'xmlrpc_port': os.environ.get('ODOO_XMLRPC_PORT', '8069'),
        'gevent_port': os.environ.get('ODOO_GEVENT_PORT', '8072'),
    }
}

def should_include_option(key, value):
    """Check if option should be written to config."""
    # Required database parameters
    if key in ['db_host', 'db_port', 'db_user', 'db_password']:
        return True
    
    # Skip empty or false values
    if value is False or value == 'False' or value == '':
        return False
    
    return True

def generate_config(output_path='/etc/odoo/odoo.conf'):
    """Generate odoo.conf from environment variables."""
    config = ConfigParser()
    
    # Build configuration from defaults and environment
    for section, options in ODOO_CONFIG.items():
        config.add_section(section)
        
        for key, default_value in options.items():
            # Environment variable overrides default
            env_key = f'ODOO_{key.upper()}'
            value = os.environ.get(env_key, default_value)
            
            if should_include_option(key, value):
                # Preserve list format for specific keys
                if key in ['log_handler', 'demo', 'translate_modules'] and value.startswith('['):
                    config.set(section, key, value)
                elif value not in [False, 'False', '']:
                    config.set(section, key, str(value))
    
    # Process additional ODOO_ environment variables
    for env_var, env_value in os.environ.items():
        if env_var.startswith('ODOO_') and env_var not in ['ODOO_MASTER_PASSWORD']:
            parts = env_var[5:].lower().split('_', 1)
            if len(parts) == 2 and parts[0] in config.sections():
                # Section-specific variable
                section, key = parts
                if key not in config[section]:
                    config.set(section, key, env_value)
            elif len(parts) >= 1:
                # Default to options section
                key = '_'.join(parts)
                if key not in config['options']:
                    config.set('options', key, env_value)
    
    # Write configuration to file
    try:
        with open(output_path, 'w') as configfile:
            config.write(configfile)
        print(f"Successfully generated {output_path}")
        
        # Debug mode output (with sensitive values masked)
        if os.environ.get('ODOO_CONFIG_DEBUG', 'False').lower() in ('true', '1', 'yes'):
            print("\nGenerated configuration (sensitive values masked):")
            sensitive_keys = ['password', 'passwd', 'secret', 'token', 'key']
            with open(output_path, 'r') as f:
                for line in f:
                    # Mask lines containing sensitive keys
                    if any(key in line.lower() for key in sensitive_keys) and '=' in line:
                        key_part = line.split('=')[0]
                        print(f"{key_part}= ********")
                    else:
                        print(line, end='')
                
    except Exception as e:
        print(f"Error generating config file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # Use provided path or default
    output_path = sys.argv[1] if len(sys.argv) > 1 else '/etc/odoo/odoo.conf'
    generate_config(output_path)