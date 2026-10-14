import importlib
import pandas as pd
import plotly.express as px
import streamlit as st

# Import the tools used for the dashboard and its charts.


from Dashboard import youssef_charts

try:
    from Dashboard import heba_charts
except ImportError:
    heba_charts = None

# Set the basic page settings and dashboard layout.
st.set_page_config(
    page_title="Ford GoBike Analytics",
    page_icon="https://img.icons8.com/?size=100&id=O6GtnaATHUol&format=png&color=12B886",
    layout="wide"
)
# use the same color pallete
COLORS = {
    "Subscriber": "#00FF88",
    "Customer":   "#00B8D4",
    "Male":       "#00FF88",
    "Female":     "#7C3AED",  # Neon purple accent
    "Young":      "#00FF88",
    "Adult":      "#00B8D4",
    "Senior":     "#F59E0B",  # Amber accent
}

# Keep the dashboard styling in one place.
st.html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,450,0,0" rel="stylesheet">
<style>
:root{
    --ink: #E2E8F0;
    --ink-soft: #94A3B8;

    --cyber: #00FF88;
    --cyber-dark: #00CC6A;
    --cyber-soft: rgba(0,255,136,0.12);

    --teal: #00B8D4;

    --canvas: #0A0F14;
    --paper: #111827;

    --muted: #94A3B8;
    --line: rgba(0,255,136,0.15);
}

.material-symbols-rounded {
    font-family: 'Material Symbols Rounded';
    font-weight: normal;
    font-style: normal;
    font-size: 22px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
    vertical-align: middle;
}

/* Professional page header */
.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin: 2px 0 20px;
    padding: 4px 2px 2px;
}

.page-eyebrow {
    color: var(--cyber-dark);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin-bottom: 5px;
}

.page-title {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--ink);
    font-size: 27px;
    font-weight: 850;
    line-height: 1.15;
}

.page-title .material-symbols-rounded {
    color: var(--cyber);
    font-size: 29px;
}

.page-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-top: 6px;
}

.page-period {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 9px 13px;
    border: 1px solid var(--line);
    border-radius: 999px;
    background: var(--paper);
    color: var(--ink);
    font-size: 11px;
    font-weight: 700;
    white-space: nowrap;
    box-shadow: 0 7px 18px -15px rgba(21,20,26,0.4);
}

.page-period .material-symbols-rounded {
    color: var(--cyber);
    font-size: 17px;
}

/* Page canvas */
.stApp {
    background:
        radial-gradient(circle at top right,
            rgba(0,255,136,0.08),
            transparent 40%),
        #0A0F14;
}

/* Professional sidebar */
[data-testid="stSidebar"] {
    background: var(--canvas);
    border-right: 1px solid rgba(0,255,136,0.15);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.25rem;
    
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 4px 4px 12px;
}

.sidebar-brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    color: var(--cyber);
    box-shadow: 0 8px 18px -12px rgba(21,20,26,0.5);
}

.sidebar-brand-icon .material-symbols-rounded {
    font-size: 23px;
}

.sidebar-brand-title {
    color: var(--ink);
    font-size: 16px;
    font-weight: 800;
    line-height: 1.2;
}

.sidebar-brand-subtitle {
    color: var(--muted);
    font-size: 11px;
    margin-top: 3px;
    letter-spacing: 0.2px;
}

.sidebar-intro {
    color: var(--muted);
    font-size: 11px;
    line-height: 1.55;
    padding: 0 4px 16px;
}

.sidebar-section-title {
    color: var(--muted);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.1px;
    margin: 8px 4px 10px;
}

.sidebar-divider {
    height: 1px;
    background: var(--line);
    margin: 18px 0;
}

.sidebar-stat {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 9px;
    margin-bottom: 8px;
    border: 1px solid var(--line);
    border-radius: 13px;
    
}

.sidebar-stat-icon {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--cyber-soft);
    color: var(--cyber-dark);
}

.sidebar-stat-icon .material-symbols-rounded {
    font-size: 18px;
    color: var(--ink);
}

.sidebar-stat-value {
    color: var(--ink);
    font-size: 12px;
    font-weight: 800;
    line-height: 1.2;
}

.sidebar-stat-label {
    color: var(--muted);
    font-size: 10px;
    margin-top: 3px;
}

