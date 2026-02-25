import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import numpy as np


# 1. THE DATASET (Hardcoded from your research notes for instant launch)
def get_data():
    data = [
        ["P1", 5.25, 4, 87, 91.72, 285.3, 97.9, 28, 7.21, "Male"],
        ["P2", 8.63, 4, 7.38, 23.86, 256.75, 39, 0, 0, "Male"], # Note: Data cleanup applied to match structure
        # ... [Truncated for brevity in display, but full logic below handles the 60 entries]
    ]
    # For the sake of the app, I've parsed your raw string into a clean dictionary format:
    raw_data = {
        'Participant_ID': [f"P{i}" for i in range(1, 61)],
        'Sleep_Hours': [5.25, 8.53, 7.29, 6.53, 4.00, 4.00, 3.45, 8.05, 6.54, 7.15, 3.23, 8.64, 7.86, 4.33, 4.15, 4.16, 4.85, 6.11, 5.58, 4.78, 6.60, 3.91, 4.78, 5.20, 5.71, 7.59, 4.25, 6.05, 6.49, 3.38, 6.58, 4.09, 3.49, 8.52, 8.62, 7.72, 4.85, 3.67, 7.02, 5.62, 3.81, 5.94, 3.31, 8.30, 4.59, 6.89, 4.89, 6.08, 6.23, 4.17, 8.64, 7.53, 8.47, 8.22, 6.52, 8.37, 3.62, 4.23, 3.37, 4.97],
        'Sleep_Quality_Score': [4, 7, 2, 6, 9, 3, 0, 7, 7, 4, 1, 6, 4, 3, 3, 9, 7, 6, 5, 3, 8, 2, 7, 5, 2, 8, 5, 3, 5, 1, 2, 6, 7, 5, 4, 8, 1, 4, 3, 6, 1, 4, 1, 6, 2, 8, 1, 1, 8, 1, 2, 3, 8, 7, 2, 1, 0, 5, 7, 2],
        'Caffeine_Intake': [87, 26, 224, 308, 197, 209, 171, 10, 43, 12, 254, 125, 203, 363, 99, 164, 302, 91, 30, 115, 64, 371, 323, 253, 348, 321, 74, 57, 215, 322, 358, 127, 44, 91, 170, 327, 344, 32, 204, 166, 88, 47, 135, 377, 129, 207, 281, 145, 388, 84, 100, 198, 120, 113, 14, 243, 201, 20, 111, 363],
        'PVT_Reaction_Time': [285.29, 304.31, 266.30, 270.77, 333.90, 367.88, 418.92, 220.73, 299.72, 246.54, 438.17, 276.98, 216.22, 356.46, 342.15, 296.88, 324.13, 275.71, 315.71, 341.15, 311.12, 412.21, 354.92, 344.64, 321.96, 250.28, 280.42, 222.97, 272.95, 386.32, 266.81, 298.96, 358.34, 255.71, 232.56, 247.40, 288.20, 401.95, 291.81, 318.85, 428.48, 276.87, 483.67, 300.30, 355.90, 292.86, 315.45, 281.26, 299.44, 296.14, 231.66, 194.92, 221.84, 294.83, 257.97, 235.46, 421.53, 266.63, 440.36, 352.99],
        'P300_Latency': [328.52, 342.22, 333.69, 339.16, 370.72, 387.71, 413.23, 314.13, 353.63, 327.04, 422.85, 342.26, 311.88, 382.00, 374.84, 352.21, 365.83, 341.63, 361.63, 374.35, 359.33, 409.88, 381.23, 376.09, 364.75, 328.91, 343.98, 315.26, 340.24, 396.93, 337.17, 353.25, 382.94, 331.63, 320.05, 327.47, 347.87, 404.75, 349.67, 363.20, 418.01, 342.20, 445.60, 353.92, 381.72, 350.20, 361.50, 344.40, 353.49, 351.84, 319.60, 301.23, 314.69, 351.19, 332.75, 321.50, 414.53, 337.08, 423.95, 380.26],
        'N_Back_Accuracy': [97.9, 87.3, 100.0, 85.3, 71.6, 76.8, 71.3, 93.9, 84.3, 87.5, 61.4, 84.0, 87.4, 85.7, 84.6, 77.3, 75.6, 89.2, 89.7, 80.0, 93.5, 60.9, 78.3, 81.2, 78.6, 84.5, 84.4, 85.9, 99.5, 65.4, 89.3, 80.1, 61.4, 91.5, 95.0, 98.4, 75.6, 58.8, 92.2, 82.7, 69.2, 79.8, 64.9, 90.8, 82.3, 91.7, 74.4, 80.0, 82.8, 74.6, 99.8, 100.0, 91.8, 91.9, 90.3, 94.0, 66.6, 75.3, 66.7, 76.8],
        'Age': [28, 20, 33, 26, 21, 18, 21, 18, 31, 38, 33, 37, 41, 25, 24, 20, 34, 18, 33, 29, 36, 39, 40, 39, 31, 23, 23, 30, 36, 39, 25, 19, 38, 18, 32, 18, 22, 33, 36, 21, 20, 34, 34, 29, 31, 38, 23, 20, 26, 22, 41, 34, 31, 38, 20, 18, 37, 38, 40, 18],
        'Gender': ["Male", "Male", "Male", "Female", "Male", "Female", "Female", "Male", "Female", "Male", "Female", "Female", "Male", "Male", "Female", "Male", "Male", "Male", "Male", "Female", "Male", "Male", "Male", "Female", "Male", "Female", "Male", "Female", "Male", "Male", "Male", "Female", "Female", "Male", "Female", "Female", "Male", "Male", "Male", "Male", "Female", "Female", "Female", "Male", "Male", "Female", "Female", "Female", "Female", "Female", "Male", "Male", "Female", "Male", "Male", "Male", "Female", "Male", "Male", "Male"]
    }
    return pd.DataFrame(raw_data)


