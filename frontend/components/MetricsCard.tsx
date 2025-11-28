export default function MetricsCard({ title, value }: any) {
  return (
    <div className="metric">
      <h4>{title}</h4>
      <strong>{value}</strong>
    </div>
  );
}
