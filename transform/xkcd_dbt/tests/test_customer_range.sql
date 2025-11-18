-- Test to ensure customer review scores are within valid range (1.0 to 10.0)
-- This test will FAIL if any rows are returned (indicating invalid review scores)
-- Customer reviews should be constrained between 1.0 (lowest) and 10.0 (highest)

SELECT *
FROM {{ ref('fact_comic_metrics') }}
WHERE customer_review < 1.0 OR customer_review > 10.0


