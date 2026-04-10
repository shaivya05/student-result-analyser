import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# PAGE SETUP
# ========================
st.set_page_config(
    page_title="Student Result Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Result Analyzer")
st.markdown("---")

# ========================
# LOAD DATA
# ========================
df = pd.read_csv('students.csv')
subjects = ['Math', 'Science', 'English', 'Computer', 'Hindi']

# Calculate everything
df['Total'] = df[subjects].sum(axis=1)
df['Average'] = df['Total'] / 5

def get_grade(avg):
    if avg >= 90: return 'A+'
    elif avg >= 80: return 'A'
    elif avg >= 70: return 'B'
    elif avg >= 60: return 'C'
    elif avg >= 40: return 'D'
    else: return 'F'

def get_status(avg):
    return 'Pass' if avg >= 40 else 'Fail'

df['Grade'] = df['Average'].apply(get_grade)
df['Status'] = df['Average'].apply(get_status)
df['Rank'] = df['Average'].rank(ascending=False).astype(int)
df['Best Subject'] = df[subjects].idxmax(axis=1)
df['Weak Subject'] = df[subjects].idxmin(axis=1)
df = df.sort_values('Rank')

# ========================
# CLASS STATISTICS
# ========================
st.header("📈 Class Statistics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Class Average", f"{df['Average'].mean():.2f}")
col2.metric("Highest Score", f"{df['Average'].max():.2f}")
col3.metric("Pass Count", f"{(df['Status']=='Pass').sum()}")
col4.metric("Fail Count", f"{(df['Status']=='Fail').sum()}")

st.markdown("---")

# ========================
# FULL CLASS REPORT TABLE
# ========================
st.header("📋 Full Class Report")
st.dataframe(
    df[['Rank','Name','Total','Average',
        'Grade','Status','Best Subject','Weak Subject']],
    use_container_width=True
)

# Download button
csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download Report as CSV",
    data=csv,
    file_name='result_report.csv',
    mime='text/csv'
)

st.markdown("---")

# ========================
# CHARTS
# ========================
st.header("📊 Class Analytics")

col1, col2 = st.columns(2)

# Grade distribution pie chart
with col1:
    st.subheader("Grade Distribution")
    grade_counts = df['Grade'].value_counts()
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(grade_counts, labels=grade_counts.index,
           autopct='%1.1f%%', startangle=90)
    ax.set_title('Grade Distribution')
    st.pyplot(fig)

# Pass/Fail pie chart
with col2:
    st.subheader("Pass/Fail Distribution")
    status_counts = df['Status'].value_counts()
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(status_counts, labels=status_counts.index,
           autopct='%1.1f%%', startangle=90,
           colors=['lightgreen','lightcoral'])
    ax.set_title('Pass/Fail Distribution')
    st.pyplot(fig)

