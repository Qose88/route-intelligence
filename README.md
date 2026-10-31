# Route Intelligence

> QoSE & BGP Path Intelligence Platform for Destination Experience Analysis

**Route Intelligence** is an open-source network intelligence platform designed to investigate how network routing and path changes affect real-world application and destination performance.

The project combines **network measurements, traceroute/path intelligence, ASN information, BGP routing data, historical analysis, and QoSE metrics** to help answer:

> **When a customer experiences poor application performance, what is happening, where does the degradation begin, what network path is involved, what changed, and which path has historically performed better?**

---

## 🚧 Project Status

**Status:** Active Development

Route Intelligence is currently being developed incrementally following a 14-day engineering roadmap.

Current progress:

- [x] Project repository initialized
- [x] Python virtual environment
- [x] PostgreSQL database
- [x] SQLAlchemy foundation
- [x] Alembic migrations
- [x] Customer model
- [x] Probe model
- [x] Destination model
- [x] FastAPI skeleton
- [x] Health endpoint
- [x] Initial Git repository
- [ ] Measurement Engine
- [ ] Path Intelligence
- [ ] BGP Intelligence
- [ ] Historical Route Analysis
- [ ] QoSE Correlation Engine
- [ ] Multi-Probe Analysis
- [ ] Application Performance Analysis
- [ ] Routing Recommendation Engine
- [ ] Dashboard
- [ ] Alerting
- [ ] Production Deployment

---

# 🎯 Project Goals

Route Intelligence focuses on **destination experience and network path intelligence**, rather than traditional infrastructure monitoring.

The platform aims to correlate:

```text
Customer / Probe
       │
       ▼
   Measurement
       │
       ├── Latency
       ├── Packet Loss
       ├── Jitter
       ├── TCP/TLS
       ├── DNS
       ├── HTTP/HTTPS
       └── Throughput
       │
       ▼
   Network Path
       │
       ├── Traceroute
       ├── MTR
       ├── Hop Analysis
       └── ASN Path
       │
       ▼
   BGP Intelligence
       │
       ├── Prefix
       ├── Origin ASN
       ├── AS Path
       ├── Next Hop
       ├── Collector
       └── RPKI
       │
       ▼
 Historical Analysis
       │
       ▼
 QoSE Correlation
       │
       ▼
 Root Cause Analysis
       │
       ▼
 Routing Recommendation
```

The final system should provide **evidence-based routing recommendations**, not automatically modify production BGP configuration.

---

# 🧠 Core Concept

The project models three primary entities:

### Customer

The organization or service recipient experiencing network/application performance.

### Probe

A measurement point used to perform network tests.

A Probe may be:

- Customer NMS
- Linux server
- MikroTik
- Monitoring server
- Cloud instance
- Other supported measurement systems

A Probe is a **measurement point**, not the measurement software itself.

### Destination

A logical application, service, or network destination that customers care about.

Examples:

- AWS Sydney
- AWS Singapore
- Microsoft Teams
- SharePoint
- OneDrive
- Google Drive
- Zscaler
- Zoom
- Webex
- Enterprise SaaS
- `8.8.8.8`

A Destination should not be treated as a single static IP address.

A logical Destination may have multiple endpoints and IP addresses depending on location, DNS resolution, CDN behavior, or service architecture.

---

# 🏗️ Architecture

The initial architecture is intentionally simple.

```text
                    ┌─────────────────────┐
                    │      Customer       │
                    └──────────┬──────────┘
                               │
                               │ owns
                               ▼
                    ┌─────────────────────┐
                    │       Probe         │
                    │                     │
                    │ Linux / MikroTik /  │
                    │ NMS / Cloud / etc.  │
                    └──────────┬──────────┘
                               │
                               │ performs
                               ▼
                    ┌─────────────────────┐
                    │    Measurement      │
                    └──────────┬──────────┘
                               │
                               │ against
                               ▼
                    ┌─────────────────────┐
                    │    Destination      │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
          Network Path     Application       BGP
          Intelligence     Performance    Intelligence
```

The relationship between Probe and Destination is represented through **Measurements**, rather than storing a direct `destination_id` inside the Probe.

---

# 📊 Measurement Types

Route Intelligence will support multiple layers of measurement.

## Network Layer

Examples:

- ICMP Ping
- UDP
- Traceroute
- MTR

Metrics:

- Latency
- Packet loss
- Jitter
- Hop-by-hop path

## Transport Layer

Examples:

- TCP connectivity
- TCP latency
- TLS connectivity

These measurements help distinguish basic ICMP behavior from actual transport-layer performance.

## Application Layer

Examples:

