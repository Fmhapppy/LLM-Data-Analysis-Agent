# LLM Data Analysis Agent

An AI-driven data analysis platform that combines data cleaning, exploratory data analysis (EDA), machine learning, visualization, and LLM-powered insights into an end-to-end workflow.

The project is designed to demonstrate practical skills in **Python data analysis, machine learning, backend API development, frontend visualization, and AI application engineering**.

---

## Overview

The LLM Data Analysis Agent allows users to upload a CSV or Excel dataset and automatically perform a complete analysis pipeline:

1. Load and inspect the dataset
2. Clean missing values and duplicate records
3. Perform exploratory data analysis
4. Calculate correlations and descriptive statistics
5. Train a machine learning model
6. Generate data visualizations
7. Produce AI-generated insights
8. Run deeper analysis through an AI Agent
9. Generate a downloadable PDF report

The project combines traditional data science methods with LLM-based reasoning to create a more accessible data analysis workflow.

---

## Key Features

### Data Processing

- CSV and Excel file support
- Automatic dataset inspection
- Dataset shape and column detection
- Numerical and categorical data handling

### Data Cleaning

- Duplicate row detection and removal
- Missing-value detection
- Median imputation for numerical variables
- Mode imputation for categorical variables
- Empty-column detection and removal
- Cleaning statistics and processing logs

### Exploratory Data Analysis

- Descriptive statistics
- Missing-value analysis
- Data type inspection
- Correlation matrix
- Relationship analysis between numerical variables

### Machine Learning

- Random Forest regression
- Automatic train/test split
- MAE evaluation
- RMSE evaluation
- Feature importance analysis

### Data Visualization

The system automatically generates:

- Correlation heatmap
- Study hours vs. final score scatter plot
- Machine learning feature importance chart

### AI Analysis

The platform uses an LLM to transform statistical and machine-learning results into natural-language insights.

The AI analysis considers:

- Correlation patterns
- Feature importance
- Model performance
- Data quality
- Potential ceiling effects
- Limitations of the dataset
- Suggestions for further analysis

### AI Agent

The AI Agent performs a second-level analysis by combining:

- EDA results
- Correlation analysis
- Machine learning results
- Feature importance
- Data quality information
- Model evaluation metrics

The Agent is explicitly instructed to distinguish **statistical association from causation** and avoid interpreting feature importance as causal influence.

### PDF Report

The system can generate a structured PDF report containing:

- Dataset overview
- Data cleaning results
- Visualizations
- Machine learning results
- AI-generated insights
- AI Agent analysis
- Recommendations for future analysis

---

## Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Data Cleaning

![Data Cleaning](screenshots/data-cleaning.png)

### Data Visualization

![Data Visualization](screenshots/visualization.png)

### Machine Learning

![Machine Learning](screenshots/machine-learning.png)

### AI Insights

![AI Insights](screenshots/ai-insights.png)

### AI Agent Deep Analysis

![AI Agent Deep Analysis](screenshots/ai-agent.png)

---

## System Architecture

```text
                    +----------------------+
                    |      User Upload     |
                    |    CSV / Excel File  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Data Processor    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Data Cleaning     |
                    | Duplicates / Missing |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |         EDA          |
                    | Stats / Correlation  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Machine Learning   |
                    |   Random Forest      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Visualization      |
                    | Heatmap / Scatter    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |     LLM Analysis     |
                    |  AI Generated Insight|
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      AI Agent        |
                    |  Deep Data Analysis  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |     PDF Report       |
                    +----------------------+
```

---

## Technology Stack

### Backend

- Python
- FastAPI
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- OpenAI-compatible API
- python-dotenv
- ReportLab

### Frontend

- React
- Vite
- JavaScript
- CSS

### Machine Learning

- Random Forest Regression
- Train/Test Split
- Mean Absolute Error
- Root Mean Squared Error
- Feature Importance

### AI

- DeepSeek API
- LLM-based data interpretation
- Structured AI Agent analysis

---

## Project Structure

```text
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
```

---

## Example Analysis

The included example dataset represents student learning and academic performance.

### Dataset

The dataset contains the following variables:

| Variable | Description |
|---|---|
| `study_hours` | Daily study hours |
| `sleep_hours` | Daily sleep hours |
| `attendance` | Attendance rate |
| `assignment_score` | Assignment score |
| `final_score` | Final examination score |

The machine learning target is:

```text
final_score
```

The model uses:

```text
study_hours
sleep_hours
attendance
assignment_score
```

as input features.

---

## Data Cleaning Results

For the example dataset:

| Metric | Result |
|---|---:|
| Original rows | 122 |
| Cleaned rows | 120 |
| Original columns | 5 |
| Cleaned columns | 5 |
| Duplicate rows removed | 2 |
| Missing values filled | 5 |
| Empty columns removed | 0 |
| Remaining missing values | 0 |
| Data retention | 98.4% |

Numerical missing values were handled using median imputation.

---

## Machine Learning Results

A Random Forest regression model was trained to predict `final_score`.

| Metric | Result |
|---|---:|
| MAE | 2.637 |
| RMSE | 4.283 |

Feature importance:

| Feature | Importance |
|---|---:|
| `study_hours` | 71.0% |
| `attendance` | 14.5% |
| `assignment_score` | 9.4% |
| `sleep_hours` | 5.1% |

These values describe the model's predictive feature importance and should **not** be interpreted as causal effects.

---

## Statistical Findings

The example analysis found the following correlations with `final_score`:

| Variable | Correlation |
|---|---:|
| `study_hours` | 0.682 |
| `attendance` | 0.203 |
| `assignment_score` | 0.167 |
| `sleep_hours` | -0.123 |