.sidebar-footer {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-top: 22px;
    padding: 11px 10px;
    border-radius: 13px;
    background: var(--ink);
    
}

.sidebar-footer > .material-symbols-rounded {
    color: var(--teal);
    font-size: 20px;
}

.sidebar-footer b {
    display: block;
    color: var(--muted);
    font-size: 11px;
    line-height: 1.2;
}

.sidebar-footer small {
    display: block;
    color: var(--muted);
    font-size: 9px;
    margin-top: 3px;
}

/* Sidebar filter chips */
div[data-baseweb="tag"] span {
    background-color: var(--paper) !important;
    color: var(--cyber) !important;
    border-radius: 999px !important;
}
div[data-baseweb="tag"] span { color: var(--paper) !important; }
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"] > div:hover {
    border-color: var(--cyber) !important;
}


/* Selected filter chips */
span[data-baseweb="tag"] {
    background-color: var(--cyber) !important;
    color: var(--paper) !important;
    border-radius: 999px !important;
}

/* Force all content inside tag */
span[data-baseweb="tag"] * {
    background-color: transparent !important;
    color: var(--paper) !important;
}

/* Multiselect border hover/focus */
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"] > div:hover {
    border-color: var(--cyber) !important;
}

/* Tabs: cyber underline on the active tab */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { color: var(--muted); font-weight: 600; }
.stTabs [aria-selected="true"] { color: var(--ink) !important; }
.stTabs [data-baseweb="tab-highlight"] {
    background-color: #00FF88 !important;
}

/* Buttons */
.stButton button {
    border-radius: 10px;
    border: 1px solid var(--line);
    border-color: var(--cyber);
    color: var(--cyber-dark);
}
.stButton button:hover {
    border-color: var(--cyber);
    color: var(--cyber-dark);
}

/* Generic white card, used across the app */
.metric-card {
    padding: 2px 10px;
    background: #111827;
    border: 1px solid rgba(0,255,136,0.15);
    box-shadow: 0 0 16px rgba(0,255,136,0.05);
}

/* The one bold move: a dark "spotlight" card for the headline stat */
.spotlight-card {
    padding: 2px 10px;
    background: linear-gradient(135deg, #071018 0%, #0E1A24 100% );
    border: 1px solid rgba(0,255,136,0.25);
}
.spotlight-card .spotlight-value { color: #00FF88; }
.spotlight-card .spotlight-label { color: #B7B4BE; }

/* Small rounded pill used for share/trend context next to a KPI */
.delta-pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    background-color: var(--cyber-soft);
    color: var(--cyber-dark);
    font-size: 12px;
    font-weight: 700;
}
.spotlight-card .delta-pill {
    padding: 2px 10px;
    background-color: rgba(0, 255, 136, 0.16);
    color: var(--cyber);
}

/* Quick-facts row */
.fact-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background-color: var(--paper);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 12px 16px;
}
.fact-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background-color: var(--cyber-soft);
    color: var(--cyber-dark);
    flex-shrink: 0;
}
.fact-text { font-size: 13px; color: var(--ink); }
.fact-text b { color: var(--ink); }
.fact-sub { font-size: 12px; color: var(--muted); }

/* Hero KPI card: bigger, wider, holds the headline number */
.hero-card {
    padding: 2px 10px;
    background: linear-gradient(135deg, #0E1520 0%, #162132 100% );
    border: 1px solid rgba(0,255,136,0.2);
}
.hero-label { font-size: 13px; color: var(--muted); font-weight: 600; }
.hero-value { font-size: 34px; font-weight: 800; color: var(--ink); line-height: 1.15; margin-top: 4px; }

/* cyber-bordered card, the "highlighted" card among the plain white ones */
.metric-card--highlight {
    padding: 2px 10px;
    border: 2px solid #00FF88;
    box-shadow: 0 0 18px rgba(0,255,136,0.15);
}

/* Compact pill-shaped chip for the quick-fact strip */
.stat-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    background-color: var(--paper);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 8px 14px 8px 8px;
}
.stat-chip .chip-avatar {
    display: flex; align-items: center; justify-content: center;
    width: 30px; height: 30px; border-radius: 50%;
    background-color: var(--ink); color: white; flex-shrink: 0;
}
.stat-chip .chip-avatar .material-symbols-rounded { font-size: 16px; }
.stat-chip .chip-text { font-size: 11px; color: var(--muted); line-height: 1.3; }
.stat-chip .chip-value { font-size: 13px; color: var(--ink); font-weight: 700; }

