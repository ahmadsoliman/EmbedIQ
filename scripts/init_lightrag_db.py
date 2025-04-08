#!/usr/bin/env python3
"""
Initialize LightRAG database in PostgreSQL.
This script creates the necessary PostgreSQL extensions and schemas for LightRAG.
"""

import os
import asyncio
import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

# Default connection parameters
DEFAULT_DB_HOST = "db"  # Change from localhost to db (Docker service name)
DEFAULT_DB_PORT = 5432
DEFAULT_DB_USER = "postgres"
DEFAULT_DB_PASSWORD = "postgres"
DEFAULT_DB_NAME = "embediq"
DEFAULT_GRAPH_NAME = "embediq"


async def setup_database(
    host=DEFAULT_DB_HOST,
    port=DEFAULT_DB_PORT,
    user=DEFAULT_DB_USER,
    password=DEFAULT_DB_PASSWORD,
    dbname=DEFAULT_DB_NAME,
    graph_name=DEFAULT_GRAPH_NAME,
):
    """Set up PostgreSQL for LightRAG with pgvector and Apache AGE."""
    print(f"Setting up PostgreSQL for LightRAG at {host}:{port}...")

    # Connect to PostgreSQL server
    max_retries = 2
    for retry in range(max_retries):
        try:
            # Add gssencmode='disable' to avoid GSSAPI authentication issues
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname="postgres",
                gssencmode="disable",
                sslmode="disable",
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            print("Successfully connected to PostgreSQL server.")
            break
        except Exception as e:
            if retry < max_retries - 1:
                print(f"Connection failed, retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Failed to connect to PostgreSQL: {e}")
                print("\nTroubleshooting tips:")
                print("1. Make sure the PostgreSQL container is running:")
                print("   docker ps | grep postgres")
                print(
                    "2. Check for the correct username/password in docker-compose.yml"
                )
                print(
                    "3. If running outside Docker, try using the service name 'db' instead of 'localhost'"
                )
                print("4. Try connecting directly with:")
                print(f"   psql -h {host} -p {port} -U {user} postgres")
                return False

    # Create database if it doesn't exist
    try:
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
        if cursor.fetchone() is None:
            print(f"Creating database '{dbname}'...")
            cursor.execute(f"CREATE DATABASE {dbname}")
        else:
            print(f"Database '{dbname}' already exists.")
    except Exception as e:
        print(f"Failed to create database: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

    # Connect to the created database
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            gssencmode="disable",
            sslmode="disable",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        print(f"Successfully connected to database '{dbname}'.")
    except Exception as e:
        print(f"Failed to connect to database {dbname}: {e}")
        return False

    # Create extensions if they don't exist
    try:
        # # pgvector for vector embeddings
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        print("Created pgvector extension.")

        # Apache AGE for graph database
        cursor.execute("CREATE EXTENSION IF NOT EXISTS age")
        print("Created Apache AGE extension.")

        # Load AGE
        cursor.execute("LOAD 'age'")
        print("Loaded Apache AGE extension.")

        # Set search path
        cursor.execute('SET search_path = ag_catalog, "$user", public')

        # Check if graph exists
        cursor.execute(f"SELECT * FROM ag_catalog.ag_graph WHERE name = '{graph_name}'")
        if cursor.fetchone() is None:
            # Create graph
            cursor.execute(f"SELECT create_graph('{graph_name}')")
            print(f"Created graph '{graph_name}'.")
        else:
            print(f"Graph '{graph_name}' already exists.")

        print(
            "\nPostgreSQL setup complete! Now you can run LightRAG with PostgreSQL storage."
        )
        print("\nTo create indices for better performance, run:")
        print(
            f"psql -h {host} -p {port} -U {user} -d {dbname} -f api/app/data/create_indices.sql"
        )
    except Exception as e:
        print(f"Failed to set up extensions or graph: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

    return True


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Initialize LightRAG database in PostgreSQL."
    )
    parser.add_argument("--host", default=DEFAULT_DB_HOST, help="PostgreSQL host")
    parser.add_argument(
        "--port", type=int, default=DEFAULT_DB_PORT, help="PostgreSQL port"
    )
    parser.add_argument("--user", default=DEFAULT_DB_USER, help="PostgreSQL user")
    parser.add_argument(
        "--password", default=DEFAULT_DB_PASSWORD, help="PostgreSQL password"
    )
    parser.add_argument(
        "--dbname", default=DEFAULT_DB_NAME, help="PostgreSQL database name"
    )
    parser.add_argument(
        "--graph-name", default=DEFAULT_GRAPH_NAME, help="Apache AGE graph name"
    )
    return parser.parse_args()


async def main():
    """Main function."""
    args = parse_args()

    # Override with environment variables if available
    host = os.environ.get("POSTGRES_HOST", args.host)
    port = int(os.environ.get("POSTGRES_PORT", args.port))
    user = os.environ.get("POSTGRES_USER", args.user)
    password = os.environ.get("POSTGRES_PASSWORD", args.password)
    dbname = os.environ.get("POSTGRES_DB", args.dbname)
    graph_name = os.environ.get("AGE_GRAPH_NAME", args.graph_name)

    await setup_database(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname,
        graph_name=graph_name,
    )


if __name__ == "__main__":
    asyncio.run(main())
