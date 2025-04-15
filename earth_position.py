# earth_position.py
from skyfield.api import load
from datetime import datetime
import pytz


def get_earth_position(date: datetime):
    eph = load('de421.bsp')  # NASA JPL ephemeris
    ts = load.timescale()

    date_utc = date.astimezone(pytz.utc)
    t = ts.utc(date_utc.year, date_utc.month, date_utc.day,
               date_utc.hour, date_utc.minute, date_utc.second)

    earth = eph['earth']
    sun = eph['sun']

    position = earth.at(t).observe(sun).apparent().ecliptic_position().au
    return position  # Returns (x, y, z) in AU


def distance(pos1, pos2):
    return sum((a - b) ** 2 for a, b in zip(pos1, pos2)) ** 0.5


# Example usage
if __name__ == "__main__":
    birth_datetime = datetime(1996, 7, 14, 8, 30, tzinfo=pytz.timezone("America/New_York"))
    birth_pos = get_earth_position(birth_datetime)

    now_pos = get_earth_position(datetime.now(pytz.utc))

    print("Birth Position:", birth_pos)
    print("Current Position:", now_pos)
    print("Distance (AU):", distance(birth_pos, now_pos))
