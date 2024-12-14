# Synthetic Data for Insurance


### Context: What is the problem and why does it matter?

Our project aims to generate synthetic datasets specifically for the insurance field. To understand the positive impact synthetic data can have on the world, let’s have a look at a concrete example: Using Synthetic Data to Revolutionize Wheelchair Insurance
Insurance for wheelchairs presents a unique challenge. Wheelchairs are costly, and the relatively small number of people requiring them makes it difficult for insurers to gather enough data to accurately estimate the frequency of claims or the associated costs. This lack of reliable data often results in insurers overestimating the risk and doubling premiums to cover uncertainties, making insurance prohibitively expensive for those who need it most.

To address this, we propose using synthetic data generation to simulate realistic scenarios. By creating artificial datasets that include information about individuals, accidents, health outcomes, and related costs, we can provide insurers with a comprehensive dataset to analyze. These datasets would include synthetic "people" experiencing various health outcomes, accidents, recoveries, and other events that insurance policies would cover.
The goal is to provide a risk model based on simulated trends that closely mirror real-world behavior. With this approach, insurers can define fair and accurate pricing for wheelchair insurance, making it more accessible while maintaining profitability.

_________________________________________________________________________________________
### State of the art
During our researchs, we found some interesting projects that have already been conducted. Some inspiring projects were the following:
Mostly AI
Mostly AI specializes in creating synthetic datasets for insurance and other industries, focusing on privacy preservation and regulatory compliance. They provide tools for insurers to generate synthetic data that mimics real customer and claims data, helping to test models and manage risks without using sensitive data. 
Hazy
Hazy provides tools for generating privacy-preserving synthetic data, particularly for use in finance, insurance, and healthcare. Their platform can simulate large-scale data scenarios, which help insurers understand complex patterns in claims and customer behavior.

_________________________________________________________________________________________
### Contribution: What are we doing that is different?
I believe every project is unique and brings something different. Our way of conducting this project is unique for several reasons.
Unlike many existing generative AI projects, ours enables users to fully customize the dataset they want to generate by allowing them to set constraints (or not if they don’t want to!) for each column (age range, marital status, income level…etc).

We provide the flexibility some users are looking for, as we centered all our project about the possible things the user could ask for.
By adopting the user’s perspective, we identified three main use cases our generative AI system must support:
-	Use case 1: Generating datasets from scratch based on user-specified columns and constraints.
-	Use case 2: Augmenting existing datasets by generating additional rows while preserving the original distributions and correlations
-	Use case 3: Generating synthetic datasets from uploaded data while applying user-defined constraints to specific columns, enabling hybrid customization.
For the last two use cases, we include visualizations so users can compare the distributions of the original and synthetic datasets. While some concepts may seem abstract at this stage, we will delve deeper into them later to provide a clearer understanding.

_________________________________________________________________________________________
### Resources
The project was completed by a team of four contributors: three other AI students and I, Hélène Capon.
To conduct this project, we used our own personal computers as well as a consequent number of python libraries such as Faker, CTGAN, Pandas, Streamlit, Random, Matplotlib, Numpy and Datetime. 
To test our model, we used mainly a dataset a teacher working from the insurance field gave us last year. This dataset contains 3 333 rows and 21 columns. 

This dataset could be used for insurance for telecommunications products. To be brief, this dataset is used for predicting customer churn (when customers leave the service). This information can help in designing policies to retain high-value customers and in targeting those likely to leave with special offers.
Here is an overview of it:
 
### Techniques and Algorithms:
-	CTGAN (Conditional Generative Adversarial Network): The primary algorithm for generating synthetic datasets that preserve the statistical properties of real-world data. CTGAN focuses on maintaining distributions and correlations and is particularly effective for tabular data.
-	Faker: a Python library used to generate fake data for various purposes, such as testing, prototyping, or populating databases. It can create realistic data like names, addresses, emails, phone numbers, dates, and even industry-specific data such as credit card numbers or job titles.


#### How was Use case 1 solved?

We are trying to generate a dataset entirely from the constraints the user enters. To do this, we chose to use Faker, which is a python library used to generate fake or synthetic data, typically for testing, development, or other purposes where real data is not necessary or available. Faker can produce random personal data (ex: names) which is exactly what the user needs in case 1.

#### How was Use case 2 solved?

Our goal in this part of the project was for our generative AI to generate synthetic datasets with the same distributions and correlations as those in a dataset uploaded by the user. In order to reach this goal, after a lot of research, we decided to use CTGAN (Conditional Generative Adversarial Network) which is a machine learning model designed specifically for generating synthetic data that mirrors the distribution of real-world datasets. It is particularly useful when dealing with tabular data that may contain categorical and continuous features, which is a challenge for traditional GAN (Generative Adversarial Network) models. Moreover, CTGAN ensures that the generated data maintains the original distribution and relationships present in the real dataset.

#### How was Use case 3 solved?

The third scenario consists of the user uploading a dataset. A synthetic dataset is generated based on the provided data while applying the user's constraints to the specified columns. This results in some columns having the same distributions as the original columns and some other columns having very different distributions if we compare them with the corresponding original columns. For instance, if we set a constraint for the column “age” (let’s say we want people from 20 to 30 years old) and that in the dataset the age range goes from 15 to 70 years old, when the graphs will be plotted, the distributions will be very different for the column “age”. 

______________________________________________________________________________________
### Results obtained 
Despite having encountered numerous amounts of difficulties, we succeeded into building the three necessary use cases and in implementing them on an interface with streamlit, open-source Python framework for building and sharing interactive, data-driven web applications quickly and easily. 
Our mission was accomplished because all the main goals were reached: 
-	Successfully generated synthetic datasets with realistic distributions and correlations.
-	Built a user-friendly platform that allows users to upload datasets, define constraints, and generate data efficiently.
-	Overcame technical obstacles like tool incompatibilities and performance issues.

______________________________________________________________________________________
### Issues encountered during the project 

This project was a new experience for us, as we had never built a generative AI before. Despite achieving our goal, we faced several challenges:
-	Lack of experience: Addressed through extensive research on similar projects and required libraries.
-	Graph plotting issues: When table_evaluator became incompatible, we wrote custom scripts to evaluate the CTGAN model and compare datasets.
-	Slow dataset generation: Generation time was significant for the third scenario but depended on selected constraints.
-	UI creation: Limited expertise led us to discover Streamlit, which simplified the development process.
  
______________________________________________________________________________________
### Areas of improvement
-	Optimize dataset generation for large or highly constrained datasets.
-	Improve the user interface to include more advanced visualization and customization options.
-	Explore alternative generative AI models to further enhance data quality.









        




         







