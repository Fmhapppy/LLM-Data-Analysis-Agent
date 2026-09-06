# LLM Data Analysis Agent

> An LLM-based intelligent data analysis assistant integrating data cleaning, exploratory data analysis, machine learning, AI reasoning, visualization, and automated report generation.

---

## Overview

**LLM Data Analysis Agent** is an end-to-end AI-powered data analysis platform designed to transform raw tabular data into structured insights and automated analytical reports.

The system integrates traditional data science techniques with Large Language Models (LLMs) and AI Agents.

Users can upload CSV or Excel datasets, select a prediction target, and automatically complete the following workflow:

```text
Data Upload
    ↓
Data Inspection
    ↓
Data Cleaning
    ↓
Exploratory Data Analysis
    ↓
Machine Learning
    ↓
Data Visualization
    ↓
AI Insights
    ↓
AI Agent Deep Analysis
    ↓
Automated PDF Report

The project focuses on combining data science, machine learning, LLM applications, and AI agents into a practical end-to-end system.

Screenshots
Dashboard

Data Cleaning

Data Visualization

Machine Learning

AI Insights

AI Agent Deep Analysis

Key Features
1. Intelligent Data Upload
Supports CSV and Excel files
Automatically detects dataset columns
Identifies numerical features
Allows users to select the prediction target
Provides basic dataset inspection before analysis
2. Automated Data Cleaning

The system automatically detects and processes common data quality issues.

Current cleaning operations include:

Duplicate row detection and removal
Missing value detection
Median imputation for numerical variables
Mode imputation for categorical variables
Completely empty column detection and removal
Cleaning process logging
Before-and-after dataset comparison

Example:

Original dataset:
122 rows × 5 columns

After cleaning:
120 rows × 5 columns

Duplicate rows removed:
2

Missing values processed:
5

Remaining missing values:
0
3. Exploratory Data Analysis

The EDA module automatically generates:

Descriptive statistics
Missing-value statistics
Data type information
Correlation matrix
Numerical feature relationships

This provides a statistical foundation for subsequent machine learning and AI analysis.

4. Machine Learning

The current implementation uses a Random Forest Regression model for numerical prediction tasks.

The system automatically calculates:

MAE (Mean Absolute Error)
RMSE (Root Mean Squared Error)
Feature importance

Example:

Model:
Random Forest Regression

MAE:
2.637

RMSE:
4.283

Feature importance:

study_hours        71.0%
attendance         14.5%
assignment_score   9.4%
sleep_hours        5.1%
5. Automated Data Visualization

The system generates multiple visualizations automatically:

Correlation heatmap
Feature-target relationship visualization
Feature importance chart

These visualizations help users understand the underlying statistical relationships and machine learning results.

6. AI Insights

After statistical analysis and machine learning, the system uses an LLM to generate structured insights.

The AI analyzes:

Dataset characteristics
Data quality
Correlation results
Machine learning performance
Feature importance
Potential analytical issues
Recommendations for further analysis

The goal is not simply to generate natural-language summaries, but to connect the outputs of traditional data analysis with AI-generated interpretation.

7. AI Agent Deep Analysis

The project also includes a dedicated AI Agent layer.

Instead of analyzing the raw dataset independently, the Agent receives the results produced by the data analysis pipeline and performs a second-level reasoning process.

The Agent considers:

EDA results
Correlation relationships
Machine learning results
Feature importance
Model evaluation metrics
Data quality issues
Potential statistical limitations
Further analysis strategies

The Agent is explicitly instructed to distinguish between:

Correlation ≠ Causation

It also avoids interpreting machine learning feature importance as direct causal effects.

8. Automated PDF Report

After the analysis pipeline is completed, the system automatically generates a structured PDF report containing:

Dataset overview
Data cleaning results
Data visualization
Machine learning evaluation
Feature importance
AI-generated insights
AI Agent deep analysis
Recommendations for future analysis

This allows the complete analysis process to be preserved as a reusable analytical report.

System Architecture
                    ┌──────────────────────┐
                    │      Frontend        │
                    │   React / Vite       │
                    └──────────┬───────────┘
                               │
                               │ HTTP API
                               ↓
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │     Backend API      │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ↓                ↓                ↓
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │ Data         │ │ EDA          │ │ Machine      │
      │ Processing   │ │ Analysis     │ │ Learning     │
      └──────────────┘ └──────────────┘ └──────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │    Visualization     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │     AI Insights      │
                    │      LLM Layer       │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │      AI Agent        │
                    │  Deep Reasoning      │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    PDF Report        │
                    └──────────────────────┘
Technology Stack
Backend
Python
FastAPI
Pandas
NumPy
Scikit-learn
Matplotlib
OpenAI-compatible API
DeepSeek LLM
Frontend
React
Vite
JavaScript
CSS
Machine Learning
Random Forest Regression
Train/Test Split
MAE
RMSE
Feature Importance
AI
Large Language Model
AI Agent
Structured JSON reasoning
Automated analytical interpretation
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
│   ├── uploads/
│   ├── outputs/
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── screenshots/
│   ├── dashboard.png
│   ├── data-cleaning.png
│   ├── visualization.png
│   ├── machine-learning.png
│   ├── ai-insights.png
│   └── ai-agent.png
│
├── README.md
└── .gitignore
Example Analysis

The project was tested using a student learning dataset containing the following variables:

study_hours
sleep_hours
attendance
assignment_score
final_score

The prediction target was:

final_score

The analysis pipeline produced the following results.

Dataset
Original records:     122
Cleaned records:      120
Features:             5
Retention rate:       98.4%
Data Cleaning
Duplicate rows removed:       2
Missing values processed:     5
Empty columns removed:        0
Remaining missing values:     0
Machine Learning
Model: Random Forest Regression

MAE:  2.637
RMSE: 4.283
Feature Importance
study_hours        71.0%
attendance         14.5%
assignment_score    9.4%
sleep_hours         5.1%
Statistical Findings

The correlation analysis showed that study_hours had the strongest relationship with final_score.

study_hours        → final_score     0.682
attendance         → final_score     0.203
assignment_score   → final_score     0.167
sleep_hours        → final_score    -0.123

The machine learning model also identified study_hours as the most important predictive feature.

This consistency between correlation analysis and model-based feature importance provides a useful analytical signal.

However, the system explicitly treats these results as associations and predictive relationships rather than causal effects.

Data Quality Analysis

The dataset contained:

2 duplicate records
5 missing values

The cleaning pipeline automatically removed the duplicate records and filled numerical missing values using median imputation.

After cleaning:

Remaining missing values = 0

The AI Agent also identified an important limitation in the target variable.

final_score showed a strong ceiling effect:

Mean:       95.9
Median:     100
75th pct:   100
Minimum:    70.4

A large number of students received full marks, reducing the variability of the target variable.

This may limit the ability of a standard regression model to distinguish between high-performing students.

AI Agent Reasoning

The AI Agent combines statistical analysis with machine learning results instead of treating them independently.

For example:

Correlation:
study_hours → final_score = 0.682

Machine Learning:
study_hours importance = 0.710

Agent Interpretation:
study_hours is the strongest predictive variable in the
current dataset, but this does not establish a causal relationship.

The Agent also considers potential issues such as:

Target ceiling effects
Small sample size
Distribution skew
Model generalization
Possible confounding variables
Larger individual prediction errors

This makes the AI layer more analytical and less dependent on simple text summarization.

Model Evaluation

The Random Forest model achieved:

MAE  = 2.637
RMSE = 4.283

MAE indicates that predictions differ from actual values by approximately 2.64 points on average.

The larger RMSE indicates that some individual predictions have relatively larger errors.

The project therefore does not treat the current model as a final production-grade predictive system.

Instead, the model is used as an analytical component within the larger AI-powered data analysis workflow.

Future Improvements

Several improvements are planned for future versions.

1. Cross-Validation

Implement:

5-fold cross-validation
10-fold cross-validation

This would provide a more reliable evaluation of model stability and generalization.

2. Model Comparison

Compare multiple algorithms:

Linear Regression
Random Forest
Gradient Boosting
Support Vector Regression
XGBoost

This would provide a more comprehensive model evaluation framework.

3. Advanced Feature Engineering

Potential derived features include:

learning_efficiency
assignment_score / study_hours

sleep_deficit
expected_sleep - sleep_hours

study_sleep_interaction
study_hours × sleep_hours

These features could help identify nonlinear relationships.

4. Better Handling of Target Distribution

Because final_score has a ceiling effect, alternative approaches could include:

Quantile Regression
Classification
Ordinal Regression
Tobit-style models
Predicting whether a student achieves full marks
5. Residual Analysis

Future versions could automatically analyze:

Prediction residuals
Outliers
High-leverage observations
Error distribution
Performance across different score ranges
6. Larger and More Diverse Datasets

Increasing the number of observations would improve:

Statistical reliability
Model stability
Generalization
AI Agent reasoning quality
API

The backend provides several HTTP endpoints.

Health / Root
GET /

Used to verify that the backend service is running.

Inspect Dataset
POST /inspect

Used to upload and inspect a dataset before performing the complete analysis.

Complete Analysis
POST /analyze

The main analysis endpoint.

The endpoint performs:

Upload
→ Cleaning
→ EDA
→ Machine Learning
→ Visualization
→ LLM Analysis
→ AI Agent
→ PDF Report
Local Setup
Requirements

Recommended environment:

Python 3.12+
Node.js
npm
Backend Setup

Navigate to the backend directory:

cd backend

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create:

backend/.env

Add your DeepSeek API key:

DEEPSEEK_API_KEY=your_api_key_here

Start the backend:

uvicorn api:app --reload

The backend will normally run at:

http://127.0.0.1:8000
Frontend Setup

Open another terminal and navigate to:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally run at:

http://localhost:5173
Environment Variables

The project uses environment variables for API credentials.

Example:

DEEPSEEK_API_KEY=your_api_key_here

API keys and other sensitive information should never be committed to GitHub.

The project .gitignore excludes:

.env
.env.*
Design Principles
Separation of Data Science and AI Reasoning

The project separates deterministic data analysis from LLM-based interpretation.

Traditional data science components are responsible for:

Data Cleaning
EDA
Statistics
Machine Learning
Visualization

The AI layer is responsible for:

Interpretation
Reasoning
Insight Generation
Recommendations
Natural Language Reporting

This separation makes the system easier to debug and evaluate.

Evidence-Based AI Analysis

The AI Agent receives actual analytical results rather than inventing numerical findings.

For example:

MAE
RMSE
Correlation
Feature Importance
Missing Values
Dataset Size

are calculated by the backend before being passed to the AI layer.

This reduces the risk of unsupported analytical conclusions.

Correlation vs Causation

The system explicitly distinguishes statistical correlation from causal relationships.

For example:

study_hours and final_score
correlation = 0.682

does not automatically mean:

Increasing study_hours causes final_score to increase.

Potential confounding factors must be considered before making causal claims.

Limitations

The current version has several limitations.

Dataset Size

The example dataset contains only 120 valid observations.

This is sufficient for demonstrating the system but not enough to establish strong generalizable conclusions.

Target Ceiling Effect

A large proportion of students received full marks, which reduces target variability.

Model Evaluation

The current implementation uses a single train/test split.

Cross-validation would provide a more robust evaluation.

Feature Availability

The current dataset contains only a small number of variables.

Additional variables could potentially improve the analysis, such as:

Previous academic performance
Course difficulty
Learning environment
Study method
Assignment completion time
Prior knowledge
Causal Interpretation

The current system performs statistical and predictive analysis, not causal inference.

Learning Outcomes

This project helped explore the integration of several areas of modern software and AI engineering:

Data preprocessing
Exploratory data analysis
Statistical analysis
Machine learning
Data visualization
REST API development
React frontend development
LLM API integration
AI Agent design
Automated report generation
End-to-end AI application architecture

The project also demonstrates how traditional machine learning and LLM-based reasoning can complement each other.

Why I Built This Project

Large Language Models can generate explanations and summaries, but reliable data analysis still requires deterministic computation.

This project explores a hybrid approach:

Traditional Data Science
        +
Machine Learning
        +
LLM
        +
AI Agent
        =
End-to-End Intelligent Data Analysis

The goal is to build a system where AI does not simply "chat about data", but instead works on top of actual statistical and machine learning results to produce more structured and explainable insights.

Project Highlights

The main strengths of the current implementation are:

End-to-end data analysis workflow
Automated data cleaning
Exploratory data analysis
Machine learning prediction
Feature importance analysis
Automated visualization
LLM-powered interpretation
AI Agent second-level reasoning
Correlation/causation awareness
Automated PDF report generation
React + FastAPI full-stack architecture
Future Vision

The long-term goal is to evolve the project into a more general-purpose AI data analysis platform.

A future version could support:

CSV / Excel / Database
        ↓
Automatic Data Profiling
        ↓
AI-Powered EDA
        ↓
Automatic Model Selection
        ↓
Model Comparison
        ↓
AI Agent Reasoning
        ↓
Interactive Visualization
        ↓
Automated Report

The system could eventually allow users without advanced data science knowledge to perform meaningful exploratory analysis and understand machine learning results through natural language.

Author

Fmhapppy

Software Engineering Student

Interested in:

Artificial Intelligence
Machine Learning
Data Science
LLM Applications
AI Agents
Full-Stack Development
License

This project is intended primarily for educational, research, and portfolio purposes.

Please check the licenses of third-party libraries and APIs before using the project in commercial applications.