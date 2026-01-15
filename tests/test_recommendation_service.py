"""
Unit tests for Recommendation Service
Tests the recommendation logic and explanation facility
"""
import pytest
from app.services.recommendation_service import RecommendationService


@pytest.mark.unit
class TestRecommendationService:
    """Test cases for RecommendationService"""
    
    def test_get_recommendations_basic(self, sample_products, sample_categories):
        """Test basic recommendation retrieval"""
        service = RecommendationService()
        
        smartphone_id = sample_categories['smartphone'].id
        user_input = {
            'category_id': smartphone_id,
            'budget': 1000,
            'usage_type': 'gaming'
        }
        
        results = service.get_recommendations(user_input, limit=5)
        
        assert 'products' in results
        assert 'total_matches' in results
        assert 'fired_rules' in results
        assert isinstance(results['products'], list)
    
    def test_category_filtering(self, sample_products, sample_categories):
        """Test strict category filtering - CRITICAL BUG FIX VERIFICATION"""
        service = RecommendationService()
        
        smartphone_id = sample_categories['smartphone'].id
        user_input = {
            'category_id': smartphone_id,
            'budget': 2000,
            'usage_type': 'general'
        }
        
        results = service.get_recommendations(user_input, limit=10)
        
        # Verify ONLY smartphones returned
        for product in results['products']:
            assert product['category'] == 'Smartphone', \
                f"Found {product['category']} when only Smartphone expected"
    
    def test_laptop_category_filtering(self, sample_products, sample_categories):
        """Test laptop category filtering"""
        service = RecommendationService()
        
        laptop_id = sample_categories['laptop'].id
        user_input = {
            'category_id': laptop_id,
            'budget': 2000,
            'usage_type': 'work'
        }
        
        results = service.get_recommendations(user_input, limit=10)
        
        # Verify ONLY laptops returned
        for product in results['products']:
            assert product['category'] == 'Laptop', \
                f"Found {product['category']} when only Laptop expected"
    
    def test_budget_filtering(self, sample_products, sample_categories):
        """Test budget constraint filtering"""
        service = RecommendationService()
        
        smartphone_id = sample_categories['smartphone'].id
        user_input = {
            'category_id': smartphone_id,
            'budget': 500,
            'usage_type': 'general'
        }
        
        results = service.get_recommendations(user_input, limit=10)
        
        # All products should be within budget
        for product in results['products']:
            assert product['price'] <= 500, \
                f"Product {product['name']} price ${product['price']} exceeds budget $500"
    
    def test_explanation_facility(self, sample_products, sample_categories, sample_rules):
        """Test that explanations are provided for recommendations"""
        service = RecommendationService()
        
        smartphone_id = sample_categories['smartphone'].id
        user_input = {
            'category_id': smartphone_id,
            'budget': 1000,
            'usage_type': 'gaming'
        }
        
        results = service.get_recommendations(user_input, limit=5)
        
        if results['products']:
            product = results['products'][0]
            
            # Verify explanation facility fields exist
            assert 'reasoning' in product
            assert 'reasoning_points' in product
            assert 'confidence' in product
            assert 'matched_rule' in product
            
            # Verify reasoning is not empty
            assert product['reasoning'], "Reasoning should not be empty"
            assert isinstance(product['reasoning_points'], list)
    
    def test_confidence_scoring(self, sample_products, sample_categories, sample_rules):
        """Test confidence scores are calculated"""
        service = RecommendationService()
        
        smartphone_id = sample_categories['smartphone'].id
        user_input = {
            'category_id': smartphone_id,
            'budget': 1000,
            'usage_type': 'gaming'
        }
        
        results = service.get_recommendations(user_input, limit=5)
        
        if results['products']:
            for product in results['products']:
                assert 'confidence' in product
                assert 0 <= product['confidence'] <= 100
    
    def test_empty_results_handling(self, sample_categories):
        """Test handling when no products match"""
        service = RecommendationService()
        
        smartphone_id = sample_categories['smartphone'].id
        user_input = {
            'category_id': smartphone_id,
            'budget': 50,  # Extremely low budget
            'usage_type': 'gaming'
        }
        
        results = service.get_recommendations(user_input, limit=5)
        
        assert results['products'] == []
        assert results['total_matches'] == 0
        assert 'message' in results
    
    def test_budget_reasoning(self, sample_products):
        """Test budget reasoning generation"""
        service = RecommendationService()
        
        # Test different price ranges
        assert service._get_budget_reasoning(200) == "Excellent value - highly affordable"
        assert service._get_budget_reasoning(450) == "Great budget option with good features"
        assert service._get_budget_reasoning(750) == "Mid-range pricing with premium features"
        assert service._get_budget_reasoning(1500) == "Premium pricing reflects high-end specifications"
    
    def test_key_features_extraction(self, sample_products):
        """Test key feature extraction from specifications"""
        service = RecommendationService()
        
        # Get a product with specifications
        product = list(sample_products.values())[0]
        
        features = service._extract_key_features(product)
        assert isinstance(features, str)
