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

    outcome_id INTEGER PRIMARY KEY,
    outcome_name TEXT NOT NULL

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

    outcome_id INTEGER,

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

    FOREIGN KEY(outcome_id)
        REFERENCES PassOutcomes(outcome_id)
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
    
    

    connection.commit()