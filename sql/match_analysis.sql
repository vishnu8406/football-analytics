SELECT
    pp.match_id,
    t.team_name,
    p.player_name,
    mp.jersey_number,
    pp.position_name
FROM PlayerPositions pp

JOIN Players p
ON pp.player_id = p.player_id

JOIN MatchPlayers mp
ON pp.match_id = mp.match_id
AND pp.player_id = mp.player_id

JOIN Teams t
ON mp.team_id = t.team_id

WHERE pp.start_reason = 'Starting XI'
ORDER BY
pp.match_id,
t.team_name,
pp.position_id;