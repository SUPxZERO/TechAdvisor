# Technical Documentation

Complete technical documentation for the TechAdvisor Expert System.

---

## Contents

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture, component diagrams, and workflow analysis |
| [API_REFERENCE.md](API_REFERENCE.md) | Complete API endpoint documentation |
| [EXPERT_SYSTEM_GUIDE.md](EXPERT_SYSTEM_GUIDE.md) | Inference engine, rules, and scoring algorithms |
| [COMPARISON_SYSTEM.md](COMPARISON_SYSTEM.md) | How specifications work and product comparison logic |
| [DATABASE.md](DATABASE.md) | Database schema, ERD, and query reference |
| [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md) | Environment setup and development workflow |


---

## Quick Links

### For Developers
- [Development Setup](DEVELOPMENT_SETUP.md) - Start here
- [API Reference](API_REFERENCE.md) - Endpoint documentation
- [Database Schema](DATABASE.md) - Data model reference

### For System Understanding
- [Architecture Overview](ARCHITECTURE.md) - Full system analysis
- [Expert System Guide](EXPERT_SYSTEM_GUIDE.md) - Inference engine details

---

## Project Overview

**TechAdvisor** is a rule-based expert system that helps users find smartphones and laptops based on their preferences. Built with:

- **Backend**: Flask 2.3.3, Python 3.12
- **Database**: MySQL 8.0 with SQLAlchemy ORM
- **Frontend**: Jinja2 templates, Tailwind CSS
- **Expert System**: Forward-chaining inference engine

---

## Getting Started

```bash
# Quick start
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_rbac.py
python seed_database.py
python run.py
```

See [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md) for detailed instructions.

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                        │
│         (Jinja2 Templates + Tailwind + JS)              │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                  Flask Application                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ auth_bp  │ │ user_bp  │ │ admin_bp │ │  api_bp  │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       └────────────┴────────────┴────────────┘          │
│                          │                               │
│  ┌───────────────────────┴───────────────────────────┐  │
│  │              Services Layer                        │  │
│  │ InferenceEngine │ RecommendationService │ Compare │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│                   Database Layer                         │
│         (MySQL 8.0 + SQLAlchemy ORM)                    │
│  Products │ Rules │ Users │ Roles │ Audit Logs          │
└─────────────────────────────────────────────────────────┘
```

---

*Last updated: January 20, 2026*
