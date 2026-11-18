
import {
  FaArrowUp,
  FaRegCommentDots,
  FaChartLine,
  FaXmark
} from "react-icons/fa6";
import api from "../services/api";
import { useState, useEffect, useRef } from "react";

function ChatPanel({ selectedDocument, setObservations }) {
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [showMetrics, setShowMetrics] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    // scrolls inside .chat-body because bottomRef is now a child of it
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const loadMetrics = async () => {
    try {
      const res = await api.get("/metrics");
      setMetrics(res.data);
      setShowMetrics(true);
    } catch (err) {
      console.log(err);
    }
  };

  const resetMetrics = async () => {
    try {
      await api.delete("/metrics/reset");
      await loadMetrics();
    } catch (err) {
      console.log(err);
    }
  };

  const handleSend = async () => {
    if (!draft.trim()) return;
    const question = draft;
    setMessages((prev) => [...prev, { type: "user", content: question }]);
    setDraft("");
    try {
      setLoading(true);
      const answerResponse = await api.post("/ask", { question, document_name: selectedDocument });
      const debugResponse  = await api.post("/debug-retrieval", { question, document_name: selectedDocument });
      setObservations(debugResponse.data);
      setMessages((prev) => [
        ...prev,
        { type: "assistant", content: answerResponse.data.answer, sources: answerResponse.data.sources },
      ]);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <div className="chat-header-left">
          Production RAG
          <span className="chat-header-tag">
            {selectedDocument === "all" ? "All Documents" : selectedDocument}
          </span>
        </div>
        <button
          className="metrics-btn"
          onClick={loadMetrics}
        >
          <FaChartLine />
          Metrics
        </button>
      </div>

      <div className="chat-body">  {/* must have overflow-y: auto + fixed height in CSS */}
        {messages.length === 0 ? (
          <div className="chat-empty">
            <div className="chat-empty-icon"><FaRegCommentDots /></div>
            <h2>Ask your documents anything</h2>
            <p>Upload PDFs and start chatting</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-header">
                <div className="avatar">{message.type === "user" ? "You" : "AI"}</div>
              </div>
              <div className="message-content">{message.content}</div>
              {message.sources && (
                <div className="sources">
                  <div className="sources-title">Sources</div>
                  <div className="sources-list">
                    {message.sources.map((source, idx) => (
                      <span key={idx} className="source-pill">
                        {typeof source === "string" ? source : `${source.document} • Page ${source.page}`}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <div className="message assistant">
            <div className="avatar">AI</div>
            <div className="message-content">Thinking...</div>
          </div>
        )}

        {/* ✅ bottomRef is now INSIDE chat-body so scrollIntoView works */}
        <div ref={bottomRef} />
      </div>

      {showMetrics && metrics && (
        <div className="metrics-overlay">
          <div className="metrics-modal">
            <div className="metrics-modal-header">
              <h2>System Metrics</h2>
              <button
                className="close-btn"
                onClick={() => setShowMetrics(false)}
              >
                <FaXmark />
              </button>
            </div>

            <div className="metrics-grid">
              <div className="metric-card">
                <h4>Requests</h4>
                <span>{metrics.requests}</span>
              </div>
              <div className="metric-card">
                <h4>Failure Rate</h4>
                <span>{metrics.failure_rate}%</span>
              </div>
              <div className="metric-card">
                <h4>Citation Rate</h4>
                <span>{metrics.citation_rate}%</span>
              </div>
              <div className="metric-card">
                <h4>Avg Latency</h4>
                <span>{metrics.avg_latency}s</span>
              </div>
              <div className="metric-card">
                <h4>P50</h4>
                <span>{metrics.p50_latency}s</span>
              </div>
              <div className="metric-card">
                <h4>P90</h4>
                <span>{metrics.p90_latency}s</span>
              </div>
              <div className="metric-card">
                <h4>P99</h4>
                <span>{metrics.p99_latency}s</span>
              </div>
              <div className="metric-card">
                <h4>AVG PROMPT TOKENS</h4>
                <span>{metrics.avg_prompt_tokens_per_request}</span>
              </div>
              <div className="metric-card">
                <h4>AVG COMPLETION TOKENS</h4>
                <span>{metrics.avg_completion_tokens_per_request}</span>
              </div>
              <div className="metric-card">
                <h4>AVG TOTAL TOKENS</h4>
                <span>{metrics.avg_total_tokens_per_request}</span>
              </div>
              <div className="metric-card">
                <h4>AVG COST / REQUEST</h4>
                <span>${metrics.avg_cost_per_request}</span>
              </div>
              <div className="metric-card">
                <h4>Total Cost</h4>
                <span>${metrics.total_cost}</span>
              </div>
            </div>

            <button
              className="reset-metrics-btn"
              onClick={resetMetrics}
            >
              Reset Metrics
            </button>
          </div>
        </div>
      )}

      <div className="chat-input-bar">
        <input
          type="text"
          placeholder="Ask a question about your documents..."
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button className="chat-send-btn" onClick={handleSend}><FaArrowUp /></button>
      </div>
    </div>
  );
}
export default ChatPanel;