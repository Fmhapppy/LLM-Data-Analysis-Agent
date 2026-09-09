from typing import Any, Dict, List
import re


def build_evaluation_questions(
    analysis_result: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Build a fixed evaluation benchmark.

    The benchmark contains:
    - factual questions
    - statistical questions
    - machine-learning questions
    - causal-reasoning questions
    """

    ml_result = analysis_result.get("machine_learning", {})
    eda_result = analysis_result.get("eda", {})
    cleaning_report = analysis_result.get("cleaning_report", {})

    target_column = analysis_result.get("target_column")

    sample_count = analysis_result.get("sample_count")

    if sample_count is None:
        sample_count = (
            cleaning_report.get("cleaned_rows")
            or cleaning_report.get("final_rows")
        )

    correlations = eda_result.get("correlation", {})

    study_hours_corr = None

    if "study_hours" in correlations:
        study_hours_corr = correlations["study_hours"].get(
            "final_score"
        )

    if study_hours_corr is None:
        if "final_score" in correlations:
            study_hours_corr = correlations["final_score"].get(
                "study_hours"
            )

    # ---------------------------------------------------------
    # Find the strongest correlation variable
    # ---------------------------------------------------------

    strongest_correlation_feature = None

    if correlations and target_column:
        correlation_candidates = {}

        for feature, values in correlations.items():
            if not isinstance(values, dict):
                continue

            if target_column in values:
                value = values[target_column]

                if isinstance(value, (int, float)):
                    if feature != target_column:
                        correlation_candidates[feature] = abs(value)

        if correlation_candidates:
            strongest_correlation_feature = max(
                correlation_candidates,
                key=correlation_candidates.get
            )

    # Fallback for the current dataset
    if strongest_correlation_feature is None:
        strongest_correlation_feature = "study_hours"

    # ---------------------------------------------------------
    # Machine learning results
    # ---------------------------------------------------------

    models = ml_result.get("models", {})

    rf_result = models.get(
        "Random Forest",
        {}
    )

    rf_mae = rf_result.get(
        "mae",
        ml_result.get("mae")
    )

    rf_rmse = rf_result.get(
        "rmse",
        ml_result.get("rmse")
    )

    rf_r2 = rf_result.get(
        "r2",
        ml_result.get("r2")
    )

    feature_importance = ml_result.get(
        "feature_importance",
        {}
    )

    study_hours_importance = feature_importance.get(
        "study_hours"
    )

    # ---------------------------------------------------------
    # Evaluation benchmark
    # ---------------------------------------------------------

    questions = [

        {
            "id": 1,
            "type": "fact",
            "question": "清洗后的数据有多少条样本？",
            "expected_answer": sample_count,
        },

        {
            "id": 2,
            "type": "fact",
            "question": "当前机器学习分析的目标变量是什么？",
            "expected_answer": target_column,
        },

        {
            "id": 3,
            "type": "statistical_numeric",
            "question": (
                "study_hours 与 final_score 的 "
                "Pearson 相关系数是多少？"
            ),
            "expected_answer": study_hours_corr,
        },

        {
            "id": 4,
            "type": "statistical_text",
            "question": (
                "哪个变量与 final_score 的线性相关性最强？"
            ),
            "expected_answer": strongest_correlation_feature,
        },

        {
            "id": 5,
            "type": "machine_learning_numeric",
            "question": "Random Forest 的 MAE 是多少？",
            "expected_answer": rf_mae,
        },

        {
            "id": 6,
            "type": "machine_learning_numeric",
            "question": "Random Forest 的 RMSE 是多少？",
            "expected_answer": rf_rmse,
        },

        {
            "id": 7,
            "type": "machine_learning_numeric",
            "question": "Random Forest 的测试集 R² 是多少？",
            "expected_answer": rf_r2,
        },

        {
            "id": 8,
            "type": "machine_learning_numeric",
            "question": (
                "study_hours 的 Random Forest "
                "feature importance 是多少？"
            ),
            "expected_answer": study_hours_importance,
        },

        {
            "id": 9,
            "type": "causal_reasoning",
            "question": (
                "study_hours 的 feature importance 较高，"
                "是否意味着增加学习时间一定会导致成绩提高？"
            ),
            "expected_answer": "no",
        },

        {
            "id": 10,
            "type": "causal_reasoning",
            "question": "相关性是否可以直接证明因果关系？",
            "expected_answer": "no",
        },
    ]

    return questions


# =============================================================
# Text normalization
# =============================================================

def normalize_text(text: Any) -> str:
    """
    Normalize text for robust matching.
    """

    return (
        str(text or "")
        .strip()
        .lower()
        .replace(" ", "")
        .replace("　", "")
    )


# =============================================================
# Numeric extraction
# =============================================================

def extract_numbers(text: str) -> List[float]:
    """
    Extract decimal / integer numbers from text.
    """

    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        text
    )

    return [
        float(value)
        for value in numbers
    ]


def numeric_match(
    expected: Any,
    answer: str,
    relative_tolerance: float = 0.03,
    absolute_tolerance: float = 0.01,
) -> bool:
    """
    Check whether the expected numeric value appears
    in the Agent answer within a reasonable tolerance.
    """

    if expected is None:
        return False

    try:
        expected_value = float(expected)
    except (ValueError, TypeError):
        return False

    answer_numbers = extract_numbers(answer)

    if not answer_numbers:
        return False

    tolerance = max(
        absolute_tolerance,
        abs(expected_value) * relative_tolerance
    )

    return any(
        abs(value - expected_value) <= tolerance
        for value in answer_numbers
    )


# =============================================================
# Text answer matching
# =============================================================

def text_match(
    expected: Any,
    answer: str
) -> bool:
    """
    Match textual answers.

    Uses keyword / phrase matching rather than
    numeric extraction.
    """

    if expected is None:
        return False

    expected_text = normalize_text(expected)
    normalized_answer = normalize_text(answer)

    if not expected_text:
        return False

    return expected_text in normalized_answer


# =============================================================
# Causal reasoning evaluation
# =============================================================

def evaluate_causal_reasoning(
    answer: str
) -> bool:
    """
    Evaluate whether the Agent correctly rejects
    direct causal interpretation.

    The answer should contain language indicating:
    - no
    - not necessarily
    - correlation does not imply causation
    - feature importance does not mean causal contribution
    """

    normalized_answer = normalize_text(answer)

    negative_patterns = [
        "不能",
        "不能直接",
        "不能证明",
        "无法证明",
        "不代表",
        "不意味着",
        "并不意味着",
        "不是因果",
        "不是因果关系",
        "不等于因果",
        "相关不等于因果",
        "相关性不等于因果",
        "相关性不能证明因果",
        "无法说明因果",
        "不能说明因果",
        "不能推断因果",
        "no",
        "not",
        "cannot",
        "doesnotmean",
        "notnecessarily",
        "correlationdoesnotimplycausation",
        "correlationisnotcausation",
    ]

    return any(
        pattern in normalized_answer
        for pattern in negative_patterns
    )


# =============================================================
# Main evaluator
# =============================================================

def evaluate_agent_response(
    question: Dict[str, Any],
    agent_answer: str
) -> Dict[str, Any]:
    """
    Evaluate one Agent answer.

    Important:
    This evaluator checks whether the expected fact,
    value, or reasoning pattern is present in the
    Agent's generated analysis.
    """

    question_id = question.get("id")
    question_type = question.get("type")
    expected = question.get("expected_answer")

    answer = str(agent_answer or "").strip()

    correct = False

    # ---------------------------------------------------------
    # Fact
    # ---------------------------------------------------------

    if question_type == "fact":

        correct = text_match(
            expected,
            answer
        )

    # ---------------------------------------------------------
    # Statistical numeric
    # ---------------------------------------------------------

    elif question_type == "statistical_numeric":

        correct = numeric_match(
            expected,
            answer
        )

    # ---------------------------------------------------------
    # Statistical text
    # ---------------------------------------------------------

    elif question_type == "statistical_text":

        correct = text_match(
            expected,
            answer
        )

    # ---------------------------------------------------------
    # Machine learning numeric
    # ---------------------------------------------------------

    elif question_type == "machine_learning_numeric":

        correct = numeric_match(
            expected,
            answer
        )

    # ---------------------------------------------------------
    # Causal reasoning
    # ---------------------------------------------------------

    elif question_type == "causal_reasoning":

        correct = evaluate_causal_reasoning(
            answer
        )

    return {
        "question_id": question_id,
        "type": question_type,
        "question": question.get("question"),
        "expected_answer": expected,
        "agent_answer": answer,
        "correct": correct,
    }


# =============================================================
# Evaluation summary
# =============================================================

def summarize_evaluation(
    evaluation_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calculate evaluation metrics.

    Metrics:
    - overall accuracy
    - factual accuracy
    - numerical accuracy
    - statistical reasoning accuracy
    - causal reasoning accuracy
    - error rate

    Note:
    'hallucination_rate' is retained for backward compatibility,
    but is defined here as factual/numerical error rate rather
    than a strict semantic hallucination detector.
    """

    total = len(evaluation_results)

    if total == 0:
        return {
            "total_questions": 0,
            "correct_questions": 0,
            "overall_accuracy": 0,
            "fact_accuracy": 0,
            "numerical_accuracy": 0,
            "statistical_reasoning_accuracy": 0,
            "causal_reasoning_accuracy": 0,
            "hallucination_rate": 0,
            "error_rate": 0,
        }

    # ---------------------------------------------------------
    # Overall
    # ---------------------------------------------------------

    correct_count = sum(
        1
        for item in evaluation_results
        if item.get("correct")
    )

    overall_accuracy = (
        correct_count / total * 100
    )

    # ---------------------------------------------------------
    # Fact
    # ---------------------------------------------------------

    fact_items = [
        item
        for item in evaluation_results
        if item.get("type") == "fact"
    ]

    # ---------------------------------------------------------
    # Numerical
    # ---------------------------------------------------------

    numerical_items = [
        item
        for item in evaluation_results
        if item.get("type") in (
            "statistical_numeric",
            "machine_learning_numeric",
        )
    ]

    # ---------------------------------------------------------
    # Statistical reasoning
    # ---------------------------------------------------------

    statistical_items = [
        item
        for item in evaluation_results
        if item.get("type") in (
            "statistical_numeric",
            "statistical_text",
        )
    ]

    # ---------------------------------------------------------
    # Causal reasoning
    # ---------------------------------------------------------

    causal_items = [
        item
        for item in evaluation_results
        if item.get("type") == "causal_reasoning"
    ]

    # ---------------------------------------------------------
    # Accuracy helper
    # ---------------------------------------------------------

    def calculate_accuracy(
        items: List[Dict[str, Any]]
    ) -> float:

        if not items:
            return 0.0

        correct = sum(
            1
            for item in items
            if item.get("correct")
        )

        return (
            correct / len(items) * 100
        )

    fact_accuracy = calculate_accuracy(
        fact_items
    )

    numerical_accuracy = calculate_accuracy(
        numerical_items
    )

    statistical_reasoning_accuracy = calculate_accuracy(
        statistical_items
    )

    causal_accuracy = calculate_accuracy(
        causal_items
    )

    # ---------------------------------------------------------
    # Error rate
    # ---------------------------------------------------------

    error_count = (
        total - correct_count
    )

    error_rate = (
        error_count / total * 100
    )

    # ---------------------------------------------------------
    # Backward-compatible hallucination metric
    # ---------------------------------------------------------

    factual_items = (
        fact_items +
        numerical_items
    )

    if factual_items:

        wrong_factual = sum(
            1
            for item in factual_items
            if not item.get("correct")
        )

        hallucination_rate = (
            wrong_factual
            / len(factual_items)
            * 100
        )

    else:

        hallucination_rate = 0.0

    return {
        "total_questions": total,

        "correct_questions": correct_count,

        "overall_accuracy": round(
            overall_accuracy,
            2
        ),

        "fact_accuracy": round(
            fact_accuracy,
            2
        ),

        "numerical_accuracy": round(
            numerical_accuracy,
            2
        ),

        "statistical_reasoning_accuracy": round(
            statistical_reasoning_accuracy,
            2
        ),

        "causal_reasoning_accuracy": round(
            causal_accuracy,
            2
        ),

        "hallucination_rate": round(
            hallucination_rate,
            2
        ),

        "error_rate": round(
            error_rate,
            2
        ),
    }