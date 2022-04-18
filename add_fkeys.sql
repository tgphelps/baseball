-- This foreign key is NOT valid
-- alter table parkcodes add constraint fk_parkcodes_leagues
-- foreign key (league)
-- references leagues (league_id);

-- okay
-- alter table nicknames add constraint fk_nicknames_leagues
-- foreign key (league_id)
-- references leagues (league_id);

-- This foreign key is NOT valid
-- alter table nicknames add constraint fk_nicknames_teams1
-- foreign key (current_team_id, league_id)
-- references teams (team_id, league_id);

-- This foreign key is NOT valid
-- alter table nicknames add constraint fk_nicknames_teams2
-- foreign key (team_id, league_id)
-- references teams (team_id, league_id);
