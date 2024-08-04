import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the CSV file path
csv_file = 'ai_usage_data.csv'

# Function to load data or create CSV file if it doesn't exist
def load_data():
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=['Task Description', 'AI Tool', 'Time Spent on AI', 'Creativity Impact', 'Time Saved', 'Skill Development Impact', 'Task Completion'])
        df.to_csv(csv_file, index=False)
    return pd.read_csv(csv_file)

# Function to save new data to CSV
def save_data(new_data):
    df = load_data()
    new_df = pd.DataFrame([new_data])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(csv_file, index=False)

# Function to calculate AI dependence score
def calculate_ai_dependence(df):
    total_time = df['Time Spent on AI'].sum()
    total_tasks = len(df)
    if total_tasks > 0:
        ai_dependence_score = total_time / total_tasks
    else:
        ai_dependence_score = 0
    return ai_dependence_score

# Function to calculate creativity score
def calculate_creativity_score(df):
    if not df.empty:
        creativity_score = df['Creativity Impact'].mean()
    else:
        creativity_score = 0
    return creativity_score

# Function to calculate productivity score
def calculate_productivity_score(df):
    total_time = df['Time Spent on AI'].sum()
    if total_time > 0:
        productivity_score = (total_time / len(df)) * 100
    else:
        productivity_score = 0
    return productivity_score

# Function to calculate time saved
def calculate_time_saved(df):
    return df['Time Saved'].sum()

# Function to calculate skill development impact
def calculate_skill_development_impact(df):
    if not df.empty:
        skill_impact = df['Skill Development Impact'].mean()
    else:
        skill_impact = 0
    return skill_impact

# Load initial data
data = load_data()

# Inject CSS for background image
st.markdown(
    """
    <style>
    .main {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1fpoIWtnKJ7QZVNw6unpPfKVJw3VUMIXBeg&s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
st.sidebar.title("AI Usage Tracker")
menu = st.sidebar.radio("Menu", ["Home", "Input AI Usage", "AI Reduction Goals", "Progress Tracker"])

# Main content based on selected menu option
if menu == "Home":
    st.title("Welcome to the AI Usage Tracker")
    st.write("""
    This application helps you monitor and reduce your AI usage to boost creativity. 
    By logging your tasks and analyzing the impact of AI, you can set and achieve goals for minimizing your reliance on AI.
    """)
    st.write("""
    ## Benefits of Reducing AI Usage
    - Enhances personal creativity
    - Improves problem-solving skills
    - Increases personal engagement in tasks
    """)

    st.write("## Measures of Effective AI Utilization")
    if not data.empty:
        st.write("### AI Dependence Score")
        ai_dependence_score = calculate_ai_dependence(data)
        st.write(f"{ai_dependence_score:.2f}%")
        st.progress(ai_dependence_score / 100)

        st.write("### Creativity Score")
        creativity_score = calculate_creativity_score(data)
        st.write(f"{creativity_score:.2f}")

        st.write("### Productivity Score")
        productivity_score = calculate_productivity_score(data)
        st.write(f"{productivity_score:.2f}%")

        st.write("### Time Saved Using AI")
        time_saved = calculate_time_saved(data)
        st.write(f"{time_saved:.2f} hours")

        st.write("### Skill Development Impact")
        skill_impact = calculate_skill_development_impact(data)
        st.write(f"{skill_impact:.2f}")

        st.write("### Task Type Distribution")
        st.bar_chart(data['Task Description'].value_counts())

        st.write("### AI Tool Effectiveness")
        st.bar_chart(data['AI Tool'].value_counts())

    else:
        st.write("No data available. Please log some AI usage to see insights.")

elif menu == "Input AI Usage":
    st.title("Log Your AI Usage")
    task_description = st.text_input("Task Description", "E.g., Developed a marketing report")
    ai_tool = st.text_input("AI Tool/Technology Used", "E.g., GPT-3")
    time_spent_ai = st.number_input("Time Spent on AI (in hours)", min_value=0.0, step=0.5)
    creativity_impact = st.slider("Creativity Impact (1-5 stars)", 1, 5, 3)
    time_saved = st.number_input("Estimated Time Saved (in hours)", min_value=0.0, step=0.5)
    skill_development_impact = st.slider("Skill Development Impact (1-5 stars)", 1, 5, 3)
    task_completion = st.selectbox("Task Completion", ["Completed", "Incomplete"])

    if st.button("Submit"):
        new_data = {
            'Task Description': task_description,
            'AI Tool': ai_tool,
            'Time Spent on AI': time_spent_ai,
            'Creativity Impact': creativity_impact,
            'Time Saved': time_saved,
            'Skill Development Impact': skill_development_impact,
            'Task Completion': task_completion
        }
        save_data(new_data)
        st.success("AI usage logged successfully!")
        st.write("Data saved to ai_usage_data.csv")

elif menu == "AI Reduction Goals":
    st.title("Set Your AI Reduction Goals")
    current_data = load_data()
    if current_data.empty:
        st.warning("No data available. Please log some AI usage first.")
    else:
        ai_dependence_score = calculate_ai_dependence(current_data)
        st.write(f"Current AI Dependence Score: {ai_dependence_score:.2f}%")

        goal_percentage = st.number_input("Set your AI Reduction Goal (in percentage)", min_value=0, max_value=100, step=5)
        st.progress(ai_dependence_score / 100)

        if st.button("Set Goal"):
            st.success("AI reduction goal set successfully!")

elif menu == "Progress Tracker":
    st.title("Track Your Progress")
    current_data = load_data()
    if current_data.empty:
        st.warning("No data available. Please log some AI usage first.")
    else:
        st.write("## AI Usage Summary")
        st.write(current_data)

        ai_dependence_score = calculate_ai_dependence(current_data)
        st.write(f"## AI Dependence Score: {ai_dependence_score:.2f}%")

        st.write("## Creativity Score")
        creativity_score = calculate_creativity_score(current_data)
        st.write(f"{creativity_score:.2f}")

        st.write("## Productivity Score")
        productivity_score = calculate_productivity_score(current_data)
        st.write(f"{productivity_score:.2f}%")

        st.write("## Time Saved Using AI")
        time_saved = calculate_time_saved(current_data)
        st.write(f"{time_saved:.2f} hours")

        st.write("## Skill Development Impact")
        skill_impact = calculate_skill_development_impact(current_data)
        st.write(f"{skill_impact:.2f}")

        st.write("## Task Type Distribution")
        fig, ax = plt.subplots()
        data['Task Description'].value_counts().plot(kind='bar', ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        st.write("## AI Tool Effectiveness")
        fig, ax = plt.subplots()
        data['AI Tool'].value_counts().plot(kind='bar', ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        st.write("## Creativity Impact Analysis")
        fig, ax = plt.subplots()
        ax.bar(data['Task Description'], data['Creativity Impact'])
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        st.write("## Time Comparison")
        fig, ax = plt.subplots()
        ax.bar(data['Task Description'], data['Time Spent on AI'])
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        st.write("## Progress Over Time")
        fig, ax = plt.subplots()
        ax.plot(data.index, data['Time Spent on AI'], marker='o')
        st.pyplot(fig)
