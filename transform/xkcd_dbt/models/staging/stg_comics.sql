
SELECT
    num AS comic_id,
    title,
    transcript,
    alt,
    img AS img_url,
    DATE(year || '-' || month || '-' || day) AS published_date,
    year,
    month,
    day
FROM {{ source('raw_xkcd', 'comics') }}