The strongest observed linear relationship was between `study_hours` and `final_score`.

However, correlation does not establish causation. The project deliberately separates statistical association from causal interpretation.

---

## AI Agent Insights

The AI Agent identifies several important characteristics of the example dataset.

### Strong Study-Hours Relationship

`study_hours` has both the strongest observed correlation with `final_score` and the highest model feature importance.

This indicates that study hours are strongly associated with the model's prediction of final scores in this dataset.

### Ceiling Effect

The distribution of `final_score` contains a noticeable ceiling effect, with the median and 75th percentile reaching 100.

This may reduce the ability of correlation and regression models to distinguish high-performing students.

### Model Evaluation

The model achieves:

```text
MAE  = 2.6367
RMSE = 4.2828
```

The higher RMSE compared with MAE suggests that some predictions have relatively larger errors.

### Further Analysis

The AI Agent recommends future improvements such as:

- K-fold cross-validation
- Residual analysis
- Model comparison
- Feature interaction analysis
- Classification or quantile-based modeling
- Additional student background variables
- Larger datasets

---

## AI Analysis Pipeline

The AI analysis workflow can be summarized as:

```text
Raw Dataset
     |
     v
Data Cleaning
     |
     v
EDA + Statistics
     |
     v
Machine Learning
     |
     v
Feature Importance
     |
     v
LLM Analysis
     |
     v
AI Agent Reasoning
     |
     v
Final Report
```

The LLM does not replace statistical analysis or machine learning. Instead, it provides an interpretation layer on top of computed results.

---

## API

The backend provides a simple HTTP API.

### Health Check

```http
GET /
```

### Dataset Inspection

```http
POST /inspect
```

### Full Analysis

```http
POST /analyze
```

The `/analyze` endpoint executes the complete pipeline:

```text
Upload
  -> Cleaning
  -> EDA
  -> Machine Learning
  -> Visualization
  -> LLM Analysis
  -> AI Agent
  -> PDF Report
```

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Fmhapppy/LLM-Data-Analysis-Agent.git
cd LLM-Data-Analysis-Agent
```

### 2. Create a Python Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

Create:

```text
backend/.env
```

Add your API key:

```text
DEEPSEEK_API_KEY=your_api_key_here
```

Do not commit `.env` or API keys to GitHub.

### 5. Start the Backend

```bash
cd backend
python api.py
```

### 6. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the local frontend URL displayed by Vite.

---

## Example Workflow

A typical user workflow is:

```text
1. Upload student_learning_dataset.csv
        ↓
2. Select final_score as target
        ↓
3. Start analysis
        ↓
4. Review data cleaning results
        ↓
5. Review statistical visualizations
        ↓
6. Review Random Forest results
        ↓
7. Review AI Insights
        ↓
8. Review AI Agent analysis
        ↓
9. Download PDF report
```

---

## Design Principles

### 1. Data First

Statistical calculations and machine learning results are generated programmatically before being passed to the LLM.

### 2. Explainability

The system exposes:

- Data cleaning operations
- Statistical relationships
- Model metrics
- Feature importance
- AI reasoning

### 3. Separation of Analysis and Interpretation

Traditional data science components produce quantitative results, while the LLM provides natural-language interpretation.

### 4. Causal Caution

The AI Agent is instructed not to treat correlation or feature importance as evidence of causality.

### 5. Reproducibility

The machine learning pipeline uses fixed random seeds where appropriate, making the example analysis reproducible.

---

## Limitations

This project is primarily a practical demonstration and has several limitations:

- The example dataset is relatively small.
- Random Forest evaluation uses a single train/test split.
- Feature importance does not imply causation.
- Correlation analysis only captures linear relationships.
- The example dataset has a ceiling effect in `final_score`.
- Additional external variables could improve the predictive model.
- The LLM interpretation depends on the quality of the computed inputs.

---

## Future Improvements

Potential future improvements include:

### Machine Learning

- K-fold cross-validation
- Hyperparameter optimization
- XGBoost / LightGBM comparison
- Classification models
- More robust feature engineering
- Residual analysis

### Data Science

- Outlier detection
- Distribution analysis
- Automatic statistical tests
- Automated feature selection
- Interactive visualization

### AI Agent

- Tool-calling architecture
- Multi-step reasoning
- Automatic hypothesis generation
- Automatic model selection
- Automatic follow-up analysis
- Natural-language data querying

### Product

- User authentication
- Dataset history
- Cloud storage
- Multi-user support
- Online report sharing
- More file formats
- Deployment to a cloud platform

---

## Learning Outcomes

This project helped consolidate practical experience in:

- Python programming
- Pandas-based data processing
- Data cleaning
- Exploratory data analysis
- Statistical correlation analysis
- Machine learning
- Model evaluation
- Data visualization
- FastAPI backend development
- React frontend development
- LLM API integration
- AI Agent design
- PDF report generation
- Git and GitHub workflow

---

## Motivation

The project was developed to explore how traditional data science workflows can be combined with modern LLM technology.

Instead of using an LLM as a standalone chatbot, the system integrates the model with a structured analytical pipeline:

```text
Data
  ↓
Computation
  ↓
Machine Learning
  ↓
LLM Interpretation
  ↓
AI Agent
  ↓
Actionable Insights
```

This architecture demonstrates a practical approach to building AI-assisted data applications.

---

## Author

**Fmhapppy**

GitHub:

https://github.com/Fmhapppy

---

## License

This project is intended for learning, experimentation, and portfolio demonstration.
