# Cosmic Birthday Tracker

This app helps you discover and celebrate your **true cosmic birthday** — the moment when Earth returns to the same position in its orbit as when you were born.

## Features

- Input your birth date, time, and timezone
- Calculate your next cosmic birthday
- Detect if your last one just passed (within 30 days)
- Visualize Earth's orbit with:
  - 2D matplotlib plot
  - 3D CGI-style orbit (Plotly)
- Show distances in both AU and miles

## How to Run

```bash
git clone https://github.com/anindhya1/cosmic_birthday_tracker.git
cd cosmic_birthday_tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app_ui.py
```

## Notes

The planetary data file de421.bsp is auto-downloaded by Skyfield (not included in the repo).

This app is built with Python and Streamlit.

## Author
@anindhya1
