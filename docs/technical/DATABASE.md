# Database Documentation

Complete database schema and data model documentation for TechAdvisor.

---

## Database Overview

- **Database**: MySQL 8.0+
- **Character Set**: utf8mb4 (supports emojis and international characters)
- **Collation**: utf8mb4_unicode_ci
- **ORM**: SQLAlchemy with Flask-Migrate

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    users    │       │    roles    │       │ permissions │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ id (PK)     │◄──┐   │ id (PK)     │
│ username    │       │ name        │   │   │ name        │
│ email       │       │ description │   │   │ slug        │
│ password    │       │ is_system   │   │   │ description │
│ role        │       │ created_at  │   │   └──────┬──────┘
│ role_id(FK) │───────│ updated_at  │   │          │
│ is_active   │       └─────────────┘   │          │
│ created_at  │               ▲         │   ┌──────┴──────┐
│ updated_at  │               │         └───│role_perms   │
└──────┬──────┘               │             │(M2M table)  │
       │                      │             └─────────────┘
       ▼
┌─────────────┐
│ audit_logs  │
├─────────────┤
│ id (PK)     │
│ user_id(FK) │
│ action      │
│ table_name  │
│ record_id   │
│ details     │
│ ip_address  │
│ created_at  │
└─────────────┘

┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   brands    │       │  products   │       │ categories  │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ id (PK)     │───────│ id (PK)     │
│ name        │       │ name        │       │ name        │
│ logo_url    │       │ brand_id(FK)│       │ description │
│ created_at  │       │ category_id │       │ created_at  │
└─────────────┘       │ price       │       └──────┬──────┘
                      │ image_url   │              │
                      │ description │              │
                      │ is_active   │              │
                      │ created_at  │              ▼
                      │ updated_at  │       ┌─────────────┐
                      └──────┬──────┘       │    rules    │
                             │              ├─────────────┤
                             ▼              │ id (PK)     │
                      ┌─────────────┐       │ name        │
                      │specifications│      │ description │
                      ├─────────────┤       │ category_id │
                      │ id (PK)     │       │ priority    │
                      │ product_id  │       │ is_active   │
                      │ spec_key    │       │ created_at  │
                      │ spec_value  │       └──────┬──────┘
                      └─────────────┘              │
                                                   ▼
                                          ┌───────────────┐
                                          │rule_conditions│
                                          ├───────────────┤
                                          │ id (PK)       │
                                          │ rule_id (FK)  │
                                          │ condition_type│
                                          │ condition_key │
                                          │ operator      │
                                          │ condition_val │
                                          └───────────────┘
