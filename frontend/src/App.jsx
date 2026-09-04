import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [targetColumn, setTargetColumn] = useState("final_score");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // =========================================================
  // 文件选择
  // =========================================================

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setResult(null);
    setError("");
  };

  // =========================================================
  // 开始分析
  // =========================================================

  const handleAnalyze = async () => {
    if (!file) {
      setError("请先选择 CSV 或 Excel 文件");
      return;
    }

    if (!targetColumn.trim()) {
      setError("请输入预测目标字段");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("file", file);
    formData.append(
      "target_column",
      targetColumn.trim()
    );

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            "分析失败，请检查后端服务"
        );
      }

      setResult(data);
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "无法连接后端服务，请确认 FastAPI 正在运行"
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // 图片地址
  // =========================================================

  const getImageUrl = (path) => {
    if (!path) {
      return "";
    }

    if (
      path.startsWith("http://") ||
      path.startsWith("https://")
    ) {
      return path;
    }

    return `http://127.0.0.1:8000${path}`;
  };

  // =========================================================
  // 数据保留率
  // =========================================================

  const getRetentionRate = () => {
    if (
      !result ||
      !result.cleaning_report
    ) {
      return "0.0";
    }

    const originalRows =
      Number(
        result.cleaning_report.original_rows
      ) || 0;

    const cleanedRows =
      Number(
        result.cleaning_report.cleaned_rows
      ) || 0;

    if (originalRows === 0) {
      return "0.0";
    }

    return (
      (cleanedRows / originalRows) *
      100
    ).toFixed(1);
  };

  // =========================================================
  // AI Insights
  // =========================================================

  const getAIInsights = () => {
    const ml = result?.machine_learning;
    const cleaning = result?.cleaning_report;

    if (!ml) {
      return {
        coreFindings: [
          "暂无足够数据生成核心发现",
        ],
        keyFactors: [],
        warnings: [],
        suggestions: [
          "请先完成一次数据分析",
        ],
      };
    }

    const sortedFeatures = Object.entries(
      ml.feature_importance || {}
    ).sort(
      (a, b) => Number(b[1]) - Number(a[1])
    );

    const topFeature =
      sortedFeatures[0];

    return {
      coreFindings: [
        topFeature
          ? `${topFeature[0]} 是当前模型中最重要的影响因素，特征重要性约为 ${(Number(
              topFeature[1]
            ) * 100).toFixed(1)}%。`
          : "当前模型暂未识别出明显的关键影响因素。",

        `模型 MAE 为 ${Number(
          ml.mae || 0
        ).toFixed(
          2
        )}，RMSE 为 ${Number(
          ml.rmse || 0
        ).toFixed(2)}。`,
      ],

      keyFactors: sortedFeatures
        .slice(0, 4)
        .map(([name, value]) => ({
          name,
          value: `${(
            Number(value) * 100
          ).toFixed(1)}%`,
        })),

      warnings: cleaning
        ? [
            cleaning.duplicate_rows_removed >
            0
              ? `检测到 ${cleaning.duplicate_rows_removed} 条重复记录，已自动删除。`
              : "未检测到重复记录。",

            cleaning.remaining_missing_values >
            0
              ? `清洗后仍存在 ${cleaning.remaining_missing_values} 个缺失值。`
              : "数据清洗完成后不存在缺失值。",
          ]
        : ["暂无数据清洗报告。"],

      suggestions: [
        "结合特征重要性进一步分析关键变量与目标变量之间的关系。",
        "增加更多样本后重新训练模型，可以进一步验证模型稳定性。",
        "结合业务背景对模型发现进行人工解释，避免仅依赖模型相关性。",
      ],
    };
  };

  const aiInsights =
    result ? getAIInsights() : null;

  // =========================================================
  // Markdown 行内渲染
  // =========================================================

  const renderInlineMarkdown = (text) => {
    if (!text) {
      return null;
    }

    const parts = [];

    const regex =
      /(\*\*.*?\*\*|`.*?`)/g;

    let lastIndex = 0;
    let match;
    let key = 0;

    while (
      (match = regex.exec(text)) !== null
    ) {
      const before = text.slice(
        lastIndex,
        match.index
      );

      if (before) {
        parts.push(
          <span key={key++}>
            {before}
          </span>
        );
      }

      const token = match[0];

      if (
        token.startsWith("**") &&
        token.endsWith("**")
      ) {
        parts.push(
          <strong key={key++}>
            {token.slice(2, -2)}
          </strong>
        );
      } else if (
        token.startsWith("`") &&
        token.endsWith("`")
      ) {
        parts.push(
          <span
            key={key++}
            className="ai-code"
          >
            {token.slice(1, -1)}
          </span>
        );
      }

      lastIndex =
        match.index + token.length;
    }

    if (lastIndex < text.length) {
      parts.push(
        <span key={key++}>
          {text.slice(lastIndex)}
        </span>
      );
    }

    return parts;
  };

  // =========================================================
  // DeepSeek AI 报告渲染
  // =========================================================

  const renderAIReport = (text) => {
    if (!text) {
      return (
        <p className="ai-empty">
          暂无 AI 分析结果
        </p>
      );
    }

    const normalizedText = String(text)
      .replace(/\r\n/g, "\n")
      .replace(/\r/g, "\n");

    const lines =
      normalizedText.split("\n");

    const elements = [];

    let unorderedItems = [];
    let orderedItems = [];

    const flushLists = () => {
      if (unorderedItems.length > 0) {
        elements.push(
          <ul
            className="ai-report-list"
            key={`ul-${elements.length}`}
          >
            {unorderedItems.map(
              (item, index) => (
                <li key={index}>
                  {renderInlineMarkdown(item)}
                </li>
              )
            )}
          </ul>
        );

        unorderedItems = [];
      }

      if (orderedItems.length > 0) {
        elements.push(
          <ol
            className="ai-report-list"
            key={`ol-${elements.length}`}
          >
            {orderedItems.map(
              (item, index) => (
                <li key={index}>
                  {renderInlineMarkdown(item)}
                </li>
              )
            )}
          </ol>
        );

        orderedItems = [];
      }
    };

    lines.forEach(
      (rawLine, index) => {
        const line = rawLine.trim();

        // 空行
        if (!line) {
          flushLists();
          return;
        }

        // Markdown 一级标题
        if (line.startsWith("# ")) {
          flushLists();

          elements.push(
            <h2
              className="ai-report-main-title"
              key={`h2-${index}`}
            >
              {renderInlineMarkdown(
                line.replace(
                  /^#\s+/,
                  ""
                )
              )}
            </h2>
          );

          return;
        }

        // Markdown 二级标题
        if (line.startsWith("## ")) {
          flushLists();

          elements.push(
            <h3
              className="ai-report-title"
              key={`h3-${index}`}
            >
              {renderInlineMarkdown(
                line.replace(
                  /^##\s+/,
                  ""
                )
              )}
            </h3>
          );

          return;
        }

        // Markdown 三级标题
        if (line.startsWith("### ")) {
          flushLists();

          elements.push(
            <h4
              className="ai-report-subtitle"
              key={`h4-${index}`}
            >
              {renderInlineMarkdown(
                line.replace(
                  /^###\s+/,
                  ""
                )
              )}
            </h4>
          );

          return;
        }

        // =====================================================
        // "1. 数据集概况" 这种标题
        // =====================================================

        const numberedHeading =
          line.match(
            /^(\d+)\.\s+(.+)$/
          );

        if (numberedHeading) {
          flushLists();

          elements.push(
            <h3
              className="ai-report-title"
              key={`number-title-${index}`}
            >
              <span className="ai-report-number">
                {numberedHeading[1]}
              </span>

              {renderInlineMarkdown(
                numberedHeading[2]
              )}
            </h3>
          );

          return;
        }

        // =====================================================
        // 无序列表
        // =====================================================

        if (
          line.startsWith("- ") ||
          line.startsWith("* ") ||
          line.startsWith("• ")
        ) {
          orderedItems = [];

          unorderedItems.push(
            line.replace(
              /^(-|\*|•)\s+/,
              ""
            )
          );

          return;
        }

        // =====================================================
        // 有序列表
        // =====================================================

        const orderedItem =
          line.match(
            /^\d+[.)]\s+(.+)$/
          );

        if (orderedItem) {
          unorderedItems = [];

          orderedItems.push(
            orderedItem[1]
          );

          return;
        }

        // =====================================================
        // 普通段落
        // =====================================================

        flushLists();

        elements.push(
          <p
            className="ai-report-paragraph"
            key={`p-${index}`}
          >
            {renderInlineMarkdown(line)}
          </p>
        );
      }
    );

    flushLists();

    return elements;
  };

  // =========================================================
  // 页面
  // =========================================================

  return (
    <div className="app">

      {/* =====================================================
          Header
      ===================================================== */}

      <header className="header">
        <div>
          <h1>
            LLM Data Analysis Agent
          </h1>

          <p>
            AI 驱动的数据分析与智能洞察平台
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Engine Online
        </div>
      </header>

      {/* =====================================================
          Upload
      ===================================================== */}

      <section className="upload-card">

        <div className="section-title">
          <span>📁</span>

          <div>
            <h2>
              上传数据
            </h2>

            <p>
              支持 CSV、Excel 数据文件
            </p>
          </div>
        </div>

        <label className="upload-box">

          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={
              handleFileChange
            }
          />

          <div className="upload-icon">
            ↑
          </div>

          <div className="upload-text">
            {file
              ? file.name
              : "点击选择数据文件"}
          </div>

          <div className="upload-hint">
            CSV / XLSX / XLS
          </div>

        </label>

        <div className="analysis-options">

          <div className="option">

            <label>
              预测目标
            </label>

            <input
              type="text"
              value={targetColumn}
              onChange={(e) =>
                setTargetColumn(
                  e.target.value
                )
              }
              placeholder="例如：final_score"
            />

          </div>

          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading
              ? "AI 正在分析..."
              : "🚀 开始 AI 分析"}
          </button>

        </div>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

      </section>

      {/* =====================================================
          Loading
      ===================================================== */}

      {loading && (
        <section className="loading-card">

          <div className="loader"></div>

          <h3>
            AI 正在分析你的数据
          </h3>

          <p>
            数据清洗 → EDA → 机器学习 → 可视化 → DeepSeek AI
          </p>

        </section>
      )}

      {/* =====================================================
          Results
      ===================================================== */}

      {result && (
        <main className="results">

          {/* =================================================
              数据概览
          ================================================= */}

          <section className="result-section">

            <div className="section-title">

              <span>📊</span>

              <div>
                <h2>
                  数据概览
                </h2>

                <p>
                  数据集基本信息与数据质量概览
                </p>
              </div>

            </div>

            <div className="stats-grid">

              {/* 原始数据 */}

              <div className="stat-card">

                <span>
                  原始数据
                </span>

                <strong>
                  {
                    result.cleaning_report
                      ?.original_rows ??
                    result.data_shape
                      ?.original?.[0] ??
                    0
                  }
                </strong>

                <small>
                  rows
                </small>

              </div>

              {/* 清洗后数据 */}

              <div className="stat-card">

                <span>
                  清洗后数据
                </span>

                <strong>
                  {
                    result.cleaning_report
                      ?.cleaned_rows ??
                    result.data_shape
                      ?.cleaned?.[0] ??
                    0
                  }
                </strong>

                <small>
                  rows
                </small>

              </div>

              {/* 特征数量 */}

              <div className="stat-card">

                <span>
                  特征数量
                </span>

                <strong>
                  {
                    result.cleaning_report
                      ?.cleaned_columns ??
                    result.data_shape
                      ?.cleaned?.[1] ??
                    result.columns
                      ?.length ??
                    0
                  }
                </strong>

                <small>
                  features
                </small>

              </div>

              {/* 数据保留率 */}

              <div className="stat-card">

                <span>
                  数据保留率
                </span>

                <strong>
                  {getRetentionRate()}%
                </strong>

                <small>
                  after cleaning
                </small>

              </div>

              {/* MAE */}

              <div className="stat-card">

                <span>
                  模型 MAE
                </span>

                <strong>
                  {Number(
                    result
                      .machine_learning
                      ?.mae ?? 0
                  ).toFixed(2)}
                </strong>

                <small>
                  prediction error
                </small>

              </div>

              {/* RMSE */}

              <div className="stat-card">

                <span>
                  模型 RMSE
                </span>

                <strong>
                  {Number(
                    result
                      .machine_learning
                      ?.rmse ?? 0
                  ).toFixed(2)}
                </strong>

                <small>
                  prediction error
                </small>

              </div>

            </div>

            {/* 数据字段 */}

            <div className="columns-box">

              <strong>
                数据字段
              </strong>

              <div className="tags">

                {(result.columns ||
                  []).map(
                  (column) => (
                    <span
                      className="tag"
                      key={column}
                    >
                      {column}
                    </span>
                  )
                )}

              </div>

            </div>

          </section>

          {/* =================================================
              数据清洗流程
          ================================================= */}

          {result.cleaning_report && (
            <section className="result-section">

              <div className="section-title">

                <span>🧹</span>

                <div>
                  <h2>
                    数据清洗流程
                  </h2>

                  <p>
                    自动完成重复值、缺失值与数据质量处理
                  </p>
                </div>

              </div>

              {/* 清洗统计 */}

              <div className="cleaning-summary">

                <div className="cleaning-card">

                  <span>
                    删除重复记录
                  </span>

                  <strong>
                    {
                      result
                        .cleaning_report
                        .duplicate_rows_removed ??
                      0
                    }
                  </strong>

                  <small>
                    duplicate rows
                  </small>

                </div>

                <div className="cleaning-card">

                  <span>
                    处理缺失值
                  </span>

                  <strong>
                    {
                      (
                        result
                          .cleaning_report
                          .numeric_missing_values_filled ||
                        0
                      ) +
                      (
                        result
                          .cleaning_report
                          .categorical_missing_values_filled ||
                        0
                      )
                    }
                  </strong>

                  <small>
                    missing values
                  </small>

                </div>

                <div className="cleaning-card">

                  <span>
                    删除空字段
                  </span>

                  <strong>
                    {
                      result
                        .cleaning_report
                        .empty_columns_removed ??
                      0
                    }
                  </strong>

                  <small>
                    empty columns
                  </small>

                </div>

                <div className="cleaning-card">

                  <span>
                    剩余缺失值
                  </span>

                  <strong>
                    {
                      result
                        .cleaning_report
                        .remaining_missing_values ??
                      0
                    }
                  </strong>

                  <small>
                    after cleaning
                  </small>

                </div>

              </div>

              {/* 清洗流程 */}

              <div className="cleaning-pipeline">

                <div className="pipeline-step">

                  <div className="pipeline-icon">
                    1
                  </div>

                  <div>
                    <strong>
                      原始数据
                    </strong>

                    <p>
                      {
                        result
                          .cleaning_report
                          .original_rows
                      }{" "}
                      行 ×{" "}
                      {
                        result
                          .cleaning_report
                          .original_columns
                      }{" "}
                      列
                    </p>
                  </div>

                </div>

                <div className="pipeline-arrow">
                  ↓
                </div>

                <div className="pipeline-step">

                  <div className="pipeline-icon">
                    2
                  </div>

                  <div>
                    <strong>
                      删除重复记录
                    </strong>

                    <p>
                      删除{" "}
                      {
                        result
                          .cleaning_report
                          .duplicate_rows_removed
                      }{" "}
                      条重复记录
                    </p>
                  </div>

                </div>

                <div className="pipeline-arrow">
                  ↓
                </div>

                <div className="pipeline-step">

                  <div className="pipeline-icon">
                    3
                  </div>

                  <div>
                    <strong>
                      处理缺失值
                    </strong>

                    <p>
                      数值字段使用中位数填充，共处理{" "}
                      {
                        result
                          .cleaning_report
                          .numeric_missing_values_filled ||
                        0
                      }{" "}
                      个；分类字段使用众数填充，共处理{" "}
                      {
                        result
                          .cleaning_report
                          .categorical_missing_values_filled ||
                        0
                      }{" "}
                      个
                    </p>
                  </div>

                </div>

                <div className="pipeline-arrow">
                  ↓
                </div>

                <div className="pipeline-step pipeline-success">

                  <div className="pipeline-icon">
                    ✓
                  </div>

                  <div>
                    <strong>
                      清洗完成
                    </strong>

                    <p>
                      {
                        result
                          .cleaning_report
                          .cleaned_rows
                      }{" "}
                      行 ×{" "}
                      {
                        result
                          .cleaning_report
                          .cleaned_columns
                      }{" "}
                      列，剩余缺失值{" "}
                      {
                        result
                          .cleaning_report
                          .remaining_missing_values
                      }
                    </p>
                  </div>

                </div>

              </div>

              {/* 清洗记录 */}

              {result
                .cleaning_report
                .cleaning_steps
                ?.length > 0 && (
                <div className="cleaning-details">

                  <strong>
                    清洗操作记录
                  </strong>

                  <ul>
                    {result
                      .cleaning_report
                      .cleaning_steps
                      .map(
                        (step, index) => (
                          <li key={index}>
                            {step}
                          </li>
                        )
                      )}
                  </ul>

                </div>
              )}

            </section>
          )}

          {/* =================================================
              数据可视化
          ================================================= */}

          {result.visualizations && (
            <section className="result-section">

              <div className="section-title">

                <span>📈</span>

                <div>
                  <h2>
                    数据可视化
                  </h2>

                  <p>
                    自动生成的数据分析图表
                  </p>
                </div>

              </div>

              <div className="charts">

                {/* 相关性热力图 */}

                <div className="chart-card">

                  <h3>
                    相关性热力图
                  </h3>

                  <img
                    src={getImageUrl(
                      result
                        .visualizations
                        .correlation_heatmap
                    )}
                    alt="Correlation Heatmap"
                  />

                </div>

                {/* 学习时间 */}

                <div className="chart-card">

                  <h3>
                    学习时间与最终成绩
                  </h3>

                  <img
                    src={getImageUrl(
                      result
                        .visualizations
                        .study_hours_vs_final_score
                    )}
                    alt="Study Hours vs Final Score"
                  />

                </div>

                {/* 特征重要性 */}

                <div className="chart-card chart-wide">

                  <h3>
                    特征重要性分析
                  </h3>

                  <img
                    src={getImageUrl(
                      result
                        .visualizations
                        .feature_importance
                    )}
                    alt="Feature Importance"
                  />

                </div>

              </div>

            </section>
          )}

          {/* =================================================
              机器学习结果
          ================================================= */}

          {result.machine_learning && (
            <section className="result-section">

              <div className="section-title">

                <span>🧠</span>

                <div>
                  <h2>
                    机器学习结果
                  </h2>

                  <p>
                    Random Forest 回归模型
                  </p>
                </div>

              </div>

              <div className="model-result">

                <div>
                  <span>
                    MAE
                  </span>

                  <strong>
                    {Number(
                      result
                        .machine_learning
                        .mae || 0
                    ).toFixed(3)}
                  </strong>
                </div>

                <div>
                  <span>
                    RMSE
                  </span>

                  <strong>
                    {Number(
                      result
                        .machine_learning
                        .rmse || 0
                    ).toFixed(3)}
                  </strong>
                </div>

              </div>

              <h3>
                特征重要性
              </h3>

              <div className="importance-list">

                {Object.entries(
                  result
                    .machine_learning
                    .feature_importance ||
                    {}
                )
                  .sort(
                    (a, b) =>
                      Number(b[1]) -
                      Number(a[1])
                  )
                  .map(
                    ([name, value]) => (
                      <div
                        className="importance-item"
                        key={name}
                      >

                        <div className="importance-name">
                          {name}
                        </div>

                        <div className="importance-bar">

                          <div
                            className="importance-fill"
                            style={{
                              width: `${Number(
                                value
                              ) * 100}%`,
                            }}
                          ></div>

                        </div>

                        <div className="importance-value">
                          {(
                            Number(value) *
                            100
                          ).toFixed(1)}
                          %
                        </div>

                      </div>
                    )
                  )}

              </div>

            </section>
          )}

          {/* =================================================
              AI Insights
          ================================================= */}

          {aiInsights && (
            <section className="result-section insights-section">

              <div className="section-title">

                <span>✨</span>

                <div>
                  <h2>
                    AI Insights
                  </h2>

                  <p>
                    基于数据清洗、统计分析与机器学习结果提炼的核心洞察
                  </p>
                </div>

              </div>

              <div className="insights-grid">

                {/* 核心发现 */}

                <div className="insight-card">

                  <div className="insight-card-header">

                    <span className="insight-icon">
                      📌
                    </span>

                    <h3>
                      核心发现
                    </h3>

                  </div>

                  <div className="insight-list">

                    {aiInsights
                      .coreFindings
                      .map(
                        (item, index) => (
                          <div
                            className="insight-item"
                            key={index}
                          >

                            <span>
                              •
                            </span>

                            <p>
                              {item}
                            </p>

                          </div>
                        )
                      )}

                  </div>

                </div>

                {/* 关键影响因素 */}

                <div className="insight-card">

                  <div className="insight-card-header">

                    <span className="insight-icon">
                      📈
                    </span>

                    <h3>
                      关键影响因素
                    </h3>

                  </div>

                  <div className="insight-factors">

                    {aiInsights
                      .keyFactors
                      .length > 0 ? (
                      aiInsights
                        .keyFactors
                        .map(
                          (factor) => (
                            <div
                              className="factor-item"
                              key={
                                factor.name
                              }
                            >

                              <span>
                                {
                                  factor.name
                                }
                              </span>

                              <strong>
                                {
                                  factor.value
                                }
                              </strong>

                            </div>
                          )
                        )
                    ) : (
                      <p>
                        暂无特征重要性数据
                      </p>
                    )}

                  </div>

                </div>

                {/* 数据质量 */}

                <div className="insight-card">

                  <div className="insight-card-header">

                    <span className="insight-icon">
                      ⚠️
                    </span>

                    <h3>
                      数据质量提醒
                    </h3>

                  </div>

                  <div className="insight-list">

                    {aiInsights
                      .warnings
                      .map(
                        (item, index) => (
                          <div
                            className="insight-item"
                            key={index}
                          >

                            <span>
                              •
                            </span>

                            <p>
                              {item}
                            </p>

                          </div>
                        )
                      )}

                  </div>

                </div>

                {/* AI 建议 */}

                <div className="insight-card">

                  <div className="insight-card-header">

                    <span className="insight-icon">
                      💡
                    </span>

                    <h3>
                      AI 建议
                    </h3>

                  </div>

                  <div className="insight-list">

                    {aiInsights
                      .suggestions
                      .map(
                        (item, index) => (
                          <div
                            className="insight-item"
                            key={index}
                          >

                            <span>
                              •
                            </span>

                            <p>
                              {item}
                            </p>

                          </div>
                        )
                      )}

                  </div>

                </div>

              </div>

            </section>
          )}

          {/* =================================================
              DeepSeek AI Analysis
          ================================================= */}

          <section className="result-section ai-section">

            <div className="section-title">

              <span>🤖</span>

              <div>
                <h2>
                  DeepSeek AI 智能分析
                </h2>

                <p>
                  基于数据、统计结果和机器学习模型自动生成
                </p>
              </div>

            </div>

            <div className="ai-report">

              {renderAIReport(
                result.ai_analysis
              )}

            </div>

          </section>

        </main>
      )}

      {/* =====================================================
          Footer
      ===================================================== */}

      <footer>
        LLM Data Analysis Agent · AI-powered Data Science Platform
      </footer>

    </div>
  );
}

export default App;