import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Tuple, Optional
import re
import hashlib
from urllib.parse import urlencode

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="HTS Survey Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Design System
class DesignSystem:
    # Brand Colors
    PRIMARY_BLUE = "#198CEC"
    SECONDARY_BLUE = "#2AB4E8"

    # UI Colors
    BACKGROUND = "#FFFFFF"
    SIDEBAR_BG = "#F5F7FA"
    CARD_BG = "#FFFFFF"

    # Text Colors
    TEXT_PRIMARY = "#1E293B"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#64748B"

    # Accent Colors
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    ERROR = "#EF4444"

    # Chart Colors
    CHART_COLORS = [
        "#198CEC", "#2AB4E8", "#22D3EE", "#0EA5E9",
        "#3B82F6", "#6366F1", "#8B5CF6", "#A855F7"
    ]

    # Semantic Colors
    DISRUPTION_COLOR = "#EF4444"
    AIR_FLEX_COLOR = "#3B82F6"
    HOTEL_FLEX_COLOR = "#8B5CF6"

# Apply professional styling
PROFESSIONAL_CSS = f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Reset and Base Styles */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: {DesignSystem.TEXT_PRIMARY};
        background-color: {DesignSystem.BACKGROUND};
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    /* Main App Container */
    .stApp {{
        background: {DesignSystem.BACKGROUND};
    }}

    /* Remove unwanted lines and borders */
    hr, .stHorizontalBlock > div:first-child {{
        display: none !important;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: {DesignSystem.SIDEBAR_BG};
        border-right: 1px solid #E2E8F0;
        padding-top: 1rem;
    }}

    section[data-testid="stSidebar"] > div {{
        padding: 0 1rem 1rem 1rem;
    }}

    /* Headers and Titles */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif;
        color: {DesignSystem.TEXT_PRIMARY};
        font-weight: 600;
        line-height: 1.2;
    }}

    h1 {{ font-size: 2rem; margin-bottom: 1.5rem; }}
    h2 {{ font-size: 1.5rem; margin-bottom: 1.25rem; }}
    h3 {{ font-size: 1.25rem; margin-bottom: 1rem; }}

    /* Labels and Form Elements */
    .stSelectbox label,
    .stMultiSelect label,
    .stRadio > label,
    .stCheckbox > label,
    [data-testid="stWidgetLabel"] {{
        color: {DesignSystem.TEXT_PRIMARY} !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
    }}

    /* Selectbox Styling */
    [data-baseweb="select"] > div {{
        background-color: {DesignSystem.BACKGROUND} !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 0.5rem !important;
        min-height: 2.5rem !important;
    }}

    [data-baseweb="select"] > div:hover {{
        border-color: {DesignSystem.PRIMARY_BLUE} !important;
    }}

    [data-baseweb="select"] > div:focus-within {{
        border-color: {DesignSystem.PRIMARY_BLUE} !important;
        box-shadow: 0 0 0 3px rgba(25, 140, 236, 0.1) !important;
    }}

    /* Radio Button Styling - MAKE SELECTION CLEARLY VISIBLE */
    [data-baseweb="radio"] {{
        color: {DesignSystem.TEXT_PRIMARY} !important;
    }}

    [data-baseweb="radio"] label {{
        color: {DesignSystem.TEXT_PRIMARY} !important;
        font-size: 0.875rem !important;
        padding: 0.375rem 0 !important;
    }}

    /* Unselected radio button */
    [data-baseweb="radio"] > div:first-child {{
        background-color: white !important;
        border: 2px solid #000000 !important;
        width: 20px !important;
        height: 20px !important;
    }}

    [data-baseweb="radio"]:hover > div:first-child {{
        border-color: #FF0000 !important;
        border-width: 3px !important;
    }}

    /* SELECTED RADIO BUTTON - BRIGHT RED FILLED CIRCLE */
    [data-baseweb="radio"] input:checked ~ div:first-child {{
        background-color: #FF0000 !important;
        border-color: #FF0000 !important;
        border-width: 2px !important;
    }}

    /* Add inner dot for selected radio */
    [data-baseweb="radio"] input:checked ~ div:first-child::after {{
        content: "" !important;
        display: block !important;
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
        background-color: #FF0000 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }}

    /* Make selected radio option HIGHLY VISIBLE with RED */
    [data-baseweb="radio"][aria-checked="true"] {{
        background-color: #FFEBEB !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 0.375rem !important;
        border-left: 4px solid #FF0000 !important;
    }}

    [data-baseweb="radio"][aria-checked="true"] label {{
        color: #000000 !important;
        font-weight: 700 !important;
    }}

    /* CRITICAL: Make the radio circle BRIGHT RED when selected */
    [data-baseweb="radio"][aria-checked="true"] > div:first-child {{
        background-color: #FF0000 !important;
        border-color: #FF0000 !important;
        position: relative !important;
    }}

    /* Add additional targeting for Streamlit radio buttons */
    .stRadio > div > label > div > div:first-child {{
        border: 2px solid #000000 !important;
        width: 18px !important;
        height: 18px !important;
    }}

    .stRadio > div > label[aria-checked="true"] > div > div:first-child {{
        background-color: #FF0000 !important;
        border-color: #FF0000 !important;
        box-shadow: inset 0 0 0 3px #FFFFFF !important;
    }}

    /* Additional styling for radio group container to highlight selection */
    .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"] {{
        background-color: #FFEBEB !important;
        margin-left: -0.5rem !important;
        padding-left: 0.75rem !important;
        border-left: 4px solid #FF0000 !important;
    }}

    /* Multi-select Styling */
    [data-baseweb="tag"] {{
        background-color: {DesignSystem.PRIMARY_BLUE} !important;
        color: white !important;
        border-radius: 0.375rem !important;
        font-size: 0.875rem !important;
        padding: 0.25rem 0.5rem !important;
    }}

    /* Button Styling */
    .stButton > button {{
        background-color: {DesignSystem.PRIMARY_BLUE};
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }}

    .stButton > button:hover {{
        background-color: #1578CC;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}

    .stDownloadButton > button {{
        background-color: {DesignSystem.BACKGROUND};
        color: {DesignSystem.PRIMARY_BLUE};
        border: 1px solid {DesignSystem.PRIMARY_BLUE};
    }}

    .stDownloadButton > button:hover {{
        background-color: {DesignSystem.PRIMARY_BLUE};
        color: white;
    }}

    /* Dividers */
    .stMarkdown hr {{
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 1.5rem 0;
    }}

    /* Custom Components */
    .metric-card {{
        background: {DesignSystem.CARD_BG};
        border: 1px solid #E2E8F0;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }}

    .stat-badge {{
        display: inline-block;
        background: {DesignSystem.SIDEBAR_BG};
        color: {DesignSystem.TEXT_SECONDARY};
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }}

    .category-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }}

    .category-disruption {{
        background: rgba(239, 68, 68, 0.1);
        color: {DesignSystem.DISRUPTION_COLOR};
    }}

    .category-air {{
        background: rgba(59, 130, 246, 0.1);
        color: {DesignSystem.AIR_FLEX_COLOR};
    }}

    .category-hotel {{
        background: rgba(139, 92, 246, 0.1);
        color: {DesignSystem.HOTEL_FLEX_COLOR};
    }}

    /* Section Headers */
    .section-header {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {DesignSystem.TEXT_MUTED};
        margin-bottom: 0.75rem;
        margin-top: 1.5rem;
    }}

    /* Expander Styling */
    .streamlit-expanderHeader {{
        background-color: {DesignSystem.SIDEBAR_BG};
        border: 1px solid #E2E8F0;
        border-radius: 0.5rem;
        color: {DesignSystem.TEXT_PRIMARY} !important;
        font-weight: 500;
        padding: 0.75rem 1rem !important;
    }}

    .streamlit-expanderContent {{
        border: 1px solid #E2E8F0;
        border-top: none;
        border-radius: 0 0 0.5rem 0.5rem;
        padding: 1rem !important;
    }}

    /* Remove Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Fix any contrast issues */
    p, span, div, label {{
        color: {DesignSystem.TEXT_PRIMARY};
    }}

    /* Caption text */
    .stCaption, [data-testid="stCaption"] {{
        color: {DesignSystem.TEXT_SECONDARY} !important;
        font-size: 0.875rem !important;
    }}

    /* Info/Warning/Error Messages */
    .stAlert {{
        border-radius: 0.5rem;
        padding: 1rem;
        border-left: 4px solid;
        background: {DesignSystem.SIDEBAR_BG};
    }}

    /* Share link styling */
    .share-link {{
        background: #F0F9FF;
        border: 1px solid {DesignSystem.PRIMARY_BLUE};
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.875rem;
        color: {DesignSystem.TEXT_PRIMARY};
        word-break: break-all;
    }}

    /* CRITICAL FIX: BRIGHT RED RADIO BUTTON SELECTIONS */
    /* All radio circles - black border */
    div[role="radiogroup"] label > div > div {{
        width: 20px !important;
        height: 20px !important;
        border: 3px solid #000000 !important;
        background: white !important;
        border-radius: 50% !important;
    }}

    /* SELECTED radio - BRIGHT RED FILLED */
    div[role="radiogroup"] label[aria-checked="true"] > div > div {{
        background: #FF0000 !important;
        border: 3px solid #FF0000 !important;
    }}

    /* Inner white dot for selected radio */
    div[role="radiogroup"] label[aria-checked="true"] > div > div::after {{
        content: "" !important;
        display: block !important;
        width: 8px !important;
        height: 8px !important;
        background: white !important;
        border-radius: 50% !important;
        margin: 3px !important;
    }}

    /* Bold text for selected option */
    div[role="radiogroup"] label[aria-checked="true"] {{
        font-weight: 900 !important;
        color: #000000 !important;
    }}
</style>
"""

# Natural sorting function
def natural_sort_key(s):
    """Sort strings naturally - F1, F2, F3... not F1, F11, F2"""
    return [int(text) if text.isdigit() else text for text in re.split('([0-9]+)', s)]

# Check for export capabilities
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
    groups = {"All Respondents": ["Total"]}

    for col_idx, group_name in question["category_groups"].items():
        if col_idx != "1":  # Skip Total column
            label = question["columns"][col_idx]
            if group_name not in groups:
                groups[group_name] = []
            if label not in groups[group_name]:
                groups[group_name].append(label)

    return groups

def is_mutually_exclusive_question(question: Dict) -> bool:
    """Check if a question has mutually exclusive answers."""
    try:
        total_base = question["bases"].get("Total", 0)
        if total_base == 0:
            return False

        total_count_sum = sum(
            response["count"].get("Total", 0)
            for response in question["responses"]
        )

        return abs(total_count_sum - total_base) <= 5
    except Exception:
        return False

def create_chart(question: Dict, segments: List[str], mode: str = "pct",
                chart_type: str = "bar", show_total: bool = False,
                selected_responses: Optional[List[str]] = None) -> go.Figure:
    """Create a chart with professional styling."""

    fig = go.Figure()

    # Get data for all segments
    all_data = []
    for segment in segments:
        data = get_segment_data(question, segment, mode)
        # Filter by selected responses if provided
        if selected_responses is not None:
            data = [(opt, val) for opt, val in data if opt in selected_responses]
        all_data.append((segment, data))

    if not all_data or not all_data[0][1]:
        return fig

    # Get x values from first segment - ensure they're strings
    x_values = [str(d[0]) for d in all_data[0][1]]

    if chart_type == "pie" and len(segments) == 1:
        # Pie chart
        values = [d[1] for d in all_data[0][1]]
        labels = x_values

        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            marker=dict(
                colors=DesignSystem.CHART_COLORS[:len(labels)],
                line=dict(color='white', width=2)
            ),
            textposition='auto',
            textinfo='label+percent' if mode == "pct" else 'label+value',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{label}</b><br>' +
                         ('%{percent}' if mode == "pct" else 'Count: %{value}') +
                         '<extra></extra>'
        ))

        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                font=dict(size=12, color=DesignSystem.TEXT_PRIMARY)
            ),
            margin=dict(l=20, r=150, t=20, b=20)
        )
    else:
        # Bar chart
        for idx, (segment_name, segment_data) in enumerate(all_data):
            y_values = [d[1] for d in segment_data]

            fig.add_trace(go.Bar(
                x=x_values,
                y=y_values,
                name=segment_name,
                marker_color=DesignSystem.CHART_COLORS[idx % len(DesignSystem.CHART_COLORS)],
                text=[f"{v:.1f}%" if mode == "pct" else f"{int(v):,}" for v in y_values],
                textposition='outside',
                textfont=dict(size=11, color=DesignSystem.TEXT_PRIMARY),
                hovertemplate='<b>%{x}</b><br>' +
                             segment_name + ': ' +
                             ('%{y:.1f}%' if mode == "pct" else '%{y:,}') +
                             '<extra></extra>'
            ))

        # Add total if requested
        if show_total and "Total" not in segments:
            total_data = get_segment_data(question, "Total", mode)
            # Filter by selected responses if provided
            if selected_responses is not None:
                total_data = [(opt, val) for opt, val in total_data if opt in selected_responses]
            y_values_total = [d[1] for d in total_data]

            fig.add_trace(go.Bar(
                x=x_values,
                y=y_values_total,
                name="Total",
                marker_color=DesignSystem.TEXT_MUTED,
                text=[f"{v:.1f}%" if mode == "pct" else f"{int(v):,}" for v in y_values_total],
                textposition='outside',
                textfont=dict(size=11, color=DesignSystem.TEXT_PRIMARY),
                opacity=0.6
            ))

        # Calculate appropriate y-axis range
        max_val = 0
        for _, segment_data in all_data:
            segment_max = max([d[1] for d in segment_data], default=0)
            max_val = max(max_val, segment_max)

        fig.update_layout(
            barmode='group',
            xaxis=dict(
                tickangle=-45 if len(x_values) > 8 else 0,
                tickfont=dict(size=11, color=DesignSystem.TEXT_PRIMARY),
                type='category'  # Force categorical x-axis
            ),
            yaxis=dict(
                range=[0, min(max_val * 1.15, 105) if mode == "pct" else max_val * 1.15],
                tickformat=".0f" + ("%" if mode == "pct" else ""),
                tickfont=dict(size=11, color=DesignSystem.TEXT_PRIMARY),
                gridcolor='#E2E8F0',
                gridwidth=1
            )
        )

    # Common layout updates
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="'Inter', sans-serif", color=DesignSystem.TEXT_PRIMARY),
        margin=dict(l=60, r=30, t=30, b=60),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="'Inter', sans-serif",
            font_color=DesignSystem.TEXT_PRIMARY
        ),
        showlegend=len(segments) > 1 or show_total,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color=DesignSystem.TEXT_PRIMARY)
        )
    )

    return fig

def create_data_table(question: Dict, segments: List[str]) -> pd.DataFrame:
    """Create a formatted data table."""
    rows = []

    for response in question["responses"]:
        row = {"Response": response["option"]}

        for segment in segments:
            if "pct" in response and segment in response["pct"]:
                row[f"{segment} %"] = response['pct'][segment]  # Keep as float for filtering
            if "count" in response and segment in response["count"]:
                row[f"{segment} n"] = int(response['count'][segment])

        rows.append(row)

    return pd.DataFrame(rows)

def main():
    # Apply professional CSS
    st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)

    # Load data
    data = load_data()

    # Sidebar
    with st.sidebar:
        # App title and controls header
        st.markdown("""
            <div style='padding: 0.5rem 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 1.5rem;'>
                <h2 style='color: #1E293B; margin: 0 0 0.5rem 0; font-size: 1.25rem;'>HTS Survey Explorer</h2>
                <h3 style='color: #198CEC; margin: 0; text-align: left; font-size: 1rem;'>📊 Controls</h3>
            </div>
        """, unsafe_allow_html=True)

        # Region Selection (preparing for future expansion)
        st.markdown('<div class="section-header">REGION</div>', unsafe_allow_html=True)
        region = st.selectbox(
            "Select Region",
            options=["United States"],
            label_visibility="collapsed",
            help="More regions coming soon"
        )

        # Display region-specific info
        if region == "United States":
            st.caption("n=1,030 US Adults who flew in past 12 months")

        # Group questions by product category
        question_groups = {
            "Profile Questions": [],
            "Disruption": [],
            "Air Flexibility": [],
            "Hotel Flexibility": []
        }

        for idx, q in enumerate(data):
            sheet = q['sheet']
            formatted = f"{sheet}: {q['question'][:50]}..."

            if sheet.startswith('P'):
                question_groups["Profile Questions"].append((idx, formatted, sheet))
            elif sheet.startswith('D') or sheet.startswith('DA'):
                question_groups["Disruption"].append((idx, formatted, sheet))
            elif sheet.startswith('F'):
                question_groups["Air Flexibility"].append((idx, formatted, sheet))
            elif sheet.startswith('HF'):
                question_groups["Hotel Flexibility"].append((idx, formatted, sheet))

        # Sort questions naturally within groups
        for group_name in question_groups:
            question_groups[group_name].sort(key=lambda x: natural_sort_key(x[2]))

        # Product Category Selection
        st.markdown('<div class="section-header">PRODUCT CATEGORY</div>', unsafe_allow_html=True)
        selected_group = st.selectbox(
            "Product Category",
            options=list(question_groups.keys()),
            index=0,
            label_visibility="collapsed"
        )

        # Question Selection
        st.markdown('<div class="section-header">QUESTION</div>', unsafe_allow_html=True)
        question_options = question_groups[selected_group]

        if question_options:
            selected_question_idx = st.selectbox(
                "Question",
                options=[idx for idx, _, _ in question_options],
                format_func=lambda x: next((label for idx, label, _ in question_options if idx == x), ""),
                label_visibility="collapsed"
            )
            current_question = data[selected_question_idx]
        else:
            st.error("No questions in this category")
            return

        # Extract demographic groups
        demographic_groups = extract_demographic_groups(current_question)

        st.markdown("---")

        # Analysis Settings
        st.markdown('<div class="section-header">ANALYSIS SETTINGS</div>', unsafe_allow_html=True)

        # Comparison Mode
        comparison_mode = st.radio(
            "Comparison Mode",
            options=["Single Segment", "Compare Within Group", "Compare Across Groups"],
            help="Choose how to analyze the data"
        )

        # Segment Selection based on mode
        selected_segments = []
        show_total = False

        if comparison_mode == "Single Segment":
            col1, col2 = st.columns(2)
            with col1:
                group = st.selectbox("Group", list(demographic_groups.keys()))
            with col2:
                segment = st.selectbox("Segment", demographic_groups.get(group, []))
            selected_segments = [segment] if segment else []

        elif comparison_mode == "Compare Within Group":
            group = st.selectbox("Select Group", list(demographic_groups.keys()))
            available = demographic_groups.get(group, [])
            selected_segments = st.multiselect(
                "Select Segments to Compare",
                options=available,
                default=available[:min(3, len(available))],
                help="Choose up to 5 segments to compare"
            )
            if group != "All Respondents":
                show_total = st.checkbox("Include Total", value=False)

        else:  # Compare Across Groups
            st.markdown("**Select two segments from any groups to compare:**")
            col1, col2 = st.columns(2)
            segments = []

            with col1:
                st.markdown("##### First Segment")
                group_a = st.selectbox(
                    "Select Group",
                    list(demographic_groups.keys()),
                    key="group_a"
                )
                segment_a = st.selectbox(
                    "Select Segment from Group",
                    demographic_groups.get(group_a, []),
                    key="seg_a",
                    help=f"Choose a segment from {group_a}"
                )
                if segment_a:
                    segments.append(segment_a)

            with col2:
                st.markdown("##### Second Segment")
                group_b = st.selectbox(
                    "Select Group",
                    list(demographic_groups.keys()),
                    key="group_b",
                    index=1 if len(demographic_groups.keys()) > 1 else 0
                )
                segment_b = st.selectbox(
                    "Select Segment from Group",
                    demographic_groups.get(group_b, []),
                    key="seg_b",
                    help=f"Choose a segment from {group_b}"
                )
                if segment_b:
                    segments.append(segment_b)

            selected_segments = segments
            if len(segments) == 2:
                st.info(f"Comparing: **{segments[0]}** vs **{segments[1]}**")
            show_total = st.checkbox("Include Total", value=False)

        st.markdown("---")

        # Display Settings
        st.markdown('<div class="section-header">DISPLAY SETTINGS</div>', unsafe_allow_html=True)

        display_mode = st.radio(
            "Data Format",
            options=["Percentage", "Raw Count"],
            horizontal=True
        )
        mode = "pct" if display_mode == "Percentage" else "count"

        # Chart type for single segment
        chart_type = "bar"
        if len(selected_segments) == 1 and is_mutually_exclusive_question(current_question):
            chart_type = st.radio(
                "Chart Type",
                options=["Bar Chart", "Pie Chart"],
                horizontal=True
            ).lower().split()[0]

    # Main Content Area
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
        # Category Badge
        sheet = current_question["sheet"]
        if sheet.startswith('D') or sheet.startswith('DA'):
            badge_html = '<span class="category-badge category-disruption">DISRUPTION</span>'
        elif sheet.startswith('F'):
            badge_html = '<span class="category-badge category-air">AIR FLEXIBILITY</span>'
        elif sheet.startswith('HF'):
            badge_html = '<span class="category-badge category-hotel">HOTEL FLEXIBILITY</span>'
        else:
            badge_html = ''

        if badge_html:
            st.markdown(badge_html, unsafe_allow_html=True)

        # Question Title
        st.markdown(f"<h2>{current_question['question']}</h2>", unsafe_allow_html=True)

        # Base Statistics
        if selected_segments:
            stats_html = "<div style='margin: 1rem 0;'>"
            for seg in selected_segments[:5]:  # Limit to 5 segments
                base_n = current_question["bases"].get(seg, 0)
                stats_html += f'<span class="stat-badge">{seg}: n={base_n:,}</span>'
            stats_html += "</div>"
            st.markdown(stats_html, unsafe_allow_html=True)

            # Create data table
            df = create_data_table(current_question, selected_segments)
            all_responses = df["Response"].tolist()

            # Initialize hidden responses in session state if not exists
            if 'hidden_responses' not in st.session_state:
                st.session_state.hidden_responses = set()

            # Filter responses for chart (show all by default, except hidden)
            selected_responses = [r for r in all_responses if r not in st.session_state.hidden_responses]

            # Show status if responses are hidden
            if st.session_state.hidden_responses:
                st.info(f"📊 Showing {len(selected_responses)} of {len(all_responses)} responses ({len(st.session_state.hidden_responses)} hidden)")

            # Chart (display first)
            if selected_responses:
                fig = create_chart(
                    current_question,
                    selected_segments,
                    mode,
                    chart_type,
                    show_total,
                    selected_responses
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={'displayModeBar': False}
                )

            # Quick hide options below chart
            st.markdown("---")
            st.markdown("**Quick Hide Options:**")

            # Use full width columns for better alignment
            col_hide1, col_hide2, col_hide3 = st.columns(3)

            with col_hide1:
                # Check for NET responses (including "NET:" format)
                net_responses = [r for r in all_responses if 'net:' in r.lower() or 'net ' in r.lower() or 'total' in r.lower() or r.lower().startswith('net')]
                if net_responses:
                    if st.button(f"Hide NET/Total ({len(net_responses)})", key=f"hide_net_{current_question['sheet']}"):
                        for resp in net_responses:
                            st.session_state.hidden_responses.add(resp)
                        st.rerun()

            with col_hide2:
                # Check for Don't Know / Not Sure responses
                dk_responses = [r for r in all_responses if any(x in r.lower() for x in ["don't know", "not sure", "no opinion", "n/a"])]
                if dk_responses:
                    if st.button(f"Hide DK/NA ({len(dk_responses)})", key=f"hide_dk_{current_question['sheet']}"):
                        for resp in dk_responses:
                            st.session_state.hidden_responses.add(resp)
                        st.rerun()

            with col_hide3:
                # Check for Other responses - aligned left
                other_responses = [r for r in all_responses if 'other' in r.lower()]
                if other_responses:
                    if st.button(f"Hide Other ({len(other_responses)})", key=f"hide_other_{current_question['sheet']}"):
                        for resp in other_responses:
                            st.session_state.hidden_responses.add(resp)
                        st.rerun()

            # Allow custom exclusions
            with st.expander("🚫 Hide Specific Responses"):
                st.markdown("**Select responses to HIDE from chart:**")

                # Get currently visible responses
                visible_responses = [r for r in all_responses if r not in st.session_state.hidden_responses]

                # Dropdown to select and hide individual responses
                if visible_responses:
                    response_to_hide = st.selectbox(
                        "Select a response to hide:",
                        options=["-- Select response --"] + visible_responses,
                        key=f"select_hide_{current_question['sheet']}"
                    )

                    if response_to_hide != "-- Select response --":
                        if st.button(f"Hide '{response_to_hide}'", key=f"hide_btn_{response_to_hide}"):
                            st.session_state.hidden_responses.add(response_to_hide)
                            st.rerun()

                # Show what's currently hidden
                if st.session_state.hidden_responses:
                    st.markdown("**Currently hidden:**")
                    for hidden in st.session_state.hidden_responses:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.caption(f"• {hidden}")
                        with col2:
                            if st.button("Show", key=f"show_{hidden}"):
                                st.session_state.hidden_responses.discard(hidden)
                                st.rerun()

                # Clear all button
                if st.session_state.hidden_responses:
                    if st.button("Show All Hidden Responses"):
                        st.session_state.hidden_responses.clear()
                        st.rerun()

            # Data table below hiding options
            with st.expander("📊 View Data Table"):
                # Show filtered data table
                if selected_responses:
                    filtered_df = df[df["Response"].isin(selected_responses)]

                    # Format percentage columns for display
                    display_df = filtered_df.copy()
                    for col in display_df.columns:
                        if " %" in col:
                            display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}%")

                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.warning("All responses are hidden. Please show at least one response.")

            # Export Options
            st.markdown("---")
            st.markdown("**Export Chart:**")
            col1_export, col2_export, col3_export = st.columns([1.5, 1.5, 3])

            sheet_id = current_question["sheet"].lower()
            segment_label = "_".join([s.lower().replace(" ", "_")[:10] for s in selected_segments[:2]])

            with col1_export:
                html_string = fig.to_html(include_plotlyjs='cdn')
                st.download_button(
                    "📄 Download HTML",
                    data=html_string,
                    file_name=f"hts_{sheet_id}_{segment_label}.html",
                    mime="text/html",
                    use_container_width=True
                )

            with col2_export:
                # Try PNG export with better error handling
                try:
                    img_bytes = fig.to_image(format="png", width=1400, height=700, scale=2)
                    st.download_button(
                        "🖼️ Download PNG",
                        data=img_bytes,
                        file_name=f"hts_{sheet_id}_{segment_label}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                except Exception:
                    # Fallback to JPEG
                    try:
                        img_bytes = fig.to_image(format="jpeg", width=1400, height=700, scale=2)
                        st.download_button(
                            "🖼️ Download JPEG",
                            data=img_bytes,
                            file_name=f"hts_{sheet_id}_{segment_label}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    except:
                        st.info("💡 Use HTML export for images", icon="ℹ️")

        else:
            st.info("Please select at least one segment to analyze")

if __name__ == "__main__":
    main()