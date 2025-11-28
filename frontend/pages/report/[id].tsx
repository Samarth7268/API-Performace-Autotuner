import { useRouter } from "next/router"
import { useEffect, useState } from "react"

import MetricsCard from "../../components/MetricsCard"
import FlameGraphViewer from "../../components/FlameGraphViewer"
import AutoTunerPanel from "../../components/AutoTunerPanel"

export default function ReportPage() {
  const { query } = useRouter()
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!query.id) return

    fetch(`http://127.0.0.1:8000/api/report/${query.id}`)
      .then(res => res.json())
      .then(json => {
        if (!json.report) {
          setError("Report not found")
          return
        }
        setData(json.report)
      })
      .catch(() => setError("Backend unreachable"))
      .finally(() => setLoading(false))
  }, [query.id])

  if (loading) return <div className="container">Loading report…</div>
  if (error) return <div className="container error">{error}</div>
  if (!data) return <div className="container">No data found.</div>

  const m = data.load_metrics
  const status = data.health_status

  const color =
    status === "HEALTHY" ? "ok" :
    status === "WARNING" ? "warn" :
    "bad"

  return (
    <div className="container">

      {/* HEADER */}
      <div className="header">
        <h1>Performance Report</h1>
        <span className={`badge ${color}`}>{status}</span>
      </div>

      <p className="subtitle">{data.summary}</p>

      {/* METRICS */}
      <div className="grid">
        <MetricsCard title="Median Latency" value={`${m.median_latency} ms`} />
        <MetricsCard title="P95 Latency" value={`${m.p95_latency} ms`} />
        <MetricsCard title="P99 Latency" value={`${m.p99_latency} ms`} />
        <MetricsCard title="RPS" value={m.rps} />
        <MetricsCard title="Error Rate" value={`${(m.error_rate * 100).toFixed(2)}%`} />
        <MetricsCard title="Throughput" value={m.throughput} />
      </div>

      {/* FLAMEGRAPH */}
      <h3>CPU Flamegraph</h3>
      <FlameGraphViewer filename={data.profile_metrics?.flamegraph_path} />

      {/* AI ADVISOR */}
      <h3>AI Advisor</h3>
      <ul className="advice">
        {(data.ai_advice || []).map((a: string, i: number) => (
          <li key={i}>{a}</li>
        ))}
      </ul>

      {/* AUTO TUNER */}
      <AutoTunerPanel tuning={data.auto_tuning} />

    </div>
  )
}
