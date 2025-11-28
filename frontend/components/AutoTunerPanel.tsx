type Trial = {
  config: { users: number; spawn_rate: number }
  metrics: { rps: number; p95_latency: number }
  score: number
}

type Tuning = {
  baseline: Trial
  best_config: Trial
  improvement: { rps_gain: number; p95_drop: number; score_gain: number }
  trials: Trial[]
  error?: string
}

export default function AutoTunerPanel({ tuning }: { tuning: Tuning }) {

  if (!tuning) return null

  if (tuning.error) {
    return (
      <div className="card">
        <h3>Auto-Tuner</h3>
        <p className="error">{tuning.error}</p>
      </div>
    )
  }

  const best = tuning.best_config
  const base = tuning.baseline

  return (
    <div className="card">
      <h2>Intelligent Auto-Tuning Engine</h2>

      {/* BEST CONFIG */}
      <div className="grid">
        <div className="metric">
          <h4>Best Users</h4>
          <div>{best.config.users}</div>
        </div>
        <div className="metric">
          <h4>Best Spawn Rate</h4>
          <div>{best.config.spawn_rate}</div>
        </div>
        <div className="metric">
          <h4>Best Score</h4>
          <div>{best.score}</div>
        </div>
      </div>

      {/* IMPROVEMENT */}
      <h3>Improvement vs Baseline</h3>
      <ul>
        <li>RPS Gain: <b>{tuning.improvement.rps_gain}</b></li>
        <li>P95 Reduction: <b>{tuning.improvement.p95_drop} ms</b></li>
        <li>Score Gain: <b>{tuning.improvement.score_gain}</b></li>
      </ul>

      {/* TRIALS TABLE */}
      <h3>Explored Configurations</h3>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Users</th>
              <th>Spawn</th>
              <th>RPS</th>
              <th>P95</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {tuning.trials.map((t, i) => {
              const isBest =
                t.config.users === best.config.users &&
                t.config.spawn_rate === best.config.spawn_rate

              return (
                <tr key={i} className={isBest ? "bestRow" : ""}>
                  <td>{t.config.users}</td>
                  <td>{t.config.spawn_rate}</td>
                  <td>{t.metrics.rps}</td>
                  <td>{t.metrics.p95_latency}</td>
                  <td>{t.score}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* BASELINE vs BEST */}
      <h3>Baseline vs Best</h3>
      <div className="grid">
        <div className="metric">
          <h4>Baseline RPS</h4>
          <div>{base.metrics.rps}</div>
        </div>
        <div className="metric">
          <h4>Best RPS</h4>
          <div>{best.metrics.rps}</div>
        </div>
        <div className="metric">
          <h4>Baseline P95</h4>
          <div>{base.metrics.p95_latency} ms</div>
        </div>
        <div className="metric">
          <h4>Best P95</h4>
          <div>{best.metrics.p95_latency} ms</div>
        </div>
      </div>

    </div>
  )
}
