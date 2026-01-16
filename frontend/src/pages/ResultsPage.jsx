import { useEffect, useState, useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function ResultsPage() {
  const [rows, setRows] = useState([]);
  const [fileName, setFileName] = useState("");
  const [chartData, setChartData] = useState([]);

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
      // Fetch formatted data for the chart
      const chartRes = await fetch("http://127.0.0.1:8000/api/formatted-vulnerabilities");
      const chartData = await chartRes.json();

      // Fetch detailed data for the table
      const tableRes = await fetch("http://127.0.0.1:8000/api/latest-vulnerabilities");
      const tableData = await tableRes.json();

      setRows(tableData.results || []);
      setFileName(tableData.file || "Unknown");

      // Process data for chart: count bugs per file
      if (chartData.results) {
        const bugCountMap = {};
        chartData.results.forEach((item) => {
          const fileName = item["file name"] || "Unknown";
          bugCountMap[fileName] = (bugCountMap[fileName] || 0) + 1;
        });

        // Convert to chart data format
        const chartDataArray = Object.entries(bugCountMap).map(
          ([fileName, count]) => ({
            name: fileName.split("/").pop() || fileName, // Show only filename, not full path
            bugs: count,
          })
        );

        setChartData(chartDataArray);
      }
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

      {/* Bar Chart Section */}
      <div style={{ width: "100%", maxWidth: "1200px", marginBottom: "40px" }}>
        <h2 style={{ marginBottom: "20px" }}>Bugs per File</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="name"
              angle={-45}
              textAnchor="end"
              height={100}
            />
            <YAxis label={{ value: "Number of Bugs", angle: -90, position: "insideLeft" }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="bugs" fill="#8884d8" name="Bug Count" />
          </BarChart>
        </ResponsiveContainer>
      </div>

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
