export default function FlameGraphViewer({ filename }: { filename: string }) {
  if (!filename) return <p>No flamegraph generated.</p>;

  const file = filename.split("\\").pop();

  return (
    <iframe
      src={`http://127.0.0.1:8000/api/flamegraph/${file}`}
      width="100%"
      height="420"
      style={{ border: "1px solid #1f2937", borderRadius: "12px" }}
    />
  );
}
