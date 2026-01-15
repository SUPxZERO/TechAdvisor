from app import create_app, db
from app.models.role import Role, Permission
from app.models.user import User

def verify_rbac():
    app = create_app()
    with app.app_context():
        print("Verifying RBAC implementation...")
        
        # 1. Check Roles
        admin_role = Role.query.filter_by(name='Admin').first()
        staff_role = Role.query.filter_by(name='Staff').first()
        
        if not admin_role or not staff_role:
            print("❌ Initial roles missing!")
            return
        print(f"✅ Found Admin and Staff roles")
        
        # 2. Check Permissions
        print(f"  - Admin has {len(admin_role.permissions)} permissions")
        print(f"  - Staff has {len(staff_role.permissions)} permissions")
        
        # 3. Check User Assignment
        admin_user = User.query.filter_by(role_obj=admin_role).first()
        if admin_user:
            print(f"✅ Found admin user: {admin_user.username}")
            # Verify permission check
            if admin_user.has_permission('role.manage'):
                print("  ✅ Admin user has 'role.manage' permission")
            else:
                print("  ❌ Admin user MISSING 'role.manage' permission")
        else:
            print("⚠️ No admin user found (check init_rbac migration)")
            
        staff_user = User.query.filter_by(role_obj=staff_role).first()
        if staff_user:
            print(f"✅ Found staff user: {staff_user.username}")
            # Verify permission check
            if staff_user.has_permission('product.view'):
                print("  ✅ Staff user has 'product.view' permission")
            else:
                print("  ❌ Staff user MISSING 'product.view' permission")
                
            if not staff_user.has_permission('role.manage'):
                 print("  ✅ Staff user correctly DOES NOT have 'role.manage' permission")
            else:
                 print("  ❌ Staff user WRONGLY has 'role.manage' permission")
        else:
            print("⚠️ No staff user found")
            
        print("\nVerification Complete!")

if __name__ == '__main__':
    verify_rbac()
