import sqlite3
import pandas as pd

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect("data/database/football.db")

# =====================================================
# BASE EVENTS
# =====================================================

events = pd.read_sql("""
SELECT
    e.event_id,
    e.match_id,
    e.event_index,
    e.possession,
    e.minute,
    e.second,
    e.location_x,
    e.location_y,
    t.team_name,
    p.player_name,
    et.event_type_name
FROM Events e
LEFT JOIN Teams t
ON e.team_id = t.team_id
LEFT JOIN Players p
ON e.player_id = p.player_id
LEFT JOIN EventTypes et
ON e.event_type_id = et.event_type_id
""", conn)

# =====================================================
# PASS EVENTS
# =====================================================

passes = pd.read_sql("""
SELECT
    pe.event_id,
    receiver.player_name AS receiver_name,
    ph.pass_height_name,
    pe.pass_length,
    pe.pass_angle,
    pe.end_location_x,
    pe.end_location_y
FROM PassEvents pe
LEFT JOIN Players receiver
ON pe.recipient_id = receiver.player_id
LEFT JOIN PassHeights ph
ON pe.pass_height_id = ph.pass_height_id
""", conn)

passes["event_detail"] = (
    "Pass → "
    + passes["receiver_name"].fillna("Unknown")
)

passes = passes[
    [
        "event_id",
        "event_detail",
        "pass_length",
        "pass_angle",
        "pass_height_name",
        "end_location_x",
        "end_location_y"
    ]
]

# =====================================================
# SHOT EVENTS
# =====================================================

shots = pd.read_sql("""
SELECT
    se.event_id,
    so.shot_outcome_name,
    se.end_location_x,
    se.end_location_y
FROM ShotEvents se
LEFT JOIN ShotOutcomes so
ON se.shot_outcome_id = so.shot_outcome_id
""", conn)

shots["event_detail"] = (
    "Shot ("
    + shots["shot_outcome_name"].fillna("")
    + ")"
)

shots["pass_length"] = None
shots["pass_angle"] = None
shots["pass_height_name"] = None

shots = shots[
    [
        "event_id",
        "event_detail",
        "pass_length",
        "pass_angle",
        "pass_height_name",
        "end_location_x",
        "end_location_y"
    ]
]

# =====================================================
# CARRY EVENTS
# =====================================================

carry = pd.read_sql("""
SELECT
    event_id,
    end_location_x,
    end_location_y
FROM CarryEvents
""", conn)

carry["event_detail"] = "Carry"

carry["pass_length"] = None
carry["pass_angle"] = None
carry["pass_height_name"] = None

carry = carry[
    [
        "event_id",
        "event_detail",
        "pass_length",
        "pass_angle",
        "pass_height_name",
        "end_location_x",
        "end_location_y"
    ]
]

# =====================================================
# GOALKEEPER EVENTS
# =====================================================

goalkeeper = pd.read_sql("""
SELECT
    ge.event_id,
    gt.goalkeeper_type_name
FROM GoalkeeperEvents ge
LEFT JOIN GoalkeeperTypes gt
ON ge.goalkeeper_type_id = gt.goalkeeper_type_id
""", conn)

goalkeeper["event_detail"] = (
    "Goalkeeper ("
    + goalkeeper["goalkeeper_type_name"].fillna("")
    + ")"
)

goalkeeper["pass_length"] = None
goalkeeper["pass_angle"] = None
goalkeeper["pass_height_name"] = None

goalkeeper["end_location_x"] = None
goalkeeper["end_location_y"] = None

goalkeeper = goalkeeper[
    [
        "event_id",
        "event_detail",
        "pass_length",
        "pass_angle",
        "pass_height_name",
        "end_location_x",
        "end_location_y"
    ]
]

# =====================================================
# GENERIC EVENT TABLES
# =====================================================

event_tables = {
    "DribbleEvents": "Dribble",
    "BallRecoveryEvents": "Ball Recovery",
    "InterceptionEvents": "Interception",
    "ClearanceEvents": "Clearance",
    "BlockEvents": "Block",
    "BallReceiptEvents": "Ball Receipt*",
    "MiscontrolEvents": "Miscontrol",
    "FoulCommittedEvents": "Foul Committed",
    "FoulWonEvents": "Foul Won"
}

generic_frames = []

for table, label in event_tables.items():

    df = pd.read_sql(
        f"""
        SELECT event_id
        FROM {table}
        """,
        conn
    )

    df["event_detail"] = label

    df["pass_length"] = None
    df["pass_angle"] = None
    df["pass_height_name"] = None

    df["end_location_x"] = None
    df["end_location_y"] = None

    generic_frames.append(
        df[
            [
                "event_id",
                "event_detail",
                "pass_length",
                "pass_angle",
                "pass_height_name",
                "end_location_x",
                "end_location_y"
            ]
        ]
    )

# =====================================================
# COMBINE DETAILS
# =====================================================

details = pd.concat(
    [
        passes,
        shots,
        carry,
        goalkeeper,
        *generic_frames
    ],
    ignore_index=True
)

# =====================================================
# MERGE
# =====================================================

