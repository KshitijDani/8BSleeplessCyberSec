import { useState } from "react";
import { useNavigate } from "react-router-dom";
import LoadingSpinner from "../components/LoadingSpinner";

export default function InputPage() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    await fetch("http://127.0.0.1:8000/api/run-graph", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl }),
    });

    navigate("/results");
  }

  return (
    <div className="container" align="center">
      <h1>8BSleepless Vulnerability Management Agent</h1>
        <div align="center">
            <form onSubmit={handleSubmit} style={{ marginTop: "2rem" }}>
                <input
                type="text"
                placeholder="Enter GitHub repo URL"
                value={repoUrl}
                required
                onChange={(e) => setRepoUrl(e.target.value)}
                />

                <button type="submit" style={{ width: "100%", marginTop: "16px" }}>
                Analyze Repo
                </button>
            </form>
        </div>
      {loading && (
        <div style={{ textAlign: "center", marginTop: "40px" }}>
          <LoadingSpinner />
          <p>Running analysis…</p>
        </div>
      )}
    </div>
  );
}
