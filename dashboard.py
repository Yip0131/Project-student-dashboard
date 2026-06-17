# ============================================
# IMC12403 DATA VISUALIZATION
# GROUP PROJECT - PART A
# SCENARIO A: University Student Performance Analytics
# BEAUTIFIED VERSION - NO PART-TIME JOB FILTER
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS - BEAUTIFIED
# ============================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1a237e, #0d47a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        letter-spacing: 2px;
    }
    .sub-header {
        text-align: center;
        color: #546e7a;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }
    
    .kpi-card {
        background: white;
        padding: 1.2rem 0.8rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.3);
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #78909c;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }
    .kpi-icon {
        font-size: 1.8rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a237e;
        padding: 0.8rem 0 0.5rem 0;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #1a237e, #42a5f5) 1;
        border-bottom-style: solid;
    }
    
    .footer {
        text-align: center;
        color: #90a4ae;
        font-size: 0.85rem;
        padding: 2rem 0 0.5rem 0;
        border-top: 2px solid #e8eaf6;
        margin-top: 2rem;
    }
    .footer span {
        color: #1a237e;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv('global_university_students_performance_habits_10000.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Please ensure 'global_university_students_performance_habits_10000.csv' is in the same folder.")
    st.stop()

# ============================================
# DATA CLEANING
# ============================================
numeric_cols = ['GPA', 'study_hours_per_day', 'class_attendance_percent', 
                'sleep_hours', 'screen_time_hours', 'social_media_hours',
                'gaming_hours', 'exercise_hours_per_week', 'mental_stress_level',
                'AI_tool_usage_hours', 'coffee_consumption_per_day',
                'extracurricular_hours_per_week', 'final_exam_score', 'assignment_score']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['GPA', 'final_exam_score'])

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0 0.5rem 0;">
    <span style="font-size: 2rem;">🎓</span>
    <h3 style="margin: 0; color: #1a237e;">Filters</h3>
    <p style="color: #78909c; font-size: 0.8rem;">Filter data to explore insights</p>
</div>
<hr style="margin: 0.5rem 0;">
""", unsafe_allow_html=True)

selected_country = st.sidebar.selectbox('🌍 Country', ['All'] + sorted(df['country'].dropna().unique().tolist()))
selected_major = st.sidebar.selectbox('📚 Major', ['All'] + sorted(df['major'].dropna().unique().tolist()))
selected_gender = st.sidebar.selectbox('👤 Gender', ['All'] + sorted(df['gender'].dropna().unique().tolist()))

st.sidebar.markdown("---")

min_gpa = float(df['GPA'].min())
max_gpa = float(df['GPA'].max())
gpa_range = st.sidebar.slider('📊 GPA Range', min_gpa, max_gpa, (min_gpa, max_gpa), 0.1)

min_study = float(df['study_hours_per_day'].min())
max_study = float(df['study_hours_per_day'].max())
study_range = st.sidebar.slider('📖 Study Hours/Day', min_study, max_study, (min_study, max_study), 0.5)

st.sidebar.markdown("---")

# ============================================
# APPLY FILTERS (NO PART-TIME JOB)
# ============================================
filtered_df = df.copy()

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
if selected_major != 'All':
    filtered_df = filtered_df[filtered_df['major'] == selected_major]
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
filtered_df = filtered_df[(filtered_df['GPA'] >= gpa_range[0]) & (filtered_df['GPA'] <= gpa_range[1])]
filtered_df = filtered_df[(filtered_df['study_hours_per_day'] >= study_range[0]) & (filtered_df['study_hours_per_day'] <= study_range[1])]

if len(filtered_df) == 0:
    st.warning("⚠️ No data matches the selected filters. Please adjust your filters.")
    st.stop()

# ============================================
# HEADER
# ============================================
st.markdown('<div class="main-header">🎓 University Student Performance Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Dashboard for Understanding Factors Affecting Academic Performance</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# KPI CARDS
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)

kpi_colors = ['#1a237e', '#0d47a1', '#1565c0', '#1976d2', '#1e88e5']
kpi_icons = ['👥', '📊', '📝', '📋', '⏰']
kpi_labels = ['Total Students', 'Average GPA', 'Avg Exam Score', 'Avg Attendance', 'Study Hours/Day']
kpi_values = [
    f"{len(filtered_df):,}",
    f"{filtered_df['GPA'].mean():.2f}",
    f"{filtered_df['final_exam_score'].mean():.1f}",
    f"{filtered_df['class_attendance_percent'].mean():.1f}%",
    f"{filtered_df['study_hours_per_day'].mean():.1f}h"
]

for col, icon, label, value, color in zip([col1, col2, col3, col4, col5], kpi_icons, kpi_labels, kpi_values, kpi_colors):
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid {color};">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value" style="color: {color};">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# VISUALIZATION 1: GPA by Major
# ============================================
st.markdown('<div class="section-header">📊 Visualization 1: GPA Distribution by Major</div>', unsafe_allow_html=True)

major_gpa = filtered_df.groupby('major')['GPA'].mean().sort_values(ascending=True).reset_index()

fig1 = px.bar(
    major_gpa,
    x='GPA',
    y='major',
    color='GPA',
    color_continuous_scale=['#ef5350', '#ffca28', '#66bb6a'],
    title='Average GPA by Major',
    height=420,
    text=None
)
fig1.update_traces(
    texttemplate=None,
    hovertemplate='<b>%{y}</b><br>GPA: %{x:.2f}<extra></extra>',
    marker=dict(line=dict(width=0.5, color='rgba(0,0,0,0.1)'))
)
fig1.update_layout(
    title=dict(
        text='Average GPA by Major',
        x=0.5,
        xanchor='center'
    ),
    showlegend=False,
    coloraxis_showscale=False,
    xaxis_range=[2.5, 4.1],
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial, sans-serif", size=12),
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis=dict(title_font=dict(size=13, weight='bold'), showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
    yaxis=dict(title_font=dict(size=13, weight='bold'))
)
st.plotly_chart(fig1, use_container_width=True)

# ============================================
# VISUALIZATION 2: Study Hours vs GPA - LEGEND RIGHT
# ============================================
st.markdown('<div class="section-header">📖 Visualization 2: Study Hours vs GPA</div>', unsafe_allow_html=True)

fig2 = px.scatter(
    filtered_df,
    x='study_hours_per_day',
    y='GPA',
    color='major',
    title='Study Hours vs GPA',
    height=420,
    opacity=0.7,
    hover_data={'student_id': True, 'country': True, 'gender': True},
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Trend line
x_vals = filtered_df['study_hours_per_day']
y_vals = filtered_df['GPA']
z = np.polyfit(x_vals, y_vals, 1)
p = np.poly1d(z)
x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)

fig2.add_trace(go.Scatter(
    x=x_trend, 
    y=p(x_trend), 
    mode='lines', 
    name='Trend Line', 
    line=dict(color='#e53935', width=2.5, dash='dash')
))

fig2.update_traces(
    marker=dict(size=9, line=dict(width=0.5, color='white')),
    hovertemplate='<b>%{customdata[0]}</b><br>Study Hours: %{x:.1f}<br>GPA: %{y:.2f}<br>Country: %{customdata[1]}<br>Gender: %{customdata[2]}<extra></extra>'
)

fig2.update_layout(
    title=dict(
        text='Study Hours vs GPA',
        x=0.5,
        xanchor='center'
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial, sans-serif", size=12),
    margin=dict(l=10, r=120, t=50, b=10),
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(size=10)
    ),
    xaxis=dict(
        title_font=dict(size=13, weight='bold'),
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        title='Study Hours per Day'
    ),
    yaxis=dict(
        title_font=dict(size=13, weight='bold'),
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        title='GPA'
    ),
    height=420
)
st.plotly_chart(fig2, use_container_width=True)

# ============================================
# VISUALIZATION 3: Attendance vs Exam Score - NO RIGHT LABEL
# ============================================
st.markdown('<div class="section-header">📋 Visualization 3: Attendance Impact on Exam Performance</div>', unsafe_allow_html=True)

filtered_df['attendance_bin'] = pd.cut(
    filtered_df['class_attendance_percent'],
    bins=[0, 70, 80, 90, 100],
    labels=['<70%', '70-80%', '80-90%', '90-100%']
)

attendance_agg = filtered_df.groupby('attendance_bin', observed=True).agg({
    'final_exam_score': 'mean',
    'student_id': 'count'
}).reset_index()
attendance_agg.columns = ['attendance_bin', 'avg_exam_score', 'student_count']

fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(
    go.Bar(
        x=attendance_agg['attendance_bin'], 
        y=attendance_agg['student_count'], 
        name='Student Count', 
        marker_color='#42a5f5', 
        opacity=0.8,
        marker=dict(line=dict(width=0.5, color='white')),
        hovertemplate='<b>%{x}</b><br>Students: %{y}<extra></extra>'
    ),
    secondary_y=False
)

fig3.add_trace(
    go.Scatter(
        x=attendance_agg['attendance_bin'], 
        y=attendance_agg['avg_exam_score'],
        name='Avg Exam Score', 
        marker=dict(color='#e53935', size=12, line=dict(width=1, color='white')),
        line=dict(width=3.5, color='#e53935'), 
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Avg Exam Score: %{y:.1f}<extra></extra>'
    ),
    secondary_y=True
)

fig3.update_layout(
    title=dict(
        text='Attendance Rate vs Exam Performance',
        x=0.5,
        xanchor='center'
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial, sans-serif", size=12),
    margin=dict(l=10, r=10, t=50, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=420
)

fig3.update_yaxes(
    title_text="Number of Students", 
    secondary_y=False,
    title_font=dict(size=13, weight='bold'),
    showgrid=True,
    gridcolor='rgba(0,0,0,0.05)'
)
fig3.update_yaxes(
    title_text="",                    # 空字符串，隐藏右边 Y 轴标题
    secondary_y=True, 
    range=[75, 100],
    showgrid=False,
    showticklabels=True
)
fig3.update_xaxes(
    title_text="Attendance Rate",
    title_font=dict(size=13, weight='bold')
)
st.plotly_chart(fig3, use_container_width=True)

# ============================================
# VISUALIZATION 4: GPA by Country & Gender
# ============================================
st.markdown('<div class="section-header">🌍 Visualization 4: GPA by Country and Gender</div>', unsafe_allow_html=True)

top_countries = filtered_df['country'].value_counts().head(8).index.tolist()
country_df = filtered_df[filtered_df['country'].isin(top_countries)]

gender_gpa = country_df.groupby(['country', 'gender'])['GPA'].mean().reset_index()

fig4 = px.bar(
    gender_gpa,
    x='country',
    y='GPA',
    color='gender',
    barmode='group',
    title='Average GPA by Country and Gender',
    color_discrete_sequence=['#1a237e', '#e53935'],
    height=420,
    text=None
)

fig4.add_hline(
    y=filtered_df['GPA'].mean(), 
    line_dash="dash", 
    line_color="#2e7d32",
    line_width=2,
    annotation_text=f"Overall Avg: {filtered_df['GPA'].mean():.2f}",
    annotation_position="top right"
)

fig4.update_traces(
    texttemplate=None,
    hovertemplate='<b>%{x}</b><br>Gender: %{marker.color}<br>GPA: %{y:.2f}<extra></extra>',
    marker=dict(line=dict(width=0.5, color='white'))
)
fig4.update_layout(
    title=dict(
        text='Average GPA by Country and Gender',
        x=0.5,
        xanchor='center'
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial, sans-serif", size=12),
    margin=dict(l=10, r=10, t=50, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(title_font=dict(size=13, weight='bold'), showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
    yaxis=dict(title_font=dict(size=13, weight='bold'), showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
    height=420
)
st.plotly_chart(fig4, use_container_width=True)

# ============================================
# VISUALIZATION 5: Intervention Priority Matrix - LEGEND RIGHT
# ============================================
st.markdown('<div class="section-header">🎯 Visualization 5: Intervention Priority Matrix</div>', unsafe_allow_html=True)

intervention_df = filtered_df.groupby('major').agg({
    'mental_stress_level': 'mean',
    'GPA': 'mean',
    'student_id': 'count'
}).reset_index()
intervention_df.columns = ['major', 'avg_stress', 'avg_gpa', 'student_count']

stress_avg = intervention_df['avg_stress'].mean()
gpa_avg = intervention_df['avg_gpa'].mean()

def get_quadrant(row):
    if row['avg_stress'] > stress_avg and row['avg_gpa'] < gpa_avg:
        return 'Crisis'
    elif row['avg_stress'] > stress_avg and row['avg_gpa'] >= gpa_avg:
        return 'Mental Health'
    elif row['avg_stress'] <= stress_avg and row['avg_gpa'] < gpa_avg:
        return 'Academic Support'
    else:
        return 'Maintain'

intervention_df['quadrant'] = intervention_df.apply(get_quadrant, axis=1)

color_map = {
    'Crisis': '#c62828',
    'Mental Health': '#f9a825',
    'Academic Support': '#ef6c00',
    'Maintain': '#2e7d32'
}

fig5 = px.scatter(
    intervention_df,
    x='avg_stress',
    y='avg_gpa',
    size='student_count',
    color='quadrant',
    text='major',
    title='Stress Level vs GPA by Major',
    labels={
        'avg_stress': 'Average Stress Level',
        'avg_gpa': 'Average GPA'
    },
    color_discrete_map=color_map,
    height=450,
    size_max=50
)

fig5.add_hline(
    y=gpa_avg, 
    line_dash="dash", 
    line_color="gray", 
    opacity=0.5,
    line_width=1.5
)
fig5.add_vline(
    x=stress_avg, 
    line_dash="dash", 
    line_color="gray", 
    opacity=0.5,
    line_width=1.5
)

fig5.update_traces(
    textposition='top center',
    hovertemplate='<b>%{text}</b><br>Stress: %{x:.2f}<br>GPA: %{y:.2f}<extra></extra>',
    marker=dict(line=dict(width=1, color='white'))
)

fig5.update_layout(
    title=dict(
        text='Stress Level vs GPA by Major',
        x=0.5,
        xanchor='center'
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial, sans-serif", size=12),
    margin=dict(l=10, r=120, t=50, b=10),
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(size=11, weight='bold'),
        title=dict(text='Intervention Priority', font=dict(size=12, weight='bold'))
    ),
    xaxis=dict(
        title_font=dict(size=13, weight='bold'),
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        title='Average Stress Level'
    ),
    yaxis=dict(
        title_font=dict(size=13, weight='bold'),
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        title='Average GPA'
    ),
    height=450
)

# Quadrant labels
fig5.add_annotation(
    x=stress_avg + 0.5,
    y=gpa_avg + 0.1,
    text="🟢 Maintain",
    showarrow=False,
    font=dict(size=11, color='#2e7d32', weight='bold'),
    opacity=0.7
)
fig5.add_annotation(
    x=stress_avg + 0.5,
    y=gpa_avg - 0.1,
    text="🟠 Academic Support",
    showarrow=False,
    font=dict(size=11, color='#ef6c00', weight='bold'),
    opacity=0.7
)
fig5.add_annotation(
    x=stress_avg - 0.5,
    y=gpa_avg + 0.1,
    text="🟡 Mental Health",
    showarrow=False,
    font=dict(size=11, color='#f9a825', weight='bold'),
    opacity=0.7
)
fig5.add_annotation(
    x=stress_avg - 0.5,
    y=gpa_avg - 0.1,
    text="🔴 Crisis",
    showarrow=False,
    font=dict(size=11, color='#c62828', weight='bold'),
    opacity=0.7
)

st.plotly_chart(fig5, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <b>IMC12403 Data Visualization</b> | Group Project - Part A | 
    Scenario A: University Student Performance Analytics |
    Powered by <span>Streamlit</span> &amp; <span>Plotly</span>
</div>
""", unsafe_allow_html=True)