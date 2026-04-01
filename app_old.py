import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Tuple, Optional
import io
import re

# Page config
st.set_page_config(
    page_title="Hopper Survey Explorer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme
st.markdown("""
<style>
    /* Force light theme */
    [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }
    .stApp {
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Brand Design System Colors
COLORS = {
    # Base / UI
    "black":    "#000000",
    "slate_80": "#354156",
    "slate_60": "#556381",
    "slate_50": "#7B8AA7",
    "slate_40": "#ABB7CD",
    "slate_30": "#BEC8DA",
    "slate_20": "#E8ECF2",
    "slate_10": "#F4F6F9",
    "white":    "#FFFFFF",

    # Primary chart gradient families
    "pink_red":       "#F23749",
    "pink_hot":       "#EF0BB6",
    "purple_vivid":   "#CE0939",
    "purple_mid":     "#9F2ECC",
    "purple_blue":    "#6F3EEE",
    "blue_primary":   "#2A7CED",
    "blue_light":     "#198CEC",
    "blue_sky":       "#2CC0E8",
    "teal":           "#22CAB4",
    "teal_mid":       "#26ABC8",
}

# Chart color palettes
CHART_PALETTE = [
    "#198CEC",  # blue light
    "#2AB4E8",  # custom blue
    "#F23749",  # pink red
    "#6F3EEE",  # purple blue
    "#22CAB4",  # teal
    "#EF0BB6",  # pink hot
    "#9F2ECC",  # purple mid
    "#2CC0E8",  # blue sky
]

SEGMENT_A_COLOR = "#198CEC"   # blue light
SEGMENT_B_COLOR = "#2AB4E8"   # custom blue
TOTAL_COLOR     = "#354156"   # slate 80

# Chart layout settings
CHART_LAYOUT = dict(
    paper_bgcolor="white",  # Force white background
    plot_bgcolor="white",   # Force white background
    font=dict(family="'Proxima Nova', 'Nunito Sans', sans-serif", color="#354156"),
    title_font=dict(size=15, color="#354156", family="'Proxima Nova', 'Nunito Sans', sans-serif"),
    xaxis=dict(
        tickfont=dict(size=11, color="#354156"),  # Changed to darker color for better readability
        showgrid=False,
        zeroline=False,
    ),
    yaxis=dict(
        tickfont=dict(size=11, color="#354156"),  # Changed to darker color for better readability
        gridcolor="#E8ECF2",
        gridwidth=1,
        zeroline=False,
    ),
    legend=dict(font=dict(size=12, color="#354156")),
    margin=dict(t=20, b=80, l=60, r=30),  # Reduced top margin
    bargap=0.25,
)

# Custom CSS for styling
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Proxima Nova', 'Nunito Sans', sans-serif;
        background-color: white !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F4F6F9;
        border-right: 1px solid #E8ECF2;
    }

    /* Question selector label */
    .question-label {
        font-size: 13px;
        font-weight: 600;
        color: #354156;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Metric/stat chips */
    .stat-chip {
        background: #E8ECF2;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 13px;
        color: #354156;  /* Changed to darker color for better readability */
        display: inline-block;
        margin: 2px;
        font-weight: 500;
    }

    /* Chart container card - simplified */
    .chart-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 4px rgba(53,65,86,0.08);
        margin-top: 10px;
    }

    /* Top accent bar */
    .top-bar {
        height: 4px;
        background: #2A7CED;
        width: 100%;
        margin-top: -1rem;
        margin-bottom: 1rem;
    }

    /* Footer text */
    .sidebar-footer {
        font-size: 11px;
        color: #556381;  /* Changed to darker color for better readability */
        line-height: 1.4;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E8ECF2;
    }

    /* Product category badges */
    .category-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .category-disruption { background: #FEE2E2; color: #DC2626; }
    .category-air { background: #DBEAFE; color: #2563EB; }
    .category-hotel { background: #E0E7FF; color: #4F46E5; }

    /* Force light theme on Plotly charts */
    .js-plotly-plot .plotly {
        background-color: white !important;
    }

    /* Fix Streamlit default text colors for light mode */

    /* Subheaders (chart titles) */
    .stMarkdown h3,
    [data-testid="stMarkdownContainer"] h3,
    .element-container h3 {
        color: #1A1A1A !important;
        font-weight: 600 !important;
    }

    /* Radio buttons and their labels - comprehensive fix */
    .stRadio > label,
    [data-testid="stRadio"] > label,
    [data-testid="stWidgetLabel"] {
        color: #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* Radio button options - multiple selectors to ensure coverage */
    .stRadio [role="radiogroup"] label,
    [data-baseweb="radio"] label,
    [data-baseweb="radio"] > div,
    [data-baseweb="radio"] span,
    .stRadio div[role="radiogroup"] > div label,
    .stRadio div[role="radiogroup"] > div > label > div,
    div[data-baseweb="radio"] div,
    div[role="radiogroup"] label {
        color: #354156 !important;
        font-weight: 400 !important;
    }

    /* Target the actual text spans inside radio options */
    [data-baseweb="radio"] label > div:last-child,
    [data-baseweb="radio"] label span,
    [role="radio"] + div,
    [role="radio"] ~ div,
    [data-testid="stMarkdownContainer"] [role="radiogroup"] * {
        color: #354156 !important;
    }

    /* Select boxes and their labels */
    .stSelectbox > label,
    [data-testid="stSelectbox"] > label {
        color: #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* Multi-select labels */
    .stMultiSelect > label,
    [data-testid="stMultiSelect"] > label {
        color: #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* Checkbox labels */
    .stCheckbox > label,
    [data-testid="stCheckbox"] > label {
        color: #354156 !important;
    }

    /* Caption text under dropdowns */
    .stCaption,
    [data-testid="stCaption"] {
        color: #354156 !important;
    }

    /* Expander headers */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary {
        color: #1A1A1A !important;
        font-weight: 500 !important;
    }

    /* Warning/Error/Info messages */
    .stAlert {
        color: #1A1A1A !important;
    }

    /* General text */
    .stMarkdown p,
    [data-testid="stMarkdownContainer"] p {
        color: #354156 !important;
    }

    /* Force all text in main area to be dark */
    [data-testid="stAppViewContainer"] {
        color: #1A1A1A !important;
    }

    /* Ensure sidebar text is also readable */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #1A1A1A !important;
    }

    /* Global override for any remaining white/light text */
    .stApp [data-baseweb],
    .stApp [data-baseweb] * {
        color: #354156 !important;
    }

    /* Specific fix for radio button text that might be white */
    input[type="radio"] + div,
    input[type="radio"] ~ label,
    input[type="radio"] ~ * {
        color: #354156 !important;
    }

    /* Override any inline styles that might be setting white color */
    [style*="color: rgb(255, 255, 255)"],
    [style*="color:#ffffff"],
    [style*="color: #ffffff"],
    [style*="color:#fff"],
    [style*="color: #fff"],
    [style*="color: white"] {
        color: #354156 !important;
    }

    /* Ensure all text in radio groups is visible */
    div[role="radiogroup"] *,
    div[role="radiogroup"] label,
    div[role="radiogroup"] span,
    div[role="radiogroup"] div {
        color: #354156 !important;
        background-color: transparent !important;
    }

    /* Ultimate override for radio buttons - target every possible selector */
    .stRadio,
    .stRadio *,
    .stRadio > div,
    .stRadio > div > div,
    .stRadio label,
    .stRadio label *,
    .stRadio label div,
    .stRadio [role="radiogroup"],
    .stRadio [role="radiogroup"] *,
    [data-testid*="radio"] *,
    [data-baseweb*="radio"] *,
    div[class*="radio"] label,
    div[class*="radio"] span,
    div[class*="radio"] div {
        color: #354156 !important;
    }

    /* Specifically target the problematic "# Raw count" text */
    .stRadio label:contains("Raw"),
    .stRadio label:contains("Percentage"),
    .stRadio div:contains("Raw"),
    .stRadio div:contains("Percentage") {
        color: #354156 !important;
    }
</style>
"""

# Natural sorting function
def natural_sort_key(s):
    """Sort strings naturally - F1, F2, F3... not F1, F11, F2"""
    return [int(text) if text.isdigit() else text for text in re.split('([0-9]+)', s)]

# Check if kaleido is available for PNG export
def check_kaleido():
    try:
        import kaleido
        return True
    except ImportError:
        return False

# Load and cache data
@st.cache_data
def load_data():
    with open("survey_data.json") as f:
        return json.load(f)

def get_segment_data(question: Dict, segment_label: str, mode: str = "pct") -> List[Tuple[str, float]]:
    """Returns list of (response_option, value) for the given segment."""
    key = "pct" if mode == "pct" else "count"
    return [
        (r["option"], r[key].get(segment_label, 0))
        for r in question["responses"]
    ]

def extract_demographic_groups(question: Dict) -> Dict[str, List[str]]:
    """Extract demographic groups and their segments from a question."""
    groups = {"Total (all respondents)": ["Total"]}

    for col_idx, group_name in question["category_groups"].items():
        if col_idx != "1":  # Skip Total column
            label = question["columns"][col_idx]
            if group_name not in groups:
                groups[group_name] = []
            if label not in groups[group_name]:
                groups[group_name].append(label)

    return groups

def is_mutually_exclusive_question(question: Dict) -> bool:
    """Check if a question has mutually exclusive answers (single-select)."""
    try:
        # Get the total base
        total_base = question["bases"].get("Total", 0)
        if total_base == 0:
            return False

        # Sum up all the counts for the Total column
        total_count_sum = sum(
            response["count"].get("Total", 0)
            for response in question["responses"]
        )

        # If sum equals base, it's single-select (mutually exclusive)
        # Allow for small rounding differences
        return abs(total_count_sum - total_base) <= 5

    except Exception:
        return False

def create_pie_chart(question: Dict, segment_label: str, mode: str = "pct") -> go.Figure:
    """Create a pie chart for mutually exclusive questions."""
    data = get_segment_data(question, segment_label, mode)

    labels = [d[0] for d in data]
    values = [d[1] for d in data]

    fig = go.Figure()

    # Create pie trace
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=CHART_PALETTE[:len(labels)],
            line=dict(color='#FFFFFF', width=2)
        ),
        textposition='outside',
        textinfo='label+percent' if mode == "pct" else 'label+value',
        textfont=dict(size=11, color="#354156"),
        hovertemplate='<b>%{label}</b><br>' +
                      ('%{percent}' if mode == "pct" else 'Count: %{value}') +
                      '<extra></extra>'
    ))

    # Update layout for pie chart
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="'Proxima Nova', 'Nunito Sans', sans-serif", color="#354156"),
        showlegend=True,
        legend=dict(
            font=dict(size=11, color="#354156", family="'Proxima Nova', 'Nunito Sans', sans-serif"),
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            bgcolor="rgba(255,255,255,0.9)"  # Add white background to legend for clarity
        ),
        margin=dict(t=20, b=40, l=40, r=200)
    )

    return fig

