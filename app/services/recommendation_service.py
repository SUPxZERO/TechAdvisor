"""
Recommendation Service
High-level service for generating product recommendations using the inference engine
"""
from app.services.inference_engine import InferenceEngine
from app.models.product import Product, Category
from app import db
from typing import Dict, List, Any
from sqlalchemy import and_, or_


class RecommendationService:
    """Service for generating product recommendations"""
    
    def __init__(self):
        self.engine = InferenceEngine()
    
    def get_recommendations(self, user_input: Dict[str, Any], limit: int = 10) -> Dict[str, Any]:
        """
        Main entry point for getting recommendations
        
        Args:
            user_input: Dictionary of user preferences (budget, usage_type, etc.)
            limit: Maximum number of products to return
        
        Returns:
            Dictionary with recommendations and metadata
        """
        # Run inference engine
        fired_recommendations = self.engine.forward_chain(user_input)
        
        if not fired_recommendations:
            return {
                'products': [],
                'message': 'No matching products found. Try adjusting your criteria.',
                'total_matches': 0
            }
        
        # Get products based on recommendations
        products = self._fetch_products(fired_recommendations, user_input, limit)
        
        # Add reasoning to products
        products_with_reasoning = self._add_reasoning(products, fired_recommendations)
        
        return {
            'products': products_with_reasoning,
            'total_matches': len(products),
            'fired_rules': len(fired_recommendations),
            'message': f'Found {len(products)} products matching your preferences'
        }
    
    def _fetch_products(self, recommendations: List[Dict], user_input: Dict, limit: int) -> List[Product]:
        """Fetch products based on fired rules and user input"""
        # Start with base query
        query = Product.query.filter_by(is_active=True)
        
        # Apply budget filter if provided
        if 'budget' in user_input:
            try:
                budget = float(user_input['budget'])
                query = query.filter(Product.price <= budget)
            except (ValueError, TypeError):
                pass
        
        # Apply category filter from recommendations
        category_ids = set()
        for rec in recommendations:
            if rec.get('category_id'):
                category_ids.add(rec['category_id'])
        
        if category_ids:
            query = query.filter(Product.category_id.in_(category_ids))
        
        # Apply brand filter if provided
        if 'preferred_brand' in user_input and user_input['preferred_brand']:
            brand_name = user_input['preferred_brand']
            query = query.join(Product.brand).filter(
                db.func.lower(Product.brand.has(name=brand_name))
            )
        
        # Order by price and limit
        products = query.order_by(Product.price.asc()).limit(limit).all()
        
        return products
    
    def _add_reasoning(self, products: List[Product], recommendations: List[Dict]) -> List[Dict]:
        """Add reasoning and confidence scores to product results"""
        results = []
        
        for product in products:
            # Find matching recommendation for this product's category
            matching_rec = None
            for rec in recommendations:
                if rec.get('category_id') == product.category_id:
                    matching_rec = rec
                    break
            
            product_dict = {
                'id': product.id,
                'name': product.name,
                'brand': product.brand.name,
                'category': product.category.name,
                'price': float(product.price),
                'description': product.description,
                'image_url': product.image_url,
                'specifications': [
                    {'key': spec.spec_key, 'value': spec.spec_value}
                    for spec in product.specifications
                ],
                'confidence': matching_rec['confidence'] if matching_rec else 50,
                'reasoning': matching_rec['reasoning'] if matching_rec else 'Matches your budget and category',
                'matched_rule': matching_rec['rule_name'] if matching_rec else None
            }
            
            results.append(product_dict)
        
        # Sort by confidence descending
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results
    
    def calculate_match_percentage(self, product: Product, user_input: Dict) -> int:
        """Calculate how well a product matches user preferences (0-100)"""
        score = 0
        total_criteria = 0
        
        # Budget match
        if 'budget' in user_input:
            total_criteria += 1
            try:
                budget = float(user_input['budget'])
                if product.price <= budget:
                    score += 1
                    # Bonus for being close to budget
                    if product.price >= budget * 0.7:
                        score += 0.5
            except:
                pass
        
        # Brand preference
        if 'preferred_brand' in user_input and user_input['preferred_brand']:
            total_criteria += 1
            if product.brand.name.lower() == user_input['preferred_brand'].lower():
                score += 1
        
        # Category match
        if 'category' in user_input:
            total_criteria += 1
            if product.category.name.lower() == user_input['category'].lower():
                score += 1
        
        if total_criteria == 0:
            return 50
        
        return int((score / total_criteria) * 100)
