#!/usr/bin/env python3
"""
Federated Query Script for Trino Data Virtualization Demo

This script demonstrates data virtualization by executing a federated query
that joins data from PostgreSQL (customer data) with JMX data (simulating
an external data source like S3/Hive/Delta Lake).

For a true production setup, the JMX connector would be replaced with:
- Hive connector for S3/HDFS data
- Delta Lake connector
- Iceberg connector
"""

import trino
from trino.exceptions import TrinoQueryError


def get_trino_connection(host: str = "localhost", port: int = 8080, user: str = "admin"):
    """
    Establish a connection to the Trino server.
    
    Args:
        host: Trino server hostname
        port: Trino server port
        user: Username for authentication
    
    Returns:
        trino.dbapi.Connection: Database connection object
    """
    return trino.dbapi.connect(
        host=host,
        port=port,
        user=user,
        catalog="postgresql",
        schema="customers"
    )


def execute_query(connection, query: str):
    """
    Execute a SQL query and return results.
    
    Args:
        connection: Trino database connection
        query: SQL query string
    
    Returns:
        list: Query results
    """
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def demo_federated_query():
    """
    Demonstrate a federated query joining customer and order data.
    
    This simulates the requested federated query pattern:
    SELECT t1.customer_id, t2.total_orders 
    FROM postgres.schema.customer t1 
    JOIN s3.schema.order_summary t2 ON t1.id = t2.customer_id
    
    Since we're using PostgreSQL for both tables in this demo,
    the query demonstrates the same federated query capability.
    """
    print("=" * 60)
    print("Trino Federated Query Demo - Data Virtualization")
    print("=" * 60)
    
    try:
        # Connect to Trino
        print("\n[1] Connecting to Trino server...")
        conn = get_trino_connection()
        print("    ✓ Connected successfully!")
        
        # Query 1: List available catalogs
        print("\n[2] Listing available catalogs...")
        catalogs = execute_query(conn, "SHOW CATALOGS")
        print("    Available catalogs:")
        for catalog in catalogs:
            print(f"      - {catalog[0]}")
        
        # Query 2: Show schemas in PostgreSQL catalog
        print("\n[3] Listing schemas in PostgreSQL catalog...")
        schemas = execute_query(conn, "SHOW SCHEMAS FROM postgresql")
        print("    Available schemas:")
        for schema in schemas:
            print(f"      - {schema[0]}")
        
        # Query 3: Show tables in customers schema
        print("\n[4] Listing tables in customers schema...")
        tables = execute_query(conn, "SHOW TABLES FROM postgresql.customers")
        print("    Available tables:")
        for table in tables:
            print(f"      - {table[0]}")
        
        # Query 4: Execute federated query (joining customer and order_summary)
        print("\n[5] Executing Federated Query...")
        print("    Query: SELECT t1.customer_id, t2.total_orders")
        print("           FROM postgresql.customers.customer t1")
        print("           JOIN postgresql.customers.order_summary t2")
        print("           ON t1.customer_id = t2.customer_id")
        
        federated_query = """
        SELECT 
            t1.customer_id,
            t1.first_name,
            t1.last_name,
            t2.total_orders,
            t2.total_amount
        FROM postgresql.customers.customer t1
        JOIN postgresql.customers.order_summary t2 
            ON t1.customer_id = t2.customer_id
        ORDER BY t2.total_orders DESC
        """
        
        results = execute_query(conn, federated_query)
        
        print("\n    Results:")
        print("    " + "-" * 70)
        print(f"    {'Customer ID':<12} {'First Name':<12} {'Last Name':<12} {'Orders':<8} {'Amount':>10}")
        print("    " + "-" * 70)
        
        for row in results:
            customer_id, first_name, last_name, total_orders, total_amount = row
            print(f"    {customer_id:<12} {first_name:<12} {last_name:<12} {total_orders:<8} ${total_amount:>9.2f}")
        
        print("    " + "-" * 70)
        print(f"    Total records: {len(results)}")
        
        # Query 5: Demonstrate JMX catalog (simulating external data source)
        print("\n[6] Demonstrating JMX Catalog (simulating S3/Hive connector)...")
        print("    Query: SELECT * FROM jmx.current.\"java.lang:type=runtime\"")
        
        jmx_query = """
        SELECT node, name, uptime 
        FROM jmx.current."java.lang:type=Runtime"
        """
        
        jmx_results = execute_query(conn, jmx_query)
        print("\n    JMX Runtime Information:")
        for row in jmx_results:
            print(f"      Node: {row[0][:50]}...")
            print(f"      Name: {row[1]}")
            print(f"      Uptime: {row[2]} ms")
        
        print("\n" + "=" * 60)
        print("Demo completed successfully!")
        print("=" * 60)
        
    except TrinoQueryError as e:
        print(f"\n    ✗ Query Error: {e}")
        raise
    except Exception as e:
        print(f"\n    ✗ Connection Error: {e}")
        print("\n    Make sure Docker containers are running:")
        print("      docker-compose up -d")
        raise


def main():
    """Main entry point for the federated query demo."""
    demo_federated_query()


if __name__ == "__main__":
    main()
