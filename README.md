# 💰 Complete Finance Backend System

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![GraphQL](https://img.shields.io/badge/GraphQL-Graphene-E10098?logo=graphql&logoColor=white)

A robust, production-ready backend system designed for a personal finance tracking application. It is built utilizing **Clean Architecture** principles and provides strict **Role-Based Access Control (RBAC)**, advanced dynamic filtering, REST APIs, and a read-only GraphQL endpoint for complex analytical queries.

---

## ✨ Key Features

- **Clean Architectural Design:** Separation of concerns between API Controllers (`routes`) and Business Logic (`services`).
- **Data Isolation:** Hard-coded security guarantees that users can only ever access their personal data.
- **Strict RBAC:** 
  - `Viewer`: Read-only access to basic data.
  - `Analyst`: Access to highly aggregated Analytics and GraphQL querying.
  - `Admin`: Full CRUD access and internal User management capabilities.
- **Advanced Dynamic Search:** Search transactions dynamically with combined queries (Min/Max limits, String-like searching, Date bounding, etc.).
- **Live Analytics Math Engine:** Total balances, incomes, and expenses are not hardcoded. They are dynamically derived via SQLAlchemy aggregations natively to prevent desyncing.
- **REST + GraphQL Combo:** Implements standard REST for basic resource mutations and GraphQL strictly for analytical payloads.
- **Cloud-Agnostic Database:** Natively utilizes `SQLite` for rapid local iteration but fully supports zero-configuration switching to `PostgreSQL` via environmental variables.

---

## 🏗️ Folder Structure

```text
├── app/
│   ├── api/            # Dependency injection (Auth hooks & DB sessions)
│   ├── core/           # Security, Logging, and Exception Handlers
│   ├── db/             # SQLAlchemy engine setup
│   ├── models/         # Database Table classes
│   ├── routes/         # FastAPI endpoint controllers
│   ├── schemas/        # Pydantic data validation classes
│   └── services/       # Core business logic
├── scripts/            # Seed data scripts
├── requirements.txt    # Python dependencies
├── railway.toml        # Cloud deployment configuration
└── main.py             # Uvicorn initial boundary hook
```

---

## 🚀 Getting Started Locally

### 1. Clone the repository & Enter directory
```bash
git clone https://github.com/your-username/finance-backend-system.git
cd finance-backend-system
```

### 2. Create the Virtual Environment
```bash
python -m venv venv
# On Windows:
source venv/Scripts/activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Seed the Database
Populate the system with standard Users, Categories, and initial transaction logic.
```bash
python scripts/seed.py
```
*(Default seeded users available: `admin@example.com`, `analyst@example.com`, `viewer@example.com` - Password for all: `password123`)*

### 5. Start the Server
```bash
uvicorn app.main:app --reload
```
You can now access the interactive OpenAPI documentation by visiting: `http://localhost:8000/docs`.

---

## ☁️ Deployment (Railway)

This repository comes pre-configured with a `railway.toml` file to allow 1-click cloud zero-downtime deployment.

1. Connect your Github Repository to your Railway Dashboard.
2. Natively, it will utilize an ephemeral SQLite database for demoing.
3. **To secure production data:** Attach a PostgreSQL plugin in Railway, and define the resulting URL into a Variable named `DATABASE_URL`. The app will instantly transition its backend table configurations to Postgres automatically.

---

## 🔐 Environment Variables

Create a `.env` file in the root directory. If none exists, development fallback strings are utilized.

| Variable Name | Type | Default Fallback | Purpose |
| ------------- | ---- | ---------------- | ------- |
| `PROJECT_NAME` | string | "Finance Backend System" | Application UI header identity. |
| `DATABASE_URL` | string | `sqlite:///./finance.db` | The SQLAlchemy connection string. |
| `SECRET_KEY` | string | `supersecretkey` | Cryptographic JWT signing key. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | `30` | JWT Lifespan limit. |

---

*This project was created as a demonstration of API design patterns utilizing the FastAPI ecosystem.*
