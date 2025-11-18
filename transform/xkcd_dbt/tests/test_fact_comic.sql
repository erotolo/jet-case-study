-- Test for orphaned fact records

SELECT *
FROM {{ ref('fact_comic_metrics') }} f
LEFT JOIN {{ ref('dim_comic') }} d
  ON f.comic_key = d.comic_key
WHERE d.comic_key IS NULL


