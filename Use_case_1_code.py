"""
This script provides a Streamlit-based application for generating synthetic customer data using the 
CustomerDataGenerator class. It supports customization of fields, constraints, and output formats 
such as CSV, Excel, and JSON.

Key Components:
----------------
1. `install_dependencies`:
   Automatically installs required Python libraries if not already present:
   - `streamlit`, `faker`, `pandas`, `openpyxl`, `xlsxwriter`.

2. `CustomerDataGenerator` Class:
   - Generates synthetic customer data with customizable fields such as Customer_ID, Name, Age, Email, 
     Gender, and more.
   - Supports constraints (e.g., age ranges, specific email domains, gender).

3. `streamlit_data_generator`:
   - Interactive Streamlit application for user input and data generation.
   - Allows users to:
     - Select fields to include in the dataset.
     - Define constraints for specific fields (e.g., "Only Gmail emails," "Age: Teenager").
     - Set the number of records to generate (up to 50,000).
     - Download the generated dataset in CSV, Excel, or JSON formats.

4. `main` Function:
   - Entry point for running the Streamlit application.

How It Works:
--------------
- The user interacts with the Streamlit sidebar to configure the dataset:
  - Select fields to include.
  - Define constraints for fields like Age, Gender, Marital Status, etc.
  - Set the number of rows.
- After clicking "Generate Data," the application generates a synthetic dataset and displays it in a table.
- Users can download the dataset in multiple formats.

Dependencies:
--------------
- Python 3.7 or higher.
- Required libraries:
  - streamlit
  - faker
  - pandas
  - openpyxl
  - xlsxwriter

Usage:
------
1. Run the script:
   ```bash
   streamlit run <script_name>.py """

import sys
import subprocess

def install_dependencies():
    """
    Automatically install required dependencies if not already present.
    This function attempts to install specified packages using pip.
    """
    required_packages = [
        'streamlit', 
        'faker', 
        'pandas', 
        'openpyxl', 
        'xlsxwriter', 
    ]

    for package in required_packages:
        try:
            __import__(package)  # Check if the package is already installed
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"{package} installed successfully.")

install_dependencies()

import random
from faker import Faker
import pandas as pd
import datetime
import os
import streamlit as st
import xlsxwriter  

