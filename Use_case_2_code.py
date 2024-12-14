"""
Synthetic Dataset Generator Application

This Streamlit-based application enables users to upload a dataset, specify parameters,
and generate a synthetic dataset using the CTGAN (Conditional Tabular GAN) model. 
The app provides the following features:

1. **Upload Dataset**:
   - Users can upload an Excel dataset which serves as the basis for generating synthetic data.

2. **Specify Parameters**:
   - Users can input the number of rows for the synthetic dataset.
   - Categorical columns can be specified to guide the CTGAN model during training.

3. **Generate Synthetic Dataset**:
   - The CTGAN model trains on the uploaded dataset to learn its structure and relationships.
   - A synthetic dataset is generated with the same statistical distributions and relationships.

4. **Visualization**:
   - The app plots side-by-side comparisons of the original and synthetic data distributions 
     (for both numerical and categorical columns).

5. **Combine Datasets**:
   - Users have the option to combine the original and synthetic datasets into one.

6. **Download Dataset**:
   - The final dataset (combined or synthetic only) can be downloaded in CSV format.

This tool is ideal for generating synthetic data for testing, simulation, or research purposes 
while preserving the privacy of the original data.
"""


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from ctgan import CTGAN

# Title of the app
st.title("Synthetic Dataset Generator")

# Step 1: Upload the dataset
uploaded_file = st.file_uploader("Upload your dataset (Excel format)", type=["xlsx"])

if uploaded_file:
    """
    If a file is uploaded:
    - Read the dataset using pandas.
    - Display the uploaded dataset in the Streamlit app.
    """
    original_data = pd.read_excel(uploaded_file)
    st.subheader("Uploaded Dataset")
    st.write(original_data)

    # Input for the number of rows in the synthetic dataset
    num_rows = st.number_input("Enter the number of rows for the generated dataset", min_value=1, step=1)

    # Input for specifying categorical columns
    categorical_columns = st.text_input("Enter the categorical columns (comma separated):", "")

    if categorical_columns:
        """
        If categorical columns are specified:
        - Parse the input into a list of column names.
        - Display the specified categorical columns.
        """
        categorical_features = [col.strip() for col in categorical_columns.split(',')]
        st.write("Categorical Columns: ", categorical_columns)

    # Step 3: Generate synthetic dataset
    if st.button("Generate Synthetic Dataset"): 
        """
        Generate a synthetic dataset using CTGAN:
        - Initialize the CTGAN model.
        - Train it on the uploaded dataset with specified categorical features.
        - Generate a synthetic dataset with the specified number of rows.
        """
        ctgan = CTGAN(verbose=True)
        ctgan.fit(original_data, categorical_features, epochs=500)
        samples = ctgan.sample(num_rows)
        st.subheader("Generated Synthetic Dataset")
        st.write(samples)

        # Generate graphs for numerical columns
        for column in original_data.select_dtypes(include=["float", "int"]).columns:
            """
            For each numerical column:
            - Plot Kernel Density Estimation (KDE) plots for original and synthetic data.
            - Display the plot in the Streamlit app.
            """
            plt.figure(figsize=(10, 5))
            sns.kdeplot(original_data[column], label="Original", shade=True)
            sns.kdeplot(samples[column], label="Synthetic", shade=True)
            plt.title(f"Distribution of {column}")
            plt.legend()
            st.pyplot(plt)
            plt.close()

        # Generate graphs for categorical columns
        for column in original_data.select_dtypes(include=['object', 'category']).columns:
            """
            For each categorical column:
            - Plot histograms for original and synthetic data.
            - Display the plot in the Streamlit app.
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
            If the user chooses to combine datasets:
            - Concatenate the original and synthetic datasets.
            - Display the combined dataset.
            """
            combined_data = pd.concat([original_data, samples])
            st.subheader("Combined Dataset")
            st.write(combined_data)
        else:
            combined_data = samples

        # Allow the user to download the final dataset
        csv = combined_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Dataset",
            data=csv,
            file_name="synthetic_dataset.csv",
            mime="text/csv",
        )
