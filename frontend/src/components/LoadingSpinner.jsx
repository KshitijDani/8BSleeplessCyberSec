export default function LoadingSpinner() {
  return (
    <div
      style={{
        border: "6px solid #eee",
        borderTop: "6px solid #3498db",
        borderRadius: "50%",
        width: "40px",
        height: "40px",
        animation: "spin 1s linear infinite",
        margin: "20px auto",
      }}
    ></div>
  );
}
