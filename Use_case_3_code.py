"""
Synthetic Dataset Generator with Constraints

This Streamlit-based application allows users to generate synthetic datasets with user-defined constraints
using the CTGAN (Conditional Tabular GAN) model. It provides the following key features:

1. **Upload Dataset**:
   - Users can upload an Excel dataset to serve as the base for synthetic data generation.

2. **Specify Parameters**:
   - Define the number of rows for the synthetic dataset.
   - Identify categorical columns for better CTGAN training.
   - Set constraints for specific columns, including:
       - **Numeric Constraints**: Define minimum and maximum allowable values.
       - **Categorical Constraints**: Specify allowed categories.

3. **Generate Synthetic Dataset**:
   - The CTGAN model learns the structure and distribution of the uploaded dataset.
   - Synthetic data is generated while respecting user-defined constraints.

4. **Visualization**:
   - The app compares distributions of original and synthetic data for both numerical and categorical columns
     using visual plots (KDE plots and histograms).

5. **Combine or Keep Separate**:
   - Users can choose to combine the synthetic dataset with the original dataset or keep them separate.

6. **Download Dataset**:
   - The final dataset (combined or synthetic only) can be downloaded as a CSV file.

This application is ideal for creating privacy-preserving synthetic data for testing, analysis, or simulation while allowing users to impose constraints for specific scenarios.
"""


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ctgan import CTGAN
import numpy as np

# Title of the app
st.title("Synthetic Dataset Generator with Constraints")

# Step 1: Upload the dataset
uploaded_file = st.file_uploader("Upload your dataset (Excel format)", type=["xlsx"])

if uploaded_file:
    """
    If a file is uploaded:
    - Read the dataset from the uploaded Excel file.
    - Display the original dataset in the Streamlit app.
    """
    original_data = pd.read_excel(uploaded_file)
    st.subheader("Uploaded Dataset")
    st.write(original_data)

    # Number of rows for synthetic data
    num_rows = st.number_input("Enter the number of rows for the generated dataset", min_value=1, step=1)
    
    # Categorical columns input
    categorical_columns = st.text_input("Enter the categorical columns (comma separated):", "")
    categorical_features = [col.strip() for col in categorical_columns.split(',')] if categorical_columns else []

    # Constraint setup
    st.subheader("Column Constraints")
    constraint_columns = st.multiselect("Select columns to apply constraints", original_data.columns)
    
    # Constraint dictionary to store user-defined constraints
    column_constraints = {}
    
    """
    For each selected column, check the column type (numeric or categorical) and collect constraints
    provided by the user. Constraints include minimum and maximum values for numeric columns, 
    and allowed values for categorical columns.
    """
    for col in constraint_columns:
        col_type = original_data[col].dtype
        
        if pd.api.types.is_numeric_dtype(col_type):
            # Numeric column constraints
            min_val = st.number_input(f"Minimum value for {col}", float(original_data[col].min()))
            max_val = st.number_input(f"Maximum value for {col}", float(original_data[col].max()))
            column_constraints[col] = {'type': 'numeric', 'min': min_val, 'max': max_val}
        
        elif pd.api.types.is_categorical_dtype(col_type) or original_data[col].dtype == 'object':
            # Categorical column constraints
            unique_values = original_data[col].unique()
            selected_values = st.multiselect(f"Allowed values for {col}", unique_values, default=list(unique_values))
            column_constraints[col] = {'type': 'categorical', 'allowed_values': selected_values}

    # Generate synthetic dataset with constraints
    if st.button("Generate Synthetic Dataset"):
        """
        If the user clicks the 'Generate Synthetic Dataset' button:
        - Initialize and train the CTGAN model with the original dataset.
        - Generate synthetic samples based on the user-defined number of rows.
        - Apply user-defined constraints to ensure the synthetic data meets specified conditions.
        """
        ctgan = CTGAN(verbose=True)
        ctgan.fit(original_data, categorical_features, epochs=500)
        
        # Generate initial synthetic samples
        samples = ctgan.sample(num_rows)
        
        # Apply constraints for numeric and categorical columns
        for col, constraint in column_constraints.items():
            if constraint['type'] == 'numeric':
                # Filter numeric column based on min and max
                mask = (samples[col] >= constraint['min']) & (samples[col] <= constraint['max'])
                
                # If not enough samples meet the constraint, regenerate
                while mask.sum() < len(samples):
                    additional_samples = ctgan.sample(num_rows - mask.sum())
                    additional_mask = (additional_samples[col] >= constraint['min']) & (additional_samples[col] <= constraint['max'])
                    samples.loc[~mask] = additional_samples.loc[additional_mask]
                    mask = (samples[col] >= constraint['min']) & (samples[col] <= constraint['max'])
            
            elif constraint['type'] == 'categorical':
                # Filter categorical column based on allowed values
                mask = samples[col].isin(constraint['allowed_values'])
                
                # If not enough samples meet the constraint, regenerate
                while mask.sum() < len(samples):
                    additional_samples = ctgan.sample(num_rows - mask.sum())
                    additional_mask = additional_samples[col].isin(constraint['allowed_values'])
                    samples.loc[~mask] = additional_samples.loc[additional_mask]
                    mask = samples[col].isin(constraint['allowed_values'])
        
        # Display synthetic dataset
        st.subheader("Generated Synthetic Dataset")
        st.write(samples)

        # Visualize distributions for numerical columns
        for column in original_data.select_dtypes(include=["float", "int"]).columns:
            """
            For each numerical column:
            - Plot Kernel Density Estimation (KDE) plots to compare the distribution of the original and synthetic data.
            """
            plt.figure(figsize=(10,5))
            sns.kdeplot(original_data[column], label="Original", shade=True)
            sns.kdeplot(samples[column], label="Synthetic", shade=True)
            plt.title(f"Distribution of {column}")
            plt.legend()
            st.pyplot(plt)
            plt.close()

        # Visualize distributions for categorical columns
        for column in original_data.select_dtypes(include=['object', 'category']).columns:
            """
            For each categorical column:
            - Plot histograms with KDE for the original and synthetic data to compare distributions.
            """
            plt.figure(figsize=(10, 5))
            sns.histplot(original_data[column], label="Original", stat="density", kde=True)
            sns.histplot(samples[column], label="Synthetic", stat="density", kde=True)
            plt.title(f"Distribution of {column}")
            plt.legend()
            st.pyplot(plt)
            plt.close()

        # Option to combine original and synthetic datasets
        st.subheader("Do you want to combine the datasets?")
        choice = st.radio("Select an option", ["Combine", "Keep Separate"])

        if choice == "Combine":
            """
            If the user selects 'Combine', concatenate the original dataset with the synthetic dataset.
            Display the combined dataset.
            """
            combined_data = pd.concat([original_data, samples])
            st.subheader("Combined Dataset")
            st.write(combined_data)
        else:
            combined_data = samples

        # Allow the user to download the final dataset (CSV format)
        csv = combined_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Dataset",
            data=csv,
            file_name="synthetic_dataset.csv",
            mime="text/csv",
        )

