{{ config(
    materialized = 'table'
) }}

SELECT
    d.comic_key,
    LENGTH(d.title) * 5 AS cost_eur,
    FLOOR(random() * 10000) AS num_views,
    ROUND((1 + (random() * 9))::numeric, 1) AS customer_review,
    CURRENT_TIMESTAMP AS load_timestamp
FROM {{ ref('dim_comic') }} d
