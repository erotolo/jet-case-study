-- Test to ensure view counts are non-negative values
-- This test will FAIL if any rows are returned (indicating invalid view counts)
-- View counts should never be negative as they represent actual user interactions

SELECT *
FROM {{ ref('fact_comic_metrics') }}
WHERE num_views < 0