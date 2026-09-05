# LLM-based Intelligent Data Analysis Agent

An end-to-end intelligent data analysis system that integrates automated data preprocessing, exploratory data analysis, machine learning, data visualization, LLM-based interpretation, agent-based analysis, and automated report generation.

The project explores how traditional data science workflows can be combined with Large Language Models (LLMs) and AI agents to improve the efficiency and interpretability of structured data analysis.

---

## Overview

Traditional data analysis often requires users to manually perform multiple steps, including data cleaning, exploratory analysis, visualization, machine learning, and result interpretation.

This project aims to build an intelligent data analysis pipeline that integrates these processes into a unified system.

Users can upload a CSV or Excel dataset, select a prediction target, and obtain a complete analytical workflow including:

- Automated data cleaning
- Exploratory data analysis
- Statistical summaries
- Correlation analysis
- Machine learning prediction
- Model evaluation
- Data visualization
- LLM-based analytical interpretation
- Agent-based deeper analysis
- Automated PDF report generation

The system combines conventional data science methods with LLM-based reasoning to transform raw datasets into structured and interpretable analytical results.

---

## Objectives

The main objectives of this project are:

- Automate common data preprocessing tasks
- Perform exploratory data analysis on structured datasets
- Apply machine learning methods to numerical datasets
- Generate interpretable data visualizations
- Evaluate machine learning model performance
- Use LLMs to interpret statistical and machine learning results
- Build an agent-based analytical reasoning layer
- Automatically generate structured analytical reports
- Provide an interactive web-based interface for data analysis

---

## System Architecture

The system follows an end-to-end data analysis pipeline:

