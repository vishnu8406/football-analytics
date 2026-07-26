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

    connection.commit()