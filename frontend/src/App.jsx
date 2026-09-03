import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [targetColumn, setTargetColumn] = useState("final_score");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setResult(null);
    setError("");
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("请先选择 CSV 或 Excel 文件");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("file", file);
    formData.append("target_column", targetColumn);

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
          data.detail || "分析失败，请检查后端服务"
        );
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getImageUrl = (path) => {
    if (!path) {
      return "";
    }

    if (path.startsWith("http")) {
      return path;
    }

    return `http://127.0.0.1:8000${path}`;
  };

  return (
    <div className="app">

      {/* 顶部 */}
      <header className="header">
        <div>
          <h1>LLM Data Analysis Agent</h1>
          <p>
            AI 驱动的数据分析与智能洞察平台
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Engine Online
        </div>
      </header>


      {/* 上传区域 */}
      <section className="upload-card">

        <div className="section-title">
          <span>📁</span>
          <div>
            <h2>上传数据</h2>
            <p>
              支持 CSV、Excel 数据文件
            </p>
          </div>
        </div>

        <label className="upload-box">

          <input
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileChange}
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
                setTargetColumn(e.target.value)
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


      {/* Loading */}
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


      {/* 分析结果 */}
      {result && (
        <main className="results">

          {/* 数据概览 */}
          <section className="result-section">

            <div className="section-title">
              <span>📊</span>
              <div>
                <h2>数据概览</h2>
                <p>
                  数据集基本信息
                </p>
              </div>
            </div>


            <div className="stats-grid">

              <div className="stat-card">
                <span>原始数据</span>
                <strong>
                  {result.data_info.original_rows}
                </strong>
                <small>行</small>
              </div>

              <div className="stat-card">
                <span>清洗后数据</span>
                <strong>
                  {result.data_info.cleaned_rows}
                </strong>
                <small>行</small>
              </div>

              <div className="stat-card">
                <span>特征数量</span>
                <strong>
                  {result.data_info.cleaned_columns}
                </strong>
                <small>列</small>
              </div>

              <div className="stat-card">
                <span>模型 MAE</span>
                <strong>
                  {result.machine_learning.mae.toFixed(2)}
                </strong>
                <small>误差</small>
              </div>

            </div>


            <div className="columns-box">

              <strong>
                数据字段
              </strong>

              <div className="tags">

                {result.data_info.columns.map(
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


          {/* 可视化 */}
          <section className="result-section">

            <div className="section-title">
              <span>📈</span>

              <div>
                <h2>数据可视化</h2>
                <p>
                  自动生成的数据分析图表
                </p>
              </div>
            </div>


            <div className="charts">

              <div className="chart-card">
                <h3>
                  相关性热力图
                </h3>

                <img
                  src={getImageUrl(
                    result.visualizations
                      .correlation_heatmap
                  )}
                  alt="Correlation Heatmap"
                />
              </div>


              <div className="chart-card">
                <h3>
                  学习时间与最终成绩
                </h3>

                <img
                  src={getImageUrl(
                    result.visualizations
                      .study_hours_vs_final_score
                  )}
                  alt="Study Hours vs Final Score"
                />
              </div>


              <div className="chart-card chart-wide">
                <h3>
                  特征重要性分析
                </h3>

                <img
                  src={getImageUrl(
                    result.visualizations
                      .feature_importance
                  )}
                  alt="Feature Importance"
                />
              </div>

            </div>

          </section>


          {/* 机器学习 */}
          <section className="result-section">

            <div className="section-title">
              <span>🧠</span>

              <div>
                <h2>机器学习结果</h2>
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
                  {result.machine_learning.mae.toFixed(
                    3
                  )}
                </strong>
              </div>


              <div>
                <span>
                  RMSE
                </span>

                <strong>
                  {result.machine_learning.rmse.toFixed(
                    3
                  )}
                </strong>
              </div>

            </div>


            <h3>
              特征重要性
            </h3>

            <div className="importance-list">

              {Object.entries(
                result.machine_learning
                  .feature_importance
              )
                .sort((a, b) => b[1] - a[1])
                .map(([name, value]) => (

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
                          width: `${value * 100}%`,
                        }}
                      ></div>

                    </div>

                    <div className="importance-value">
                      {(value * 100).toFixed(1)}%
                    </div>

                  </div>

                ))}

            </div>

          </section>


          {/* AI 报告 */}
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

              {result.ai_analysis}

            </div>

          </section>

        </main>
      )}


      {/* Footer */}
      <footer>
        LLM Data Analysis Agent · AI-powered Data Science Platform
      </footer>

    </div>
  );
}

export default App;