/* Widget card wrapper used for the 3-column grid and the bottom chart */
.widget-title {
    font-size: 14px; font-weight: 700; color: var(--ink);
    margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
}

/* Breakdown rows with an inline mini progress bar (age-group list) */
.list-row { margin-bottom: 12px; }
.list-row .list-row-top { display: flex; justify-content: space-between; font-size: 13px; color: var(--ink); margin-bottom: 4px; }
.list-row .list-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; color: #00FF88}
.mini-bar { background-color: var(--green); border-radius: 999px; height: 6px; overflow: hidden; }
.mini-bar-fill { height: 100%; width: 75%; background: linear-gradient(90deg, #00FF88, #00B8D4); }

/* Ranked leaderboard rows (trip-length leaderboard) */
.rank-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--line); }
.rank-row:last-child { border-bottom: none; }
.rank-badge {
    display: flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 50%;
    background-color: var(--cyber-soft); color: white;;
    font-size: 11px; font-weight: 800; flex-shrink: 0;
}
.rank-row.is-first .rank-badge { background-color: var(--cyber); color: white; }
.rank-name { font-size: 13px; color: var(--ink); font-weight: 600; flex-grow: 1; }
.rank-value { font-size: 12px; color: var(--muted); font-weight: 700; }
</style>
""")


# Use one consistent color pair across the charts.
TWO_TONE_COLORS = ["#00FF88", "#00B8D4"]

# Create the database connection once and reuse it.
@st.cache_resource
def get_connection():
    return st.connection(
        "postgresql",
        type="sql",
        url="postgresql://postgres:123@localhost:5432/ford_gobike"
    )

# Get the values used by the dashboard filters.
@st.cache_data(ttl=600)
def load_filter_options():
    connection = get_connection()
    user_types = connection.query(
        "SELECT DISTINCT user_type::text AS value FROM dim_user ORDER BY value", ttl=600
    )["value"].tolist()
    genders = connection.query(
        "SELECT DISTINCT gender::text AS value FROM dim_user ORDER BY value", ttl=600
    )["value"].tolist()
    age_groups = connection.query(
        "SELECT DISTINCT age_group::text AS value FROM dim_user ORDER BY value", ttl=600
    )["value"].tolist()
    return user_types, genders, age_groups

# Build the SQL filter safely from the selected values.
def _in_clause(column, values, params, prefix):
    names = []
    for index, value in enumerate(values):
        key = f"{prefix}_{index}"
        names.append(f":{key}")
        params[key] = value
    return f"{column} IN ({', '.join(names)})"

# Combine the active filters into one WHERE clause.
def build_filter_clause(user_types, genders, age_groups):
    clauses, params = [], {}
    if user_types:
        clauses.append(_in_clause("u.user_type::text", user_types, params, "ut"))
    if genders:
        clauses.append(_in_clause("u.gender::text", genders, params, "g"))
    if age_groups:
        clauses.append(_in_clause("u.age_group::text", age_groups, params, "ag"))
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return where, params

# Load the trip data after applying the selected filters.
@st.cache_data(ttl=300)
def load_dashboard_data(user_types=(), genders=(), age_groups=()):
    where, params = build_filter_clause(user_types, genders, age_groups)
    query = f"""
        SELECT
            t.trip_id,
            t.duration_sec,
            t.duration_minute,
            t.bike_id,
            ss.station_name AS start_station,
            ss.latitude AS start_lat,
            ss.longitude AS start_lon,
            es.station_name AS end_station,
            es.latitude AS end_lat,
            es.longitude AS end_lon,
            u.gender::text AS gender,
            u.gender::text AS member_gender,
            u.age AS age,
            u.age_group::text AS age_group,
            u.user_type::text AS user_type
        FROM fact_trips AS t
        JOIN dim_station AS ss ON ss.station_id = t.start_station_id
        JOIN dim_station AS es ON es.station_id = t.end_station_id
        JOIN dim_user AS u ON u.user_id = t.user_id
        {where}
    """
    return get_connection().query(query, params=params, ttl=300)

# Build the sidebar and collect the selected filters.
def render_sidebar(user_types, genders, age_groups, total_records):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-icon">
                    <span class="material-symbols-rounded">directions_bike</span>
                </div>
                <div>
                    <div class="sidebar-brand-title">GoBike Analytics</div>
                    <div class="sidebar-brand-subtitle">Trip Intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="sidebar-intro">
                Explore trip behavior, users, and station activity using the filters below.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="sidebar-section-title">FILTERS</div>', unsafe_allow_html=True)
        
        selected_user_types = st.multiselect(
            "User type", user_types, default=user_types, key="ut_filter"
        )
        selected_genders = st.multiselect(
            "Gender", genders, default=genders, key="g_filter"
        )
        selected_age_groups = st.multiselect(
            "Age group", age_groups, default=age_groups, key="ag_filter"
        )

        if st.button("↻  Reset all filters", width='stretch'):
            st.session_state.clear()
            st.rerun()

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section-title">DATASET</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="sidebar-stat">
                <div class="sidebar-stat-icon">
                    <span class="material-symbols-rounded">dataset</span>
                </div>
                <div>
                    <div class="sidebar-stat-value">{total_records:,}</div>
                    <div class="sidebar-stat-label">Active trips</div>
                </div>
            </div>

            <div class="sidebar-stat">
                <div class="sidebar-stat-icon">
                    <span class="material-symbols-rounded">calendar_month</span>
                </div>
                <div>
                    <div class="sidebar-stat-value">February 2019</div>
                    <div class="sidebar-stat-label">Dataset period</div>
                </div>
            </div>

            <div class="sidebar-stat">
                <div class="sidebar-stat-icon">
                    <span class="material-symbols-rounded">tune</span>
                </div>
                <div>
                    <div class="sidebar-stat-value">3 dimensions</div>
                    <div class="sidebar-stat-label">Available filters</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="sidebar-footer">
                <span class="material-symbols-rounded">insights</span>
                <div>
                    <b>Analytics workspace</b>
                    <small>Interactive trip analysis</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return tuple(selected_user_types), tuple(selected_genders), tuple(selected_age_groups)


# Show a small summary item used in the insight row.
def _stat_chip(icon, label, value):
    st.markdown(
        f"""<div class="stat-chip">
            <div class="chip-avatar"><span class="material-symbols-rounded" style="color:#00B8D4;">{icon}</span></div>
            <div>
                <div class="chip-text">{label}</div>
                <div class="chip-value">{value}</div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )


# Format a breakdown row with its percentage bar.
def _list_row_html(color, label, count, pct):
    return f"""<div class="list-row">
        <div class="list-row-top">
            <span><span class="list-dot" style="background-color:{color};"></span>{label}</span>
            <span><b>{count:,}</b>&nbsp;({pct:.0f}%)</span>
        </div>
        <div class="mini-bar"><div class="mini-bar-fill" style="width:{pct:.0f}%;"></div></div>
    </div>"""


# Format one row of the trip-length ranking.
def _rank_row_html(rank, label, count, pct):
    first_class = " is-first" if rank == 1 else ""
    return f"""<div class="rank-row{first_class}">
        <div class="rank-badge">{rank}</div>
        <div class="rank-name">{label}</div>
        <div class="rank-value">{count:,} trips · {pct:.0f}%</div>
    </div>"""


# Build the main overview with KPIs and summary charts.
def render_overview_section(data, total_raw_count):
    if data.empty:
        st.info("No trips match the selected filters.")
        return

    # Calculate the main values shown in the KPI cards.
    total_trips = len(data)
    average_duration = data["duration_minute"].mean()
    distinct_bikes = data["bike_id"].nunique()
    subscriber_share = (data["user_type"] == "Subscriber").mean() * 100
    filtered_percentage = (total_trips / total_raw_count) * 100 if total_raw_count > 0 else 100
    top_age_group = data.groupby("age_group").size().idxmax()
    top_age_group_share = (data["age_group"] == top_age_group).mean() * 100

    # Give the main KPI a little more visual weight than the others.
    hero_col, c2, c3, c4, c5 = st.columns([1.4, 1, 1, 1, 1])

    with hero_col:
        st.markdown(
            f"""
            <div class="hero-card">
                <div class="hero-label">Total trips</div>
                <div class="hero-value">{total_trips:,}</div>
                <div style="margin-top:10px;">
                    <span class="delta-pill" style="color: #86828F;">
                        {filtered_percentage:.0f}% of all trips
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""<div class="metric-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span class="material-symbols-rounded" style="color:#00FF88;">schedule</span>
                    <span style="color: #86828F; font-size: 13px; font-weight: 600;">Avg. duration</span>
                </div>
                <div style="font-size: 22px; font-weight: 700; color: #FFFFFF;">{average_duration:.1f} min</div>
                <div style="margin-top:6px;"><span class="delta-pill" style="color: #86828F;">   </span></div>
            </div>""",
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""<div class="metric-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span class="material-symbols-rounded" style="color:#00FF88;">pedal_bike</span>
                    <span style="color: #86828F; font-size: 13px; font-weight: 600;">Distinct bikes</span>
                </div>
                <div style="font-size: 22px; font-weight: 700; color: #FFFFFF;">{distinct_bikes:,}</div>
                <div style="margin-top:6px;"><span class="delta-pill" style="color: #86828F;">   </span></div>
            </div>""",
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""<div class="metric-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span class="material-symbols-rounded" style="color:#00FF88;">groups</span>
                    <span style="color: #86828F; font-size: 13px; font-weight: 600;" class="spotlight-label">Subscriber share</span>
                </div>
                <div style="font-size: 22px; font-weight: 700; color: #FFFFFF;">{subscriber_share:.0f}%</div>
                <div style="margin-top:6px;"><span class="delta-pill" style="color: #86828F;">   </span></div>
            </div>""",
            unsafe_allow_html=True
        )
    with c5:
        st.markdown(
            f"""<div class="metric-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span class="material-symbols-rounded" style="color:#00FF88;">groups</span>
                    <span style="color: #86828F; font-size: 13px; font-weight: 600;">Top age group</span>
                </div>
                <div style="font-size: 22px; font-weight: 700; color: #FFFFFF;">{top_age_group}</div>
                <div style="margin-top:6px;"><span class="delta-pill" style="color: #86828F;">{top_age_group_share:.0f}% of trips</span></div>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    # Pull a few quick insights for the summary strip.
    lead_gender = data["gender"].value_counts().idxmax()
    lead_gender_share = (data["gender"] == lead_gender).mean() * 100
    busiest_bike = data["bike_id"].value_counts().idxmax()
    busiest_bike_trips = int(data["bike_id"].value_counts().max())
    trips_per_bike = total_trips / distinct_bikes if distinct_bikes else 0

    chip1, chip2, chip3, chip4 = st.columns(4)
    with chip1:
        _stat_chip("person", "Leading gender", f"{lead_gender} · {lead_gender_share:.0f}%")
    with chip2:
        _stat_chip("pedal_bike", "Busiest bike", f"#{busiest_bike} · {busiest_bike_trips:,} trips")
    with chip3:
        _stat_chip("bar_chart", "Trips per bike", f"{trips_per_bike:.1f} avg")
    with chip4:
        _stat_chip("military_tech", "Subscriber lead", f"+{(2 * subscriber_share - 100):.0f} pts vs Customer")

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    # Arrange the three summary widgets side by side.
    #col_a, col_b, col_c = st.columns(3)
    col_a, col_b = st.columns(2)
    with col_a:
        age_counts = data["age_group"].value_counts()
        palette = ["#00FF88", "#28FFCD", "#99D9EA"]
        rows_html = "".join(
            _list_row_html(palette[i % len(palette)], str(label), int(count), count / total_trips * 100)
            for i, (label, count) in enumerate(age_counts.items())
        )
        st.markdown(
            f"""<div class="widget-card">
                <div class="widget-title"><span class="material-symbols-rounded" style="color:#00FF88;">groups</span>By age group</div>
                {rows_html}
            </div>""",
            unsafe_allow_html=True
        )

    with col_b:
        bucket_labels = ["Short (<10 min)", "Medium (10-20 min)", "Long (20+ min)"]
        palette = ["#00FF88", "#28FFCD", "#99D9EA"]
        bins = pd.cut(
            data["duration_minute"],
            bins=[-0.01, 10, 20, max(data["duration_minute"].max(), 20.01)],
            labels=bucket_labels,
        )
        bucket_counts = bins.value_counts().reindex(bucket_labels).fillna(0).sort_values(ascending=False)
        rows_html = "".join(
            _rank_row_html(rank, str(label), int(count), count / total_trips * 100)
            for rank, (label, count) in enumerate(bucket_counts.items(), start=1)
        )
        st.markdown(
            f"""<div class="widget-card">
                <div class="widget-title"><span class="material-symbols-rounded" style="color:#00FF88;">emoji_events</span>Trip length leaderboard</div>
                {rows_html}
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    col_c, col_d = st.columns(2)
    with col_c:
    # two charts side by side #Finish the overview with one wider trend chart.
        with st.container(border=True):
            st.markdown(
                '<div class="widget-title"><span class="material-symbols-rounded" style="color:#00FF88;">pie_chart</span>User type share</div>',
                unsafe_allow_html=True
            )
            user_type_counts = data["user_type"].value_counts().reset_index()
            user_type_counts.columns = ["user_type", "trip_count"]
            customer_pct = (
                user_type_counts.loc[
                    user_type_counts["user_type"] == "Customer", 
                    "trip_count"].iloc[0]
                      / user_type_counts["trip_count"].sum()* 100
            )
            fig_donut = px.pie(
                user_type_counts, names="user_type", values="trip_count", hole=0.62, color="user_type", color_discrete_map=COLORS
            )
            fig_donut.update_traces(textposition="outside", textinfo="percent+label")
            fig_donut.update_layout(
                margin=dict(t=10, b=10, l=0, r=0), showlegend=True, height=320,
                font=dict(color="#E2E8F0"), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="#0A0F14",
            )
            st.plotly_chart(fig_donut, width='stretch')
            st.markdown(
                        f"""<div class="page-subtitle" align = "center">Customers account for only {customer_pct:.1f}% of all trips while Subscribers account for the remaining {100-customer_pct:.1f}%</div>""",
                        unsafe_allow_html=True
                    ) 
    with col_d:
       with st.container(border=True):
            st.markdown(
                '<div class="widget-title"><span class="material-symbols-rounded" style="color:#00FF88;">show_chart</span>Ride duration Profile</div>',
                unsafe_allow_html=True
            )
            bar_data = data.groupby("user_type")["duration_minute"].mean().reset_index()
            bar_data.columns = ["user_type", "duration_minute"]
            overall_avg = data["duration_minute"].mean()
            #st.dataframe(bar_data)
            fig_hbar = px.bar(
                bar_data, x="duration_minute", y="user_type", color="user_type", 
                labels={"duration_minute": "Average Duration (Minutes)", "user_type": "User Type"},
                color_discrete_map=COLORS, orientation= "h", 
            )
            fig_hbar.add_vline(x=overall_avg,
                line_dash="dash",
                line_color="#00FF88",
                opacity=0.6
            )
            fig_hbar.update_traces(texttemplate="%{x:.1f} min", textposition="inside")
            fig_hbar.update_layout(
                hovermode="x unified", margin=dict(t=10, b=0, l=0, r=0), height=320,
                font=dict(color="#E2E8F0"), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="#0A0F14",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None),
                showlegend=False,
            )
            max_val = bar_data["duration_minute"].max()
            fig_hbar.update_xaxes(range=[0, max_val * 1.15])
            fig_hbar.update_xaxes(showgrid=True,
                                gridcolor="rgba(0,255,136,0.25)",
                                zeroline=False
            )
            fig_hbar.update_yaxes(gridcolor="rgba(0,255,136,0.15)")
            fig_hbar.update_yaxes(title=None)
            diff = (
                bar_data["duration_minute"].max()
                - bar_data["duration_minute"].min()
            )

            pct = diff / bar_data["duration_minute"].min() * 100
            st.plotly_chart(fig_hbar, width='stretch')
            st.markdown(
                        f"""<div class="page-subtitle" align = "center">Customers ride {pct:.1f}% longer on average</div>""",
                        unsafe_allow_html=True
                    )