class CustomerDataGenerator:
    """
    A class to generate synthetic customer data with customizable fields and constraints.
    """
    def __init__(self):
        """
        Initializes the CustomerDataGenerator with available fields and a Faker instance.
        """
        self.faker = Faker()
        self.available_fields = [
            'Customer_ID', 'Name', 'Age', 'Email', 
            'Gender', 'Marital Status', 'Disability', 
            'Hospital Visits', 'Policy Start Date', 'Policy End Date'
        ]

    def generate_customer_id(self):
        """
        Generate a unique random customer ID in the format "CUST-####".
        Returns:
            str: A string representing the customer ID.
        """
        return f"CUST-{random.randint(1000, 9999)}"

    def generate_name(self):
        """
        Generate a random name using the Faker library.
        Returns:
            str: A string representing the name.
        """
        return self.faker.name()

    def generate_age(self, age_constraint=None):
        """
        Generate a random age, optionally constrained to a specific range.
        Args:
            age_constraint (str): A predefined age group ('Child', 'Teenager', etc.).
        Returns:
            int: A randomly generated age.
        """
        if age_constraint == 'Child':
            return random.randint(1, 12)
        elif age_constraint == 'Teenager':
            return random.randint(13, 19)
        elif age_constraint == 'Young Adult':
            return random.randint(20, 35)
        elif age_constraint == 'Middle Age':
            return random.randint(36, 55)
        elif age_constraint == 'Senior':
            return random.randint(56, 85)
        else:
            return random.randint(1, 85)

    def generate_email(self, name, email_constraint=None):
        """
        Generate a random email address based on the name and optional domain constraint.
        Args:
            name (str): The user's name to be used in the email address.
            email_constraint (str): Specific email domain (e.g., 'Gmail').
        Returns:
            str: A string representing the email address.
        """
        email_domains = []
        if email_constraint == 'Gmail':
            email_domains = ['gmail.com']
        elif email_constraint == 'Yahoo':
            email_domains = ['yahoo.com']
        elif email_constraint == 'Hotmail':
            email_domains = ['hotmail.com']
        else:
            email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        
        formatted_name = name.lower().replace(' ', '.')
        return f"{formatted_name}@{random.choice(email_domains)}"

    def generate_gender(self, gender_constraint=None):
        """
        Generate a random gender or use a specified gender constraint.
        Args:
            gender_constraint (str): Optional predefined gender ('Male', 'Female', 'Other').
        Returns:
            str: The generated gender.
        """
        if gender_constraint:
            return gender_constraint
        return random.choice(['Male', 'Female', 'Other'])

    def generate_marital_status(self, marital_constraint=None):
        """
        Generate a random marital status, with optional constraints.
        Args:
            marital_constraint (str): 'Yes' for Married/Divorced/Widowed, 'No' for Single.
        Returns:
            str: The generated marital status.
        """
        if marital_constraint == 'Yes':
            return random.choice(['Married', 'Divorced', 'Widowed'])
        elif marital_constraint == 'No':
            return 'Single'
        else:
            return random.choice(['Single', 'Married', 'Divorced', 'Widowed'])

    def generate_disability(self, disability_constraint=None):
        """
        Generate a random disability status with weighted probabilities.
        Args:
            disability_constraint (str): 'Yes' for specific disabilities, 'No' for None.
        Returns:
            str: The generated disability status.
        """
        disabilities = [
            'None', 'Physical', 'Visual', 'Hearing', 
            'Cognitive', 'Chronic Condition'
        ]
        
        if disability_constraint == 'Yes':
            return random.choice(disabilities[1:])
        elif disability_constraint == 'No':
            return 'None'
        else:
            return random.choices(
                disabilities, 
                weights=[70, 10, 5, 5, 5, 5]
            )[0]

    def generate_hospital_visits(self):
        """
        Generate a random number of hospital visits between 0 and 10.
        Returns:
            int: The generated number of hospital visits.
        """
        return random.randint(0, 10)

    def generate_policy_date(self, date_constraint=None):
        """
        Generate a random date based on constraints (e.g., last year, next 5 years).
        Args:
            date_constraint (str/dict): A predefined range or custom start and end dates.
        Returns:
            datetime.date: A random date within the specified range.
        """
        today = datetime.date.today()
        
        if date_constraint == 'Last Year':
            start = today - datetime.timedelta(days=365)
            end = today
        elif date_constraint == 'Last 2 Years':
            start = today - datetime.timedelta(days=730)
            end = today
        elif date_constraint == 'Last 5 Years':
            start = today - datetime.timedelta(days=1825)
            end = today
        elif date_constraint == 'Next Year':
            start = today
            end = today + datetime.timedelta(days=365)
        elif date_constraint == 'Next 2 Years':
            start = today
            end = today + datetime.timedelta(days=730)
        elif date_constraint == 'Next 5 Years':
            start = today
            end = today + datetime.timedelta(days=1825)
        elif isinstance(date_constraint, dict) and date_constraint.get('type') == 'custom':
            start = datetime.datetime.strptime(date_constraint['start'], '%Y-%m-%d').date()
            end = datetime.datetime.strptime(date_constraint['end'], '%Y-%m-%d').date()
        else:
            start = today - datetime.timedelta(days=1825)
            end = today + datetime.timedelta(days=1825)
        
        time_between_dates = end - start
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start + datetime.timedelta(days=random_number_of_days)

    def generate_data(self, selected_fields, constraints, num_records):
        """
        Generate a synthetic dataset based on selected fields and constraints.
        Args:
            selected_fields (list): Fields to include in the dataset.
            constraints (dict): Constraints for specific fields (e.g., age ranges).
            num_records (int): Number of records to generate.
        Returns:
            pd.DataFrame: A Pandas DataFrame containing the generated dataset.
        """
        data = []
        for _ in range(num_records):
            record = {}
            for field in selected_fields:
                if field == 'Customer_ID':
                    record[field] = self.generate_customer_id()
                elif field == 'Name':
                    name = self.generate_name()
                    record[field] = name
                elif field == 'Age':
                    record[field] = self.generate_age(constraints.get('Age', None))
                elif field == 'Email':
                    record[field] = self.generate_email(
                        record.get('Name', self.generate_name()),
                        constraints.get('Email', None)
                    )
                elif field == 'Gender':
                    record[field] = self.generate_gender(constraints.get('Gender', None))
                elif field == 'Marital Status':
                    record[field] = self.generate_marital_status(
                        constraints.get('Marital Status', None)
                    )
                elif field == 'Disability':
                    record[field] = self.generate_disability(
                        constraints.get('Disability', None)
                    )
                elif field == 'Hospital Visits':
                    record[field] = self.generate_hospital_visits()
                elif field == 'Policy Start Date':
                    record[field] = self.generate_policy_date(
                        constraints.get('Policy Start Date', None)
                    )
                elif field == 'Policy End Date':
                    record[field] = self.generate_policy_date(
                        constraints.get('Policy End Date', None)
                    )
            data.append(record)
        return pd.DataFrame(data)

