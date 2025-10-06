

with source_data as (
    select 
        occurred,
        city,
        state,
        country,
        shape,
        summary,
        reported,
        media,
        explanation
    from UFO.RAW.ufo_reports_raw
    where occurred is not null
),

deduplicated as (
    select distinct 
        occurred,
        city,
        state,
        country,
        shape,
        summary,
        reported,
        media,
        explanation
    from source_data
),

normalized as (
    select 
        date(try_to_timestamp(occurred, 'MM/DD/YYYY HH24:MI')) as date,
        time(try_to_timestamp(occurred, 'MM/DD/YYYY HH24:MI')) as time,
        city,
        state,
        country,
        shape,
        summary,
        reported,
        coalesce(media, 'N') as media,
        case 
            when upper(explanation) like '%AIRCRAFT%' then 'Aircraft'
            when upper(explanation) like '%BALLOON%' or upper(explanation) like '%BALLOONS%' then 'Balloon'
            when upper(explanation) like '%BAT%' then 'Bat'
            when upper(explanation) like '%BIRD%' or upper(explanation) like '%BIRDS%' then 'Bird'
            when upper(explanation) like '%BLIMP%' then 'Blimp'
            when upper(explanation) like '%BOAT%' or upper(explanation) like '%BOATS%' then 'Boat'
            when upper(explanation) like '%BUILDING%' then 'Building'
            when upper(explanation) like '%CLOUD%' then 'Cloud'
            when upper(explanation) like '%COMET%' then 'Comet'
            when upper(explanation) like '%CONTRAIL%' then 'Contrail'
            when upper(explanation) like '%CRATER%' then 'Crater'
            when upper(explanation) like '%DEBRIS%' then 'Debris'
            when upper(explanation) like '%DRONE%' or upper(explanation) like '%DRONES%' then 'Drone'
            when upper(explanation) like '%FLARE%' or upper(explanation) like '%FLARES%' then 'Flare'
            when upper(explanation) like '%FIREWORK%' or upper(explanation) like '%FIREWORKS%' then 'Fireworks'
            when upper(explanation) like '%HEADLIGHT%' or upper(explanation) like '%HEADLIGHTS%' then 'Headlights'
            when upper(explanation) like '%HOAX%' then 'Hoax'
            when upper(explanation) like '%INSECT%' or upper(explanation) like '%INSECTS%' then 'Insect'
            when upper(explanation) like '%ISS%' then 'ISS'
            when upper(explanation) like '%KITE%' then 'Kite'
            when upper(explanation) like '%LANTERN%' or upper(explanation) like '%CHINESE LANTERN%' or upper(explanation) like '%CHINESE LANTERNS%' then 'Chinese Lantern'
            when upper(explanation) like '%LASER%' then 'Laser'
            when upper(explanation) like '%LIGHTNING%' then 'Lightning'
            when upper(explanation) like '%METEOR%' then 'Meteor'
            when upper(explanation) like '%MOON%' then 'Moon'
            when upper(explanation) like '%PLANET%' or upper(explanation) like '%STAR%' then 'Planet/Star'
            when upper(explanation) like '%ROCKET%' then 'Rocket'
            when upper(explanation) like '%SATELLITE%' or upper(explanation) like '%SATELLITES%' then 'Satellite'
            when upper(explanation) like '%SEARCHLIGHT%' then 'Searchlight'
            when upper(explanation) like '%SMOKE%' then 'Smoke'
            when upper(explanation) like '%SPACE JUNK%' then 'Space Junk'
            when upper(explanation) like '%STARLINK%' then 'Starlink'
            when upper(explanation) like '%SUNDOG%' then 'Sundog'
            when upper(explanation) like '%AURORA%' then 'Aurora'
            when upper(explanation) like '%BALL LIGHTNING%' then 'Ball Lightning'
            when upper(explanation) like '%REFLECTION%' then 'Reflection'
            when upper(explanation) like '%UNEXPLAINED%' then 'Unexplained'
            else coalesce(explanation, 'N/A')
        end as explanation_normalized
    from deduplicated
),

sorted_data as (
    select 
        date,
        time,
        city,
        state,
        country,
        shape,
        summary,
        reported,
        media,
        explanation_normalized
    from normalized
    order by date asc, time asc
)

select 
    row_number() over (order by date asc, time asc) as id,
    date,
    time,
    city,
    state,
    country,
    shape,
    summary,
    reported,
    media,
    explanation_normalized as explanation
from sorted_data