# Data Virtualization - Federated Query Engine

A portfolio project demonstrating **Data Virtualization** using **Trino** (formerly PrestoSQL) as a federated query engine. This setup allows simultaneous querying across multiple heterogeneous data sources through a single SQL interface.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Trino Query Engine                      │
│                    (Federated SQL Layer)                     │
└─────────────────────┬───────────────────┬───────────────────┘
                      │                   │
              ┌───────▼───────┐   ┌───────▼───────┐
              │   PostgreSQL   │   │      JMX      │
              │   Connector    │   │   Connector   │
              │  (Catalog:     │   │  (Simulating  │
              │   postgresql)  │   │   S3/Hive)    │
              └───────┬───────┘   └───────┬───────┘
                      │                   │
              ┌───────▼───────┐   ┌───────▼───────┐
              │   PostgreSQL   │   │  JVM Metrics  │
              │   Database     │   │  (Runtime)    │
              └───────────────┘   └───────────────┘
```

## Project Structure

```
.
├── docker-compose.yml              # Container orchestration
├── federated_query.py              # Python demo script
├── requirements.txt                # Python dependencies
├── postgres/
│   └── init.sql                    # Database initialization
└── trino/
    └── etc/
        ├── config.properties       # Trino server config
        ├── jvm.config              # JVM settings
        ├── node.properties         # Node identification
        └── catalog/
            ├── postgresql.properties   # PostgreSQL connector
            └── jmx.properties          # JMX connector
```

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for running the query script)
- 4GB+ RAM available for containers

## Quick Start

### 1. Start the Infrastructure

```bash
# Clone the repository
git clone https://github.com/yadavanujkumar/Data-Virtualization-Federated-Query-Engine.git
cd Data-Virtualization-Federated-Query-Engine

# Start PostgreSQL and Trino containers
docker-compose up -d

# Wait for services to be healthy (about 30-60 seconds)
docker-compose ps
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Federated Query Demo

```bash
python federated_query.py
```

## Data Sources

### PostgreSQL Catalog (`postgresql`)
- **Schema**: `customers`
- **Tables**:
  - `customer`: Customer master data (id, customer_id, first_name, last_name, email)
  - `order_summary`: Order aggregations (customer_id, total_orders, total_amount)

### JMX Catalog (`jmx`)
- Provides JVM runtime metrics
- Simulates an external data source like S3/Hive/Delta Lake
- **Schema**: `current`
- **Tables**: Various JVM MBeans (e.g., `java.lang:type=Runtime`)

## Sample Federated Query

```sql
-- Join customer data with order summary
SELECT 
    t1.customer_id,
    t1.first_name,
    t1.last_name,
    t2.total_orders,
    t2.total_amount
FROM postgresql.customers.customer t1
JOIN postgresql.customers.order_summary t2 
    ON t1.customer_id = t2.customer_id
ORDER BY t2.total_orders DESC;
```

## Accessing Trino UI

Open your browser and navigate to: **http://localhost:8080**

## Manual Query Execution

You can also run queries directly using the Trino CLI:

```bash
# Enter the Trino container
docker exec -it federated-trino trino

# Run queries
trino> SHOW CATALOGS;
trino> SHOW SCHEMAS FROM postgresql;
trino> SELECT * FROM postgresql.customers.customer;
```

## Configuration Details

### Trino Configuration (`trino/etc/config.properties`)
```properties
coordinator=true
node-scheduler.include-coordinator=true
http-server.http.port=8080
discovery.uri=http://localhost:8080
```

### PostgreSQL Connector (`trino/etc/catalog/postgresql.properties`)
```properties
connector.name=postgresql
connection-url=jdbc:postgresql://postgres:5432/customers_db
connection-user=admin
connection-password=admin123
```

### JMX Connector (`trino/etc/catalog/jmx.properties`)
```properties
connector.name=jmx
```

## Extending to Real S3/Hive

To connect to actual S3 data, replace the JMX connector with a Hive connector:

```properties
# trino/etc/catalog/hive.properties
connector.name=hive
hive.metastore.uri=thrift://metastore:9083
hive.s3.aws-access-key=YOUR_ACCESS_KEY
hive.s3.aws-secret-key=YOUR_SECRET_KEY
hive.s3.endpoint=s3.amazonaws.com
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (optional)
docker-compose down -v
```

## Technology Stack

- **Query Engine**: Trino 
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose
- **Client**: Python with trino-python-client

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.