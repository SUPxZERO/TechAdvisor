# TechAdvisor API Documentation

Complete reference for all API endpoints in the TechAdvisor Expert System.

---

## Base URL

```
Development: http://127.0.0.1:5001
Production:  https://your-domain.com
```

---

## Public Endpoints (No Authentication)

### Products

#### Get All Products
```http
GET /api/products
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category name (e.g., "Smartphone", "Laptop") |
| `brand` | string | Filter by brand name (e.g., "Apple", "Samsung") |

**Response:**
```json
[
  {
    "id": 1,
    "name": "iPhone 15 Pro Max",
    "brand": "Apple",
    "category": "Smartphone",
    "price": 1199.00,
    "image_url": "/static/images/iphone15.jpg",
    "description": "The first iPhone with titanium design...",
    "specifications": {
      "Processor": "A17 Pro",
      "RAM": "8GB",
      "Storage": "256GB"
    }
  }
]
```

---

#### Get Single Product
```http
GET /api/products/{id}
```

**Response:**
```json
{
  "id": 1,
  "name": "iPhone 15 Pro Max",
  "brand": "Apple",
  "category": "Smartphone",
  "price": 1199.00,
  "image_url": "/static/images/iphone15.jpg",
  "description": "The first iPhone with titanium design...",
  "specifications": {
    "Processor": "A17 Pro",
    "RAM": "8GB",
    "Storage": "256GB",
    "Screen": "6.7 Super Retina XDR",
    "Battery": "4422 mAh"
  }
}
```

**Error Response (404):**
```json
{
  "error": "Not Found"
}
```

---

### Brands

#### Get All Brands
```http
GET /api/brands
```

**Response:**
```json
[
  {"id": 1, "name": "Apple", "logo_url": null},
  {"id": 2, "name": "Samsung", "logo_url": null},
  {"id": 3, "name": "Dell", "logo_url": "/static/logos/dell.png"}
]
```

---

### Categories

#### Get All Categories
```http
GET /api/categories
```

**Response:**
```json
[
  {"id": 1, "name": "Smartphone", "description": "Mobile smartphones for communication..."},
  {"id": 2, "name": "Laptop", "description": "Portable computers for work..."}
]
```

---

## User Endpoints (Form-Based)

### Get Recommendations
```http
POST /recommend
Content-Type: application/x-www-form-urlencoded

category=smartphone&budget=1000&usage_type=gaming&preferred_brand=Samsung
```

**Form Fields:**
| Field | Type | Required | Values |
|-------|------|----------|--------|
| `category` | string | Yes | `smartphone`, `laptop` |
| `budget` | integer | Yes | 100-10000 (USD) |
| `usage_type` | string | Yes | `gaming`, `work`, `study`, `general`, `creative` |
| `preferred_brand` | string | No | Any brand name |
| `additional_notes` | string | No | Max 500 chars |

**Response:** HTML page with recommendations (server-rendered)

---

### Compare Products
```http
GET /compare?ids=1,2,3
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | string | Comma-separated product IDs (2-4 products) |

**Response:** HTML page with side-by-side comparison

---

### Compare Analysis (Pros/Cons)
```http
GET /compare-analysis?ids=1,2
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | string | Exactly 2 product IDs |

**Response:** HTML page with detailed pros/cons analysis

---

## Authentication Endpoints

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123&remember_me=true
```

**Form Fields:**
| Field | Type | Required |
|-------|------|----------|
| `username` | string | Yes |
| `password` | string | Yes |
| `remember_me` | boolean | No |

**Success:** Redirect to `/admin/dashboard`  
**Failure:** Re-render login page with flash message

---

### Logout
```http
GET /auth/logout
```

**Response:** Redirect to home page

---

## Admin Endpoints (Authentication Required)

All `/admin/*` endpoints require authenticated session with appropriate role.

### Dashboard
```http
GET /admin/dashboard
```
Returns dashboard with statistics.

---

### Products CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/products` | List all products |
| GET | `/admin/products/new` | Show create form |
| POST | `/admin/products/new` | Create product |
| GET | `/admin/products/{id}` | Show edit form |
| POST | `/admin/products/{id}` | Update product |
| POST | `/admin/products/{id}/delete` | Delete product |

---

### Rules CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/rules` | List all rules |
| GET | `/admin/rules/new` | Show create form |
| POST | `/admin/rules/new` | Create rule |
| GET | `/admin/rules/{id}` | Show edit form |
| POST | `/admin/rules/{id}` | Update rule |
| POST | `/admin/rules/{id}/delete` | Delete rule |

---

### Brands CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/brands` | List all brands |
| GET | `/admin/brands/new` | Show create form |
| POST | `/admin/brands/new` | Create brand |
| GET | `/admin/brands/{id}` | Show edit form |
| POST | `/admin/brands/{id}` | Update brand |
| POST | `/admin/brands/{id}/delete` | Delete brand |

---

### User Management (Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/users` | List all users |
| GET | `/auth/register` | Show registration form |
| POST | `/auth/register` | Create new user |

---

### Role Management (Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/roles` | List all roles |
| GET | `/admin/roles/new` | Show create form |
| POST | `/admin/roles/new` | Create role |
| GET | `/admin/roles/{id}` | Show edit form |
| POST | `/admin/roles/{id}` | Update role |
| POST | `/admin/roles/{id}/delete` | Delete role |

---

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Login required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## CSRF Protection

All POST requests require a valid CSRF token. Include in forms:

```html
<form method="POST">
    {{ form.csrf_token }}
    <!-- form fields -->
</form>
```

---

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- Login attempts: 5/minute
- API requests: 100/minute
