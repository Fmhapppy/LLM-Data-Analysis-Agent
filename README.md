# LLM Data Analysis Agent

> An end-to-end AI-powered data analysis platform that combines automated data cleaning, exploratory data analysis, machine learning, visualization, and LLM-based analytical reasoning.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)](https://react.dev/)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange.svg)](https://scikit-learn.org/)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-purple.svg)](https://www.deepseek.com/)

---

## Overview

**LLM Data Analysis Agent** is an AI-assisted data analysis platform designed to automate the process from raw data to actionable insights.

Traditional data analysis often requires users to manually perform multiple steps:

```text
Raw Dataset
    ↓
Data Cleaning
    ↓
Exploratory Data Analysis
    ↓
Visualization
    ↓
Machine Learning
    ↓
Result Interpretation
    ↓
Analytical Report

This project integrates these steps into a unified pipeline and introduces an LLM-powered Analysis Agent that interprets statistical results, machine learning outputs, data quality information, and correlations.

The goal is not to replace traditional statistical or machine learning methods, but to combine them with large language models to create a more accessible and automated data analysis workflow.

Key Features
1. Automated Data Cleaning

The system automatically processes uploaded CSV/Excel datasets.

Current cleaning pipeline includes:

Duplicate row detection and removal
Completely empty column removal
Missing value detection
Median imputation for numerical variables
Mode imputation for categorical variables
Cleaning statistics and processing logs

Example:

Original rows:       122
Cleaned rows:        120
Duplicate rows:        2
Missing values:        5
Remaining missing:    0
2. Exploratory Data Analysis

The EDA module automatically generates:

Descriptive statistics
Data type information
Missing-value statistics
Correlation matrix
Numerical feature relationships

This allows the system to identify potential patterns before machine learning is performed.

3. Machine Learning

The current implementation uses a Random Forest Regression model.

The pipeline automatically:

Selects numerical variables
Separates features and target
Splits the dataset into training and testing sets
Trains the Random Forest model
Generates predictions
Calculates model evaluation metrics
Extracts feature importance

Current evaluation metrics include:

MAE — Mean Absolute Error
RMSE — Root Mean Squared Error
Feature Importance
4. Automated Visualization

The platform generates visualizations automatically using Matplotlib.

Current visualizations include:

Correlation heatmap
Feature-target relationship plot
Feature importance chart

Generated visualization files are stored in:

backend/outputs/
5. LLM-Powered Analysis Agent

The project introduces an AI analysis layer on top of conventional data science methods.

The Agent receives:

Dataset structure
Data cleaning results
EDA statistics
Correlation information
Machine learning metrics
Feature importance

It then produces structured analytical insights.

The Agent is specifically instructed to:

Distinguish correlation from causation
Interpret feature importance correctly
Use actual MAE/RMSE values
Identify potential data-quality issues
Detect distribution or ceiling effects
Combine statistical and machine-learning evidence
Recommend appropriate next-step analyses

Example reasoning:

Correlation ≠ Causation

A strong correlation between study_hours
and final_score indicates statistical association.

It does not prove that increasing study_hours
directly causes higher final_score.
System Architecture
                    ┌─────────────────────┐
                    │     User Dataset    │
                    │   CSV / Excel File  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Data Processor   │
                    │ Load & Inspect Data │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Data Cleaner     │
                    │ Deduplication       │
                    │ Missing Values      │
                    │ Empty Columns       │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
      ┌─────────────────┐          ┌─────────────────┐
      │       EDA       │          │ Machine Learning│
      │ Statistics      │          │ Random Forest   │
      │ Correlation     │          │ MAE / RMSE      │
      └────────┬────────┘          │ Feature Import. │
               │                   └────────┬────────┘
               │                            │
               └──────────────┬─────────────┘
                              ▼
                   ┌─────────────────────┐
                   │    Visualization    │
                   │ Heatmap / Plots     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   Analysis Agent    │
                   │       LLM           │
                   │ Reasoning & Insights│
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   Final AI Report   │
                   │ Insights & Next Step│
                   └─────────────────────┘
Technology Stack
Layer	Technology
Programming Language	Python 3.12
Backend	FastAPI
Data Processing	Pandas, NumPy
Data Analysis	Pandas
Machine Learning	Scikit-learn
Visualization	Matplotlib
Frontend	React
LLM	DeepSeek
API Communication	OpenAI-compatible API
Configuration	python-dotenv
Version Control	Git / GitHub
Project Structure
LLM-Data-Analysis-Agent/
│
├── backend/
│   ├── api.py
│   ├── main.py
│   ├── data_processor.py
│   ├── data_cleaner.py
│   ├── eda.py
│   ├── ml_model.py
│   ├── visualizations.py
│   ├── llm_analyzer.py
│   ├── analysis_agent.py
│   ├── pdf_report.py
│   ├── requirements.txt
│   ├── .env
│   ├── uploads/
│   └── outputs/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── ...
│
├── .gitignore
├── README.md
└── ...

.env, uploaded datasets, generated outputs, virtual environments, and other local files are excluded from version control.

Example Analysis

The included demonstration dataset contains student learning-related variables:

study_hours
sleep_hours
attendance
assignment_score
final_score

The prediction target is:

final_score
Data Cleaning

The demonstration dataset initially contained:

122 rows
5 numerical variables
2 duplicate rows
5 missing values

After cleaning:

Rows:              120
Columns:             5
Duplicates removed:  2
Missing values:      5
Remaining missing:   0
Machine Learning Results

A Random Forest regression model was trained to predict final_score.

Metric	Result
MAE	2.637
RMSE	4.283

Feature importance:

Feature	Importance
study_hours	71.0%
attendance	14.5%
assignment_score	9.4%
sleep_hours	5.1%

These results indicate that study_hours provided the strongest predictive signal within this particular model and dataset.

Importantly, feature importance should not be interpreted as proof of causality.

Statistical Findings

The demonstration dataset produced the following correlations with final_score:

Variable	Correlation with final_score
study_hours	0.682
attendance	0.203
assignment_score	0.167
sleep_hours	-0.123

The relatively strong association between study_hours and final_score makes it an interesting variable for further analysis.

However:

Correlation describes statistical association and does not establish a causal relationship.

The system therefore explicitly separates statistical evidence from causal claims in its AI-generated analysis.

Data Quality Considerations

The AI Analysis Agent also identified a potential ceiling effect in the demonstration dataset.

The distribution of final_score contains a concentration of observations near the maximum score, which may limit the ability of a regression model to distinguish high-performing students.

This is an important example of why model metrics should not be interpreted independently of the underlying data distribution.

AI Analysis Agent

The Analysis Agent combines outputs from multiple analytical components:

Data Cleaning
      +
EDA
      +
Correlation Analysis
      +
Machine Learning
      +
Feature Importance
      ↓
   LLM Agent
      ↓
Structured Insights

The Agent generates structured results in categories including:

Core Findings
Key Factors
Data Quality
Relationships
Model Evaluation
Next Analysis

This allows the LLM to function as an analytical reasoning layer, rather than simply generating a natural-language summary of the dataset.

Example Agent Output

The Agent may identify findings such as:

Core Finding:
study_hours shows the strongest association with final_score.

Key Factor:
study_hours is also the most important feature in the
Random Forest model.

Model Evaluation:
MAE = 2.6367
RMSE = 4.2828

Data Quality:
2 duplicate records were removed and 5 missing values
were imputed.

Next Analysis:
Use cross-validation, residual analysis, alternative
models, and additional explanatory variables to further
evaluate model robustness.
Running Locally
1. Clone the repository
git clone https://github.com/Fmhapppy/LLM-Data-Analysis-Agent.git
cd LLM-Data-Analysis-Agent
2. Create a Python virtual environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate
3. Install backend dependencies
cd backend
pip install -r requirements.txt
4. Configure the LLM API

Create:

backend/.env

Add:

DEEPSEEK_API_KEY=your_api_key_here

Never commit your API key to GitHub.

5. Start the backend

From the backend directory:

uvicorn api:app --reload

The backend will normally be available at:

http://127.0.0.1:8000
6. Start the frontend

Open another terminal:

cd frontend
npm install
npm run dev

Then open the local frontend URL shown by Vite.

API Overview
Health / Root
GET /
Inspect Dataset
POST /inspect

Upload a CSV or Excel file to inspect:

Column names
Data types
Dataset dimensions
Basic information
Analyze Dataset
POST /analyze

The analysis endpoint performs the complete pipeline:

Upload
→ Load
→ Clean
→ EDA
→ Machine Learning
→ Visualization
→ AI Analysis
→ Analysis Agent
→ Report
Design Principles

The project follows several principles when combining AI with data science.

1. Traditional analysis first, LLM reasoning second

The LLM does not replace statistical calculations or machine learning.

Instead:

Data Science Methods
        ↓
Reliable Numerical Results
        ↓
LLM Interpretation

This reduces the risk of allowing the language model to invent numerical findings.

2. Evidence-based AI interpretation

The Agent receives actual computed values such as:

Correlation coefficients
MAE
RMSE
Feature importance
Missing values
Dataset dimensions

The LLM is therefore expected to reason from existing analytical evidence.

3. Correlation is not causation

The system explicitly avoids turning correlations or feature importance into causal claims.

For example:

study_hours → high model importance

does NOT automatically mean

more study_hours → higher final_score

Additional experimental or causal analysis would be required to establish such a relationship.

4. Model results require context

Metrics such as MAE and RMSE are interpreted together with:

Dataset size
Target distribution
Missing values
Feature relationships
Potential ceiling effects
Model limitations
Future Improvements

Several improvements are planned for future versions.

Model Improvements
K-fold cross-validation
Hyperparameter optimization
Linear Regression baseline
Gradient Boosting
XGBoost / LightGBM comparison
Automated model selection
Statistical Analysis
Residual analysis
Outlier detection
Confidence intervals
Statistical significance testing
Distribution analysis
Multicollinearity diagnostics
AI Agent Improvements
Tool-calling architecture
Multi-step reasoning workflow
Automatic hypothesis generation
Automated experiment planning
Agent-driven model comparison
More robust structured output validation
Data Science Improvements
Support for larger datasets
Automatic feature engineering
Categorical variable encoding
Time-series analysis
Classification tasks
Clustering
Anomaly detection
Product Improvements
Interactive visualization
Dataset history
Analysis session management
Exportable analytical reports
More flexible model configuration
Limitations

This project is currently a prototype / portfolio-level AI data analysis system.

Important limitations include:

Demonstration datasets are relatively small.
Random Forest hyperparameters are not extensively optimized.
Model performance is currently evaluated using a single train/test split.
Causal relationships cannot be established from the current analysis pipeline.
LLM-generated interpretations should be reviewed against the underlying numerical results.
The current implementation primarily focuses on numerical datasets.

These limitations provide clear directions for future development.

Learning Outcomes

Through this project, I explored the integration of:

Python
   +
Data Processing
   +
Exploratory Data Analysis
   +
Machine Learning
   +
Data Visualization
   +
LLM APIs
   +
AI Agents
   +
FastAPI
   +
React

More importantly, the project focuses on how LLMs can work together with conventional data science methods rather than treating an LLM as a replacement for statistical or machine learning techniques.

Project Motivation

The motivation behind this project is to explore a practical question:

How can large language models make data analysis more accessible while still preserving the reliability of traditional data science methods?

The project attempts to answer this by combining deterministic data-processing and machine-learning pipelines with an LLM-based reasoning layer.

The resulting workflow transforms raw data into:

Raw Data
    ↓
Clean Data
    ↓
Statistical Evidence
    ↓
Machine Learning Results
    ↓
AI Reasoning
    ↓
Actionable Insights
Author

Fmhapppy

Software Engineering Student

Interested in:

Artificial Intelligence
Data Science
Machine Learning
LLM Applications
AI Agents
Software Engineering

GitHub:

https://github.com/Fmhapppy

License

This project is intended primarily for educational, research, and portfolio purposes.