def create_single_chart(question: Dict, segment_label: str, mode: str = "pct") -> go.Figure:
    """Create a single segment bar chart."""
    data = get_segment_data(question, segment_label, mode)

    x_values = [d[0] for d in data]
    y_values = [d[1] for d in data]

    fig = go.Figure()

    # Add bar trace
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=CHART_PALETTE[0],
        text=[f"{v:.1f}%" if mode == "pct" else f"n={int(v)}" for v in y_values],
        textposition='outside',
        textfont=dict(size=12, color="#354156"),
        name=segment_label,
        showlegend=False
    ))

    # Update layout
    fig.update_layout(**CHART_LAYOUT)

    # Set y-axis range and format
    if mode == "pct":
        fig.update_yaxes(
            range=[0, max(y_values) * 1.15 if y_values else 105],
            tickformat=".0f",
            ticksuffix="%"
        )
    else:
        fig.update_yaxes(
            range=[0, max(y_values) * 1.15 if y_values else 100]
        )

    # Update x-axis
    fig.update_xaxes(tickangle=-45 if len(x_values) > 8 else 0)

    return fig

def create_multi_segment_chart(question: Dict, segments: List[str],
                              mode: str = "pct", show_total: bool = False) -> go.Figure:
    """Create a grouped bar chart comparing multiple segments."""
    fig = go.Figure()

    # Get data for all segments
    all_data = []
    for segment in segments:
        data = get_segment_data(question, segment, mode)
        all_data.append((segment, data))

    # Get x values from first segment
    x_values = [d[0] for d in all_data[0][1]] if all_data else []

    # Add traces for each segment
    for idx, (segment_name, segment_data) in enumerate(all_data):
        y_values = [d[1] for d in segment_data]

        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            marker_color=CHART_PALETTE[idx % len(CHART_PALETTE)],
            text=[f"{v:.1f}%" if mode == "pct" else f"n={int(v)}" for v in y_values],
            textposition='outside',
            textfont=dict(size=11, color="#354156"),
            name=segment_name
        ))

    # Optionally add Total
    if show_total and "Total" not in segments:
        total_data = get_segment_data(question, "Total", mode)
        y_values_total = [d[1] for d in total_data]

        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values_total,
            marker_color=TOTAL_COLOR,
            text=[f"{v:.1f}%" if mode == "pct" else f"n={int(v)}" for v in y_values_total],
            textposition='outside',
            textfont=dict(size=11, color="#354156"),
            name="Total"
        ))

    # Update layout
    fig.update_layout(**CHART_LAYOUT)
    fig.update_layout(barmode='group')

    # Set y-axis range and format
    max_val = 0
    for _, segment_data in all_data:
        segment_max = max([d[1] for d in segment_data], default=0)
        max_val = max(max_val, segment_max)

    if mode == "pct":
        fig.update_yaxes(
            range=[0, min(max_val * 1.15, 105)],
            tickformat=".0f",
            ticksuffix="%"
        )
    else:
        fig.update_yaxes(
            range=[0, max_val * 1.15 if max_val else 100]
        )

    # Update x-axis
    fig.update_xaxes(tickangle=-45 if len(x_values) > 8 else 0)

    return fig

