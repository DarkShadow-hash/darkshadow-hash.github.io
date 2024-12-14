# Synthetic_Data_for_Insurance
This repository contains all the codes and explanations of a project called "Synthetic Data for Insurance" I did with three other students. Have fun reading and implementing it and don't forget to rate this project !
This project provides a Streamlit-based application for generating synthetic datasets using CTGAN (Conditional Generative Adversarial Networks), with customizable constraints on numeric and categorical columns. It enables users to upload datasets, set column constraints, and generate synthetic data while preserving original data distributions.
_________________________________________________________________________________________________________
Features
- Upload and display your dataset (Excel format).
- Set constraints for numeric and categorical columns (e.g., specify age ranges or allowed values for certain fields).
- Generate synthetic data based on the original dataset while adhering to the specified constraints.
- Compare the distributions of original and synthetic data through visualizations.
- Option to combine the original and synthetic datasets or keep them separate.
- Download the generated synthetic dataset in CSV format.
_________________________________________________________________________________________________________
Installation
To run this application, you need Python 3.7 or higher installed. You'll also need to install the required dependencies.
1. Clone the repository or download the script
If you don't already have the repository, clone it using Git or download the script directly.
```bash
git clone https://github.com/your-repo/synthetic-dataset-generator.git
cd synthetic-dataset-generator
```
2. Install dependencies
The required Python libraries are listed below. To install them, you can either use a `requirements.txt` file or manually install each one.
Option 1: Using `requirements.txt`
1. Create a `requirements.txt` file with the following content:
```
streamlit
faker
ctgan
pandas
openpyxl
xlsxwriter
matplotlib
seaborn
numpy
```
2. Install all dependencies using the following command:
```bash
pip install -r requirements.txt
```
Option 2: Manual installation
Alternatively, install each library individually:
```bash
pip install streamlit
pip install faker
pip install ctgan
pip install pandas
pip install openpyxl
pip install xlsxwriter
pip install matplotlib
pip install seaborn
pip install numpy
```
_________________________________________________________________________________________________________
Running the Application
Once all dependencies are installed, you can run the application by using Streamlit.
1. In your terminal, navigate to the directory containing the script and run the following command:
```bash
streamlit run synthetic_dataset_generator.py
```
2. The app will launch in your default web browser at `http://localhost:8501`.
_________________________________________________________________________________________________________
Basic Features
Upload Dataset
- Upload your Excel file through the Streamlit interface.
- The app will read and display your dataset.

Set Constraints
- Numeric Columns: For each numeric column, you can specify minimum and maximum values.
- Categorical Columns: For categorical columns, you can specify the allowed values.

Generate Synthetic Data
- Once you've set the constraints, click on “Generate Synthetic Dataset”.
- The app will train a CTGAN model on your data and generate synthetic records based on your constraints.

Visualize Data
- The app will display visual comparisons (KDE plots and histograms) of the original and synthetic data distributions for both numeric and categorical columns.

Combine or Keep Separate
- You can choose to combine the synthetic dataset with the original dataset or keep them separate.

Download the Dataset
- Download the generated synthetic dataset in CSV format by clicking the “Download Dataset” button.
_________________________________________________________________________________________________________
Dependencies
The application uses the following libraries:
- Faker: Generates synthetic data (names, e-mails, etc.).
- CTGAN: A Conditional Generative Adversarial Network used to generate realistic synthetic data based on the input dataset.
- Pandas: For data manipulation and analysis.
- Streamlit: A framework for building interactive web applications in Python.
- Matplotlib & Seaborn: For visualizing data distributions.
- NumPy: For numerical operations.
- Datetime: To handle and generate date-based data.
