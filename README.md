# LLM Data Analysis Agent

> **An LLM-powered data analysis system integrating data preprocessing, statistical analysis, machine learning, model evaluation, error analysis, and automated Agent evaluation.**
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)](https://react.dev/)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-Machine%20Learning-F7931E.svg)](https://scikit-learn.org/)
[![LLM](https://img.shields.io/badge/LLM-Analysis%20Agent-purple.svg)](#llm-analysis-agent)

---

## 1. Overview

**LLM Data Analysis Agent** is an end-to-end intelligent data analysis system designed to combine conventional statistical and machine learning workflows with large language model reasoning.

Instead of treating an LLM as a simple chatbot, the system separates the analytical process into structured stages:

```text
Dataset
   │
   ▼
Data Validation & Cleaning
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Statistical Analysis
   │
   ▼
Machine Learning
   │
   ├── Linear Regression
   └── Random Forest
   │
   ▼
Model Comparison
   │
   ▼
Cross Validation
   │
   ▼
Error Analysis
   │
   ▼
LLM Analysis Agent
   │
   ▼
Automated Agent Evaluation
   │
   ▼
PDF Analytical Report
```

The project focuses on three complementary capabilities:

1. **Data-driven computation** — deterministic preprocessing, statistical analysis and machine learning.
2. **LLM-based analytical reasoning** — converting structured analytical results into interpretable findings.
3. **Agent evaluation** — automatically testing whether the generated analysis correctly reflects the underlying data and model results.

The project is intended as a research-oriented engineering project exploring the integration of **machine learning, statistical reasoning, and LLM agents**.

---

# 2. Motivation

Traditional automated data analysis systems can efficiently calculate statistical indicators and train machine learning models, but the results are often difficult for non-experts to interpret.

Conversely, an LLM can generate natural-language explanations, but directly asking an LLM to analyze raw data introduces risks such as:

* numerical inaccuracies;
* unsupported conclusions;
* confusion between correlation and causation;
* incorrect interpretation of model feature importance;
* hallucinated findings.

This project therefore adopts a **structured analytical pipeline**:

> **Computation first, reasoning second, evaluation third.**

The machine learning and statistical modules generate structured evidence, while the LLM is responsible for synthesizing and interpreting these results.

A separate evaluation layer then checks whether the Agent's generated analysis is consistent with the analytical evidence.

---

# 3. Key Features

## 3.1 Data Processing

The system supports structured tabular datasets and performs:

* CSV / Excel loading
* data type inspection
* missing-value detection
* duplicate detection
* numerical missing-value imputation
* categorical missing-value imputation
* basic data-quality reporting

Example cleaning result from the included dataset:

```text
Original samples:       122
Cleaned samples:        120
Duplicate records:        2
Missing values:           5
Remaining missing:        0
```

---

## 3.2 Exploratory Data Analysis

The EDA module automatically generates:

* descriptive statistics;
* missing-value analysis;
* data-type information;
* correlation analysis;
* feature-target relationships.

For the current experimental dataset:

```text
study_hours ↔ final_score
Pearson r ≈ 0.682
```

The system also identifies weaker relationships involving:

```text
attendance
assignment_score
sleep_hours
```

The results are provided to the downstream analysis Agent as structured analytical evidence.

---

## 3.3 Machine Learning Pipeline

The project currently compares two regression models:

### Linear Regression

Used as a simple baseline model.

### Random Forest Regression

Used as a nonlinear ensemble model capable of capturing more complex relationships between features and the target variable.

The system evaluates models using:

* MAE
* RMSE
* R²

### Experimental Result

On the current student-learning dataset:

| Model             |        MAE |       RMSE |         R² |
| ----------------- | ---------: | ---------: | ---------: |
| Linear Regression |     3.2844 |     4.9696 |     0.5163 |
| **Random Forest** | **2.6367** | **4.2828** | **0.6408** |

Under the current train/test split, Random Forest achieved lower MAE and RMSE and a higher R² than Linear Regression.

> These results describe performance on the current dataset and split. They should not be interpreted as evidence that Random Forest will necessarily generalize equally well to other datasets.

---

# 4. Cross Validation

To reduce dependence on a single train/test split, the project additionally performs **5-fold cross validation**.

For Random Forest:

```text
Mean R²:      0.5730
Std R²:       0.1940

Mean MAE:     2.4852
Std MAE:      0.5230

Mean RMSE:    4.1380
Std RMSE:     0.9790
```

The relatively large R² standard deviation is explicitly retained as part of the analysis rather than hidden.

This is important because the dataset contains only 120 cleaned samples and exhibits a strong ceiling effect in the target variable.

Therefore, the project treats cross-validation results as an estimate of model stability rather than proof of robust real-world generalization.

---

# 5. Error Analysis

Model evaluation goes beyond reporting aggregate metrics.

The system also analyzes individual test-set predictions, including:

* actual value;
* predicted value;
* residual;
* absolute error;
* maximum prediction error;
* over-/under-prediction patterns.

For the current experiment:

```text
Test samples:       24
Mean residual:     -1.0252
Maximum absolute error: 12.1330
```

One large error was observed where:

```text
Actual score:       81.2
Predicted score:    93.333
Absolute error:     12.133
```

This observation is consistent with the dataset's strong ceiling effect and limited number of low-score samples.

---

# 6. LLM Analysis Agent

The LLM component is not directly responsible for calculating statistical metrics.

Instead, the analytical pipeline first computes structured results and then provides these results to the Agent.

The Agent synthesizes:

* data quality;
* descriptive statistics;
* correlations;
* feature relationships;
* feature importance;
* model metrics;
* cross-validation results;
* error analysis;
* model limitations;
* recommendations for further analysis.

The generated analysis is structured into several sections:

```text
core_findings
key_factors
data_quality
relationships
model_evaluation
next_analysis
```

This structured output makes the Agent's reasoning easier to inspect, evaluate, and integrate into downstream reports.

---

# 7. Statistical Reasoning and Causal Boundaries

One important design goal is to prevent the LLM from confusing statistical association with causation.

For example:

```text
study_hours
Pearson correlation with final_score ≈ 0.682
```

and:

```text
Random Forest feature importance
study_hours ≈ 0.7103
```

do **not** imply:

> Increasing study hours will necessarily cause an increase in final scores.

The Agent is explicitly instructed to distinguish:

```text
Correlation
    ≠
Causation

Feature Importance
    ≠
Causal Contribution
```

This distinction is incorporated into the automated evaluation benchmark.

---

# 8. Automated Agent Evaluation

A major component of the project is the **Agent Evaluation module**.

Rather than evaluating the LLM only through subjective inspection, the system constructs a fixed benchmark based on the actual analytical results.

The current benchmark contains 10 questions covering:

### Factual Reasoning

* cleaned sample count;
* target variable.

### Statistical Reasoning

* Pearson correlation;
* strongest correlated variable.

### Machine Learning

* MAE;
* RMSE;
* R²;
* feature importance.

### Causal Reasoning

* whether feature importance implies causality;
* whether correlation proves causation.

Example:

```text
Q:
study_hours 的 feature importance 较高，
是否意味着增加学习时间一定会导致成绩提高？

Expected:
No.
```

The evaluator checks the Agent's generated analysis against the expected analytical evidence.

---

# 9. Agent Evaluation Results

Current benchmark result:

| Metric                       |   Result |
| ---------------------------- | -------: |
| Evaluation Questions         |       10 |
| Correct Questions            |  10 / 10 |
| Overall Accuracy             | **100%** |
| Fact Accuracy                | **100%** |
| Numerical Accuracy           | **100%** |
| Causal Reasoning Accuracy    | **100%** |
| Factual/Numerical Error Rate |   **0%** |

```text
Agent Evaluation

████████████████████ 100%

10 / 10 Correct
```

The current result demonstrates that, on this fixed benchmark and analytical dataset, the Agent successfully reproduced the key statistical and machine-learning findings and respected the predefined causal-reasoning constraints.

> **Evaluation limitation:** the current benchmark evaluates whether the generated Agent analysis contains the expected facts, numerical values, and reasoning patterns. It is not intended to be a universal measure of LLM hallucination or general reasoning ability.

Future versions will expand the benchmark to a larger and more diverse question set.

---

# 10. Data Quality and Analytical Limitations

The current dataset contains:

```text
122 original samples
120 cleaned samples
5 missing values
2 duplicate records
```

The target variable `final_score` has a strong ceiling effect:

```text
Mean:      ≈ 95.9
Median:    100
75% quantile: 100
Maximum:   100
```

This means a large proportion of observations are concentrated near the upper boundary.

Consequently:

* regression performance may be affected by target truncation;
* low-score predictions may be less reliable;
* model evaluation may be sensitive to the train/test split;
* 120 observations are insufficient to establish strong real-world generalization.

The project therefore treats the current experiment as a **prototype analytical study**, rather than a production-grade predictive system.

---

# 11. Technical Architecture

```text
                         ┌─────────────────────┐
                         │      User Dataset   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Data Processor      │
                         │ CSV / Excel Loader  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Data Cleaner        │
                         │ Missing Values      │
                         │ Duplicate Removal   │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ EDA / Statistics │             │ ML Pipeline      │
          │ Correlation      │             │ Linear Regression│
          │ Descriptive      │             │ Random Forest    │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   │                         ┌──────┴───────┐
                   │                         │              │
                   │                         ▼              ▼
                   │                   Cross Validation  Error Analysis
                   │
                   └──────────────┬─────────────────┘
                                  │
                                  ▼
                       ┌────────────────────────┐
                       │ LLM Analysis Agent     │
                       │ Structured Reasoning   │
                       └────────────┬───────────┘
                                    │
                                    ▼
                       ┌────────────────────────┐
                       │ Agent Evaluation       │
                       │ Fact / Numerical /     │
                       │ Statistical / Causal   │
                       └────────────┬───────────┘
                                    │
                                    ▼
                       ┌────────────────────────┐
                       │ PDF Analytical Report  │
                       └────────────────────────┘
```

---

# 12. Technology Stack

### Programming

* Python
* JavaScript
* HTML / CSS

### Data Science

* Pandas
* NumPy
* Scikit-learn
* Matplotlib

### Machine Learning

* Linear Regression
* Random Forest Regression
* K-Fold Cross Validation
* Regression Metrics
* Feature Importance
* Error Analysis

### LLM / AI

* Large Language Model
* Structured LLM Analysis
* AI Agent
* Prompt Engineering
* Statistical Reasoning
* Automated Agent Evaluation

### Backend

* FastAPI
* REST API
* Python-based analytical pipeline

### Frontend

* React
* Vite

### Engineering

* Git / GitHub
* Modular backend architecture
* Structured JSON results
* PDF report generation

---

# 13. Project Structure

```text
LLM-Data-Analysis-Agent/
│
├── backend/
│   ├── analysis_agent.py
│   ├── agent_evaluation.py
│   ├── api.py
│   ├── data_cleaner.py
│   ├── data_processor.py
│   ├── eda.py
│   ├── llm_analyzer.py
│   ├── ml_model.py
│   ├── pdf_report.py
│   ├── visualizations.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   └── package.json
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
└── requirements.txt
```

---

# 14. Screenshots

## Dashboard

![Dashboard](screenshots/dashboard.png)

## Data Cleaning

![Data Cleaning](screenshots/data-cleaning.png)

## Visualization

![Visualization](screenshots/visualization.png)

## Machine Learning

![Machine Learning](screenshots/machine-learning.png)

## AI Insights

![AI Insights](screenshots/ai-insights.png)

## Analysis Agent

![AI Agent](screenshots/ai-agent.png)

---

# 15. Running the Project

## Backend

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python -m uvicorn api:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

---

## Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 16. Example Analytical Workflow

After uploading a dataset, the system automatically performs:

```text
1. Load dataset
       ↓
2. Validate target variable
       ↓
3. Remove duplicates
       ↓
4. Handle missing values
       ↓
5. Generate descriptive statistics
       ↓
6. Calculate correlations
       ↓
7. Train Linear Regression
       ↓
8. Train Random Forest
       ↓
9. Compare models
       ↓
10. Perform 5-fold cross validation
       ↓
11. Analyze prediction errors
       ↓
12. Generate visualizations
       ↓
13. Generate LLM analytical report
       ↓
14. Evaluate Agent reasoning
       ↓
15. Generate PDF report
```

---

# 17. Research-Oriented Contributions

The main contribution of this project is not simply integrating an LLM into a data analysis interface.

The project explores a more structured architecture:

### 17.1 Hybrid Analytical Architecture

Combines deterministic computational methods with probabilistic language-model reasoning.

```text
Deterministic Computation
        +
Machine Learning
        +
LLM Reasoning
        +
Automated Evaluation
```

### 17.2 Evidence-Grounded Agent Reasoning

The LLM receives structured analytical evidence rather than being asked to independently calculate all statistical results.

This reduces the risk of numerical inconsistency and makes the generated conclusions easier to audit.

### 17.3 Explicit Statistical Reasoning Boundaries

The Agent is evaluated on whether it distinguishes:

```text
Correlation
Feature Importance
Prediction
Causation
```

This is particularly important for analytical applications where misleading causal interpretations can result from purely observational data.

### 17.4 Agent Evaluation

The project introduces an automated benchmark layer that tests whether the generated analysis remains consistent with the underlying computational results.

This creates an additional feedback layer:

```text
Data
 ↓
Analysis
 ↓
LLM Reasoning
 ↓
Evaluation
```

rather than simply:

```text
Data
 ↓
LLM
 ↓
Answer
```

---

# 18. Limitations

The current prototype has several limitations.

### Dataset Size

The current experiment contains only 120 cleaned observations.

Therefore, model performance should not be generalized to larger populations without additional validation.

### Target Ceiling Effect

`final_score` has a strong concentration around the upper boundary.

This can reduce the ability of regression models to distinguish high-performing samples and may contribute to larger errors on lower-scoring samples.

### Limited Feature Space

The current dataset contains only four predictive features:

```text
study_hours
sleep_hours
attendance
assignment_score
```

Additional variables could potentially improve analysis, such as:

* prior academic performance;
* course difficulty;
* learning method;
* study consistency;
* assessment difficulty;
* historical performance.

### Agent Evaluation Scope

The current benchmark contains only 10 fixed questions.

It measures consistency with predefined analytical facts and reasoning requirements, but does not constitute a comprehensive evaluation of LLM reasoning or hallucination.

---

# 19. Future Work

Several directions are planned for future development.

## 19.1 Larger Agent Evaluation Benchmark

Expand the benchmark from 10 questions to 20–50+ questions covering:

* factual consistency;
* numerical reasoning;
* statistical interpretation;
* model comparison;
* error analysis;
* causal reasoning;
* limitation identification;
* recommendation quality.

---

## 19.2 Repeated Cross Validation

Evaluate model stability under repeated cross-validation instead of relying on a single 5-fold split.

---

## 19.3 SHAP-based Explainability

Integrate SHAP or similar model-explanation methods to provide more detailed feature-level interpretation.

This would complement conventional Random Forest feature importance.

---

## 19.4 Better Error Analysis

Add:

* residual plots;
* prediction-vs-actual plots;
* error distribution;
* subgroup error analysis;
* systematic bias detection.

---

## 19.5 Alternative Prediction Tasks

Because of the ceiling effect in `final_score`, future versions could investigate:

* classification;
* ordinal prediction;
* ranking models;
* alternative target transformations.

---

## 19.6 Agent Evaluation with Independent QA

A future version will separate:

```text
Analysis Agent
        ↓
Generated Report
        ↓
Independent Evaluation Agent
        ↓
Score
```

Instead of relying only on keyword-based benchmark matching, an independent evaluator could assess:

* factual correctness;
* numerical correctness;
* reasoning validity;
* unsupported claims;
* causal overstatement;
* recommendation quality.

---

# 20. What I Learned

This project helped me explore the intersection of:

* software engineering;
* data analysis;
* machine learning;
* large language models;
* AI agents;
* statistical reasoning;
* model evaluation.

One of the most important lessons was that **generating an analytical answer is not the same as validating an analytical answer**.

An LLM can produce fluent explanations while still making numerical or logical mistakes.

Therefore, a reliable analytical Agent should be designed around:

```text
Evidence
   ↓
Computation
   ↓
Reasoning
   ↓
Validation
```

rather than relying solely on language-model generation.

The project also reinforced the importance of distinguishing statistical association from causal inference. High correlation or high model feature importance can identify useful predictive relationships, but neither alone establishes causality.

---

# 21. Project Status

### Current Version

**V2 — Research-oriented prototype**

### Completed

* [x] CSV / Excel data processing
* [x] Data cleaning
* [x] Missing-value handling
* [x] Duplicate detection
* [x] Exploratory data analysis
* [x] Correlation analysis
* [x] Linear Regression baseline
* [x] Random Forest regression
* [x] Model comparison
* [x] MAE / RMSE / R² evaluation
* [x] 5-fold cross validation
* [x] Feature importance
* [x] Prediction error analysis
* [x] Automated visualization
* [x] LLM analysis Agent
* [x] Structured Agent output
* [x] Causal reasoning constraints
* [x] Automated Agent Evaluation
* [x] PDF analytical report
* [x] React + FastAPI interface

### Planned

* [ ] 20–50 question Agent benchmark
* [ ] Repeated cross validation
* [ ] SHAP explainability
* [ ] Residual visualization
* [ ] Independent evaluation Agent
* [ ] Larger and more diverse datasets
* [ ] Research-oriented experiment report

---

# 22. Author

**Fmhapppy**

Software Engineering Undergraduate
Interested in:

* Artificial Intelligence
* Data Science
* Machine Learning
* LLM Agents
* AI-assisted Software Engineering

GitHub:

**https://github.com/Fmhapppy**

---

# 23. License

This project is intended primarily for educational, research, and portfolio purposes.
