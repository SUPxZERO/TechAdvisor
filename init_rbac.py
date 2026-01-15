from app import create_app, db
from app.models.role import Role, Permission
from app.models.user import User

from sqlalchemy import text, inspect

def init_rbac():
    """Initialize Role-Based Access Control system"""
    app = create_app()
    
    with app.app_context():
        print("Creating tables...")
        # Create tables if they don't exist
        db.create_all()
        
        print("Checking database schema...")
        engine = db.engine
        inspector = inspect(engine)
        
        # Check if role_id exists in users table
        columns = [c['name'] for c in inspector.get_columns('users')]
        if 'role_id' not in columns:
            print("Adding role_id column to users table...")
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN role_id INT"))
                conn.execute(text("ALTER TABLE users ADD CONSTRAINT fk_users_role_id FOREIGN KEY (role_id) REFERENCES roles(id)"))
                conn.commit()
            print("  + Added role_id column and FK constraint.")
        
        # 1. Define Permissions
        permissions_data = [
            # User Management
            {'name': 'View Users', 'slug': 'user.view', 'description': 'Can view list of users'},
            {'name': 'Create Users', 'slug': 'user.create', 'description': 'Can create new users'},
            {'name': 'Edit Users', 'slug': 'user.edit', 'description': 'Can edit user details'},
            {'name': 'Delete Users', 'slug': 'user.delete', 'description': 'Can delete users'},
            
            # Role Management
            {'name': 'View Roles', 'slug': 'role.view', 'description': 'Can view list of roles'},
            {'name': 'Manage Roles', 'slug': 'role.manage', 'description': 'Can create/edit/delete roles'},
            
            # Product Management
            {'name': 'View Products', 'slug': 'product.view', 'description': 'Can view products'},
            {'name': 'Create Products', 'slug': 'product.create', 'description': 'Can create new products'},
            {'name': 'Edit Products', 'slug': 'product.edit', 'description': 'Can edit products'},
            {'name': 'Delete Products', 'slug': 'product.delete', 'description': 'Can delete products'},
            
            # Rule Management
            {'name': 'View Rules', 'slug': 'rule.view', 'description': 'Can view rules'},
            {'name': 'Manage Rules', 'slug': 'rule.manage', 'description': 'Can create/edit/delete rules'},
            
            # Brand Management
            {'name': 'View Brands', 'slug': 'brand.view', 'description': 'Can view list of brands'},
            {'name': 'Manage Brands', 'slug': 'brand.manage', 'description': 'Can create/edit/delete brands'},
        ]
        
        print("Seeding permissions...")
        perms = {}
        for p_data in permissions_data:
            perm = Permission.query.filter_by(slug=p_data['slug']).first()
            if not perm:
                perm = Permission(**p_data)
                db.session.add(perm)
                print(f"  + Created permission: {p_data['slug']}")
            else:
                print(f"  . Permission exists: {p_data['slug']}")
            perms[p_data['slug']] = perm
        db.session.commit()
        
        # 2. Define Roles
        roles_data = [
            {'name': 'Admin', 'description': 'Full system access', 'is_system': True},
            {'name': 'Staff', 'description': 'Standard staff access', 'is_system': True},
        ]
        
        print("\nSeeding roles...")
        roles = {}
        for r_data in roles_data:
            role = Role.query.filter_by(name=r_data['name']).first()
            if not role:
                role = Role(**r_data)
                db.session.add(role)
                print(f"  + Created role: {r_data['name']}")
            else:
                print(f"  . Role exists: {r_data['name']}")
                role.is_system = r_data.get('is_system', False)
            roles[r_data['name']] = role
        db.session.commit()
        
        # 3. Assign Permissions to Roles
        # Re-fetch permissions to be safe
        all_perms = Permission.query.all()
        
        # Admin gets ALL permissions
        print("\nAssigning permissions to Admin...")
        roles['Admin'].permissions = all_perms
        
        # Staff gets Product/Rule management but NOT User/Role management
        print("Assigning permissions to Staff...")
        staff_perms = [
            perms['product.view'], perms['product.create'], perms['product.edit'], perms['product.delete'],
            perms['rule.view'], perms['rule.manage'],
            perms['brand.view'], perms['brand.manage'], # Staff can manage brands
            perms['user.view'], # Staff can see users but not manage them
            perms['role.view']
        ]
        roles['Staff'].permissions = staff_perms
        db.session.commit()
        
        # 4. Migrate Existing Users
        print("\nMigrating existing users...")
        users = User.query.filter(User.role_id == None).all()
        for user in users:
            if user.role == 'admin':
                user.role_obj = roles['Admin']
                print(f"  > User {user.username} (admin) -> Admin Role")
            elif user.role == 'staff':
                user.role_obj = roles['Staff']
                print(f"  > User {user.username} (staff) -> Staff Role")
            else:
                print(f"  ? User {user.username} has unknown legacy role: {user.role}")
        
        db.session.commit()
        print("\nRBAC Initialization Complete!")

if __name__ == '__main__':
    init_rbac()
