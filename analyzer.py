import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('students.csv')

subjects = ['Math', 'Science', 'English', 'Computer', 'Hindi']

# Calculate total and average
df['Total'] = df[subjects].sum(axis=1)
df['Average'] = df['Total'] / 5

# Assign grades
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

# Rank students
df['Rank'] = df['Average'].rank(ascending=False).astype(int)

# Best and weak subject per student
df['Best Subject'] = df[subjects].idxmax(axis=1)
df['Weak Subject'] = df[subjects].idxmin(axis=1)

# Sort by rank
df = df.sort_values('Rank')

# ========================
# CLASS REPORT
# ========================
print("="*60)
print("       STUDENT RESULT ANALYZER - CLASS REPORT")
print("="*60)
print(df[['Rank','Name','Total','Average',
          'Grade','Status']].to_string(index=False))
print("="*60)

# Class statistics
print(f"\nClass Average:  {df['Average'].mean():.2f}")
print(f"Highest Score:  {df['Average'].max():.2f} "
      f"- {df.loc[df['Average'].idxmax(), 'Name']}")
print(f"Lowest Score:   {df['Average'].min():.2f} "
      f"- {df.loc[df['Average'].idxmin(), 'Name']}")
print(f"Total Students: {len(df)}")
print(f"Pass Count:     {(df['Status']=='Pass').sum()}")
print(f"Fail Count:     {(df['Status']=='Fail').sum()}")

# Subject wise average
print("\nSubject-wise Class Average:")
for sub in subjects:
    print(f"  {sub}: {df[sub].mean():.2f}")

# ========================
# INDIVIDUAL REPORTS
# ========================
print("\n" + "="*60)
print("       INDIVIDUAL STUDENT REPORTS")
print("="*60)
for _, row in df.iterrows():
    print(f"\n--- {row['Name']}'s Report ---")
    print(f"  Rank:         {row['Rank']}")
    print(f"  Total:        {row['Total']}")
    print(f"  Average:      {row['Average']:.2f}")
    print(f"  Grade:        {row['Grade']}")
    print(f"  Status:       {row['Status']}")
    print(f"  Best Subject: {row['Best Subject']}")
    print(f"  Weak Subject: {row['Weak Subject']}")

# ========================
# SAVE REPORT
# ========================
df.to_csv('result_report.csv', index=False)
print("\n" + "="*60)
print("Report saved to result_report.csv ✓")

# ========================
# VISUALIZATIONS
# ========================

# 1. Grade distribution pie chart
grade_counts = df['Grade'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(grade_counts, labels=grade_counts.index,
        autopct='%1.1f%%', startangle=90)
plt.title('Grade Distribution')
plt.savefig('grade_distribution.png')
plt.show()

# 2. Subject wise average bar chart
subject_avgs = df[subjects].mean()
plt.figure(figsize=(8,5))
plt.bar(subjects, subject_avgs, color='skyblue')
plt.title('Subject-wise Class Average')
plt.ylabel('Average Marks')
plt.ylim(0, 100)
for i, v in enumerate(subject_avgs):
    plt.text(i, v + 1, f'{v:.1f}', ha='center')
plt.savefig('subject_averages.png')
plt.show()

# 3. Student performance bar chart
plt.figure(figsize=(10,5))
plt.bar(df['Name'], df['Average'], color='lightgreen')
plt.title('Student-wise Average Marks')
plt.ylabel('Average Marks')
plt.xlabel('Students')
plt.ylim(0, 100)
plt.xticks(rotation=45)
for i, v in enumerate(df['Average']):
    plt.text(i, v + 1, f'{v:.1f}', ha='center')
plt.tight_layout()
plt.savefig('student_performance.png')
plt.show()

print("Charts saved ✓")
print("="*60)