```text
                    ┌──────────────────────┐
                    │      User Upload     │
                    │    CSV / Excel File  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI API     │
                    │   File Processing    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │ Data Cleaning│ │     EDA      │ │ Machine      │
      │              │ │              │ │ Learning     │
      │ Missing Value│ │ Statistics   │ │ Random Forest│
      │ Duplicates   │ │ Correlation  │ │ Regression   │
      │ Empty Fields │ │ Data Types   │ │ MAE / RMSE   │
      └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                 │                │
             └─────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │    Visualization     │
                    │                      │
                    │ Correlation Heatmap  │
                    │ Feature Relationship │
                    │ Feature Importance   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    LLM Analysis      │
                    │      DeepSeek        │
                    │                      │
                    │ Result Interpretation│
                    │ Key Findings         │
                    │ Data Insights        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Analysis Agent     │
                    │                      │
                    │ Multi-dimensional    │
                    │ Result Reasoning     │
                    │ Key Factors          │
                    │ Next Analysis        │
                    └──────────┬───────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
            ┌────────────────┐   ┌────────────────┐
            │ React Dashboard│   │   PDF Report   │
            │                │   │                │
            │ Data Overview  │   │ Data Analysis  │
            │ Cleaning       │   │ ML Results     │
            │ Visualization  │   │ AI Insights    │
            │ AI Analysis    │   │ Charts         │
            └────────────────┘   └────────────────┘
Core Features
1. Data Upload

The system supports structured datasets in:

CSV
Excel

After uploading a dataset, the system automatically inspects the data and identifies:

Number of rows
Number of columns
Column names
Numerical fields
Potential prediction targets
2. Automated Data Cleaning

The preprocessing module handles common data quality issues.

Current preprocessing operations include:

Duplicate row detection and removal
Missing value detection
Numerical missing value imputation using the median
Categorical missing value imputation using the mode
Completely empty column removal
Cleaning process statistics

The system also generates a structured cleaning report describing the preprocessing operations.

3. Exploratory Data Analysis

The EDA module provides:

Descriptive statistics
Mean
Standard deviation
Minimum and maximum values
Quartiles
Missing value statistics
Data type inspection
Correlation analysis

For numerical variables, Pearson correlation coefficients are calculated to identify potential relationships between variables.

4. Machine Learning

The current machine learning pipeline uses:

Random Forest Regression

The system automatically:

Selects numerical features
Separates features and prediction target
Splits the dataset into training and testing sets
Trains a Random Forest regression model
Generates predictions
Evaluates model performance
Calculates feature importance

Evaluation metrics include:

Mean Absolute Error (MAE)
Root Mean Squared Error (RMSE)
Feature Importance

The current workflow can be summarized as:

Dataset
   ↓
Numerical Feature Selection
   ↓
Train / Test Split
   ↓
Random Forest Regression
   ↓
Prediction
   ↓
MAE / RMSE
   ↓
Feature Importance
5. Data Visualization

The visualization module automatically generates analytical charts.

Correlation Heatmap

The correlation heatmap provides an overview of relationships between numerical variables.

Feature Relationship Visualization

The system can visualize relationships between important input variables and the prediction target.

For example:

Study Hours → Final Score

This allows users to visually inspect potential relationships within the dataset.

Feature Importance

The Random Forest model generates feature importance scores.

These scores are visualized to help identify which variables contribute most strongly to the model's predictions.

6. LLM-based Analysis

The system integrates a Large Language Model to interpret structured analytical results.

The LLM receives information generated by the data science pipeline, including:

Data cleaning results
Descriptive statistics
Correlation analysis
Machine learning performance
Feature importance

The model then generates human-readable analytical insights.

Importantly, the LLM is not directly responsible for numerical computation.

Instead, the system separates numerical analysis from natural-language reasoning:

Raw Dataset
     ↓
Traditional Data Science Pipeline
     ↓
Structured Analytical Results
     ↓
LLM Interpretation
     ↓
Human-readable Insights

This architecture allows statistical and machine learning calculations to remain deterministic while using LLMs for interpretation and reasoning.

7. Agent-based Deep Analysis

In addition to the LLM analysis module, the project introduces an analysis agent.

The agent receives structured analytical results and performs higher-level reasoning across multiple analytical components.

The current agent generates structured outputs including:

Core findings
Key factors
Data quality assessment
Variable relationships
Model evaluation
Recommended next analysis

The agent returns structured JSON that can be directly consumed by the frontend.

Example structure:

{
  "core_findings": [],
  "key_factors": [],
  "data_quality": [],
  "relationships": [],
  "model_evaluation": [],
  "next_analysis": []
}

This architecture provides a foundation for extending the system toward more autonomous analytical workflows.

8. Interactive Web Dashboard

The frontend is implemented using React.

The dashboard provides:

Dataset upload
Automatic field detection
Prediction target selection
Analysis execution
Data overview
Data cleaning results
Visualization display
Machine learning results
AI-generated insights
Agent-based analysis
PDF report access

The backend provides REST APIs through FastAPI.

9. Automated PDF Report

After the analysis is completed, the system automatically generates a structured PDF report.

The report contains:

Dataset overview
Data cleaning results
EDA statistics
Correlation analysis
Generated visualizations
Machine learning metrics
Feature importance
AI-generated analysis

The generated report allows analytical results to be exported and reviewed independently from the web interface.

Technology Stack
Programming Languages
Python
JavaScript
Backend
FastAPI
Pandas
NumPy
Scikit-learn
Matplotlib
ReportLab
Frontend
React
CSS
Artificial Intelligence
Large Language Models
DeepSeek API
AI Agent architecture
Development Tools
Git
GitHub
REST API
JSON
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
│   └── outputs/
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── App.css
│
├── .gitignore
├── README.md
└── requirements.txt
Installation
1. Clone the repository
git clone https://github.com/Fmhapppy/LLM-Data-Analysis-Agent.git
cd LLM-Data-Analysis-Agent
2. Create a Python virtual environment
python -m venv .venv

Activate the environment on Windows:

.venv\Scripts\activate
3. Install backend dependencies
pip install -r requirements.txt
Configure the LLM API

Create the following file:

backend/.env

Add your DeepSeek API key:

DEEPSEEK_API_KEY=your_api_key_here

For security reasons, API keys and other credentials should never be committed to the repository.

Running the Backend

Navigate to the backend directory:

cd backend

Start the FastAPI server:

uvicorn api:app --reload

The backend will be available at:

http://127.0.0.1:8000
Running the Frontend

Navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Then open the local development address provided by Vite.

Example Analysis Workflow

A typical analysis process is:

1. Upload CSV / Excel Dataset
              ↓
2. Inspect Dataset
              ↓
3. Select Prediction Target
              ↓
4. Start Analysis
              ↓
5. Clean Dataset
              ↓
6. Perform EDA
              ↓
7. Train Random Forest Model
              ↓
8. Generate Visualizations
              ↓
9. Generate LLM Insights
              ↓
10. Run Analysis Agent
              ↓
11. Generate PDF Report
Example Dataset

The system has been tested using a structured student learning dataset containing variables such as:

Study hours
Sleep hours
Attendance
Assignment score
Final score

The dataset demonstrates the complete analytical workflow from data preprocessing to machine learning and AI-assisted interpretation.

Engineering Design Principles
Separation of Computation and Reasoning

The system separates numerical computation from natural-language reasoning.

Traditional data science components are responsible for:

Data cleaning
Statistical computation
Correlation analysis
Machine learning
Model evaluation
Visualization

The LLM and analysis agent are responsible for:

Result interpretation
Insight generation
Pattern summarization
Analytical recommendations

This design reduces the need for LLMs to perform numerical calculations directly.

Modular Architecture

Each major analytical function is implemented as an independent module.

Data Processor
      ↓
Data Cleaner
      ↓
EDA
      ↓
Machine Learning
      ↓
Visualization
      ↓
LLM Analyzer
      ↓
Analysis Agent
      ↓
PDF Report

This modular architecture makes individual components easier to test, replace, and extend.

Current Capabilities

The core end-to-end workflow has been implemented:

Data Upload
    ↓
Data Cleaning
    ↓
EDA
    ↓
Machine Learning
    ↓
Visualization
    ↓
LLM Analysis
    ↓
Agent Analysis
    ↓
PDF Report

The current system is a functional prototype demonstrating the integration of traditional data science techniques with LLM-based analysis and agentic reasoning.

Future Work

Potential future improvements include:

Automatic regression and classification task detection
Support for additional machine learning algorithms
Hyperparameter optimization
Automated feature engineering
Statistical significance testing
Advanced anomaly detection
Natural-language dataset querying
Multi-step autonomous analysis agents
Agent-driven visualization selection
Interactive analytical conversations
Support for larger datasets
Experiment tracking
More advanced analytical report generation
Project Significance

This project explores the integration of traditional data science workflows with modern LLM and agent technologies.

Instead of replacing conventional analytical methods with an LLM, the system uses a hybrid architecture:

Traditional Data Science
          +
Machine Learning
          +
Large Language Models
          +
AI Agents
          ↓
Intelligent Data Analysis System

This approach combines deterministic numerical computation with flexible natural-language reasoning and provides a foundation for building more intelligent data analysis applications.

Author

Fmhapppy

GitHub:

https://github.com/Fmhapppy/LLM-Data-Analysis-Agent

License

This project is intended for educational, research, and portfolio purposes.


### 你替换完以后

直接：

```bash
git add README.md
git commit -m "Improve project documentation"
git push origin main