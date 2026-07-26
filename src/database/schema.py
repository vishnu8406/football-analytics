
import sqlite3

def create_tables(connection):
    """
    Create all required database tables.

    Parameters
    ----------
    connection : sqlite3.Connection
        Active SQLite database connection.

    Returns
    -------
    None
    """

    cursor = connection.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS Matches (

    match_id INTEGER PRIMARY KEY,

    competition_id INTEGER,
    season_id INTEGER,

    home_team_id INTEGER,
    away_team_id INTEGER,

    stadium_id INTEGER,
    referee_id INTEGER,

    home_score INTEGER,
    away_score INTEGER,
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

    connection.commit()