- DNS
- HTTP
- HTTPS
- Application-specific checks

Application performance should not automatically be inferred from ICMP results.

## Throughput

Throughput measurements can be used to investigate bandwidth-related performance problems.

Speed-test results should not be treated as definitive proof of destination application performance.

---

# 🌐 Path Intelligence

The platform preserves both raw and normalized path information.

Example:

```text
Probe
  │
  ▼
Customer Edge
  │
  ▼
VELO
  │
  ▼
Transit / Peering
  │
  ▼
Upstream
  │
  ▼
Destination Network
```

Traceroute evidence should preserve the original hop-level information while also allowing normalization into an ASN path.

Example:

```text
Raw hops:

10.10.10.1
10.20.20.1
203.x.x.x
...

Normalized:

AS24207 → AS2914 → AS3356 → Destination ASN
```

The raw evidence remains important for troubleshooting and auditability.

---

# 🛰️ BGP Intelligence

Route Intelligence is designed to correlate observed network paths with routing information.

Potential BGP data sources include:

- RIPE RIS
- RIPEstat
- RouteViews
- Looking Glass services
- Other public routing data sources

The system may collect information such as:

```text
Prefix
Origin ASN
AS Path
Next Hop
Collector
Timestamp
RPKI Status
```

Multiple BGP vantage points should be considered whenever possible.

A single BGP collector should not automatically be treated as representing the complete Internet routing view.

---

# 📈 Historical Intelligence

Historical data is one of the core components of Route Intelligence.

The platform separates:

```text
Measurement History
Path History
BGP History
Experiment History
Recommendation History
```

This allows the system to answer questions such as:

> Was this path previously used?

> What was the latency when the previous path was active?

> Did the BGP path change before the QoSE degradation?

> Has another path historically performed better?

---

# 🔍 QoSE Correlation

The platform should correlate:

```text
BGP Change
      +
Path Change
      +
QoSE Change
```

However:

> **A BGP path change alone must never be treated as proof of root cause.**

Correlation should consider:

- Timing
- Sample size
- Number of affected probes
- Destination
- Latency distribution
- Packet loss
- Jitter
- Alternative explanations
- Single-customer vs multi-customer impact
- Other destinations using the same path

The objective is to produce an evidence-based confidence level rather than a premature conclusion.

---

# 🌍 Multi-Probe Analysis

Multiple probes can provide stronger evidence.

For example:

```text
Jakarta Probe ─────┐
                   │
Bandung Probe ─────┼──► Same ASN Path ──► Same Destination
                   │
Surabaya Probe ────┘
```

If several probes experience degradation around the same time and share relevant path characteristics, confidence in a network-path-related issue can increase.

However:

> A shared destination does not automatically mean that the underlying network problem is shared.

---

# ↔️ Inbound / Outbound Path

Route Intelligence also considers routing direction.

```text
Outbound:

Customer → ISP → Transit → Destination


Inbound:

Destination → Transit → ISP → Customer
```

The two directions may follow different paths.

Therefore, the platform should eventually support analysis of:

- Outbound path
- Inbound path
- Asymmetric routing
- Direction-specific performance

---

# 💡 Routing Recommendations

The final system may generate recommendations such as:

```text
Destination: AWS Sydney

Current Path:
AS24207 → AS2914 → AS3356 → AWS

Historical Alternative:
AS24207 → Peer → AWS

Observed Impact:
+72 ms latency
+2.1% packet loss

Historical Alternative:
Lower median latency
Lower packet loss
Stable across multiple probes

Recommendation:
Investigate alternative routing path.
```

Recommendations are **advisory only**.

Route Intelligence will **not automatically modify production BGP configuration**.

---

# 🗺️ Development Roadmap

## Day 1 — Foundation

- Repository
- Python environment
- PostgreSQL
- FastAPI
- SQLAlchemy
- Alembic
- Customer
- Probe
- Destination
- Git

## Day 2 — Measurement Engine

- Ping
- MTR
- Traceroute
- TCP
- DNS
- HTTPS
- Measurement storage
- Raw measurement output

## Day 3 — Path Intelligence

- Hop parsing
- ASN mapping
- Path normalization
- Path history

## Day 4 — BGP Intelligence

- RIPE RIS
- RIPEstat
- BGP prefix information
- Origin ASN
- AS Path
- RPKI

## Day 5 — Historical Route Analysis

- BGP history
- Path changes
- Route-change detection
- Before/after comparison

## Day 6 — QoSE Correlation

- Latency changes
- Loss changes
- Jitter changes
- BGP/path correlation
- Confidence scoring

## Day 7 — Multi-Probe Analysis

