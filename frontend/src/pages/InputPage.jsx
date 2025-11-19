import { useState } from "react";
import { useNavigate } from "react-router-dom";
import LoadingSpinner from "../components/LoadingSpinner";

export default function InputPage() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  function navigateToResults() {
    navigate("/results");
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    // TO-DO: Cleanup and pass URL as a variable.
    await fetch("http://127.0.0.1:8000/api/run-graph", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl }),
    });

    navigateToResults()
  }

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        textAlign: "center",
        padding: "0 20px",
      }}
    >
      <h1 style={{ marginBottom: "100px" }}>
        8BSleepless Vulnerability Management Agent
      </h1>

      <form onSubmit={handleSubmit} style={{ width: "100%", maxWidth: "500px" }}>
        <input
          type="text"
          placeholder="Enter GitHub repo URL"
          value={repoUrl}
          required
          onChange={(e) => setRepoUrl(e.target.value)}
          style={{ width: "95%", marginBottom: "16px" }}
        />

        <button type="submit" style={{ width: "100%", marginBottom: "16px" }}>Analyze Repo</button>
        <button onClick={navigateToResults} style={{ width: "100%", marginBottom: "16px" }}>View Latest Report</button>
      </form>

      {loading && (
        <div style={{ marginTop: "40px" }}>
          <LoadingSpinner />
          <p>Running analysis…</p>
        </div>
      )}
    </div>
  );
}
