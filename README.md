# 🏗️ Smart Construction Planning & Budget Estimation System

A full-stack platform that helps users plan a residential construction project and get an early, data-backed estimate of required materials, cost, duration, risks — plus a site-supervision workflow for tracking the actual build.

The system combines **deterministic engineering calculations**, **rule-based risk logic**, and **trained machine learning models** to produce preliminary construction plans, budgets, and predictions — and is explicit about which parts are which, rather than labeling everything "AI."

---

## ✨ What it does

| Area | Capability |
|---|---|
| **Project Setup** | Capture land area, built-up area, floors, basement, parking for a residential project |
| **Quantity Estimation** | Engineering formulas calculate cement, steel, sand, aggregate, and brick requirements |
| **Cost Estimation** | Four calibrated pricing tiers (Economy / Standard / Premium / Luxury) based on real Indian construction rates, cross-validated against real Chennai resale market data |
| **ML Cost & Duration Prediction** | A trained Random Forest model predicts total cost and construction duration, validated to track closely (within ~2%) with the engineering-based estimate |
| **Risk & Safety Checks** | Rule-based flags for basement waterproofing, multi-floor life-safety review, structural design requirements, and more |
| **Construction Supervision** | A 5-stage build tracker (Layout → Foundation → Superstructure → Finishes → Closing) with inspection checklists, pass/fail/N/A status, and photo upload per checklist item, with auto-complete logic when a stage's checklist is cleared |
| **Concrete Mix Advisor** | A second, independent ML model (trained on the UCI Concrete Compressive Strength dataset) predicts 28-day compressive strength and nearest IS concrete grade from a proposed mix design |
| **Visual Dashboards** | Cost breakdown pie charts and category comparison bar charts per project |

---

## 🧱 Tech Stack

**Backend**
- Python, FastAPI, SQLAlchemy, SQLite
- scikit-learn (Linear Regression, Random Forest), pandas, joblib

**Frontend**
- React (Vite), React Router, Tailwind CSS, Axios, Recharts

**Environment**
- Built and tested on macOS (Apple Silicon)

---

## 🏛️ Architecture

```
React Frontend (Vite, multi-page)
        │  Axios HTTP calls
        ▼
FastAPI Backend
        │
        ├── Engineering Engine (quantities, cost formulas — deterministic)
        ├── Risk Engine (rule-based checks)
        ├── Supervision Engine (stage state machine + inspections)
        ├── ML Models (.joblib) — cost/duration prediction, concrete strength
        │
        ▼
SQLite Database (projects, stages, inspections, photos)
```

The project deliberately separates **what is calculated** (engineering formulas — reliable, explainable) from **what is predicted** (ML models — trained and evaluated, used where patterns in data add value beyond a fixed formula). This distinction is treated as a feature, not a limitation.

---

## 📊 Machine Learning

Two independent, separately trained models:

### 1. Cost & Duration Prediction
- Trained on a synthetic dataset (4,000 records) generated to mirror the system's own category-based pricing logic, with randomized noise to simulate real-world variation
- Compared Linear Regression vs. Random Forest; Random Forest selected for both targets
- **Cost model: R² = 0.973** · **Duration model: R² = 0.967**
- Predictions are category-aware (tied to the Economy/Standard/Premium/Luxury tier selected)
- Cross-validated against real Chennai property price data (1,592 listings): construction-cost estimates land at ~30–35% of median resale price per sq.ft — consistent with typical construction-cost-to-total-price ratios in Indian metro real estate

### 2. Concrete Mix Strength Prediction
- Trained on the UCI Concrete Compressive Strength dataset
- Random Forest model predicts 28-day compressive strength (MPa) from mix composition (cement, slag, fly ash, water, superplasticizer, aggregates, age)
- Classifies the result to the nearest standard IS concrete grade (M10–M60)

> **Note on data:** The cost/duration model is trained on synthetic data by design, since real historical project-cost data was not available at build time. The training pipeline (`notebooks/generate_data.py` + `notebooks/train_model.py`) is structured so real project data can directly replace the synthetic dataset and be retrained with no code changes.

---

## 🗂️ Project Structure

```
smart-construction/
├── backend/
│   ├── app/
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── engine/       # Engineering + risk + cost calculation logic
│   │   ├── ml/           # Trained model files (.joblib)
│   │   ├── routes/       # API endpoints
│   │   ├── uploads/      # Inspection photo storage
│   │   └── main.py
│   └── notebooks/        # Data generation + model training scripts
└── frontend/
    └── src/
        ├── pages/        # ProjectListPage, ProjectDetailPage, ConcreteAdvisorPage
        ├── components/   # Shared UI (GlassCard, etc.)
        └── api.js
```

---

## 🚀 Getting Started

### Backend

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # or install individually — see below
uvicorn app.main:app --reload
```

Core backend dependencies: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pandas`, `scikit-learn`, `joblib`, `python-multipart`

API docs available at: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at: `http://localhost:5173`

### Regenerating ML models

```bash
cd backend
python notebooks/generate_data.py
python notebooks/train_model.py
```

---

## 🔌 API Overview

| Endpoint | Description |
|---|---|
| `POST /projects/` | Create a project |
| `GET /projects/` | List all projects |
| `GET /projects/{id}/quantities` | Engineering material quantity estimate |
| `GET /projects/{id}/cost?category=` | Cost estimate for a pricing tier |
| `GET /projects/{id}/predict?category=` | ML-predicted cost & duration |
| `GET /projects/{id}/risks` | Rule-based risk/safety check |
| `GET /projects/{id}/stages` | Construction stage tracker (auto-initializes on first call) |
| `PATCH /projects/{id}/stages/{stage_id}/start` | Activate a stage, populate its checklist |
| `PATCH /projects/inspections/{id}` | Update an inspection item's status |
| `POST /projects/inspections/{id}/photos` | Upload a photo for an inspection item |
| `POST /concrete/predict-strength` | Predict concrete compressive strength from a mix design |

Full interactive documentation at `/docs` (Swagger UI).

---

## 📐 Scope & Design Decisions

This project deliberately scopes itself around what a **residential builder / site supervisor** owns — structural inspection, cost/quantity planning, and risk flagging. The following are intentionally **out of scope**, as they are owned by separate specialized teams in real practice:

- Electrical, plumbing, and other MEP trades
- Automatic floor-plan reading / computer-vision parsing of architectural drawings (a genuinely hard, unsolved research problem — not attempted)
- Full RFI / shop-drawing / snag-list / handover workflows (documented as future scope — the stage/inspection pattern built here is directly extensible to these)

---

## 🔭 Future Scope

- Finishes supervision, RFIs, shop drawing register, material approval log, snag list, and handover tracking (extending the same stage/inspection pattern used in Construction Supervision)
- Budget & time optimization advisor (material swap suggestions with recalculated cost deltas)
- Material trade-off explorer (structured comparison of brick/sand/cement/steel options)
- Climate- and location-based plan-type recommendations
- Retraining the cost/duration model on real historical project data as it becomes available

---

## 📄 License

This project was built as an academic/portfolio project. Feel free to fork and adapt.
