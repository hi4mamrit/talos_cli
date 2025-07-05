# 🧠 Talos: YAML-First LLM DAG Orchestrator

Talos is a lightweight, DAG-based orchestration framework for running LLM agent workflows, inspired by Airflow — but built for LLM-native automation using YAML files and minimal infra overhead.

---

## 🚀 Features

- ✅ YAML-based DAG definition (`config/test.yaml`)
- ✅ Agent abstraction layer for tasks like summarization, extraction, etc.
- ✅ Pluggable architecture: add custom agents via `orchestrator/agents`
- ✅ CLI interface to run DAGs like Docker/K8s:
  ```bash
  uv run main.py --file config/test.yaml
  ```
- ✅ Dependency-respecting step execution

---

## 📦 Project Structure

```
LLM_ORCHESTRATOR/
├── config/                 # DAG & agent configuration
│   ├── test.yaml          # Sample DAG definition
│   └── agents.yaml        # Registered agents and config
├── data/                  # Inputs for agents (emails, etc.)
│   └── email_client/      # Email processing logic
│       ├── fetcher.py
│       └── task_extractor.py
├── orchestrator/          # Core DAG runner
│   ├── dag_executor.py    # DAG parsing & step execution
│   └── agents/            # Custom agents live here
│       ├── helloWorld.py
│       └── summarizer.py
├── utils/                 # Utility functions (TBD)
├── main.py                # CLI Entrypoint
├── pyproject.toml         # Project metadata
├── .lock                  # uv lock file for dependencies
├── Dockerfile             # uv-based container build
└── docker-compose.yaml    # Easy container execution
```

---

## 🛠️ Running the Project

### 1. 🐳 Using Docker

```bash
docker-compose build
docker-compose up
```

### 2. 🧪 Local Dev

```bash
uv pip install --system -r .lock
uv run main.py --file config/test.yaml
```

---

## ✍️ Authoring a DAG

Create a YAML file under `config/`:

```yaml
name: test_sample_dag
steps:
  - id: test_step
    agent: helloWorld
    depends_on: []
```

You can register agents in `config/agents.yaml`.

---

## 🧩 Agents

Each agent must implement a `run()` method and register under `config/agents.yaml`. Sample agents:

- `helloWorld`: Basic test agent
- `summarizer`: Summarizes input from emails or text
- `fetcher`, `task_extractor`: Email-oriented pipeline

---

## 🧱 TODOs / Roadmap

- [ ] Add agent registry class
- [ ] Add error handling, retries
- [ ] Parallel execution (where `depends_on` permits)
- [ ] Scheduling (cron-style)
- [ ] Logs and visual DAG UI

---

## 🧑‍💻 Maintainer

Built by Abhijnan Acharya, inspired by frustration with tangled LLM prompt chains and LangChain fatigue.

---

## 📄 License

MIT License.