```

---

## Table Definitions

### users
Stores admin and staff accounts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK, AUTO_INCREMENT | Unique identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| role | ENUM('admin','staff') | NOT NULL | Legacy role field |
| role_id | INT | FK→roles(id) | RBAC role reference |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |
| created_at | TIMESTAMP | DEFAULT NOW | Creation timestamp |
| updated_at | TIMESTAMP | ON UPDATE NOW | Last modification |

**Indexes:** idx_username, idx_email, idx_role

---

### roles
RBAC role definitions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Role name |
| description | VARCHAR(255) | | Role description |
| is_system | BOOLEAN | DEFAULT FALSE | Protected system role |
| created_at | TIMESTAMP | | Creation timestamp |
| updated_at | TIMESTAMP | | Last modification |

---

### permissions
Granular permission definitions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Human-readable name |
| slug | VARCHAR(50) | UNIQUE, NOT NULL | Code identifier (e.g., product.create) |
| description | VARCHAR(255) | | Permission description |

---

### role_permissions
Many-to-many join table for roles and permissions.

| Column | Type | Constraints |
|--------|------|-------------|
| role_id | INT | PK, FK→roles(id) |
| permission_id | INT | PK, FK→permissions(id) |

---

### brands
Product manufacturers.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Brand name |
| logo_url | VARCHAR(255) | | Logo image URL |
| created_at | TIMESTAMP | | Creation timestamp |

**Indexes:** idx_name

---

### categories
Product categories (Smartphone, Laptop, etc.).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Category name |
| description | TEXT | | Category description |
| created_at | TIMESTAMP | | Creation timestamp |

**Indexes:** idx_name

---

### products
Main product catalog.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Product name |
| brand_id | INT | FK→brands(id), NOT NULL | Manufacturer |
| category_id | INT | FK→categories(id), NOT NULL | Product type |
| price | DECIMAL(10,2) | NOT NULL | Price in USD |
| image_url | VARCHAR(500) | | Product image |
| description | TEXT | | Product description |
| is_active | BOOLEAN | DEFAULT TRUE | Visibility status |
| created_at | TIMESTAMP | | Creation timestamp |
| updated_at | TIMESTAMP | | Last modification |

**Indexes:** idx_name, idx_brand, idx_category, idx_price, idx_active

**Foreign Keys:**
- brand_id → brands(id) ON DELETE RESTRICT
- category_id → categories(id) ON DELETE RESTRICT

---

### specifications
Product specifications (key-value pairs).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| product_id | INT | FK→products(id), NOT NULL | Parent product |
| spec_key | VARCHAR(100) | NOT NULL | Specification name |
| spec_value | TEXT | NOT NULL | Specification value |

**Indexes:** idx_product_spec (composite: product_id, spec_key)

**Foreign Keys:**
- product_id → products(id) ON DELETE CASCADE

---

### rules
Expert system inference rules.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Rule name |
| description | TEXT | | Rule purpose |
| category_id | INT | FK→categories(id) | Target category |
| priority | INT | DEFAULT 0, NOT NULL | Execution priority (1-100) |
| is_active | BOOLEAN | DEFAULT TRUE | Rule enabled status |
| created_at | TIMESTAMP | | Creation timestamp |

**Indexes:** idx_priority, idx_active, idx_category

**Foreign Keys:**
- category_id → categories(id) ON DELETE SET NULL

---

### rule_conditions
Conditions that must be satisfied for a rule to fire.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| rule_id | INT | FK→rules(id), NOT NULL | Parent rule |
| condition_type | VARCHAR(50) | NOT NULL | Condition category |
| condition_key | VARCHAR(100) | NOT NULL | Attribute to check |
| operator | VARCHAR(20) | NOT NULL | Comparison operator |
| condition_value | VARCHAR(255) | NOT NULL | Expected value |

**Indexes:** idx_rule, idx_type

**Foreign Keys:**
- rule_id → rules(id) ON DELETE CASCADE

---

### audit_logs
System activity tracking.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PK | Unique identifier |
| user_id | INT | FK→users(id) | Acting user |
| action | VARCHAR(100) | NOT NULL | Action performed |
| table_name | VARCHAR(50) | | Affected table |
| record_id | INT | | Affected record ID |
| details | TEXT | | Additional details (JSON) |
| ip_address | VARCHAR(45) | | Client IP address |
| created_at | TIMESTAMP | | Action timestamp |

**Indexes:** idx_user, idx_action, idx_created

**Foreign Keys:**
- user_id → users(id) ON DELETE SET NULL

---

## Common Queries

### Get products with specifications
```sql
SELECT p.*, 
       GROUP_CONCAT(CONCAT(s.spec_key, ':', s.spec_value) SEPARATOR '|') as specs
FROM products p
LEFT JOIN specifications s ON p.id = s.product_id
WHERE p.is_active = TRUE
GROUP BY p.id;
```

### Get active rules with conditions
```sql
SELECT r.*, c.name as category_name,
       COUNT(rc.id) as condition_count
FROM rules r
LEFT JOIN categories c ON r.category_id = c.id
LEFT JOIN rule_conditions rc ON r.id = rc.rule_id
WHERE r.is_active = TRUE
GROUP BY r.id
ORDER BY r.priority DESC;
```

### Get user with role and permissions
```sql
SELECT u.*, r.name as role_name,
       GROUP_CONCAT(p.slug) as permissions
FROM users u
LEFT JOIN roles r ON u.role_id = r.id
LEFT JOIN role_permissions rp ON r.id = rp.role_id
LEFT JOIN permissions p ON rp.permission_id = p.id
WHERE u.id = ?
GROUP BY u.id;
```

---

## Migrations

Run migrations with Flask-Migrate:

```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade
```

---

## Backup & Restore

### Backup
```bash
mysqldump -u root -p techadvisor > backup_$(date +%Y%m%d).sql
```

### Restore
```bash
mysql -u root -p techadvisor < backup_20260120.sql
```