def create_data_table(question: Dict, segments: List[str],
                     show_total_in_table: bool = True) -> pd.DataFrame:
    """Create a data table for the current view."""
    rows = []

    for response in question["responses"]:
        row = {"Response": response["option"]}

        # Add data for each selected segment
        for segment in segments:
            row[f"{segment} %"] = f"{response['pct'].get(segment, 0):.1f}%"
            row[f"{segment} n"] = int(response['count'].get(segment, 0))

        # Add Total data if requested and not already included
        if show_total_in_table and "Total" not in segments:
            row["Total %"] = f"{response['pct'].get('Total', 0):.1f}%"
            row["Total n"] = int(response['count'].get('Total', 0))

        rows.append(row)

    return pd.DataFrame(rows)

# Main app
def main():
    # Inject custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # JavaScript to force all text to be dark (backup solution)
    st.markdown("""
    <script>
    // Force all radio button text to be dark
    const fixRadioColors = () => {
        const radios = document.querySelectorAll('[role="radiogroup"] label, [data-baseweb="radio"] div');
        radios.forEach(el => {
            el.style.color = '#354156';
            el.style.setProperty('color', '#354156', 'important');
        });
    };

    // Run on page load and periodically
    if (document.readyState === 'complete') {
        fixRadioColors();
    } else {
        window.addEventListener('load', fixRadioColors);
    }
    setInterval(fixRadioColors, 500);
    </script>
    """, unsafe_allow_html=True)

    # Top accent bar
    st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

    # Load data
    data = load_data()

    # Sidebar
    with st.sidebar:
        st.markdown('<p class="question-label">Select Question</p>', unsafe_allow_html=True)

        # Group questions by product category
        question_groups = {
            "Profile Questions": [],
            "Disruption": [],
            "Air Flexibility": [],
            "Hotel Flexibility": []
        }

        for idx, q in enumerate(data):
            sheet = q['sheet']
            formatted = f"{sheet} — {q['question']}"

            if sheet.startswith('P'):
                question_groups["Profile Questions"].append((idx, formatted, sheet))
            elif sheet.startswith('D') or sheet.startswith('DA'):
                question_groups["Disruption"].append((idx, formatted, sheet))
            elif sheet.startswith('F'):
                question_groups["Air Flexibility"].append((idx, formatted, sheet))
            elif sheet.startswith('HF'):
                question_groups["Hotel Flexibility"].append((idx, formatted, sheet))

        # Sort questions within each group naturally
        for group_name in question_groups:
            question_groups[group_name].sort(key=lambda x: natural_sort_key(x[2]))

        # Create grouped dropdown
        selected_group = st.selectbox(
            "Product Category",
            options=list(question_groups.keys()),
            key="product_category",
            index=1  # Default to Disruption
        )

        # Filter questions based on selected group
        question_options = question_groups[selected_group]

        # Question selector
        if question_options:
            selected_question_idx = st.selectbox(
                label="Question",
                options=[idx for idx, _, _ in question_options],
                format_func=lambda x: next((label for idx, label, _ in question_options if idx == x), ""),
                key="question_selector",
                label_visibility="visible"
            )
        else:
            st.error("No questions in this category")
            selected_question_idx = 0

        current_question = data[selected_question_idx]
        st.caption(current_question["question"])

        st.divider()

        # Extract demographic groups for current question
        demographic_groups = extract_demographic_groups(current_question)

        # Comparison mode selection
        st.markdown('<p class="question-label">Comparison Mode</p>', unsafe_allow_html=True)
        comparison_mode = st.radio(
            "",
            options=["Single Segment", "Compare Within Group", "Compare Across Groups"],
            key="comparison_mode",
            label_visibility="collapsed"
        )

        # Force radio button text to be dark
        st.markdown("""
        <style>
        /* Fix for white radio button text */
        div[data-testid="stRadio"] label div {
            color: #354156 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.divider()

        selected_segments = []

        if comparison_mode == "Single Segment":
            # Single segment selection
            st.markdown('<p class="question-label">Select Segment</p>', unsafe_allow_html=True)

            group_a = st.selectbox(
                "Group",
                options=list(demographic_groups.keys()),
                key="single_group"
            )

            segment_a = st.selectbox(
                "Segment",
                options=demographic_groups[group_a] if group_a in demographic_groups else ["Total"],
                key="single_segment"
            )
            selected_segments = [segment_a]

        elif comparison_mode == "Compare Within Group":
            # Multi-segment selection within same group
            st.markdown('<p class="question-label">Select Group and Segments</p>', unsafe_allow_html=True)

            group = st.selectbox(
                "Group",
                options=list(demographic_groups.keys()),
                key="multi_group"
            )

            available_segments = demographic_groups[group] if group in demographic_groups else []

            # Multi-select for segments
            selected_segments = st.multiselect(
                "Select segments to compare",
                options=available_segments,
                default=available_segments[:2] if len(available_segments) >= 2 else available_segments,
                key="multi_segments"
            )

            # Option to include total
            if group != "Total (all respondents)":
                show_total = st.checkbox("Also show Total", key="show_total_multi", value=False)
            else:
                show_total = False

        else:  # Compare Across Groups
            # Legacy mode - compare two segments from potentially different groups
            st.markdown('<p class="question-label">Segment A</p>', unsafe_allow_html=True)

            group_a = st.selectbox(
                "Group",
                options=list(demographic_groups.keys()),
                key="group_a"
            )

            segment_a = st.selectbox(
                "Segment",
                options=demographic_groups[group_a] if group_a in demographic_groups else ["Total"],
                key="segment_a"
            )

            st.markdown('<p class="question-label">Segment B</p>', unsafe_allow_html=True)

            group_b = st.selectbox(
                "Group",
                options=list(demographic_groups.keys()),
                key="group_b"
            )

            segment_b = st.selectbox(
                "Segment",
                options=demographic_groups[group_b] if group_b in demographic_groups else ["Total"],
                key="segment_b"
            )

            selected_segments = [segment_a, segment_b]

            # Option to show total
            show_total = st.checkbox("Also show Total", key="show_total_cross", value=False)

        st.divider()

        # Display mode toggle
        st.markdown('<p class="question-label">Display Mode</p>', unsafe_allow_html=True)
        display_mode = st.radio(
            "",
            options=["% Percentage", "# Raw count"],
            key="display_mode",
            label_visibility="collapsed"
        )
        mode = "pct" if display_mode == "% Percentage" else "count"

        # Force radio button text to be dark
        st.markdown("""
        <style>
        /* Emergency fix for white radio button text */
        div[data-testid="stRadio"] > div > div > div > div > label > div:last-child {
            color: #354156 !important;
        }
        div[data-testid="stRadio"] label {
            color: #354156 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # Chart type toggle (only for single segment and mutually exclusive questions)
        is_single_select = is_mutually_exclusive_question(current_question)
        chart_type = "bar"  # default

        if is_single_select and comparison_mode == "Single Segment":
            st.divider()
            st.markdown('<p class="question-label">Chart Type</p>', unsafe_allow_html=True)
            chart_type_selection = st.radio(
                "",
                options=["📊 Bar Chart", "🥧 Pie Chart"],
                key="chart_type",
                label_visibility="collapsed"
            )
            chart_type = "pie" if chart_type_selection == "🥧 Pie Chart" else "bar"

        # Footer
        st.markdown(
            '<div class="sidebar-footer">'
            'Hopper Travel Flexibility Survey<br>'
            'n=1,030 | US Adults who flew in past 12 months'
            '</div>',
            unsafe_allow_html=True
        )

    # Main panel
    # Show product category badge
    sheet = current_question["sheet"]
    if sheet.startswith('D') or sheet.startswith('DA'):
        st.markdown('<span class="category-badge category-disruption">DISRUPTION</span>', unsafe_allow_html=True)
    elif sheet.startswith('F'):
        st.markdown('<span class="category-badge category-air">AIR FLEXIBILITY</span>', unsafe_allow_html=True)
    elif sheet.startswith('HF'):
        st.markdown('<span class="category-badge category-hotel">HOTEL FLEXIBILITY</span>', unsafe_allow_html=True)

    st.subheader(current_question["question"])

    # Base stats
    if selected_segments:
        base_html = ""
        for seg in selected_segments:
            base_html += f'<span class="stat-chip">{seg}: n={current_question["bases"].get(seg, 0)}</span> '
        st.markdown(base_html, unsafe_allow_html=True)

    # Create and display chart in a styled container
    with st.container():
        if len(selected_segments) == 0:
            st.warning("Please select at least one segment")
        elif len(selected_segments) == 1 and chart_type == "pie" and is_single_select:
            fig = create_pie_chart(current_question, selected_segments[0], mode)
        elif len(selected_segments) == 1:
            fig = create_single_chart(current_question, selected_segments[0], mode)
        else:
            # Multi-segment comparison
            if comparison_mode == "Compare Within Group":
                fig = create_multi_segment_chart(current_question, selected_segments, mode,
                                                show_total if 'show_total' in locals() else False)
            else:  # Compare Across Groups
                fig = create_multi_segment_chart(current_question, selected_segments, mode,
                                                show_total if 'show_total' in locals() else False)

        # Display chart
        if 'fig' in locals():
            st.plotly_chart(fig, use_container_width=True, key="main_chart",
                          config={'displayModeBar': False})

            # Export buttons
            col1, col2, col3 = st.columns([1, 1, 3])

            sheet_id = current_question["sheet"].lower()
            segment_label = "_".join([s.lower().replace(" ", "_").replace("+", "plus")
                                     for s in selected_segments[:2]])  # Limit filename length

            # HTML export (always available)
            with col1:
                html_string = fig.to_html(include_plotlyjs='cdn')
                st.download_button(
                    label="⬇ Download HTML",
                    data=html_string,
                    file_name=f"hopper_{sheet_id}_{segment_label}.html",
                    mime="text/html"
                )

            # PNG export (only if kaleido works)
            with col2:
                if check_kaleido():
                    try:
                        img_bytes = fig.to_image(format="png", width=1400, height=700, scale=2)
                        st.download_button(
                            label="⬇ Download PNG",
                            data=img_bytes,
                            file_name=f"hopper_{sheet_id}_{segment_label}.png",
                            mime="image/png"
                        )
                    except Exception:
                        pass  # Silently skip if export fails

    # Data table
    if selected_segments:
        with st.expander("View data table"):
            df = create_data_table(
                current_question,
                selected_segments,
                show_total_in_table='show_total' in locals() and show_total
            )
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()