# plot_orbit.py
from earth_position import get_earth_position
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt

def plot_birth_now_next(birth_datetime, timezone_str="UTC"):
    tz = pytz.timezone(timezone_str)
    birth_dt = tz.localize(birth_datetime)
    now_dt = datetime.now(pytz.utc)

    # Get positions
    birth_pos = get_earth_position(birth_dt)
    now_pos = get_earth_position(now_dt)

    # Predict next cosmic birthday
    closest_date = now_dt
    min_distance = float('inf')
    for i in range(366):
        check_date = now_dt + timedelta(days=i)
        check_pos = get_earth_position(check_date)
        d = sum((a - b) ** 2 for a, b in zip(birth_pos, check_pos)) ** 0.5
        if d < min_distance:
            min_distance = d
            closest_date = check_date
            next_birthday_pos = check_pos

    # Plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_title("Earth's Orbit: Birth • Now • Next Cosmic Birthday")

    # Orbit Circle
    orbit = plt.Circle((0, 0), 1, color='gray', fill=False, linestyle='--', label='Ideal Orbit')
    ax.add_artist(orbit)

    # Sun
    ax.plot(0, 0, 'yo', label='Sun')

    # Positions
    ax.plot(birth_pos[0], birth_pos[1], 'bo', label='Birth')
    ax.plot(now_pos[0], now_pos[1], 'go', label='Now')
    ax.plot(next_birthday_pos[0], next_birthday_pos[1], 'mo', label='Next Cosmic Birthday')

    # Labels
    ax.annotate("Birth", (birth_pos[0], birth_pos[1]), textcoords="offset points", xytext=(5,5), ha='left')
    ax.annotate("Now", (now_pos[0], now_pos[1]), textcoords="offset points", xytext=(5,5), ha='left')
    ax.annotate("Next", (next_birthday_pos[0], next_birthday_pos[1]), textcoords="offset points", xytext=(5,5), ha='left')

    ax.set_xlabel("X (AU)")
    ax.set_ylabel("Y (AU)")
    ax.grid(True)
    ax.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    birth_date = datetime(1996, 7, 14, 8, 30)
    plot_birth_now_next(birth_date, "America/New_York")
