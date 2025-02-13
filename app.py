import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the dashboard
st.title("Basic Data Dashboard")

# Add a welcome message
st.write("Welcome to the Basic Data Dashboard! Upload a CSV file to get started.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Display a success message
    st.success("File uploaded successfully!")

    st.write("### Dataset Preview")

    # # Show the first five rows of the data
    # st.write("Here’s a preview of the dataset:")
    # st.dataframe(df.head())  # Display the first 5 rows of the dataframe

    rows = st.slider("Select number of rows to display", min_value=5, max_value=len(df), value=5)
    st.dataframe(df.head(rows))

    st.write("### Data Insights")

    # Show number of rows and columns
    st.write(f"**Total Rows:** {df.shape[0]}")
    st.write(f"**Total Columns:** {df.shape[1]}")

    # Show column names
    st.write("**Column Names:**", list(df.columns))

    # Show basic statistics
    st.write("### Summary Statistics")
    st.write(df.describe())

    # Show missing values
    st.write("### Missing Values")
    st.write(df.isnull().sum())


    st.write("## Data Visualizations")





    # ---- Select Rows for Visualization ----
    st.write("### Select Rows for Visualization")

    # Slider to select how many rows to use for visualization
    num_rows_to_visualize = st.slider("Select number of rows for visualization:", min_value=5, max_value=len(df), value=min(10, len(df)))

    # Get a subset of the dataframe based on selected rows
    df_visualization = df.head(num_rows_to_visualize)





    st.write("### Column Selection for Visualization")

    # Select column for histogram
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    selected_numeric_columns = st.multiselect("Select numeric columns for visualizations:", numeric_columns, default=numeric_columns[:5])
    selected_categorical_columns = st.multiselect("Select categorical columns for visualizations:", categorical_columns, default=categorical_columns[:5])





    # if numeric_columns:
    #     st.write("### Histogram")
    #     column = st.selectbox("Select a numeric column for histogram:", numeric_columns)
    #
    #     fig, ax = plt.subplots()
    #     sns.histplot(df[column], bins=20, kde=True, ax=ax)
    #     st.pyplot(fig)


    # if selected_numeric_columns:
    #     st.write("### Histograms")
    #     for column in selected_numeric_columns:
    #         fig, ax = plt.subplots()
    #         sns.histplot(df[column], bins=20, kde=True, ax=ax)
    #         ax.set_title(f"Histogram of {column}")
    #         st.pyplot(fig)

    if selected_numeric_columns:
        st.write("### Histograms")
        for column in selected_numeric_columns:
            fig, ax = plt.subplots()
            sns.histplot(df_visualization[column], bins=20, kde=True, ax=ax)
            ax.set_title(f"Histogram of {column} (first {num_rows_to_visualize} rows)")
            st.pyplot(fig)





    # Select column for bar chart

    # if categorical_columns:
    #     st.write("### Bar Chart")
    #     cat_column = st.selectbox("Select a categorical column for bar chart:", categorical_columns)
    #
    #     fig, ax = plt.subplots()
    #     df[cat_column].value_counts().plot(kind="bar", ax=ax, color="skyblue")
    #     ax.set_ylabel("Count")
    #     st.pyplot(fig)


    # if selected_categorical_columns:
    #     st.write("### Bar Charts")
    #     for cat_column in selected_categorical_columns:
    #         fig, ax = plt.subplots()
    #         df[cat_column].value_counts().plot(kind="bar", ax=ax, color="skyblue")
    #         ax.set_ylabel("Count")
    #         ax.set_title(f"Bar Chart of {cat_column}")
    #         st.pyplot(fig)


    if selected_categorical_columns:
        st.write("### Bar Charts")
        for cat_column in selected_categorical_columns:
            fig, ax = plt.subplots()
            df_visualization[cat_column].value_counts().plot(kind="bar", ax=ax, color="skyblue")
            ax.set_ylabel("Count")
            ax.set_title(f"Bar Chart of {cat_column} (first {num_rows_to_visualize} rows)")
            st.pyplot(fig)








    # Correlation heatmap (for numerical columns)
    # if len(numeric_columns) > 1:
    #     st.write("### Correlation Heatmap")
    #     fig, ax = plt.subplots(figsize=(8, 6))
    #     sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
    #     st.pyplot(fig)


    # if len(selected_numeric_columns) > 1:
    #     st.write("### Correlation Heatmap")
    #     fig, ax = plt.subplots(figsize=(8, 6))
    #     sns.heatmap(df[selected_numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
    #     st.pyplot(fig)


    if len(selected_numeric_columns) > 1:
        st.write("### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df_visualization[selected_numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title(f"Correlation Heatmap (first {num_rows_to_visualize} rows)")
        st.pyplot(fig)






    st.write("## Filtering & Searching")

    # Select column to filter
    filter_column = st.selectbox("Select a column to filter:", df.columns)

    # Get unique values in the selected column
    unique_values = df[filter_column].dropna().unique()

    # Create a multiselect for filtering
    selected_values = st.multiselect(f"Filter {filter_column} by:", unique_values)

    # Apply filtering if values are selected
    if selected_values:
        filtered_df = df[df[filter_column].isin(selected_values)]
        st.write("### Filtered Data")
        st.dataframe(filtered_df)
    else:
        st.write("No filter applied. Showing full dataset.")

    # Search box
    search_term = st.text_input("Search for a value in the dataset:")

    if search_term:
        search_results = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False, na=False)).any(axis=1)]
        st.write("### Search Results")
        st.dataframe(search_results)