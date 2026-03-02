# 🍝 Scalable Multi-Branch Restaurant ERP Platform

A production-oriented, multi-branch restaurant ERP and ordering platform built with:

- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **Redis**
- **Celery**
- **React**
- **Docker**

This project focuses on **scalability, ERP modeling, concurrency safety, and production-level architecture** rather than simple CRUD APIs.

---

# 🚀 Project Vision

The goal was to design a system similar to a real-world restaurant chain that supports:

- Multiple branches
- Branch-specific inventory
- Automatic stock deduction
- Async order processing
- Caching
- Horizontal scalability
- Containerized deployment

This system is built with **enterprise-level engineering principles** in mind.

---

# 🏗 Architecture Overview
```bash
Client (React Frontend)
            ↓
Django REST API (DRF + JWT)
            ↓
PostgreSQL Database
            ↓
Redis (Caching + Celery Broker)
            ↓
Celery Workers (Async Tasks)
```


---

# 🏢 Multi-Branch System

Each branch maintains:

- Its own inventory
- Its own orders
- Its own staff
- Its own low-stock thresholds

This design enables:

- Horizontal scaling
- Data isolation per branch
- Future sharding strategy
- Real-world ERP expansion capability

---

# 📦 Core Features

## 1️⃣ Menu & Ordering

- Public menu API
- Authenticated order placement (JWT)
- Order price snapshotting
- Atomic transactions for stock deduction
- Concurrency-safe logic using `select_for_update()`

Example:

```python
@transaction.atomic
def place_order(...):
    menu_item = MenuItem.objects.select_for_update().get(id=menu_item_id)
```
## 2️⃣ Inventory & ERP Logic

* Ingredient management
* Branch-level inventory tracking
* Automatic stock deduction per order
* Low stock threshold detection
* Supplier and purchase order modeling
* Stock is tracked per branch:
```bash
Branch → Ingredient → Stock Quantity
```
This mirrors real ERP-style inventory control.

---

## 3️⃣ Scalability Features
### 🔹 Redis Caching

* Menu endpoints cached
* Reduces database load
* Improves response latency
* Cache invalidation strategy:
* Clear cache when menu items update
* TTL-based fallback expiration


### 🔹 Asynchronous Processing (Celery + Redis)

* Used for:
* Order confirmation emails
* Low stock alerts
* Analytics updates
* Why async?
* Reduces API response time
* Offloads heavy tasks from request cycle
* Improves user experience


### 🔹 Database Optimization

* Indexes added on:
* user_id
* order_id
* created_at
* branch_id
* Optimizations used:
* .select_related()
* .prefetch_related()
* Query analysis with EXPLAIN

### 🔹 Concurrency Handling

Handled using:

* transaction.atomic
* select_for_update
* Row-level locking

Prevents race conditions and overselling inventory.

---
# 🔐 Authentication & API Design

JWT Authentication

Role-based permissions

Versioned APIs (/api/v1/)

Rate limiting enabled

Example:
```bash
POST /api/v1/orders/place/
Authorization: Bearer <access_token>
```

---

# 🐳 Dockerized Setup

Includes:

* Django container
* PostgreSQL container
* Redis container
* Celery worker container

Run everything with:
```bash
docker-compose up --build
```
---
# 🗂 Project Structure
```bash
restaurant-erp/
│
├── core/                 # Django project settings
│     ├── settings.py
│     ├── urls.py
│     ├── celery.py 
│     ├── ... 
├── menu/                 # Menu & ingredients
│     ├── tasks.py        # Celery Task for Ingredient stock low
│     ├── ...             # Rest same as Order's
├── orders/               # Orders & business logic
│     ├── migrations/...
│     ├── admin.py
│     ├── apps.py 
│     ├── models/
│     ├── serializers.py
│     ├── services.py 
│     ├── tests/
│     ├── urls.py
│     ├── views.py 
├── restaurants/...         # Branch & inventory
├── users/...               # Authentication
│
├── frontend/...            # React application
│
├── manage.py
├── .env
├── docker-compose.yml
├── Dockerfile
└── requirements.txt 
```

---
# ⚙️ Tech Stack

* Python 3.11+
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* React
* Docker
---

# 📊 Production-Level Considerations

This project demonstrates:

* Clean separation of business logic (services.py)
* ERP-style database modeling
* Horizontal scalability readiness
* Async task architecture
* Secure API layer
* Containerized deployment
---

# 🔧 Running Locally (Without Docker)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

celery -A config worker --loglevel=info

Ensure PostgreSQL and Redis are running.
```
---
# 🧩 Future Improvements

* Kubernetes deployment
* CI/CD pipeline
* Real-time stock updates via WebSockets
* Payment gateway integration
* Observability stack (Prometheus + Grafana)

---

# 🎯 What This Project Demonstrates

This is not just a restaurant ordering system.

It demonstrates:

* ERP modeling principles
* Concurrency-safe backend design
* Distributed system thinking
* Async architecture
* Production-oriented engineering

---
## 👨‍💻 Author

Built as a production-minded backend architecture project to explore scalable system design using Django and modern infrastructure tools.