# --- APP SETUP ---
st.set_page_config(page_title="NeuroCC | Advanced Analytics", layout="wide")
df = get_data()


st.title("NeuroCC: Full-Spectrum Research Dashboard")
st.markdown("---")


# 2. SIDEBAR - CONTROLS
st.sidebar.header("Variable Controls")
target_var = st.sidebar.selectbox("Select Dependent Variable", ["PVT_Reaction_Time", "P300_Latency", "N_Back_Accuracy"])
gender_filter = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
age_range = st.sidebar.slider("Age Filter", int(df['Age'].min()), int(df['Age'].max()), (18, 45))


filtered_df = df[(df['Gender'].isin(gender_filter)) & (df['Age'].between(age_range[0], age_range[1]))]


# 3. MAIN KPIS
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Sample Size", len(filtered_df))
kpi2.metric("Avg Sleep", f"{filtered_df['Sleep_Hours'].mean():.1f}h")
kpi3.metric("Avg RT", f"{filtered_df['PVT_Reaction_Time'].mean():.1f}ms")
kpi4.metric("Avg Accuracy", f"{filtered_df['N_Back_Accuracy'].mean():.1f}%")


# 4. ANALYTICS TABS
tab1, tab2, tab3 = st.tabs(["Regression & Impact", "3D Landscape", "Dataset"])


with tab1:
    st.subheader(f"Multivariate OLS Regression: Predicting {target_var}")
   
    # Prep data for regression
    reg_df = filtered_df.copy()
    reg_df['Gender_Bin'] = reg_df['Gender'].map({'Male': 0, 'Female': 1})
   
    X = reg_df[['Sleep_Hours', 'Sleep_Quality_Score', 'Caffeine_Intake', 'Age', 'Gender_Bin']]
    X = sm.add_constant(X)
    y = reg_df[target_var]
   
    model = sm.OLS(y, X).fit()
   
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.write("**Coefficient Analysis**")
        st.dataframe(model.params.rename("Effect Size"))
        st.write(f"**Model R-Squared:** {model.rsquared:.3f}")
       
    with col_right:
        # Forest Plot (Coefficient Visualizer)
        coef_df = model.params[1:].reset_index()
        coef_df.columns = ['Variable', 'Value']
        fig_coef = px.bar(coef_df, x='Value', y='Variable', orientation='h',
                          title="Variable Influence (Weight)",
                          color='Value', color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_coef, use_container_width=True)


with tab2:
    st.subheader("The Cognitive Horizon")
    st.info("Rotate this graph to see how low sleep creates a 'performance cliff' that caffeine cannot bridge.")
    fig_3d = px.scatter_3d(
        filtered_df, x='Sleep_Hours', y='Caffeine_Intake', z=target_var,
        color='N_Back_Accuracy', size='Age', opacity=0.8,
        hover_data=['Participant_ID'],
        color_continuous_scale='Viridis',
        title=f"3D Mapping: Sleep vs Caffeine vs {target_var}"
    )
    st.plotly_chart(fig_3d, use_container_width=True)


with tab3:
    st.subheader("Raw Research Data")
    st.dataframe(filtered_df.style.highlight_max(axis=0, subset=['PVT_Reaction_Time'], color='#ff4b4b33'))


# 5. BRAINWAVE VS REACTION TIME
st.markdown("---")
st.subheader("The P300 vs PVT Correlation")
fig_corr = px.scatter(filtered_df, x="P300_Latency", y="PVT_Reaction_Time",
                     trendline="ols", color="Sleep_Hours",
                     title="Does Neural Processing Speed (P300) Predict Physical Speed (PVT)?")
st.plotly_chart(fig_corr, use_container_width=True)

