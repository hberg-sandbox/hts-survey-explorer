import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Tuple, Optional
import re

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

    /* Radio Button Styling */
    [data-baseweb="radio"] {{
        color: {DesignSystem.TEXT_PRIMARY} !important;
    }}

    [data-baseweb="radio"] label {{
        color: {DesignSystem.TEXT_PRIMARY} !important;
        font-size: 0.875rem !important;
        padding: 0.375rem 0 !important;
    }}

    [data-baseweb="radio"] > div:first-child {{
        background-color: {DesignSystem.BACKGROUND} !important;
        border: 2px solid #CBD5E1 !important;
    }}

    [data-baseweb="radio"]:hover > div:first-child {{
        border-color: {DesignSystem.PRIMARY_BLUE} !important;
    }}

    [data-baseweb="radio"] input:checked ~ div:first-child {{
        background-color: {DesignSystem.PRIMARY_BLUE} !important;
        border-color: {DesignSystem.PRIMARY_BLUE} !important;
    }}

    /* Make selected radio option more visible */
    [data-baseweb="radio"][aria-checked="true"] {{
        background-color: #E0F2FE !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 0.375rem !important;
        border-left: 3px solid {DesignSystem.PRIMARY_BLUE} !important;
    }}

    [data-baseweb="radio"][aria-checked="true"] label {{
        color: #0C4A6E !important;
        font-weight: 600 !important;
    }}

    /* Additional styling for radio group container to highlight selection */
    .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"] {{
        background-color: #E0F2FE !important;
        margin-left: -0.5rem !important;
        padding-left: 0.75rem !important;
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

    /* Footer */
    .app-footer {{
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E2E8F0;
        font-size: 0.875rem;
        color: {DesignSystem.TEXT_MUTED};
        text-align: center;
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

    /* Charts Container */
    .chart-container {{
        background: {DesignSystem.CARD_BG};
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
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
                chart_type: str = "bar", show_total: bool = False) -> go.Figure:
    """Create a chart with professional styling."""

    fig = go.Figure()

    # Get data for all segments
    all_data = []
    for segment in segments:
        data = get_segment_data(question, segment, mode)
        all_data.append((segment, data))

    if not all_data or not all_data[0][1]:
        return fig

    # Get x values from first segment
    x_values = [d[0] for d in all_data[0][1]]

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
                tickfont=dict(size=11, color=DesignSystem.TEXT_PRIMARY)
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
                row[f"{segment} %"] = f"{response['pct'][segment]:.1f}%"
            if "count" in response and segment in response["count"]:
                row[f"{segment} n"] = f"{int(response['count'][segment]):,}"

        rows.append(row)

    return pd.DataFrame(rows)

def main():
    # Apply professional CSS
    st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)

    # Load data
    data = load_data()

    # Main header
    st.markdown("""
        <h2 style='text-align: center; color: #1E293B; margin-bottom: 0.5rem; font-size: 1.5rem;'>
            HTS Survey Explorer
        </h2>
        <p style='text-align: center; color: #64748B; margin-bottom: 1.5rem; font-size: 0.875rem;'>
            Travel Flexibility Survey Analysis | n=1,030 US Adults
        </p>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        # Logo/Title area
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 1.5rem;'>
                <h2 style='color: #198CEC; margin: 0;'>📊 Controls</h2>
            </div>
        """, unsafe_allow_html=True)

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
            "",
            options=list(question_groups.keys()),
            index=0,
            label_visibility="collapsed"
        )

        # Question Selection
        st.markdown('<div class="section-header">QUESTION</div>', unsafe_allow_html=True)
        question_options = question_groups[selected_group]

        if question_options:
            selected_question_idx = st.selectbox(
                "",
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

        # Footer
        st.markdown("""
            <div style='margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #E2E8F0;'>
                <p style='font-size: 0.75rem; color: #94A3B8; text-align: center;'>
                    <strong>Survey Details</strong><br>
                    n=1,030 US Adults<br>
                    Flew in past 12 months<br>
                    © 2024 HTS
                </p>
            </div>
        """, unsafe_allow_html=True)

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
                n = current_question["bases"].get(seg, 0)
                stats_html += f'<span class="stat-badge">{seg}: n={n:,}</span>'
            stats_html += "</div>"
            st.markdown(stats_html, unsafe_allow_html=True)

        # Chart
        if selected_segments:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            fig = create_chart(
                current_question,
                selected_segments,
                mode,
                chart_type,
                show_total
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={'displayModeBar': False}
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # Export Options
            st.markdown("**Export Chart:**")
            col1, col2, col3 = st.columns([1.5, 1.5, 3])

            sheet_id = current_question["sheet"].lower()
            segment_label = "_".join([s.lower().replace(" ", "_")[:10] for s in selected_segments[:2]])

            with col1:
                html_string = fig.to_html(include_plotlyjs='cdn')
                st.download_button(
                    "📄 Download HTML",
                    data=html_string,
                    file_name=f"hts_{sheet_id}_{segment_label}.html",
                    mime="text/html",
                    use_container_width=True
                )

            with col2:
                # Try PNG export with better error handling
                try:
                    # Attempt PNG export with timeout
                    with st.spinner("Generating PNG..."):
                        img_bytes = fig.to_image(
                            format="png",
                            width=1400,
                            height=700,
                            scale=2,
                            engine="kaleido"
                        )
                    st.download_button(
                        "🖼️ Download PNG",
                        data=img_bytes,
                        file_name=f"hts_{sheet_id}_{segment_label}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                except Exception as e:
                    # Fallback to JPEG
                    try:
                        img_bytes = fig.to_image(
                            format="jpeg",
                            width=1400,
                            height=700,
                            scale=2
                        )
                        st.download_button(
                            "🖼️ Download JPEG",
                            data=img_bytes,
                            file_name=f"hts_{sheet_id}_{segment_label}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    except:
                        # Final fallback - interactive HTML
                        st.info("💡 Use HTML export for images", icon="ℹ️")

            # Data Table
            with st.expander("📊 View Data Table"):
                df = create_data_table(current_question, selected_segments)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("Please select at least one segment to analyze")

        # Footer
        st.markdown("""
            <div class="app-footer">
                <p>HTS Survey Explorer • Professional Analytics Dashboard</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()