def streamlit_data_generator():
    """
    Launch the Streamlit application to interactively generate synthetic data.
    Provides options for selecting fields, applying constraints, and downloading results.
    """
    st.title("Customer Data Generator")

    generator = CustomerDataGenerator()

    st.sidebar.header("Data Generation Settings")
    
    st.sidebar.subheader("Select Fields")
    selected_fields = st.sidebar.multiselect(
        "Choose Fields to Generate", 
        generator.available_fields,
        default=['Customer_ID', 'Name', 'Age']
    )

    constraints = {}

    # Handle constraints for each field
    if 'Age' in selected_fields:
        st.sidebar.subheader("Age Constraints")
        age_constraint = st.sidebar.selectbox(
            "Age Group", 
            ['All', 'Child', 'Teenager', 'Young Adult', 'Middle Age', 'Senior']
        )
        constraints['Age'] = age_constraint if age_constraint != 'All' else None

    if 'Email' in selected_fields:
        st.sidebar.subheader("Email Constraints")
        email_constraint = st.sidebar.selectbox(
            "Email Domain", 
            ['All', 'Gmail', 'Yahoo', 'Hotmail']
        )
        constraints['Email'] = email_constraint if email_constraint != 'All' else None

    if 'Gender' in selected_fields:
        st.sidebar.subheader("Gender Constraints")
        gender_constraint = st.sidebar.selectbox(
            "Gender", 
            ['All', 'Male', 'Female', 'Other']
        )
        constraints['Gender'] = gender_constraint if gender_constraint != 'All' else None

    if 'Marital Status' in selected_fields:
        st.sidebar.subheader("Marital Status Constraints")
        marital_constraint = st.sidebar.selectbox(
            "Marital Status", 
            ['All', 'Yes', 'No']
        )
        constraints['Marital Status'] = marital_constraint if marital_constraint != 'All' else None

    if 'Disability' in selected_fields:
        st.sidebar.subheader("Disability Constraints")
        disability_constraint = st.sidebar.selectbox(
            "Disability", 
            ['All', 'Yes', 'No']
        )
        constraints['Disability'] = disability_constraint if disability_constraint != 'All' else None

    # Handle date constraints
    date_fields = [field for field in ['Policy Start Date', 'Policy End Date'] if field in selected_fields]
    for field in date_fields:
        st.sidebar.subheader(f"{field} Constraints")
        date_constraint_type = st.sidebar.selectbox(
            f"{field} Range", 
            ['All', 'Last Year', 'Last 2 Years', 'Last 5 Years', 
             'Next Year', 'Next 2 Years', 'Next 5 Years', 'Custom Date Range']
        )
        
        if date_constraint_type == 'Custom Date Range':
            start_date = st.sidebar.date_input(f"{field} Start Date")
            end_date = st.sidebar.date_input(f"{field} End Date")
            constraints[field] = {
                'type': 'custom',
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            }
        elif date_constraint_type != 'All':
            constraints[field] = date_constraint_type

    num_records = st.sidebar.slider(
        "Number of Records", 
        min_value=1, 
        max_value=50000, 
        value=100
    )

    if st.sidebar.button("Generate Data"):
        if not selected_fields:
            st.error("Please select at least one field.")
            return

        generated_data = generator.generate_data(selected_fields, constraints, num_records)
        
        st.dataframe(generated_data)

        st.subheader("Download Generated Data")
        
        csv = generated_data.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='generated_customer_data.csv',
            mime='text/csv'
        )

        excel_buffer = pd.ExcelWriter('generated_customer_data.xlsx', engine='xlsxwriter')
        generated_data.to_excel(excel_buffer, index=False)
        excel_buffer.save()
        
        with open('generated_customer_data.xlsx', 'rb') as f:
            st.download_button(
                label="Download as Excel",
                data=f,
                file_name='generated_customer_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        json_data = generated_data.to_json(orient='records')
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name='generated_customer_data.json',
            mime='application/json'
        )

def main():
    """
    Main entry point for running the Streamlit data generation application.
    """
    streamlit_data_generator()

if __name__ == "__main__":
    main()
