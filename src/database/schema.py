import sqlite3


def create_tables(connection: sqlite3.Connection) -> None:

    """
    Create all database tables required for the football analytics project.

    Parameters
    ----------
    connection : sqlite3.Connection
        Active SQLite database connection.

    Returns
    -------
    None
    """

    # Enable foreign key constraints
    
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.execute("PRAGMA journal_mode = WAL;")

    cursor = connection.cursor()

    # ------------------------------------------------------------------
    # Competitions
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Competitions (
            competition_id INTEGER PRIMARY KEY,
            competition_name TEXT NOT NULL
        );
    """)

    # ------------------------------------------------------------------
    # Seasons
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Seasons (
            season_id INTEGER PRIMARY KEY,
            season_name TEXT NOT NULL,
            competition_id INTEGER NOT NULL,

            FOREIGN KEY (competition_id)
                REFERENCES Competitions(competition_id)
        );
    """)

    # ------------------------------------------------------------------
    # Teams
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL
        );
    """)

    # ------------------------------------------------------------------
    # Stadiums
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stadiums (
            stadium_id INTEGER PRIMARY KEY,
            stadium_name TEXT NOT NULL
        );
    """)

    # ------------------------------------------------------------------
    # Referees
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Referees (
            referee_id INTEGER PRIMARY KEY,
            referee_name TEXT NOT NULL
        );
    """)

    # ------------------------------------------------------------------
    # Players
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Players (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT NOT NULL,
            player_nickname TEXT,
            country_id INTEGER,
            country_name TEXT
        );
    """)

    # ------------------------------------------------------------------
    # Positions
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Positions (
            position_id INTEGER PRIMARY KEY,
            position_name TEXT NOT NULL
        );
    """)

    # ------------------------------------------------------------------
    # Matches
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Matches (

            match_id INTEGER PRIMARY KEY,

            competition_id INTEGER NOT NULL,
            season_id INTEGER NOT NULL,

            home_team_id INTEGER NOT NULL,
            away_team_id INTEGER NOT NULL,

            stadium_id INTEGER,
            referee_id INTEGER,

            home_score INTEGER NOT NULL,
            away_score INTEGER NOT NULL,

            match_week INTEGER,
            match_date TEXT,
            kick_off TEXT,

            FOREIGN KEY (competition_id)
                REFERENCES Competitions(competition_id),

            FOREIGN KEY (season_id)
                REFERENCES Seasons(season_id),

            FOREIGN KEY (home_team_id)
                REFERENCES Teams(team_id),

            FOREIGN KEY (away_team_id)
                REFERENCES Teams(team_id),

            FOREIGN KEY (stadium_id)
                REFERENCES Stadiums(stadium_id),

            FOREIGN KEY (referee_id)
                REFERENCES Referees(referee_id)
        );
    """)

    # ------------------------------------------------------------------
    # Match Players
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MatchPlayers (

            match_id INTEGER,
            player_id INTEGER,
            team_id INTEGER,
            jersey_number INTEGER,

            PRIMARY KEY (match_id, player_id),

            FOREIGN KEY (match_id)
                REFERENCES Matches(match_id),

            FOREIGN KEY (player_id)
                REFERENCES Players(player_id),

            FOREIGN KEY (team_id)
                REFERENCES Teams(team_id)
        );
    """)

    # ------------------------------------------------------------------
    # Player Positions
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PlayerPositions (

            match_id INTEGER,
            player_id INTEGER,
            position_id INTEGER,
            position_name TEXT,

            from_time TEXT,
            to_time TEXT,

            from_period INTEGER,
            to_period INTEGER,

            start_reason TEXT,
            end_reason TEXT,

            PRIMARY KEY (
                match_id,
                player_id,
                position_id,
                from_time
            ),

            FOREIGN KEY (match_id)
                REFERENCES Matches(match_id),

            FOREIGN KEY (player_id)
                REFERENCES Players(player_id),

            FOREIGN KEY (position_id)
                REFERENCES Positions(position_id)
        );
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS EventTypes (

    event_type_id INTEGER PRIMARY KEY,
    event_type_name TEXT NOT NULL

);
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS PlayPatterns (

    play_pattern_id INTEGER PRIMARY KEY,
    play_pattern_name TEXT NOT NULL

);
        """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS PassHeights (

    pass_height_id INTEGER PRIMARY KEY,
    pass_height_name TEXT NOT NULL

);
        """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS PassTypes (

    pass_type_id INTEGER PRIMARY KEY,
    pass_type_name TEXT NOT NULL

);
        """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS BodyParts (

    body_part_id INTEGER PRIMARY KEY,
    body_part_name TEXT NOT NULL

);
        """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS PassOutcomes (

    pass_outcome_id INTEGER PRIMARY KEY,
    pass_outcome_name TEXT NOT NULL

);
        """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS Events (

    event_id TEXT PRIMARY KEY,

    match_id INTEGER NOT NULL,

    event_index INTEGER,

    period INTEGER,
    minute INTEGER,
    second INTEGER,

    timestamp TEXT,

    event_type_id INTEGER,

    team_id INTEGER,
    player_id INTEGER,
    position_id INTEGER,

    possession INTEGER,
    possession_team_id INTEGER,

    play_pattern_id INTEGER,

    duration REAL,

    location_x REAL,
    location_y REAL,

    FOREIGN KEY(match_id)
        REFERENCES Matches(match_id),

    FOREIGN KEY(event_type_id)
        REFERENCES EventTypes(event_type_id),

    FOREIGN KEY(team_id)
        REFERENCES Teams(team_id),

    FOREIGN KEY(player_id)
        REFERENCES Players(player_id),

    FOREIGN KEY(position_id)
        REFERENCES Positions(position_id),

    FOREIGN KEY(possession_team_id)
        REFERENCES Teams(team_id),

    FOREIGN KEY(play_pattern_id)
        REFERENCES PlayPatterns(play_pattern_id)
);
        """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS PassEvents (

    event_id TEXT PRIMARY KEY,

    recipient_id INTEGER,

    pass_type_id INTEGER,

    pass_height_id INTEGER,

    body_part_id INTEGER,

    pass_outcome_id INTEGER,

    pass_length REAL,

    pass_angle REAL,

    end_location_x REAL,

    end_location_y REAL,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(recipient_id)
        REFERENCES Players(player_id),

    FOREIGN KEY(pass_type_id)
        REFERENCES PassTypes(pass_type_id),

    FOREIGN KEY(pass_height_id)
        REFERENCES PassHeights(pass_height_id),

    FOREIGN KEY(body_part_id)
        REFERENCES BodyParts(body_part_id),

    FOREIGN KEY(pass_outcome_id)
        REFERENCES PassOutcomes(pass_outcome_id)
);
        """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS ShotOutcomes (

    shot_outcome_id INTEGER PRIMARY KEY,
    shot_outcome_name TEXT NOT NULL

);
""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ShotTypes (

    shot_type_id INTEGER PRIMARY KEY,
    shot_type_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ShotTechniques (

    shot_technique_id INTEGER PRIMARY KEY,
    shot_technique_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ShotEvents (

    event_id TEXT PRIMARY KEY,

    shot_outcome_id INTEGER,
    shot_type_id INTEGER,
    shot_technique_id INTEGER,
    body_part_id INTEGER,

    statsbomb_xg REAL,

    under_pressure BOOLEAN,

    first_time BOOLEAN,
    deflected BOOLEAN,
    one_on_one BOOLEAN,
    open_goal BOOLEAN,
    redirect BOOLEAN,
    follows_dribble BOOLEAN,
    aerial_won BOOLEAN,
    saved_off_target BOOLEAN,
    saved_to_post BOOLEAN,

    key_pass_event_id TEXT,

    end_location_x REAL,
    end_location_y REAL,
    end_location_z REAL,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(shot_outcome_id)
        REFERENCES ShotOutcomes(shot_outcome_id),

    FOREIGN KEY(shot_type_id)
        REFERENCES ShotTypes(shot_type_id),

    FOREIGN KEY(shot_technique_id)
        REFERENCES ShotTechniques(shot_technique_id),

    FOREIGN KEY(body_part_id)
        REFERENCES BodyParts(body_part_id),

    FOREIGN KEY(key_pass_event_id)
        REFERENCES Events(event_id)

);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS CarryEvents (

    event_id TEXT PRIMARY KEY,

    end_location_x REAL,
    end_location_y REAL,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id)
);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS DribbleOutcomes (

    dribble_outcome_id INTEGER PRIMARY KEY,
    dribble_outcome_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS DribbleEvents (

    event_id TEXT PRIMARY KEY,

    dribble_outcome_id INTEGER,

    overrun BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(dribble_outcome_id)
        REFERENCES DribbleOutcomes(dribble_outcome_id)

);""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS BallRecoveryEvents (

    event_id TEXT PRIMARY KEY,

    offensive BOOLEAN,
    recovery_failure BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id)

);""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS InterceptionOutcomes (

    interception_outcome_id INTEGER PRIMARY KEY,
    interception_outcome_name TEXT NOT NULL

);""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS InterceptionEvents (

    event_id TEXT PRIMARY KEY,

    interception_outcome_id INTEGER,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(interception_outcome_id)
        REFERENCES InterceptionOutcomes(interception_outcome_id)

);""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS ClearanceEvents (

    event_id TEXT PRIMARY KEY,

    body_part_id INTEGER,

    aerial_won BOOLEAN,
    head BOOLEAN,
    left_foot BOOLEAN,
    right_foot BOOLEAN,
    other BOOLEAN,

    out BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(body_part_id)
        REFERENCES BodyParts(body_part_id)

);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS BlockEvents (

    event_id TEXT PRIMARY KEY,

    deflection BOOLEAN,
    offensive BOOLEAN,
    save_block BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id)

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS BallReceiptOutcomes (

    ball_receipt_outcome_id INTEGER PRIMARY KEY,
    ball_receipt_outcome_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS BallReceiptEvents (

    event_id TEXT PRIMARY KEY,

    ball_receipt_outcome_id INTEGER,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(ball_receipt_outcome_id)
        REFERENCES BallReceiptOutcomes(ball_receipt_outcome_id)

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS MiscontrolEvents (

    event_id TEXT PRIMARY KEY,

    aerial_won BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id)

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Cards (

    card_id INTEGER PRIMARY KEY,
    card_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS FoulCommittedTypes (

    foul_committed_type_id INTEGER PRIMARY KEY,
    foul_committed_type_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS FoulCommittedEvents (

    event_id TEXT PRIMARY KEY,

    foul_committed_type_id INTEGER,
    card_id INTEGER,

    advantage BOOLEAN,
    offensive BOOLEAN,
    penalty BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(foul_committed_type_id)
        REFERENCES FoulCommittedTypes(foul_committed_type_id),

    FOREIGN KEY(card_id)
        REFERENCES Cards(card_id)

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS FoulWonEvents (

    event_id TEXT PRIMARY KEY,

    advantage BOOLEAN,
    defensive BOOLEAN,
    penalty BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id)

);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS SubstitutionOutcomes (

    substitution_outcome_id INTEGER PRIMARY KEY,
    substitution_outcome_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS SubstitutionEvents (

    event_id TEXT PRIMARY KEY,

    replacement_player_id INTEGER,

    substitution_outcome_id INTEGER,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(replacement_player_id)
        REFERENCES Players(player_id),

    FOREIGN KEY(substitution_outcome_id)
        REFERENCES SubstitutionOutcomes(substitution_outcome_id)

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS BadBehaviourEvents (

    event_id TEXT PRIMARY KEY,

    card_id INTEGER,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(card_id)
        REFERENCES Cards(card_id)

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS DuelTypes (

    duel_type_id INTEGER PRIMARY KEY,
    duel_type_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS DuelOutcomes (

    duel_outcome_id INTEGER PRIMARY KEY,
    duel_outcome_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS DuelEvents (

    event_id TEXT PRIMARY KEY,

    duel_type_id INTEGER,
    duel_outcome_id INTEGER,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(duel_type_id)
        REFERENCES DuelTypes(duel_type_id),

    FOREIGN KEY(duel_outcome_id)
        REFERENCES DuelOutcomes(duel_outcome_id)

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS GoalkeeperOutcomes (

    goalkeeper_outcome_id INTEGER PRIMARY KEY,
    goalkeeper_outcome_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS GoalkeeperTypes (

    goalkeeper_type_id INTEGER PRIMARY KEY,
    goalkeeper_type_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS GoalkeeperTechniques (

    goalkeeper_technique_id INTEGER PRIMARY KEY,
    goalkeeper_technique_name TEXT NOT NULL

);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS GoalkeeperEvents (

    event_id TEXT PRIMARY KEY,

    goalkeeper_outcome_id INTEGER,
    goalkeeper_type_id INTEGER,

    position_id INTEGER,
    goalkeeper_technique_id INTEGER,
    body_part_id INTEGER,

    end_location_x REAL,
    end_location_y REAL,
    end_location_z REAL,

    lost_in_play BOOLEAN,
    lost_out BOOLEAN,

    punched_out BOOLEAN,

    shot_saved_off_target BOOLEAN,
    shot_saved_to_post BOOLEAN,

    success_in_play BOOLEAN,
    success_out BOOLEAN,

    FOREIGN KEY(event_id)
        REFERENCES Events(event_id),

    FOREIGN KEY(goalkeeper_outcome_id)
        REFERENCES GoalkeeperOutcomes(goalkeeper_outcome_id),

    FOREIGN KEY(goalkeeper_type_id)
        REFERENCES GoalkeeperTypes(goalkeeper_type_id),

    FOREIGN KEY(position_id)
        REFERENCES Positions(position_id),

    FOREIGN KEY(goalkeeper_technique_id)
        REFERENCES GoalkeeperTechniques(goalkeeper_technique_id),

    FOREIGN KEY(body_part_id)
        REFERENCES BodyParts(body_part_id)

);""")
    


    
    
    

    connection.commit()