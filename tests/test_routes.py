"""
Integration tests for routes
Tests user-facing and admin routes
"""
import pytest


@pytest.mark.integration
class TestUserRoutes:
    """Test user-facing routes"""
    
    def test_home_page(self, client):
        """Test home page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'TechAdvisor' in response.data
    
    def test_questionnaire_page(self, client):
        """Test questionnaire page loads"""
        response = client.get('/recommend')
        assert response.status_code == 200
        assert b'category' in response.data.lower()
        assert b'budget' in response.data.lower()
    
    def test_recommend_submission(self, client, sample_products, sample_categories):
        """Test recommendation form submission"""
        response = client.post('/recommend', data={
            'category': 'smartphone',
            'budget': 1000,
            'usage_type': 'gaming',
            'preferred_brand': ''
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should show results
        assert b'recommendation' in response.data.lower() or b'product' in response.data.lower()


@pytest.mark.integration
class TestAdminRoutes:
    """Test admin routes"""
    
    def test_admin_dashboard_requires_auth(self, client):
        """Test that admin dashboard requires authentication"""
        response = client.get('/admin/dashboard')
        # Should redirect to login
        assert response.status_code == 302 or response.status_code == 401
    
    def test_rules_page_requires_auth(self, client):
        """Test that rules page requires authentication"""
        response = client.get('/admin/rules')
        assert response.status_code == 302 or response.status_code == 401
    
    def test_products_page_requires_auth(self, client):
        """Test that products page requires authentication"""
        response = client.get('/admin/products')
        assert response.status_code == 302 or response.status_code == 401
