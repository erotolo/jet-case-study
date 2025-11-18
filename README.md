# XKCD Data Pipeline - JET Case Study

A complete ELT data pipeline that ingests XKCD comics and transforms them into analytics-ready data using Airflow, dbt, and PostgreSQL.

## Project Overview

This project carries out the following:
- **Extracts** daily XKCD comics from the API
- **Loads** raw data into PostgreSQL
- **Transforms** data using dbt into dimensional models
- **Orchestrates** the entire pipeline with Apache Airflow


## Quick Start

### Prerequisites
- Docker Desktop
- Docker Compose
- Git

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd jet-case-study
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your preferences (optional - defaults work for local development)
vim .env
```
**Note:**
For adhoc runs/demo purposes it is reccommended to set the SKIP_SENSOR option to `True`. This allows the pipeline to run if the latest comic has not yet landed. 

### 3. Start Services
```bash
# Start all services
docker compose up --build

# Or run in background
docker compose up -d --build
```

### 4. Access Applications
- **Airflow UI**: http://localhost:${AIRFLOW_WEBSERVER_PORT} (default: 8080)
  - Username: `${AIRFLOW_ADMIN_USERNAME}` (default: admin)
  - Password: `${AIRFLOW_ADMIN_PASSWORD}` (default: admin)
- **dbt Documentation**: http://localhost:${DBT_DOCS_PORT} (default: 8081)
- **PostgreSQL**: localhost:${POSTGRES_EXTERNAL_PORT} (default: 5432)

### 5. Run the Pipeline
1. Go to Airflow UI
2. Find the `xkcd_pipeline` DAG
3. Turn on the toggle to activate it
4. Click "Trigger DAG" to run manually


## Data Models and Scheduling

### Staging Layer
- **stg_comics**: Cleaned and typed raw comic data

### Mart Layer
- **dim_comic**: Comic dimension with metadata
- **fact_comic_metrics**: Performance metrics (views, ratings, costs)

### Data Quality Tests
- Referential integrity between fact and dimension tables
- Non-negative view counts
- Review scores within valid range (1-10)

## Pipeline Schedule

- **Schedule**: Monday, Wednesday, Friday at 9:00 AM UTC
- **Max Active Runs**: 1 (prevents parallel execution)


## Development Setup

### Docker-Based Development (Recommended)
This project is designed to run entirely in Docker containers:

```bash
# Full development environment
docker compose up -d --build

# Make code changes in your local IDE
# Test changes in containers
docker compose exec airflow-webserver dbt run
docker compose exec airflow-webserver python -m pytest tests/
```

### Local IDE Setup
While the pipeline runs in Docker, you can still use your local IDE for testing and development:

```bash
# Install dependencies for IDE support (autocomplete, etc.)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This gives you IDE benefits while keeping execution in containers.


## Development Workflow with Docker

### Making Changes to dbt Models
1. Edit files in `transform/xkcd_dbt/models/`
2. Test locally:
   ```bash
   docker compose exec airflow-webserver bash
   cd /opt/airflow/dbt
   dbt run --select model_name
   dbt test --select model_name
   ```
3. Commit changes
4. Trigger DAG in Airflow UI

### Adding New Models
1. Create SQL file in appropriate `models/` subdirectory
2. Add tests and documentation to `schema.yml`
3. Update model dependencies in SQL files
4. Test the full pipeline

### Viewing Logs
```bash
# Airflow logs
docker compose logs airflow-webserver
docker compose logs airflow-scheduler

# All services
docker compose logs -f
```

### Customizing Configuration
```bash
# Edit environment variables
nano .env

# Apply changes (restart services)
docker compose down
docker compose up -d --build
```


## Troubleshooting

### Common Issues


**"Admin user already exists" error**
- This is normal on restart, user creation is idempotent

**Port conflicts**
- Check your `.env` file for port configurations
- Ensure ports are not in use: `netstat -an | grep :8080`

**dbt docs not loading**
- Ensure pipeline has run at least once
- Check that configured DBT_DOCS_PORT is not blocked
- Restart the dbt-docs service: `docker compose restart dbt-docs`

**No data in tables**
- Check if DAG is active in Airflow UI
- Verify XKCD_BASE_URL is accessible
- Check Airflow task logs for errors

### Debug Mode
```bash
# Access Airflow container
docker compose exec airflow-webserver bash

# Check environment variables
env | grep POSTGRES
env | grep XKCD

# Test dbt connection
cd /opt/airflow/dbt
dbt debug

```


## Testings

### dbt Tests
```bash
# Run all tests
docker compose exec airflow-webserver dbt test --profiles-dir /opt/airflow/.dbt

# Run specific test
docker compose exec airflow-webserver dbt test --select fact_comic_metrics
```

### Manual Data Validation
```sql
-- Check data quality
SELECT 
    COUNT(*) as total_comics,
    MIN(published_date) as earliest_comic,
    MAX(published_date) as latest_comic
FROM comics;
```

### Ingestion unit testing
To run all tests:

```bash
    pytest tests/
```