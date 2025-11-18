{{ config(
    materialized = 'table'
) }}

SELECT
    {{ dbt_utils.generate_surrogate_key(['comic_id']) }} AS comic_key,
    comic_id,
    title,
    transcript,
    alt,
    img_url,
    published_date,
    year,
    month,
    day,
    CURRENT_TIMESTAMP AS updated_at_timestamp
FROM {{ ref('stg_comics') }}
