# 🚀 API Performance AutoTuner
Intelligent API Load Testing, Profiling & Self-Optimizing Engine using Bandits + AI

## 📌 Overview
API Performance AutoTuner is an intelligent system that benchmarks an API, analyzes performance bottlenecks, applies automated tuning strategies using a bandit-based learning algorithm, and provides AI-powered optimization insights — all through a real-time web dashboard.

The system continuously tests different concurrency configurations (users, spawn rates) and automatically learns the best-performing setup using reinforcement-style optimization.

---

## 🎯 Key Features

### ✅ Load Testing Engine
Uses Locust to generate traffic and measure:
- Latency percentiles (P95, P99)
- Requests/sec (RPS)
- Throughput
- Error rate

### ✅ CPU Profiling & Flamegraph
- Captures runtime behavior with py-spy
- Generates flamegraph visualizations
- Detects top CPU hotspots automatically

### ✅ Intelligent Auto-Tuning (Bandit Algorithm)
Uses multi-armed bandit strategy to:
- Try multiple concurrency configs
- Score each configuration
- Learn optimal values automatically

Returns:
- Best configuration
- Baseline comparison
- Performance improvements
- Full tuning history

### ✅ AI Optimization Advisor (Ollama)
- Local LLM agent analyzes metric patterns
- Returns optimization suggestions
- No API keys or cloud dependency

### ✅ Real-time Frontend Dashboard (Next.js)
- Visual metrics
- AI advice
- Optimization results
- Flamegraph rendering
- Tuning history

---

## 🖥 Tech Stack

### Backend
- FastAPI
- Locust
- py-spy
- Bandit learning logic
- Python multiprocessing
- Ollama (Local LLM agent)

### Frontend
- Next.js (TypeScript)
- CSS dashboard
- Charts & grids
- Real-time report fetch

### AI
- Ollama (local inference)
- Prompt-controlled recommendation engine



