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
        matched_rules = self.engine.infer(user_input)
        
        if not matched_rules:
            return {
                'products': [],
                'message': 'No matching products found. Try adjusting your criteria.',
                'total_matches': 0,
                'fired_rules': 0
            }
        
        # Get products based on recommendations
        products = self._fetch_products(matched_rules, user_input, limit)
        
        # Add reasoning to products
        products_with_reasoning = self._add_reasoning(products, matched_rules)
        
        return {
            'products': products_with_reasoning,
            'total_matches': len(products),
            'fired_rules': len(matched_rules),
            'message': f'Found {len(products)} products matching your preferences'
        }
    
    def _fetch_products(self, matched_rules: List, user_input: Dict, limit: int) -> List[Product]:
        """Fetch products based on matched rules and user input"""
        # Start with base query
        query = Product.query.filter_by(is_active=True)
        
        # Apply budget filter if provided
        if 'budget' in user_input:
            try:
                budget = float(user_input['budget'])
                query = query.filter(Product.price <= budget)
            except (ValueError, TypeError):
                pass
        
        # Apply category filter from matched rules
        category_ids = set()
        for rule in matched_rules:
            if rule.category_id:
                category_ids.add(rule.category_id)
        
        if category_ids:
            query = query.filter(Product.category_id.in_(category_ids))
        
        # Apply brand filter if provided
        if 'preferred_brand' in user_input and user_input['preferred_brand']:
            brand_name = user_input['preferred_brand']
            from app.models.product import Brand
            brand = Brand.query.filter(db.func.lower(Brand.name) == brand_name.lower()).first()
            if brand:
                query = query.filter_by(brand_id=brand.id)
        
        # Order by price and limit
        products = query.order_by(Product.price.asc()).limit(limit).all()
        
        return products
    
    def _add_reasoning(self, products: List[Product], matched_rules: List) -> List[Dict]:
        """Add reasoning and confidence scores to product results"""
        results = []
        
        for product in products:
            # Find matching rule for this product's category
            matching_rule = None
            for rule in matched_rules:
                if rule.category_id == product.category_id:
                    matching_rule = rule
                    break
            
            # Calculate confidence based on priority
            confidence = min(100, 50 + (matching_rule.priority if matching_rule else 50))
            
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
                'confidence': confidence,
                'reasoning': f"Matches your {matching_rule.name}" if matching_rule else 'Matches your budget and category',
                'matched_rule': matching_rule.name if matching_rule else None
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
