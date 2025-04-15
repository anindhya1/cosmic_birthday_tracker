import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from earth_position import get_earth_position
from pytz import timezone as get_timezone
from pytz import all_timezones
import pytz
import plotly.graph_objects as go
import numpy as np

def plot_cgi_orbit(birth_pos, now_pos, next_pos):
    fig = go.Figure()

    # Plot Sun
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=10, color='yellow'),
        name='Sun',
        text=["Sun"],
        textposition="top center"
    ))

    # Plot orbit circle
    orbit_points = 360
    orbit_x = [np.cos(theta * np.pi / 180) for theta in range(orbit_points)]
    orbit_y = [np.sin(theta * np.pi / 180) for theta in range(orbit_points)]
    orbit_z = [0] * orbit_points
    fig.add_trace(go.Scatter3d(
        x=orbit_x, y=orbit_y, z=orbit_z,
        mode='lines',
        line=dict(color='gray', dash='dot'),
        name='Ideal Orbit'
    ))

    # Plot Birth Position
    fig.add_trace(go.Scatter3d(
        x=[birth_pos[0]], y=[birth_pos[1]], z=[birth_pos[2]],
        mode='markers+text',
        marker=dict(size=6, color='blue'),
        name='Birth',
        text=["Birth"],
        textposition="top center"
    ))

    # Plot Current Position
    fig.add_trace(go.Scatter3d(
        x=[now_pos[0]], y=[now_pos[1]], z=[now_pos[2]],
        mode='markers+text',
        marker=dict(size=6, color='green'),
        name='Now',
        text=["Now"],
        textposition="top center"
    ))

    # Plot Next Cosmic Birthday
    fig.add_trace(go.Scatter3d(
        x=[next_pos[0]], y=[next_pos[1]], z=[next_pos[2]],
        mode='markers+text',
        marker=dict(size=6, color='magenta'),
        name='Cosmic Birthday',
        text=["Cosmic"],
        textposition="top center"
    ))

    fig.update_layout(
        title="🌌 Earth's Orbit (CGI Style)",
        scene=dict(
            xaxis_title='X (AU)',
            yaxis_title='Y (AU)',
            zaxis_title='Z (AU)',
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        legend=dict(x=0.02, y=0.98)
    )

    return fig


st.set_page_config(page_title="Cosmic Birthday Tracker 🌍", layout="centered")
st.title("🌍 Cosmic Birthday Tracker")
st.markdown("**Find your true birthday — when Earth returns to where it was when you were born.**")

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    date_input = st.date_input(
        "Your Birth Date",
        value=datetime(1996, 7, 14).date(),
        min_value=datetime(1900, 1, 1).date(),
        max_value=datetime.now().date()
    )
    time_input = st.time_input("Your Birth Time")
with col2:
    timezone_input = st.selectbox(
        "Choose Your Timezone",
        options=all_timezones,
        index=all_timezones.index("UTC")
    )

if st.button("Find My True Cosmic Birthday 🚀"):
    try:
        # Combine date & time
        birth_datetime = datetime.combine(date_input, time_input)
        tz = get_timezone(timezone_input)
        localized_birth = tz.localize(birth_datetime)

        # Get birth position
        birth_pos = get_earth_position(localized_birth)
        now = datetime.now(pytz.utc)
        now_pos = get_earth_position(now)

        # --- Search recent past (30 days)
        recent_past_date = None
        recent_past_distance = float('inf')

        for i in range(1, 31):
            check_date = now - timedelta(days=i)
            check_pos = get_earth_position(check_date)
            d = sum((a - b)**2 for a, b in zip(birth_pos, check_pos)) ** 0.5
            if d < recent_past_distance:
                recent_past_distance = d
                recent_past_date = check_date
                recent_past_pos = check_pos

        # --- Search future (1 year)
        closest_date = None
        min_distance = float('inf')

        for i in range(366):
            check_date = now + timedelta(days=i)
            check_pos = get_earth_position(check_date)
            d = sum((a - b)**2 for a, b in zip(birth_pos, check_pos)) ** 0.5
            if d < min_distance:
                min_distance = d
                closest_date = check_date
                next_birthday_pos = check_pos

        # --- Display upcoming birthday (always)
        st.success(f"🌠 Your **next cosmic birthday** is on **{closest_date.strftime('%Y-%m-%d %H:%M:%S UTC')}**")
        miles = min_distance * 92955807.3
        st.info(f"🪐 Earth will be only **{min_distance:.6f} AU** ({miles:,.0f} miles) from your birth position.")

        # --- Conditionally show recent one (within last 30 days)
        if recent_past_date:
            days_ago = (now - recent_past_date).days
            if days_ago <= 30:
                st.info(f"🎉 Your most recent cosmic birthday was on **{recent_past_date.strftime('%Y-%m-%d %H:%M:%S UTC')}** — just {days_ago} days ago!")
                recent_miles = recent_past_distance * 92955807.3
                st.info(
                    f"🪐 Earth was only **{recent_past_distance:.6f} AU** ({recent_miles:,.0f} miles) from your birth position.")

        # --- Plot (always show upcoming)
        display_date = closest_date
        display_pos = next_birthday_pos

        # Debug output (visible in terminal)
        print("Closest past:", recent_past_date.isoformat() if recent_past_date else "None", "Distance:", recent_past_distance)
        print("Closest future:", closest_date.isoformat() if closest_date else "None", "Distance:", min_distance)

        # --- Plot ---
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_title("Earth's Orbit\nBirth • Now • Next Cosmic Birthday")

        # Sun
        ax.plot(0, 0, 'yo', label='Sun')
        circle = plt.Circle((0, 0), 1, color='gray', linestyle='--', fill=False)
        ax.add_artist(circle)

        # Points
        ax.plot(birth_pos[0], birth_pos[1], 'bo', label='Birth')
        ax.plot(now_pos[0], now_pos[1], 'go', label='Now')
        ax.plot(display_pos[0], display_pos[1], 'mo', label='Next Birthday')

        # Labels
        ax.annotate("Birth", (birth_pos[0], birth_pos[1]), textcoords="offset points", xytext=(5, 5), ha='left')
        ax.annotate("Now", (now_pos[0], now_pos[1]), textcoords="offset points", xytext=(5, 5), ha='left')
        ax.annotate("Next", (display_pos[0], display_pos[1]), textcoords="offset points", xytext=(5, 5), ha='left')

        ax.set_xlabel("X (AU)")
        ax.set_ylabel("Y (AU)")
        ax.grid(True)
        ax.legend()
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)

        st.pyplot(fig)

        # --- CGI Style 3D Plot
        st.markdown("### 🧊 CGI-Style 3D Orbit Visualization")
        fig3d = plot_cgi_orbit(birth_pos, now_pos, next_birthday_pos)
        st.plotly_chart(fig3d, use_container_width=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
