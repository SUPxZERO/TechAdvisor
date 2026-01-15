# TechAdvisor - Quick Start Guide

## Prerequisites
- Python 3.12+
- MySQL 8.0+ (running on port 3307)
- Git

## Setup Instructions

### 1. Navigate to Project
```bash
cd "E:\promgramming\Y3n\Expert System\Assignment\TechAdvisor"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
The `.env` file has been created with your MySQL settings:
- Database: `techadvisor`
- Port: `3307`
- User: `root`
- Password: `ROOT`

### 4. Database is Ready
The database schema has been imported successfully.

### 5. Run the Application
```bash
python run.py
```

The server will start on: **http://127.0.0.1:5001**

## Current Status

✅ **Sprint 0 Complete**
- Project structure created
- Database schema imported
- Flask server running successfully

⚠️ **Expected Behavior**
The server is running, but you'll see a "TemplateNotFound" error when accessing routes. This is normal - HTML templates will be created in Sprint 4.

## What's Working

- ✅ Flask application starts
- ✅ Database models defined
- ✅ Routes configured
- ✅ Inference engine implemented
- ✅ Recommendation service ready
- ✅ API endpoints available

## Next Steps

**Sprint 1: Backend Foundation** (Weeks 3-4)
1. Create admin registration
2. Build authentication templates
3. Implement session management
4. Add security features
5. Create basic admin dashboard

## Troubleshooting

### Port Already in Use
If you see "socket in a way forbidden by its access permissions":
- The app has been configured to use port **5001** instead of 5000
- If 5001 is also blocked, edit `run.py` and change the port number

### Database Connection Error
If you see "Can't connect to MySQL server":
- Verify MySQL is running: `mysql -u root -P3307 -p`
- Check `.env` file has correct credentials
- Confirm database exists: `SHOW DATABASES;`

### Module Import Errors
If you see import errors:
- Ensure you're in the project directory
- Reinstall dependencies: `pip install -r requirements.txt`

## Project Structure

```
TechAdvisor/
├── app/                    # Main application
│   ├── models/            # Database models
│   ├── routes/            # URL routes
│   ├── services/          # Business logic
│   └── templates/         # HTML (Sprint 4)
├── docs/                  # Documentation
├── tests/                 # Test files (Sprint 5)
├── .env                   # Your configuration
├── config.py             # App settings
└── run.py                # Start server
```

## Available Routes (when templates are added)

- `/` - Home page
- `/recommend` - Get recommendations
- `/compare` - Compare products
- `/auth/login` - Admin login
- `/admin/dashboard` - Admin panel

## API Endpoints (Ready to Use)

- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product details
- `GET /api/brands` - List brands
- `GET /api/categories` - List categories

## Team

- **Seng Sokang** - Project Manager / QA
- **Lim Rattana** - Backend Developer
- **Chey Chansomny** - Frontend Developer

---

**Status**: ✅ Development environment ready
**Next Sprint**: Sprint 1 - Backend Foundation
