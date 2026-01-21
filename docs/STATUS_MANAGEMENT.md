# Status Management Implementation Guide

## Overview

This document describes the activate/deactivate status management feature implemented for Users, Products, and Rules in the TechAdvisor Expert System.

## Features Implemented

### 1. Database Level
- **User Table**: `is_active` field (Boolean, default: True)
- **Product Table**: `is_active` field (Boolean, default: True)  
- **Rule Table**: `is_active` field (Boolean, default: True)
- **Indexes**: Created indexes on `is_active` fields for faster filtering

### 2. Backend - Models
All models support status management through the `is_active` field:

```python
# User Model
class User(UserMixin, db.Model):
    is_active = db.Column(db.Boolean, default=True, nullable=False)

# Product Model
class Product(db.Model):
    is_active = db.Column(db.Boolean, default=True, nullable=False)

# Rule Model
class Rule(db.Model):
    is_active = db.Column(db.Boolean, default=True, nullable=False)
```

### 3. Backend - Forms
All forms include the status control:

```python
# UserForm
is_active = BooleanField('Active', default=True)

# ProductForm
is_active = BooleanField('Active (visible to users)', default=True)

# RuleForm
is_active = BooleanField('Active (enabled in recommendations)', default=True)
```

### 4. Backend - Routes
New toggle status routes have been added to `/admin` blueprint:

#### Product Status Toggle
```
POST/GET: /admin/products/<int:product_id>/toggle-status
Permission: product.edit
Action: Toggles product.is_active between True and False
Logs: Audit log entry created
Flash: Success message shown
```

#### User Status Toggle
```
POST/GET: /admin/users/<int:user_id>/toggle-status
Permission: user.edit
Action: Toggles user.is_active between True and False
Restriction: Cannot deactivate current user
Logs: Audit log entry created
Flash: Success message shown
```

#### Rule Status Toggle
```
POST/GET: /admin/rules/<int:rule_id>/toggle-status
Permission: rule.manage
Action: Toggles rule.is_active between True and False
Logs: Audit log entry created
Flash: Success message shown
```

### 5. Service Layer - Filtering

#### Recommendation Service
- Only queries **active products** when fetching recommendations
- Only uses **active rules** in inference engine matching

#### Inference Engine
- Only matches **active rules** during inference process
- Filters: `Rule.query.filter_by(is_active=True)`

#### API Routes
- Product listing returns only **active products**
- Filter: `Product.query.filter_by(is_active=True)`

#### User Routes
- Comparison feature only includes **active products**
- Filter: `Product.query.filter(Product.id.in_(ids), Product.is_active == True)`

### 6. Frontend - Admin Templates

#### Products List (`admin/products.html`)
- Status column displays: "Active" (green) or "Inactive" (gray)
- New "Deactivate/Activate" link in actions column
- Color-coded: Yellow for deactivate, Green for activate

#### Users Management (`admin/users.html`)
- Status badge on user cards: "Active" (green) or "Inactive" (gray)
- New "Deactivate/Activate" button in hover overlay
- Prevents deactivating current user
- Color-coded: Yellow for deactivate, Green for activate

#### Rules Management (`admin/rules.html`)
- Status column displays: "Active" (green) or "Inactive" (gray)
- New "Deactivate/Activate" link in actions column
- Color-coded: Yellow for deactivate, Green for activate

## Usage Workflow

### Deactivating a Product
1. Go to Admin Dashboard → Products
2. Find the product in the list
3. Click "Deactivate" button in the Actions column
4. Product is marked inactive and won't appear in recommendations
5. Inactive badge is shown in the status column

### Deactivating a User
1. Go to Admin Dashboard → Users
2. Hover over the user card to reveal actions
3. Click "Deactivate" button
4. User account is disabled but record remains in database
5. Inactive badge is shown on the card

### Deactivating a Rule
1. Go to Admin Dashboard → Rules
2. Find the rule in the list
3. Click "Deactivate" button in the Actions column
4. Rule will not be evaluated in the inference engine
5. Inactive badge is shown in the status column

### Re-activating Resources
1. Navigate to the resource (Product, User, or Rule)
2. Click the "Activate" button (appears for inactive items)
3. Resource is immediately available again

## Audit Trail

All status changes are logged to the AuditLog table:

```python
audit_log = AuditLog(
    user_id=current_user.id,
    action='status_update',
    table_name='products',  # or 'users', 'rules'
    record_id=resource.id,
    details=f'deactivated product: Product Name'
)
```

