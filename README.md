# LLM-based Intelligent Data Analysis Agent

> An end-to-end AI-powered data analysis system integrating data preprocessing, exploratory data analysis, machine learning, visualization, LLM reasoning, and agent-based analysis.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB" />
  <img src="https://img.shields.io/badge/Scikit--learn-Machine%20Learning-orange" />
  <img src="https://img.shields.io/badge/DeepSeek-LLM-purple" />
</p>

---

## Overview

Traditional data analysis usually requires users to manually perform data cleaning, exploratory analysis, visualization, machine learning, and result interpretation.

This project integrates these processes into a unified AI-assisted data analysis pipeline.

Users can upload a CSV or Excel dataset, select a prediction target, and obtain analytical results through an interactive web dashboard.

The system combines **traditional data science methods** with **LLM-based reasoning and AI agents** to transform raw datasets into structured and interpretable insights.

---

## Key Features

| Module | Function |
|---|---|
| 📂 Data Upload | CSV / Excel dataset upload |
| 🧹 Data Cleaning | Missing values, duplicates, empty columns |
| 📊 EDA | Statistics, data types, correlation analysis |
| 🤖 Machine Learning | Random Forest regression |
| 📈 Visualization | Correlation heatmap, feature relationships, feature importance |
| 🧠 LLM Analysis | AI-powered interpretation of analytical results |
| 🔍 Analysis Agent | Structured multi-dimensional analytical reasoning |
| 📄 PDF Report | Automatic analytical report generation |
| 💻 Web Dashboard | Interactive React-based interface |

---

## System Architecture

