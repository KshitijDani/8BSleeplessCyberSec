import { useEffect, useState, useMemo } from "react";

export default function ResultsPage() {
  const [rows, setRows] = useState([]);
  const [fileName, setFileName] = useState("");

  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "asc",
  });

  const severityOrder = {
    Critical: 4,
    High: 3,
    Medium: 2,
    Low: 1,
    Info: 0,
  };

  useEffect(() => {
    async function fetchResults() {
      const res = await fetch("http://127.0.0.1:8000/api/latest-vulnerabilities");
      const data = await res.json();
      setRows(data.results || []);
      setFileName(data.file || "Unknown");
    }
    fetchResults();
  }, []);

  function parseLineValue(lineVal) {
    if (!lineVal) return -1;

    // If it's a range like "45-47"
    if (typeof lineVal === "string" && lineVal.includes("-")) {
      const [start] = lineVal.split("-").map((n) => parseInt(n.trim(), 10));
      return start || -1;
    }

    // If it's a single number
    const num = parseInt(lineVal, 10);
    return isNaN(num) ? -1 : num;
  }

  const sortedRows = useMemo(() => {
    if (!sortConfig.key) return rows;

    const sorted = [...rows];

    sorted.sort((a, b) => {
      let valA = a[sortConfig.key];
      let valB = b[sortConfig.key];

      // Severity special sorting
      if (sortConfig.key === "severity") {
        valA = severityOrder[valA] ?? -1;
        valB = severityOrder[valB] ?? -1;
      }

      // Numeric sorting for code lines
      else if (sortConfig.key === "code_lines") {
        valA = parseLineValue(valA);
        valB = parseLineValue(valB);
      }

      // Normalize string values
      else {
        if (typeof valA === "string") valA = valA.toLowerCase();
        if (typeof valB === "string") valB = valB.toLowerCase();
      }

      if (valA < valB) return sortConfig.direction === "asc" ? -1 : 1;
      if (valA > valB) return sortConfig.direction === "asc" ? 1 : -1;
      return 0;
    });

    return sorted;
  }, [rows, sortConfig]);

  function requestSort(column) {
    setSortConfig((prev) => {
      if (prev.key === column) {
        return {
          key: column,
          direction: prev.direction === "asc" ? "desc" : "asc",
        };
      }
      return { key: column, direction: "asc" };
    });
  }

  function sortIndicator(column) {
    if (sortConfig.key !== column) return "";
    return sortConfig.direction === "asc" ? " ▲" : " ▼";
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "40px 20px",
      }}
    >
      <h1 style={{ marginBottom: "10px" }}>Analysis Results</h1>

      <p style={{ marginBottom: "30px", opacity: 0.85 }}>
        <strong>Latest Report:</strong> {fileName}
      </p>

      <div style={{ width: "100%", maxWidth: "1200px" }}>
        <table style={{ width: "100%", cursor: "pointer" }}>
          <thead>
            <tr>
              <th onClick={() => requestSort("file_name")}>
                File{sortIndicator("file_name")}
              </th>
              <th onClick={() => requestSort("api")}>
                API{sortIndicator("api")}
              </th>
              <th onClick={() => requestSort("attack_type")}>
                Attack Type{sortIndicator("attack_type")}
              </th>
              <th onClick={() => requestSort("payload")}>
                Payload{sortIndicator("payload")}
              </th>
              <th onClick={() => requestSort("severity")}>
                Severity{sortIndicator("severity")}
              </th>
              <th onClick={() => requestSort("remediation")}>
                Remediation{sortIndicator("remediation")}
              </th>
              <th onClick={() => requestSort("code_lines")}>
                Code Lines{sortIndicator("code_lines")}
              </th>
            </tr>
          </thead>

          <tbody>
            {sortedRows.map((r, i) => (
              <tr key={i}>
                <td>{r.file_name}</td>
                <td>{r.api}</td>
                <td>{r.attack_type}</td>
                <td>{r.payload}</td>
                <td>{r.severity}</td>
                <td>{r.remediation}</td>
                <td>{r.code_lines}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
