#!/usr/bin/env python3
"""
Initialize PostgreSQL database for LightRAG with required extensions.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()


def init_db():
    """Initialize PostgreSQL database with required extensions."""
    # Get connection parameters from environment
    host = os.environ.get("POSTGRES_HOST", "db")
    port = os.environ.get("POSTGRES_PORT", "5432")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    database = os.environ.get("POSTGRES_DATABASE", "embediq")

    print(f"\n==== Initializing LightRAG Database ====")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: {database}")

    try:
        # First connect to default postgres database to create our database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database="postgres",
            connect_timeout=5,
            gssencmode="disable",
            sslmode="disable",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Create database if it doesn't exist
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database,))
        if not cur.fetchone():
            print(f"\nCreating database {database}...")
            cur.execute(f"CREATE DATABASE {database}")
            print("✓ Database created successfully")
        else:
            print(f"\nDatabase {database} already exists")

        cur.close()
        conn.close()

        # Connect to our database to create extensions
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=5,
            gssencmode="disable",
            sslmode="disable",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Check and create required extensions
        extensions = ["vector", "age"]
        for ext in extensions:
            cur.execute("SELECT 1 FROM pg_extension WHERE extname = %s", (ext,))
            if not cur.fetchone():
                print(f"\nCreating extension {ext}...")
                cur.execute(f"CREATE EXTENSION IF NOT EXISTS {ext}")
                print(f"✓ Extension {ext} created successfully")
            else:
                print(f"\nExtension {ext} already exists")

        # Initialize AGE graph
        graph_name = os.environ.get("AGE_GRAPH_NAME", "embediq")
        cur.execute("SELECT 1 FROM ag_graph WHERE name = %s", (graph_name,))
        if not cur.fetchone():
            print(f"\nCreating AGE graph {graph_name}...")
            cur.execute(f"SELECT create_graph('{graph_name}')")
            print("✓ Graph created successfully")
        else:
            print(f"\nGraph {graph_name} already exists")

        cur.close()
        conn.close()

        print("\n✅ Database initialization completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during database initialization: {e}")
        return False


if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