```text
                         User
                          │
                          ▼
                ┌──────────────────┐
                │   React Dashboard │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │    FastAPI API    │
                └─────────┬────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    Data Processing    │
              └───────────┬───────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
      ┌──────────┐  ┌──────────┐  ┌──────────────┐
      │ Cleaning │  │   EDA    │  │ Machine      │
      │          │  │          │  │ Learning     │
      │ Missing  │  │ Statistics│  │ Random Forest│
      │ Duplicate│  │Correlation│  │ MAE / RMSE  │
      └────┬─────┘  └────┬─────┘  └──────┬───────┘
           │             │               │
           └─────────────┼───────────────┘
                         ▼
                ┌──────────────────┐
                │  Visualization   │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │   LLM Analysis   │
                │    DeepSeek      │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Analysis Agent   │
                └─────────┬────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
          ┌──────────────┐  ┌──────────────┐
          │ Web Dashboard│  │  PDF Report  │
          └──────────────┘  └──────────────┘
Data Analysis Pipeline
Raw Dataset
     │
     ▼
Data Inspection
     │
     ▼
Data Cleaning
     │
     ▼
Exploratory Data Analysis
     │
     ▼
Machine Learning
     │
     ▼
Visualization
     │
     ▼
LLM Interpretation
     │
     ▼
Agent-based Analysis
     │
     ▼
Automated Report
Data Cleaning

The preprocessing module automatically handles common data quality problems.

Current operations include:

Duplicate row detection and removal
Missing value detection
Numerical missing values → median imputation
Categorical missing values → mode imputation
Completely empty column removal
Cleaning statistics generation

The system also produces a structured cleaning report describing the preprocessing process.

Exploratory Data Analysis

The EDA module provides:

Descriptive statistics
Mean
Standard deviation
Minimum / maximum
Quartiles
Data types
Missing values
Pearson correlation analysis

The resulting statistics are passed to subsequent machine learning and AI analysis modules.

Machine Learning

The current machine learning pipeline uses:

Random Forest Regression
Numerical Features
        │
        ▼
Train / Test Split
        │
        ▼
Random Forest
        │
        ▼
Prediction
        │
        ├───────────────┐
        ▼               ▼
      MAE             RMSE
        │
        ▼
Feature Importance

The model currently reports:

Mean Absolute Error (MAE)
Root Mean Squared Error (RMSE)
Feature importance

The machine learning component performs numerical computation independently from the LLM.

Visualization

The system automatically generates analytical visualizations including:

Correlation Heatmap

Shows relationships between numerical variables.

Feature Relationship

Visualizes the relationship between important features and the prediction target.

Example:

Study Hours → Final Score
Feature Importance

Displays the relative importance of input variables according to the Random Forest model.

LLM-based Analysis

The system uses DeepSeek to interpret structured analytical results.

Instead of asking the LLM to perform numerical calculations directly, the system first completes the traditional data science pipeline.

Dataset
   ↓
Data Science Pipeline
   ↓
Structured Results
   ↓
DeepSeek
   ↓
Natural Language Insights

The LLM receives information such as:

Data cleaning results
Descriptive statistics
Correlations
Model performance
Feature importance

It then generates human-readable analytical insights.

Analysis Agent

An additional analysis agent performs higher-level reasoning over the analytical results.

The agent currently produces structured outputs covering:

Core findings
Key factors
Data quality
Variable relationships
Model evaluation
Recommended next analysis

Example output structure:

{
  "core_findings": [],
  "key_factors": [],
  "data_quality": [],
  "relationships": [],
  "model_evaluation": [],
  "next_analysis": []
}

The structured output allows the frontend to independently render different analytical sections.

Web Dashboard

The frontend is implemented with React.

The dashboard provides:

Dataset upload
Automatic field detection
Prediction target selection
Analysis execution
Data overview
Cleaning results
Visualizations
Machine learning results
AI insights
Agent analysis
PDF report access
Automated PDF Report

After completing the analysis pipeline, the system automatically generates a PDF report containing:

Dataset overview
Data cleaning results
EDA statistics
Correlation analysis
Visualizations
Machine learning metrics
Feature importance
AI-generated analysis
Technology Stack
Backend
Python
FastAPI
Pandas
NumPy
Scikit-learn
Matplotlib
ReportLab
Frontend
React
JavaScript
CSS
AI
DeepSeek API
Large Language Models
AI Agent architecture
Development
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
2. Create a virtual environment
python -m venv .venv

Windows:

.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
Configuration

Create:

backend/.env

Add:

DEEPSEEK_API_KEY=your_api_key_here

Never commit API keys or other sensitive credentials to GitHub.

Running the Backend
cd backend
uvicorn api:app --reload

Backend:

http://127.0.0.1:8000
Running the Frontend
cd frontend
npm install
npm run dev

Then open the local address provided by Vite.

Example Dataset

The system has been tested using a student learning dataset containing:

Study hours
Sleep hours
Attendance
Assignment score
Final score

This dataset demonstrates the complete workflow from preprocessing to machine learning and AI-assisted interpretation.

Engineering Principles
1. Separation of Computation and Reasoning

Numerical computation is handled by traditional data science libraries.

LLMs are primarily used for:

Result interpretation
Insight generation
Pattern summarization
Analytical recommendations

This separates deterministic numerical analysis from probabilistic language reasoning.

2. Modular Architecture

Each major component is implemented as an independent module:

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

This modular design makes individual components easier to test, replace, and extend.

Current Status

Functional Prototype

The complete end-to-end workflow has been implemented:

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

The project is currently being refined with improvements to analytical capabilities, user experience, documentation, and system architecture.

Future Work

Potential improvements include:

Automatic regression / classification detection
Additional machine learning algorithms
Hyperparameter optimization
Automated feature engineering
Statistical significance testing
Advanced anomaly detection
Natural-language dataset querying
Multi-step autonomous analysis
Agent-driven visualization selection
Interactive analytical conversations
Support for larger datasets
Experiment tracking
Project Significance

This project explores a hybrid approach to intelligent data analysis.

Rather than replacing traditional data science methods with an LLM, the system combines:

Traditional Data Science
          +
Machine Learning
          +
Large Language Models
          +
AI Agents
          ↓
Intelligent Data Analysis

The project demonstrates how deterministic analytical methods can be combined with flexible language-based reasoning to build more accessible and intelligent data analysis applications.

Author

Fmhapppy

GitHub:
https://github.com/Fmhapppy/LLM-Data-Analysis-Agent

License

This project is intended for educational, research, and portfolio purposes.