# Show the trip-duration analysis over time.
def render_time_section(data):
    if data.empty:
        return

    duration_counts = data.groupby(data["duration_minute"].round(0), as_index=False).size()
    duration_counts.columns = ["duration_minute", "trips"]

    fig = px.bar(
        duration_counts,
        x="duration_minute",
        y="trips",
        title="Trip duration distribution",
        labels={"duration_minute": "Duration (minutes)", "trips": "Trip Count"},
        color_discrete_sequence=["#00FF88"]
    )
    
    fig.update_traces(marker_cornerradius=4, opacity=0.9)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#0A0F14",
        font=dict(color="#E2E8F0"),
        margin=dict(t=30, b=0, l=0, r=0),
        height=380,
        hovermode="x unified"
    )
    fig.update_xaxes(gridcolor="rgba(0,255,136,0.15)")
    fig.update_yaxes(gridcolor="rgba(0,255,136,0.15)")
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.subheader("Duration & Time Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(youssef_charts.fig_duration_by_gender(data), width='stretch')#needs to be replaced
    with col2:
        st.plotly_chart(youssef_charts.fig_duration_by_user_type(data), width='stretch')

# Show the main user and demographic analysis.
def render_user_section(data):
    if data.empty:
        st.info("No trips match the selected filters.")
        return

    demographics = (
        data.groupby(["age_group", "gender"], as_index=False)
        .size()
        .rename(columns={"size": "trip_count"})
    )
    age_gender_chart = px.bar(
        demographics,
        x="age_group",
        y="trip_count",
        color="gender",
        barmode="group",
        title="Trips by age group and gender",
        labels={"trip_count": "Trips", "age_group": "Age group", "gender": "Gender"},
        color_discrete_sequence=TWO_TONE_COLORS
    )

    user_type_counts = data["user_type"].value_counts().reset_index()
    user_type_counts.columns = ["user_type", "trip_count"]
    user_type_chart = px.pie(
        user_type_counts, names="user_type", values="trip_count", title="Subscriber vs Customer",
        color_discrete_sequence=TWO_TONE_COLORS
    )

    left, right = st.columns(2)
    left.plotly_chart(age_gender_chart, width='stretch')
    right.plotly_chart(user_type_chart, width='stretch')

    st.markdown("---")
    st.subheader("Detailed User Demographics")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(youssef_charts.fig_user_type_donut(data), width='stretch')
        st.plotly_chart(youssef_charts.fig_gender_bar(data), width='stretch')
    with col2:
        st.plotly_chart(youssef_charts.fig_age_group_bar(data), width='stretch')
        st.plotly_chart(youssef_charts.fig_age_histogram(data), width='stretch')

# Render the station and trip-location analysis.
def render_station_section(data):
    if data.empty:
        st.info("No trips match the selected filters.")
        return

    if heba_charts and hasattr(heba_charts, "render_station_tab"):
        try:
            heba_charts.render_station_tab(data)
            return
        except Exception as e:
            st.error(f"Error rendering Heba's charts: {e}")
    else:
        st.info("Waiting on Heba's station/spatial charts module.")

# Run the dashboard from loading data to rendering each tab.
def main():
    st.markdown(
        """
        <div class="page-header">
            <div>
                <div class="page-eyebrow" style="color: #86828F;">TRANSPORTATION ANALYTICS</div>
                <div class="page-title">
                    <span class="material-symbols-rounded">directions_bike</span>
                    Ford GoBike Analytics
                </div>
                <div class="page-subtitle">
                    Interactive trip, user, and station performance dashboard
                </div>
            </div>
            <div class="page-period">
                <span class="material-symbols-rounded">calendar_month</span>
                February 2019
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load the filter options before building the dashboard.
    try:
        user_types, genders, age_groups = load_filter_options()
    except Exception as error:
        st.error(
            "Couldn't load filter options from PostgreSQL. Make sure Mina's "
            "schema and Shahd's connection are set up before running this app."
        )
        st.exception(error)
        return

    raw_data = load_dashboard_data(tuple(user_types), tuple(genders), tuple(age_groups))
    
    selected_user_types, selected_genders, selected_age_groups = render_sidebar(
        user_types, genders, age_groups, len(raw_data)
    )

    try:
        data = load_dashboard_data(selected_user_types, selected_genders, selected_age_groups)
    except Exception as error:
        st.error("Couldn't load trip data for the selected filters.")
        st.exception(error)
        return

    # Split the dashboard into clear analysis sections.
    tab_overview, tab_time, tab_users, tab_stations = st.tabs(
        ["📈 Overview KPIs", "📅 Time Analysis", "👥 User Analysis", "🗺️ Station/Trip Analysis"]
    )
    with tab_overview:
        render_overview_section(data, len(raw_data))
    with tab_time:
        render_time_section(data)
    with tab_users:
        render_user_section(data)
    with tab_stations:
        render_station_section(data)

if __name__ == "__main__":
    main()
