# XKCD Data Transformation Pipeline

This dbt project transforms raw XKCD comic data into a clean, analytics-ready data warehouse.

## Project Overview

**Purpose**: Transform ingested XKCD comic data into dimensional models for analysis and reporting.

**Data Flow**: 
```
Raw Comics Data (PostgreSQL) → Staging Models → Mart Models → Analytics
```

## Architecture

### Data Models
- **Staging**: `stg_comics` - Clean and type raw comic data
- **Marts**: 
  - `dim_comic` - Comic dimension table
  - `fact_comic_metrics` - Comic metrics fact table

### Data Sources
- **raw_xkcd.comics** - Raw comic data from ingestion pipeline


## Data Quality Tests

- **Referential Integrity**: Fact tables reference valid dimension keys
- **Data Validation**: View counts are non-negative, reviews in valid range (1-10)
- **Freshness**: Source data updated within 24 hours


## Development Workflow

1. **Make Changes**: Edit models in `models/` directory
2. **Test Locally**: `dbt run --select model_name`
3. **Validate**: `dbt test --select model_name`
4. **Deploy**: Commit to git (triggers production run)

## Key Metrics

This project enables analysis of:
- Comic popularity trends
- Customer satisfaction ratings
- Publication patterns
- Content performance metrics