This allows administrators to track:
- Who made the change
- What was changed
- When it was changed
- The specific resource affected

## Impact on User Experience

### For End Users
- Inactive products don't appear in:
  - Recommendation results
  - Product comparison
  - Product listings in API
  - Product detail pages

### For Admins/Staff
- Can quickly disable resources without deletion
- Data is preserved for historical purposes
- Easy to reactivate resources if needed
- No data loss, only visibility control

## API Behavior

The API endpoints automatically respect the `is_active` status:

```
GET /api/products → Only returns is_active=True
GET /api/products/<id> → Returns product if active
POST /api/recommendations → Uses only active rules
```

## Database Migration

A migration file has been created to ensure the `is_active` fields exist and are properly indexed:

```
File: migrations/versions/add_status_management.py
Revision: add_status_management
Down Revision: 826f02a7bff7
```

To apply the migration:
```bash
flask db upgrade
```

## Best Practices

1. **Prefer Deactivation Over Deletion**
   - Deactivate products/rules instead of deleting them
   - Preserves historical data and audit trails
   - Allows easy reactivation if needed

2. **Document Reasons**
   - Use audit logs to track why items were deactivated
   - Consider adding notes in the system

3. **Regular Review**
   - Periodically review inactive items
   - Archive or permanently delete old records as needed

4. **Testing**
   - Verify inactive items don't appear in recommendations
   - Test API endpoints return only active products
   - Confirm admin interfaces show status correctly

## Related Files Modified

1. **Models**
   - `app/models/user.py` - Already had `is_active`
   - `app/models/product.py` - Already had `is_active`
   - `app/models/rule.py` - Already had `is_active`

2. **Forms**
   - `app/forms/user_forms.py` - Already had `is_active` field
   - `app/forms/product_forms.py` - Already had `is_active` field
   - `app/forms/rule_forms.py` - Already had `is_active` field

3. **Routes**
   - `app/routes/admin.py` - Added toggle status routes
   - `app/routes/user.py` - Updated to filter active products
   - `app/routes/api.py` - Already filters by is_active

4. **Services**
   - `app/services/recommendation_service.py` - Already filters by is_active
   - `app/services/inference_engine.py` - Already filters by is_active
   - `app/services/comparison_service.py` - Works with active products

5. **Templates**
   - `app/templates/admin/products.html` - Added deactivate/activate button
   - `app/templates/admin/users.html` - Added deactivate/activate button
   - `app/templates/admin/rules.html` - Added deactivate/activate button

6. **Migrations**
   - `migrations/versions/add_status_management.py` - New migration

## Testing Checklist

- [ ] Create a new product and verify it's visible in recommendations
- [ ] Deactivate the product and verify it disappears from recommendations
- [ ] Reactivate the product and verify it reappears
- [ ] Create a new rule and verify it's used in inference
- [ ] Deactivate the rule and verify it's not used in inference
- [ ] Reactivate the rule and verify it's used again
- [ ] Create a new user account
- [ ] Deactivate the user and verify they can't log in
- [ ] Reactivate the user and verify they can log in
- [ ] Check audit logs for status change entries
- [ ] Verify inactive products don't appear in API responses
- [ ] Verify admin interface shows correct status badges

## Future Enhancements

1. **Soft Delete Pattern**
   - Track `deleted_at` timestamp
   - Implement permanent deletion after retention period

2. **Status History**
   - Store status change history in a separate table
   - Track status transitions over time

3. **Bulk Actions**
   - Bulk deactivate/activate multiple items
   - Batch status changes from admin dashboard

4. **Scheduled Activation**
   - Schedule items to activate/deactivate at specific times
   - Support product launches and limited-time offers

5. **Status Notifications**
   - Notify users when recommended products are deactivated
   - Alert admins about inactive items

## Support & Troubleshooting

### Products not showing in recommendations
- Check: Is `is_active = True` in the database?
- Check: Are the rules matching the product category active?
- Check: Is the product price within user's budget?

### Inactive users still showing in admin list
- The admin user list shows all users regardless of status
- Status is displayed in the "Inactive" badge
- Use filters to show only active users (future enhancement)

### Rules not firing
- Check: Is `is_active = True` for the rule?
- Check: Do conditions match user input?
- Check: Is the category filter correct?

## Contact & Questions

For questions about the status management feature, refer to:
- Project Documentation: `/docs/`
- Technical Guide: `/docs/technical/`
- Code Comments in: `app/routes/admin.py`
