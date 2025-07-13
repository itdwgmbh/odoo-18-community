#!/opt/odoo/venv/bin/python
"""Wait for PostgreSQL database to become available."""
import argparse
import psycopg2
import sys
import time


if __name__ == '__main__':
    # Parse database connection arguments
    arg_parser = argparse.ArgumentParser(description='Wait for PostgreSQL to be ready')
    arg_parser.add_argument('--db_host', required=True, help='Database host')
    arg_parser.add_argument('--db_port', required=True, help='Database port')
    arg_parser.add_argument('--db_user', required=True, help='Database user')
    arg_parser.add_argument('--db_password', required=True, help='Database password')
    arg_parser.add_argument('--timeout', type=int, default=5, help='Connection timeout in seconds')

    args = arg_parser.parse_args()

    # Attempt connection with timeout
    start_time = time.time()
    error = None
    
    while (time.time() - start_time) < args.timeout:
        try:
            # Connect to PostgreSQL default database
            conn = psycopg2.connect(
                user=args.db_user,
                host=args.db_host,
                port=args.db_port,
                password=args.db_password,
                dbname='postgres'
            )
            conn.close()
            print("Database is ready!")
            sys.exit(0)
        except psycopg2.OperationalError as e:
            error = e
            time.sleep(1)
            print("Waiting for database connection...")
    
    # Timeout reached
    print(f"Database connection failure after {args.timeout}s: {error}", file=sys.stderr)
    sys.exit(1)
