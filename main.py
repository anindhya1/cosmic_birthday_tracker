# main.py
from fastapi import FastAPI, Query
from datetime import datetime
from earth_position import get_earth_position, distance
import pytz
from datetime import timedelta

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Cosmic Birthday Tracker API!"}

@app.get("/birth-position")
def birth_position(date: str, timezone: str = "UTC"):
    """
    Get Earth's position on a birth date.
    Example: /birth-position?date=1996-07-14T08:30&timezone=America/New_York
    """
    try:
        tz = pytz.timezone(timezone)
        date_obj = datetime.fromisoformat(date)
        date_obj = tz.localize(date_obj)
        pos = get_earth_position(date_obj)
        return {"x": pos[0], "y": pos[1], "z": pos[2]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/current-position")
def current_position():
    """Get Earth's current position in space."""
    now = datetime.now(pytz.utc)
    pos = get_earth_position(now)
    return {"x": pos[0], "y": pos[1], "z": pos[2]}

@app.get("/distance-to-birth-position")
def distance_to_birth_position(date: str, timezone: str = "UTC"):
    """
    Get distance from Earth's current position to its position at birth.
    Example: /distance-to-birth-position?date=1996-07-14T08:30&timezone=America/New_York
    """
    try:
        tz = pytz.timezone(timezone)
        date_obj = datetime.fromisoformat(date)
        date_obj = tz.localize(date_obj)
        birth_pos = get_earth_position(date_obj)
        now_pos = get_earth_position(datetime.now(pytz.utc))
        d = distance(birth_pos, now_pos)
        return {"distance_au": d}
    except Exception as e:
        return {"error": str(e)}
@app.get("/next-cosmic-birthday")
def next_cosmic_birthday(date: str, timezone: str = "UTC"):
    """
    Find the next date when Earth is closest to its birth position.
    Example: /next-cosmic-birthday?date=1996-07-14T08:30&timezone=America/New_York
    """
    try:
        tz = pytz.timezone(timezone)
        birth_datetime = datetime.fromisoformat(date)
        birth_datetime = tz.localize(birth_datetime)
        birth_pos = get_earth_position(birth_datetime)

        now = datetime.now(pytz.utc)
        closest_date = now
        min_distance = float('inf')

        for i in range(366):  # look ahead one year
            check_date = now + timedelta(days=i)
            check_pos = get_earth_position(check_date)
            d = distance(birth_pos, check_pos)

            if d < min_distance:
                min_distance = d
                closest_date = check_date

        return {
            "cosmic_birthday": closest_date.isoformat(),
            "min_distance_au": min_distance
        }

    except Exception as e:
        return {"error": str(e)}