import { useEffect, useState } from "react";

export default function ResultsPage() {
  const [rows, setRows] = useState([]);
  const [fileName, setFileName] = useState("");

  useEffect(() => {
    async function fetchResults() {
      const res = await fetch("http://127.0.0.1:8000/api/latest-vulnerabilities");
      const data = await res.json();
      setRows(data.results || []);
      setFileName(data.file || "Unknown");
    }

    fetchResults();
  }, []);

  return (
    <div className="container" align="center">
      <h1 align="center">Analysis Results</h1>
      <p align="center"><strong>Latest Report:</strong> {fileName}</p>

      <table>
        <thead>
          <tr>
            <th>File</th>
            <th>API</th>
            <th>Attack Type</th>
            <th>Payload</th>
            <th>Severity</th>
            <th>Remediation</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td>{r.file_name}</td>
              <td>{r.api}</td>
              <td>{r.attack_type}</td>
              <td>{r.payload}</td>
              <td>{r.severity}</td>
              <td>{r.remediation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
