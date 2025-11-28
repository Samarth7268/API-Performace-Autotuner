import { useState } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();

  const [url, setUrl] = useState("");
  const [users, setUsers] = useState(20);
  const [rate, setRate] = useState(5);
  const [time, setTime] = useState(10);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function runTest() {
    setError("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/benchmark", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
          url,
          users,
          spawn_rate: rate,
          runtime: time
        })
      });

      const data = await res.json();

      if (!data.report_id) {
        throw new Error("Benchmark failed");
      }

      router.push(`/report/${data.report_id}`);

    } catch (e:any) {
      setError(e.message || "Backend not reachable");
    }

    setLoading(false);
  }

  return (
    <div className="container">
      <h1>API Performance Autotuner</h1>

      <div className="card">
        <input placeholder="API URL" value={url} onChange={e => setUrl(e.target.value)}/>

        <div className="row">
          <input type="number" value={users} onChange={e=>setUsers(+e.target.value)} placeholder="Users"/>
          <input type="number" value={rate} onChange={e=>setRate(+e.target.value)} placeholder="Spawn Rate"/>
          <input type="number" value={time} onChange={e=>setTime(+e.target.value)} placeholder="Runtime"/>
        </div>

        <button disabled={loading} onClick={runTest}>
          {loading ? "Running..." : "Start Benchmark"}
        </button>

        {error && <p style={{color:"#fca5a5"}}>{error}</p>}
      </div>
    </div>
  );
}