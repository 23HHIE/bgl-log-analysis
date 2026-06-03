# BGL Supercomputer Log Analysis

A scalable distributed log analysis system built on **Lambda Architecture**, processing 2.67 million log entries from the [BlueGene/L supercomputer](https://zenodo.org/record/3227177) at Lawrence Livermore National Labs.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Lambda Architecture                       │
│                                                                   │
│  BGL.log ──► Spark Batch ─────────────────────► Batch Results   │
│                                                        │         │
│  BGL.log ──► Kafka Producer ──► Kafka Topic           │         │
│                                      │                │         │
│                               Spark Structured        │         │
│                               Streaming               │         │
│                                      │                │         │
│                               FastAPI + WebSocket ◄───┘         │
│                                      │                          │
│                               React Dashboard                    │
│                          (real-time + batch results)            │
└─────────────────────────────────────────────────────────────────┘
```

### Components

| Layer | Technology | Role |
|-------|-----------|------|
| **Batch** | PySpark | Answers 5 analytical questions over full dataset |
| **Stream Ingest** | Kafka Producer | Simulates real-time log ingestion |
| **Stream Processing** | Spark Structured Streaming | Real-time event aggregation & alerting |
| **API** | FastAPI + WebSocket | Serves batch results (REST) + live events (WS) |
| **Frontend** | React | Real-time dashboard — live feed, charts, alerts |
| **Infrastructure** | Docker Compose | Single-command local deployment |

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url>
cd bgl-log-analysis

# 2. Place BGL.log in the data/ directory
cp /path/to/BGL.log data/

# 3. Start all services
docker-compose up --build

# 4. Open the dashboard
open http://localhost:3000

# 5. Run batch analysis
docker-compose exec spark-master spark-submit /app/spark_batch.py
```

## Analytical Questions Answered (Batch)

| # | Question |
|---|---------|
| Q2 | How many **fatal** log entries on **Tuesday or Thursday** resulted from a **machine check interrupt**? |
| Q7 | For each **week**, what is the average number of **DDR error** occurrences? |
| Q10 | What are the **top 3 most frequent days of the week** across all log entries? |
| Q14 | Which **node** generated the largest number of **KERNRTSP** events? |
| Q18 | When was the **earliest fatal kernel error** containing **"Lustre mount FAILED"**? |

## Real-Time Dashboard Features

- **Live Log Feed** — scrolling stream of incoming log events as Kafka consumes them
- **FATAL Alert Panel** — real-time highlight of critical events by severity
- **Events Per Minute** — live chart showing log ingestion rate over time
- **Node Activity** — which nodes are most active in the current stream window

## Project Structure

```
bgl-log-analysis/
├── batch/                    # PySpark batch jobs
│   ├── spark_batch.py        # Entry point — runs all 5 questions
│   ├── parser.py             # BGL log line parser (shared)
│   └── questions/            # One module per analytical question
│       ├── q2_fatal_machine_check.py
│       ├── q7_ddr_errors_weekly.py
│       ├── q10_top_days.py
│       ├── q14_kernrtsp_node.py
│       └── q18_lustre_fatal.py
├── streaming/
│   ├── producer/             # Kafka producer — replays BGL.log
│   └── consumer/             # Spark Structured Streaming consumer
├── api/                      # FastAPI backend
│   ├── routers/
│   │   ├── batch_results.py  # REST: GET /results
│   │   └── stream.py         # WebSocket: ws://localhost:8000/ws
│   └── models/schemas.py
├── frontend/                 # React dashboard
│   └── src/
│       ├── components/
│       │   ├── BatchResults.jsx
│       │   ├── LiveFeed.jsx
│       │   ├── AlertPanel.jsx
│       │   └── Charts/
│       └── services/         # API + WebSocket clients
├── data/                     # BGL.log goes here (gitignored)
├── output/                   # Batch results JSON (gitignored)
└── docker-compose.yml
```

## Tech Stack

- **PySpark 3.x** — distributed batch processing
- **Apache Kafka** — distributed message streaming
- **Spark Structured Streaming** — real-time stream processing
- **FastAPI** — async Python API with WebSocket support
- **React** — real-time frontend dashboard
- **Docker Compose** — local multi-container orchestration

## Dataset

BlueGene/L supercomputer logs from Lawrence Livermore National Labs.
- 2,679,601 log entries
- 372 MB uncompressed
- Source: [Zenodo](https://zenodo.org/record/3227177)