- Shared path detection
- Shared degradation
- Probe comparison
- Geographic comparison

## Day 8 — Application & Throughput

- DNS
- HTTP/HTTPS
- TCP/TLS
- Application performance
- Throughput measurements

## Day 9 — Recommendation Engine

- Historical path comparison
- Alternative path identification
- Performance comparison
- Advisory recommendation

## Day 10 — API

- REST API
- Query endpoints
- Historical analysis endpoints
- Recommendation endpoints

## Day 11 — Dashboard

- Destination view
- Probe view
- Path visualization
- BGP changes
- QoSE trends

## Day 12 — Alerting

- Path change alerts
- QoSE degradation
- BGP anomalies
- Correlation alerts

## Day 13 — Testing

- Unit tests
- Integration tests
- Measurement validation
- BGP data validation
- Failure scenarios

## Day 14 — Deployment

- Production configuration
- Service management
- Logging
- Monitoring
- Security hardening
- Documentation

---

# 🛠️ Technology Stack

Current stack:

| Component | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migration | Alembic |
| Server | Uvicorn |
| Configuration | Pydantic Settings |
| Version Control | Git |
| BGP Data | RIPE RIS / RIPEstat / other sources |
| Network Measurements | ICMP / TCP / UDP / MTR / Traceroute |

The technology stack may evolve as the project develops.

---

# 📁 Project Structure

Current structure:

```text
route-intelligence/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── destination.py
│   │   └── probe.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── tests/
│
├── .gitignore
├── alembic.ini
└── README.md
```

The architecture will evolve as additional modules are introduced.

---

# 🚀 Getting Started

## Requirements

Recommended environment:

- Python 3.13+
- PostgreSQL 17+
- Git
- Linux environment recommended for network measurement components

## Clone

```bash
git clone https://github.com/Qose88/route-intelligence.git
cd route-intelligence
```

## Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

> `requirements.txt` will be maintained as the dependency set is finalized.

## Configuration

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://route_app:YOUR_PASSWORD@localhost:5432/route_intelligence
```

**Never commit `.env` to Git.**

## Run migrations

```bash
alembic upgrade head
```

## Start API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok"
}
```

---

# 🔐 Security Principles

Route Intelligence follows several basic security principles:

- Credentials must not be committed to Git.
- `.env` is excluded from version control.
- Database access uses a dedicated application role.
- Least-privilege database permissions are preferred.
- Raw network evidence should be preserved without exposing sensitive customer information.
- Production routing changes are never performed automatically.
- Secrets should be managed outside application source code.

---

# 🧪 Engineering Principles

The project follows these principles:

### Evidence before conclusion

Network observations should be collected before declaring a root cause.

### Preserve raw evidence

Raw traceroute, MTR, measurement, and BGP evidence should remain available for investigation.

### Correlation ≠ causation

A routing change does not automatically mean the routing change caused the degradation.

### Shortest path ≠ best path

The shortest AS path is not necessarily the best-performing path.

### Lower latency ≠ always better

Latency must be considered together with loss, jitter, application behavior, and historical stability.

### ICMP loss ≠ application loss

ICMP behavior may differ from TCP or application-layer behavior.

### Traceroute timeout ≠ packet loss

A timeout at one hop does not automatically indicate end-to-end packet loss.

### Automation with guardrails

Recommendations may be automated, but production routing changes require human control.

---

# 🤝 Contributing

Contributions, ideas, experiments, and network-engineering discussions are welcome.

Before implementing major features, please consider:

1. What problem does this solve?
2. What network evidence does it use?
3. How does it affect the architecture?
4. What assumptions are being made?
5. Can the result be validated?
6. Does the implementation preserve raw evidence?

---

# 📜 License

License: **TBD**

The project is currently under active development and the final license has not yet been selected.

---

# 👥 Project Team

Route Intelligence is developed collaboratively by network engineering and software engineering contributors.

## Core Contributors

| Contributor | GitHub | Focus |
|---|---|---|
| **Adi Saputra** | [adisaputra-prog](https://github.com/adisaputra-prog) | Network Engineering, QoSE, Routing & BGP |

## Contribution Areas

Contributors may participate in areas including:

- 🌐 Network Engineering
- 📡 QoSE & Destination Experience
- 🛰️ BGP & Routing Intelligence
- 🔬 Network Measurement
- 🐍 Python Development
- 🗄️ Database & Backend
- 📊 Data Analysis
- 🖥️ Dashboard & Visualization
- 🧪 Testing & Validation
- 📚 Documentation

> Contributors can be added as the project grows.
---

> **Route Intelligence is built to turn network measurements and routing data into actionable network intelligence.**
