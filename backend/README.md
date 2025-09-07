# Mini E-commerce Backend (Flask + SQLAlchemy)

This is the backend for the mini e-commerce system with:

- Hierarchical category tree (dynamic depth)  
- List products for a category **including** all its subcategories (recursive)  
- Shopping cart with per-user carts (defaults to `"guest"`)  
- Related products (graph-like associations)  
- Proper layering: **controllers → services → repositories → models**  

> Frontend is present in `frontend/` folder. This backend is under `backend/` folder.

---

## Tech

- Python 3.10+
- Flask 3
- SQLAlchemy ORM
- SQLite (default)
- Marshmallow (available; DTOs are simple dicts for clarity)

---

## Quick Start

```bash
# 1) Clone and cd
cd backend

# 2) (Recommended) Install Python 3.10
#    Options for different OS are below.

# 3) Create and activate a virtualenv
python3.10 -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 4) Install deps
pip install -r requirements.txt

# 5) Seed the database with sample data
python seed.py

# 6) Run
python app.py
# Server: http://127.0.0.1:5000
