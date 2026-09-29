import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [incidentId, setIncidentId] = useState("INC-1042");
  const [service, setService] = useState("payment-api");
  const [severity, setSeverity] = useState("SEV-1");
  const [deployment, setDeployment] = useState("v2.5.0");
  const [symptoms, setSymptoms] = useState(
    "high latency\nhigh error rate\ndatabase connection exhaustion"
  );

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function investigate() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/incidents/investigate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          incident_id: incidentId,
          service,
          severity,
          symptoms: symptoms
            .split("\n")
            .map((item) => item.trim())
            .filter(Boolean),
          deployment: deployment || null,
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        "Could not connect to IncidentMind backend. Make sure FastAPI is running on port 8001."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>IncidentMind</h1>
          <p>Production Incident Investigation Assistant</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Ready
        </div>
      </header>

      <main>
        <section className="card incident-card">
          <div className="section-title">
            <div>
              <h2>New Incident</h2>
              <p>Provide the current production symptoms.</p>
            </div>
          </div>

          <div className="grid">
            <label>
              Incident ID
              <input
                value={incidentId}
                onChange={(e) => setIncidentId(e.target.value)}
              />
            </label>

            <label>
              Service
              <input
                value={service}
                onChange={(e) => setService(e.target.value)}
              />
            </label>

            <label>
              Severity
              <select
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
              >
                <option>SEV-1</option>
                <option>SEV-2</option>
                <option>SEV-3</option>
                <option>SEV-4</option>
              </select>
            </label>

            <label>
              Deployment
              <input
                value={deployment}
                onChange={(e) => setDeployment(e.target.value)}
              />
            </label>
          </div>

          <label>
            Symptoms
            <textarea
              rows="5"
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="One symptom per line"
            />
          </label>

          <button
            className="investigate-button"
            onClick={investigate}
            disabled={loading}
          >
            {loading ? "Investigating..." : "Investigate Incident"}
          </button>

          {error && <div className="error">{error}</div>}
        </section>

        {result && (
          <>
            <section className="card">
              <div className="section-title">
                <div>
                  <h2>Investigation Report</h2>
                  <p>
                    Evidence retrieved from organizational incident memory.
                  </p>
                </div>

                <span className="badge">{result.severity}</span>
              </div>

              <div className="summary">
                <h3>Summary</h3>
                <p>{result.summary}</p>
              </div>
            </section>

            <section className="card">
              <h2>Root Cause Hypotheses</h2>

              {result.root_cause_hypotheses?.length ? (
                result.root_cause_hypotheses.map((item, index) => (
                  <div className="hypothesis" key={index}>
                    <div className="hypothesis-number">{index + 1}</div>

                    <div>
                      <h3>{item.hypothesis}</h3>

                      <h4>Supporting evidence</h4>

                      {item.evidence?.map((evidence, evidenceIndex) => (
                        <p className="evidence" key={evidenceIndex}>
                          {evidence}
                        </p>
                      ))}
                    </div>
                  </div>
                ))
              ) : (
                <p>No strong historical hypothesis found.</p>
              )}
            </section>

            <section className="two-column">
              <div className="card">
                <h2>Investigation Steps</h2>

                <ul>
                  {result.investigation_steps?.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ul>
              </div>

              <div className="card">
                <h2>Recommended Actions</h2>

                <ul>
                  {result.recommended_actions?.map((action, index) => (
                    <li key={index}>{action}</li>
                  ))}
                </ul>
              </div>
            </section>

            <section className="card">
              <h2>Historical Evidence</h2>

              <div className="evidence-list">
                {result.historical_evidence?.map((item, index) => (
                  <div className="history-item" key={index}>
                    <span className="history-type">
                      {item.type || "memory"}
                    </span>

                    <p>{item.evidence}</p>
                  </div>
                ))}
              </div>
            </section>

            <div className="demo-note">
              {result.ai_status}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;