sequence = events.merge(
    details,
    on="event_id",
    how="left"
)

# =====================================================
# FALLBACK DETAILS
# =====================================================

sequence["event_detail"] = (
    sequence["event_detail"]
    .fillna(sequence["event_type_name"])
)

# =====================================================
# REMOVE NOISE EVENTS
# =====================================================

IGNORE_EVENTS = [
    "Starting XI",
    "Half Start",
    "Half End",
    "Player On",
    "Player Off",
    "Tactical Shift",
    "Referee Ball-Drop",
    "Injury Stoppage"
]

sequence = sequence[
    ~sequence["event_type_name"].isin(IGNORE_EVENTS)
]

# =====================================================
# SORT
# =====================================================

sequence = sequence.sort_values(
    [
        "match_id",
        "possession",
        "event_index"
    ]
)
# =====================================================
# POSSESSION OWNER
# =====================================================

ownership = (
    sequence.groupby(
        ["match_id", "possession"]
    )["team_name"]
    .agg(lambda x: x.value_counts().idxmax())
    .reset_index()
)

ownership.columns = [
    "match_id",
    "possession",
    "possession_owner"
]

sequence = sequence.merge(
    ownership,
    on=["match_id", "possession"],
    how="left"
)

# =====================================================
# POSSESSION OUTCOME
# =====================================================

def classify_possession(events):

    events = set(
        str(e)
        for e in events
        if pd.notna(e)
    )

    # ---------------------------------
    # SHOT OUTCOMES (Highest Priority)
    # ---------------------------------

    if "Shot (Goal)" in events:
        return "Goal"

    elif "Shot (Post)" in events:
        return "Hit Post"

    elif "Shot (Saved to Post)" in events:
        return "Saved to Post"

    elif "Shot (Saved)" in events:
        return "Saved Shot"

    elif "Shot (Saved Off Target)" in events:
        return "Saved Off Target"

    elif "Shot (Blocked)" in events:
        return "Blocked Shot"

    elif "Shot (Off T)" in events:
        return "Off Target"

    elif "Shot (Wayward)" in events:
        return "Wayward"

    # ---------------------------------
    # POSSESSION LOST
    # ---------------------------------

    elif "Interception" in events:
        return "Interception"

    elif "Dispossessed" in events:
        return "Dispossessed"

    elif "Miscontrol" in events:
        return "Turnover"

    # ---------------------------------
    # FOULS
    # ---------------------------------

    elif "Foul Won" in events:
        return "Foul Won"

    elif "Foul Committed" in events:
        return "Foul Committed"

    # ---------------------------------
    # DEFENSIVE EVENTS
    # ---------------------------------

    elif "Clearance" in events:
        return "Clearance"

    elif "Ball Recovery" in events:
        return "Ball Recovery"

    # ---------------------------------
    # OWN GOALS
    # ---------------------------------

    elif "Own Goal For" in events:
        return "Own Goal For"

    elif "Own Goal Against" in events:
        return "Own Goal Against"

    return "Ended Normally"


possession_outcomes = (
    sequence.groupby(
        ["match_id", "possession"]
    )["event_detail"]
    .apply(classify_possession)
    .reset_index()
)

possession_outcomes.columns = [
    "match_id",
    "possession",
    "possession_outcome"
]

sequence = sequence.merge(
    possession_outcomes,
    on=["match_id", "possession"],
    how="left"
)

# =====================================================
# POSSESSION METADATA
# =====================================================

possession_info = (
    sequence.groupby(
        ["match_id", "possession"]
    )
    .agg(
        possession_start_minute=("minute", "min"),
        possession_end_minute=("minute", "max"),
        possession_event_count=("event_id", "count")
    )
    .reset_index()
)

sequence = sequence.merge(
    possession_info,
    on=["match_id", "possession"],
    how="left"
)
# =====================================================
# FINAL COLUMN ORDER
# =====================================================

sequence = sequence[
    [
        "event_id",
        "match_id",

        "event_index",

        "possession",
        "possession_owner",
        "possession_outcome",

        "possession_start_minute",
        "possession_end_minute",
        "possession_event_count",

        "minute",
        "second",

        "team_name",
        "player_name",

        "event_type_name",
        "event_detail",

        "location_x",
        "location_y",

        "end_location_x",
        "end_location_y",

        "pass_length",
        "pass_angle",
        "pass_height_name"
    ]
]

# =====================================================
# SAVE
# =====================================================

output_file = "reports/csv/event_sequence/sequence_events.csv"

sequence.to_csv(
    output_file,
    index=False
)

# =====================================================
# CHECK POSSESSION OWNERSHIP
# =====================================================

print("=" * 60)
print("SEQUENCE EVENTS CREATED")
print("=" * 60)

print("\nRows:")
print(len(sequence))

print("\nColumns:")
print(sequence.columns.tolist())

print("\nPossession Ownership Check:")

ownership = (
    sequence.groupby(
        ["match_id", "possession"]
    )["team_name"]
    .nunique()
    .value_counts()
)

print(ownership)

print(f"\nSaved -> {output_file}")

conn.close()