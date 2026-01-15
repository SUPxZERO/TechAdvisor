# TechAdvisor Expert System

A web-based rule-based expert system that helps users find the perfect smartphone or laptop based on their needs, budget, and preferences.

## Project Overview

**Duration**: 12 Weeks (6 Sprints × 2 Weeks)  
**Team Size**: 3 Members  
**Methodology**: Agile (Iterative Model)

## Technology Stack

- **Frontend**: HTML, Jinja2, Tailwind CSS, Vanilla JavaScript
- **Backend**: Python 3.12, Flask 2.3, SQLAlchemy, WTForms
- **Database**: MySQL 8.0
- **Testing**: Pytest
- **Version Control**: Git

## Project Structure

```
TechAdvisor/
├── app/                    # Main application package
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # Flask route blueprints
│   ├── services/          # Business logic (inference engine, recommendations)
│   ├── forms/             # WTForms for validation
│   ├── templates/         # Jinja2 HTML templates
│   ├── static/            # CSS, JS, images
│   └── utils/             # Helper functions
├── tests/                 # Unit and integration tests
├── migrations/            # Database migrations
├── docs/                  # Documentation (SRS, ERD, API docs)
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── run.py               # Application entry point
```

## Features

### For Users
- **Smart Questionnaire**: Answer 5 simple questions to get personalized recommendations
- **Top 3 Recommendations**: Get the best products with detailed explanations
- **Product Comparison**: Compare two products side-by-side
- **No Login Required**: Instant access for end users

### For Admins/Staff
- **Product Management**: Full CRUD operations for products, brands, and categories
- **Rule Management**: Create and modify recommendation rules without coding
- **Dashboard**: View statistics and system insights
- **Audit Logs**: Track all system changes

## Installation

### Prerequisites
- Python 3.12+
- MySQL 8.0+
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TechAdvisor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up database**
   ```bash
   # Create database in MySQL
   mysql -u root -p
   CREATE DATABASE techadvisor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   exit;
   
   # Run migrations
   flask db upgrade
   
   # Seed initial data
   python seed.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - User Interface: http://localhost:5000
   - Admin Login: http://localhost:5000/auth/login

## Default Admin Account

- **Username**: admin
- **Password**: admin123
- **Note**: Change password after first login

## Development

### Running Tests
```bash
pytest
pytest --cov=app  # With coverage report
```

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

## Team Members

- **Seng Sokang** - Project Manager / QA
- **Lim Rattana** - Backend Developer
- **Chey Chansomny** - Frontend Developer

## Sprint Progress

- [x] Sprint 0: Project Setup & Planning (Week 1-2)
- [ ] Sprint 1: Backend Foundation (Week 3-4)
- [ ] Sprint 2: Data & Rules Management (Week 5-6)
- [ ] Sprint 3: Expert System Logic (Week 7-8)
- [ ] Sprint 4: Frontend Development (Week 9-10)
- [ ] Sprint 5: Integration & Testing (Week 11)
- [ ] Sprint 6: Documentation & Deployment (Week 12)

## Documentation

- [Sprint Plan](docs/sprint_plan.md)
- [SRS Document](docs/SRS.md)
- [ERD Diagram](docs/ERD.md)
- [API Documentation](docs/API_Documentation.md)
- [User Manual](docs/USER_MANUAL.md)
- [Admin Manual](docs/ADMIN_MANUAL.md)

## License

This project is developed for educational purposes as part of a university assignment.

## Acknowledgments

- Course Instructor
- IT Experts for rule validation
- Test users for feedback
"# TechAdvisor" 
