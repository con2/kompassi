-- PostgreSQL >= 9.2
SELECT p.*
from kompassi.zombies.programme_programme p
INNER JOIN programme_category c ON (p.category_id = c.id)
WHERE c.event_id = %s
AND p.id <> %s
AND p.room_id = %s
AND p.start_time IS NOT NULL
AND p.length IS NOT NULL
AND tstzrange(%s, %s, '[)') && tstzrange(p.start_time, p.end_time, '[)');
