# Sonali.API – FastAPI Web API (Clean Architecture)

## 📌 Overview

**Sonali.API (Python)** is a **FastAPI Web API** project following **Clean Architecture** principles.  
It separates concerns into distinct layers for **maintainability, scalability, and testability**.

- **Domain Layer** – Core business entities, Pydantic schemas, interfaces, and validation.
- **DomainService Layer** – Handles data retrieval with **raw SQL / SQLAlchemy Core** for optimized read operations (CQRS pattern).
- **Infrastructure.DAL Layer** – Manages data persistence (Insert/Update/Delete) using **SQLAlchemy ORM**.
- **Utilities Layer** – Provides reusable helpers, JWT handling, and extensions.
- **API Layer** – Entry point with FastAPI routes, dependencies, middlewares, and services.

This architecture ensures separation of concerns, CQRS pattern adoption, and flexible data access strategies.

---

## 🏗️ Project Structure

```
Sonali.API/
│── app/
│   ├── main.py                → FastAPI entry point
│   ├── routes/                → API endpoints
│   ├── controllers/           → Thin controllers handling requests
│   ├── middlewares/           → Custom middlewares
│   ├── services/              → Application services
│   ├── dependencies.py        → Dependency injection
│   └── config.py              → App configuration (DB, JWT, etc.)

Sonali.API/domain/
│── entities/                  → Business entities (SQLAlchemy models or Pydantic schemas)
│── schemas/                   → Pydantic DTOs
│── interfaces/                → Service/repository interfaces
│── validators/                → Validation logic

Sonali.API/domain_service/
│── base/                      → Base query services
│── repositories/              → Raw SQL / optimized read queries
│── interfaces/                → Query contracts

Sonali.API/infrastructure/dal/
│── base/                      → Base repository classes
│── repositories/              → ORM repositories for writes

Sonali.API/utilities/
│── helpers/                   → Utility/helper functions
│── jwt_utils.py               → JWT token generation/validation
│── extensions.py              → Common extensions/utilities
```

---

## ⚙️ Technology Stack

- **Python 3.11+**
- **FastAPI** – Web framework
- **SQLAlchemy** – ORM for persistence
- **Pydantic** – Data validation & DTOs
- **Alembic** – Database migrations
- **JWT** – Authentication
- **Clean Architecture + CQRS pattern**

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

- Python 3.11+
- PostgreSQL / MySQL / SQLite
- VS Code / PyCharm / Any IDE
- Optional: Poetry or pipenv for dependency management

### 2️⃣ Setup & Run

```bash
# Clone repository
git clone <your-repo-url>
cd Sonali.API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Run API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:  
👉 `http://localhost:8000/docs` (Swagger UI)

---

## 🔑 Authentication

**Uses JWT (JSON Web Tokens).**

- Configure `config.py` with secret key and JWT settings.
- Pass JWT token via `Authorization: Bearer <token>` header.

---

## 📂 CQRS Implementation

- **Queries (Reads)** → DomainService Layer (raw SQL / SQLAlchemy Core for performance)
- **Commands (Writes)** → Infrastructure.DAL Layer (SQLAlchemy ORM for Insert/Update/Delete)

Optimizes reads and maintains clean separation for writes.

---

## 🛠️ Utilities

- **Helper Functions** – Common functions (dates, calculations, formatting)
- **JWT Utilities** – Token generation, decoding, and validation
- **Extensions** – Custom exceptions, pagination, response wrappers

---

## ✅ Advantages

- Clear separation of concerns
- CQRS support (Read/Write segregation)
- Easy to extend and maintain
- Testable and modular

---

## 📝 Example API Usage

### 1️⃣ Login

**POST** `/api/auth/login`

Request:

```json
{
  "username": "admin",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer",
  "expires": "2025-08-18T18:00:00Z"
}
```

Use token in subsequent requests:  
```
Authorization: Bearer <jwt-token>
```

---

### 2️⃣ CRUD Sample (Voucher)

#### Create Voucher

**POST** `/api/vouchers`

```json
{
  "voucher_no": "V123",
  "user_id": 1,
  "amount": 500.0,
  "date": "2025-08-18"
}
```

#### Read Vouchers

**GET** `/api/vouchers?user_id=1&voucher_no=V123`

#### Update Voucher

**PUT** `/api/vouchers/1`

```json
{
  "amount": 600.0
}
```

#### Delete Voucher

**DELETE** `/api/vouchers/1`

---

## 🧪 Testing

- **Unit Tests:** Use `pytest` for services and repositories
- **Integration Tests:** Use `httpx` or `TestClient` for API endpoints

### Example: Unit Test for Repository

```python
import pytest
from app.repositories.voucher_repository import VoucherRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.entities.voucher import Voucher

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_voucher(db_session):
    repo = VoucherRepository(db_session)
    voucher = Voucher(voucher_no="V001", user_id=1, amount=100)
    repo.add(voucher)
    db_session.commit()
    assert db_session.query(Voucher).count() == 1
```

---

## 📌 Future Improvements

- Implement **Unit of Work** for SQLAlchemy ORM
- Add **CQRS with separate handlers**
- Containerize with **Docker & Kubernetes**
- Add **async queries** for performance
- Implement **API versioning**

---

✅ This README provides a complete guide for **Python FastAPI developers**, onboarding, project structure, and testing.