from app.services.inference_engine import InferenceEngine
from app.models.product import Product, Category, Brand
from app import db


class RecommendationService:
    """Service for generating product recommendations"""
    
    def __init__(self):
        self.engine = InferenceEngine()
    
    def get_recommendations(self, user_inputs, limit=3):
        """Get top N product recommendations based on user inputs"""
        # Run inference engine to match rules
        matched_rules = self.engine.infer(user_inputs)
        
        # Get candidate products based on user inputs
        candidate_products = self._get_candidate_products(user_inputs)
        
        # Score and rank products
        scored_products = self._score_products(candidate_products, user_inputs, matched_rules)
        
        # Return top N recommendations
        return scored_products[:limit]
    
    def _get_candidate_products(self, inputs):
        """Filter products based on user inputs"""
        query = Product.query.filter_by(is_active=True)
        
        # Filter by category
        if 'category' in inputs:
            category = Category.query.filter_by(name=inputs['category']).first()
            if category:
                query = query.filter_by(category_id=category.id)
        
        # Filter by budget
        if 'max_budget' in inputs:
            try:
                max_budget = float(inputs['max_budget'])
                query = query.filter(Product.price <= max_budget)
            except (ValueError, TypeError):
                pass
        
        # Filter by brand preference
        if 'preferred_brand' in inputs and inputs['preferred_brand'] not in ['Any', 'any', '']:
            brand = Brand.query.filter_by(name=inputs['preferred_brand']).first()
            if brand:
                query = query.filter_by(brand_id=brand.id)
        
        return query.all()
    
    def _score_products(self, products, inputs, rules):
        """Score products based on how well they match requirements"""
        scored = []
        
        for product in products:
            score = 0
            explanations = []
            
            # Base score from price match
            if 'max_budget' in inputs:
                try:
                    budget = float(inputs['max_budget'])
                    product_price = float(product.price)
                    if product_price <= budget:
                        # Better score for products using more of the budget (value)
                        score += (product_price / budget) * 30
                        explanations.append(f"Within your ${budget:,.0f} budget")
                except (ValueError, TypeError):
                    pass
            
            # Score from matched rules
            for rule in rules:
                score += rule.priority
                if rule.description:
                    explanations.append(rule.description)
            
            # Score from specifications matching usage type
            usage_score, usage_reasons = self._score_for_usage(product, inputs.get('usage_type'))
            score += usage_score
            explanations.extend(usage_reasons)
            
            # Brand preference bonus
            if 'preferred_brand' in inputs and inputs['preferred_brand'] not in ['Any', 'any', '']:
                if product.brand.name.lower() == inputs['preferred_brand'].lower():
                    score += 10
                    explanations.append(f"Your preferred brand: {product.brand.name}")
            
            scored.append({
                'product': product,
                'score': score,
                'explanations': explanations
            })
        
        # Sort by score descending
        return sorted(scored, key=lambda x: x['score'], reverse=True)
    
    def _score_for_usage(self, product, usage_type):
        """Score product based on usage type"""
        score = 0
        reasons = []
        
        if not usage_type:
            return score, reasons
        
        # Get product specifications as dict
        specs = {spec.spec_key.lower(): spec.spec_value for spec in product.specifications}
        
        usage_type = usage_type.lower()
        
        if usage_type == 'gaming':
            # Check for gaming-relevant specs
            if 'gpu' in specs and any(term in specs['gpu'].lower() for term in ['rtx', 'radeon', 'nvidia']):
                score += 20
                reasons.append('Powerful GPU for gaming')
            
            if 'ram' in specs:
                try:
                    ram_value = specs['ram'].lower().replace('gb', '').strip()
                    ram_gb = int(ram_value)
                    if ram_gb >= 16:
                        score += 15
                        reasons.append(f'{ram_gb}GB RAM ideal for gaming')
                except (ValueError, TypeError):
                    pass
            
            if 'processor' in specs and any(term in specs['processor'].lower() for term in ['i7', 'i9', 'ryzen 7', 'ryzen 9']):
                score += 15
                reasons.append('High-performance processor')
        
        elif usage_type == 'office':
            # Office work priorities
            if 'battery' in specs and 'hour' in specs['battery'].lower():
                score += 15
                reasons.append('Long battery life for productivity')
            
            if 'weight' in specs:
                try:
                    weight_str = specs['weight'].lower().replace('kg', '').replace('lbs', '').strip()
                    weight = float(weight_str)
                    if weight < 2.0:
                        score += 10
                        reasons.append('Lightweight and portable')
                except (ValueError, TypeError):
                    pass
        
        elif usage_type == 'study':
            # Student-friendly features
            score += 10
            reasons.append('Great for students')
            
            if 'battery' in specs:
                score += 10
                reasons.append('Good battery life for all-day use')
        
        elif usage_type == 'multimedia':
            # Content creation
            if 'ram' in specs:
                try:
                    ram_value = specs['ram'].lower().replace('gb', '').strip()
                    ram_gb = int(ram_value)
                    if ram_gb >= 16:
                        score += 15
                        reasons.append(f'{ram_gb}GB RAM for multimedia work')
                except (ValueError, TypeError):
                    pass
            
            if 'display' in specs and any(term in specs['display'].lower() for term in ['4k', 'retina', 'oled']):
                score += 15
                reasons.append('High-quality display for content creation')
        
        return score, reasons
