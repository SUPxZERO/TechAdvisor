"""
Comparison Service
Intelligent product comparison with pros/cons analysis for decision support
"""
from app.models.product import Product
from app import db
from typing import Dict, List, Any, Tuple
from decimal import Decimal


class ComparisonService:
    """Service for intelligent product comparison with pros/cons analysis"""
    
    def __init__(self):
        """Initialize comparison service with category benchmarks"""
        # Define category-specific benchmarks for evaluation
        self.benchmarks = {
            'smartphone': {
                'ram': {'excellent': 12, 'good': 8, 'minimum': 6},
                'storage': {'excellent': 256, 'good': 128, 'minimum': 64},
                'battery': {'excellent': 5000, 'good': 4000, 'minimum': 3000},
                'camera_mp': {'excellent': 108, 'good': 48, 'minimum': 12}
            },
            'laptop': {
                'ram': {'excellent': 16, 'good': 8, 'minimum': 4},
                'storage': {'excellent': 512, 'good': 256, 'minimum': 128},
                'ssd': {'excellent': 1024, 'good': 512, 'minimum': 256},
                'battery_hours': {'excellent': 12, 'good': 8, 'minimum': 5}
            }
        }
        
        # Specification keywords to look for
        self.spec_keywords = {
            'performance': ['processor', 'cpu', 'ram', 'memory', 'graphics', 'gpu'],
            'storage': ['storage', 'ssd', 'hard drive', 'hdd', 'rom'],
            'display': ['display', 'screen', 'resolution', 'refresh rate'],
            'camera': ['camera', 'mp', 'megapixel', 'lens'],
            'battery': ['battery', 'mah', 'charging', 'power'],
            'connectivity': ['5g', '4g', 'wifi', 'bluetooth', 'nfc'],
            'build': ['weight', 'build', 'material', 'waterproof', 'durability']
        }
    
    def compare_two_products(
        self, 
        product1: Product, 
        product2: Product, 
        user_preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Main comparison orchestrator for two products
        
        Args:
            product1: First product to compare
            product2: Second product to compare
            user_preferences: Optional user preferences from session
        
        Returns:
            Dictionary with comprehensive comparison data including pros, cons, and winner
        """
        user_preferences = user_preferences or {}
        
        # Extract pros and cons for each product
        product1_pros = self.extract_pros(product1, user_preferences)
        product1_cons = self.extract_cons(product1, user_preferences)
        
        product2_pros = self.extract_pros(product2, user_preferences)
        product2_cons = self.extract_cons(product2, user_preferences)
        
        # Get comparative advantages
        comparative_advantages = self.get_comparative_advantages(product1, product2)
        
        # Calculate overall scores
        score1 = self.calculate_overall_score(product1, user_preferences)
        score2 = self.calculate_overall_score(product2, user_preferences)
        
        # Determine winner
        winner = 1 if score1 > score2 else (2 if score2 > score1 else 0)
        winner_reason = self._generate_winner_reason(product1, product2, score1, score2, comparative_advantages)
        
        return {
            'product1': {
                'id': product1.id,
                'name': product1.name,
                'brand': product1.brand.name,
                'category': product1.category.name,
                'price': float(product1.price),
                'image_url': product1.image_url,
                'description': product1.description,
                'pros': product1_pros,
                'cons': product1_cons,
                'score': score1,
                'specifications': {spec.spec_key: spec.spec_value for spec in product1.specifications}
            },
            'product2': {
                'id': product2.id,
                'name': product2.name,
                'brand': product2.brand.name,
                'category': product2.category.name,
                'price': float(product2.price),
                'image_url': product2.image_url,
                'description': product2.description,
                'pros': product2_pros,
                'cons': product2_cons,
                'score': score2,
                'specifications': {spec.spec_key: spec.spec_value for spec in product2.specifications}
            },
            'comparative_advantages': comparative_advantages,
            'winner': winner,
            'winner_reason': winner_reason,
            'price_difference': abs(float(product1.price) - float(product2.price)),
            'same_category': product1.category_id == product2.category_id
        }
    
    def extract_pros(self, product: Product, user_preferences: Dict[str, Any]) -> List[str]:
        """
        Extract product strengths based on specifications and user needs
        
        Args:
            product: Product to analyze
            user_preferences: User preferences for context-aware analysis
        
        Returns:
            List of product strengths/advantages
        """
        pros = []
        category_name = product.category.name.lower()
        specs = {spec.spec_key: spec.spec_value for spec in product.specifications}
        
        # Price-based pros
        budget = user_preferences.get('budget')
        if budget:
            try:
                budget_float = float(budget)
                price_float = float(product.price)
                
                if price_float <= budget_float * 0.7:
                    pros.append(f"Excellent value - priced at ${price_float:.2f}, well under your ${budget_float:.2f} budget")
                elif price_float <= budget_float:
                    pros.append(f"Fits your budget perfectly at ${price_float:.2f}")
            except (ValueError, TypeError):
                pass
        
        # Brand preference match
        preferred_brand = user_preferences.get('preferred_brand')
        if preferred_brand and product.brand.name.lower() == preferred_brand.lower():
            pros.append(f"Your preferred brand: {product.brand.name}")
        
        # Specification-based pros
        for spec in product.specifications:
            key_lower = spec.spec_key.lower()
            value_lower = spec.spec_value.lower()
            
            # RAM analysis
            if 'ram' in key_lower or 'memory' in key_lower:
                ram_value = self._extract_number(spec.spec_value)
                if ram_value:
                    benchmark = self.benchmarks.get(category_name, {}).get('ram', {})
                    if ram_value >= benchmark.get('excellent', 16):
                        pros.append(f"Excellent RAM capacity: {spec.spec_value}")
                    elif ram_value >= benchmark.get('good', 8):
                        pros.append(f"Good RAM for multitasking: {spec.spec_value}")
            
            # Storage analysis
            if 'storage' in key_lower or 'ssd' in key_lower:
                storage_value = self._extract_number(spec.spec_value)
                if storage_value:
                    benchmark = self.benchmarks.get(category_name, {}).get('storage', {})
                    if storage_value >= benchmark.get('excellent', 512):
                        pros.append(f"Ample storage space: {spec.spec_value}")
                    elif storage_value >= benchmark.get('good', 256):
                        pros.append(f"Sufficient storage: {spec.spec_value}")
            
            # Battery analysis
            if 'battery' in key_lower:
                battery_value = self._extract_number(spec.spec_value)
                if battery_value:
                    if category_name == 'smartphone' and battery_value >= 4500:
                        pros.append(f"Long-lasting battery: {spec.spec_value}")
                    elif category_name == 'laptop' and battery_value >= 10:
                        pros.append(f"Extended battery life: {spec.spec_value}")
            
            # Display analysis
            if 'display' in key_lower or 'screen' in key_lower:
                if any(keyword in value_lower for keyword in ['oled', 'amoled', '4k', 'retina', '120hz', '144hz']):
                    pros.append(f"Premium display: {spec.spec_value}")
            
            # Camera analysis (for smartphones)
            if category_name == 'smartphone' and ('camera' in key_lower):
                camera_mp = self._extract_number(spec.spec_value)
                if camera_mp and camera_mp >= 48:
                    pros.append(f"High-quality camera: {spec.spec_value}")
            
            # Processor analysis
            if 'processor' in key_lower or 'cpu' in key_lower:
                if any(keyword in value_lower for keyword in ['i7', 'i9', 'ryzen 7', 'ryzen 9', 'm1', 'm2', 'm3', 'snapdragon 8']):
                    pros.append(f"Powerful processor: {spec.spec_value}")
            
            # Graphics analysis
            if 'graphics' in key_lower or 'gpu' in key_lower:
                if any(keyword in value_lower for keyword in ['rtx', 'dedicated', 'nvidia', 'radeon']):
                    pros.append(f"Dedicated graphics: {spec.spec_value}")
            
            # Connectivity features
            if '5g' in value_lower:
                pros.append("5G connectivity support")
            if 'wifi 6' in value_lower or 'wi-fi 6' in value_lower:
                pros.append("Latest WiFi 6 standard")
        
        # Usage type specific pros
        usage_type = user_preferences.get('usage_type', '').lower()
        if usage_type == 'gaming':
            has_good_graphics = any('graphics' in s.spec_key.lower() for s in product.specifications)
            has_good_ram = any('ram' in s.spec_key.lower() and self._extract_number(s.spec_value, 0) >= 16 
                              for s in product.specifications)
            if has_good_graphics and has_good_ram:
                pros.append("Optimized for gaming performance")
        
        # If no pros found, add generic one
        if not pros:
            pros.append("Solid specifications for everyday use")
        
        return pros[:6]  # Limit to top 6 pros
    
    def extract_cons(self, product: Product, user_preferences: Dict[str, Any]) -> List[str]:
        """
        Extract product weaknesses relative to category standards
        
        Args:
            product: Product to analyze
            user_preferences: User preferences for context-aware analysis
        
        Returns:
            List of product weaknesses/limitations
        """
        cons = []
        category_name = product.category.name.lower()
        specs = {spec.spec_key: spec.spec_value for spec in product.specifications}
        
        # Price-based cons
        budget = user_preferences.get('budget')
        if budget:
            try:
                budget_float = float(budget)
                price_float = float(product.price)
                
                if price_float > budget_float:
                    cons.append(f"Over budget by ${price_float - budget_float:.2f}")
                elif price_float >= budget_float * 0.95:
                    cons.append(f"At the upper limit of your budget")
            except (ValueError, TypeError):
                pass
        
        # Check for missing important features
        has_ram = any('ram' in s.spec_key.lower() for s in product.specifications)
        has_storage = any('storage' in s.spec_key.lower() or 'ssd' in s.spec_key.lower() 
                         for s in product.specifications)
        has_battery = any('battery' in s.spec_key.lower() for s in product.specifications)
        
        if not has_ram:
            cons.append("RAM specifications not disclosed")
        if not has_storage:
            cons.append("Storage information not available")
        if not has_battery:
            cons.append("Battery details not specified")
        
        # Specification-based cons
        for spec in product.specifications:
            key_lower = spec.spec_key.lower()
            value_lower = spec.spec_value.lower()
            
            # Low RAM
            if 'ram' in key_lower or 'memory' in key_lower:
                ram_value = self._extract_number(spec.spec_value)
                if ram_value:
                    benchmark = self.benchmarks.get(category_name, {}).get('ram', {})
                    if ram_value < benchmark.get('minimum', 4):
                        cons.append(f"Limited RAM: {spec.spec_value} may struggle with multitasking")
            
            # Low storage
            if 'storage' in key_lower or 'ssd' in key_lower:
                storage_value = self._extract_number(spec.spec_value)
                if storage_value:
                    benchmark = self.benchmarks.get(category_name, {}).get('storage', {})
                    if storage_value < benchmark.get('minimum', 128):
                        cons.append(f"Limited storage: {spec.spec_value} may require external storage")
            
            # Small battery (for smartphones)
            if category_name == 'smartphone' and 'battery' in key_lower:
                battery_value = self._extract_number(spec.spec_value)
                if battery_value and battery_value < 3500:
                    cons.append(f"Smaller battery: {spec.spec_value} may require frequent charging")
            
            # Integrated graphics only (for gaming laptops)
            if 'graphics' in key_lower or 'gpu' in key_lower:
                if 'integrated' in value_lower and user_preferences.get('usage_type', '').lower() == 'gaming':
                    cons.append("Integrated graphics not ideal for gaming")
        
        # Check for older connectivity
        has_5g = any('5g' in s.spec_value.lower() for s in product.specifications)
        if category_name == 'smartphone' and not has_5g:
            cons.append("No 5G support (4G only)")
        
        # If no cons found, note that positively
        if not cons:
            cons.append("No significant drawbacks identified")
        
        return cons[:6]  # Limit to top 6 cons
    
    def get_comparative_advantages(self, product1: Product, product2: Product) -> Dict[str, Dict]:
        """
        Determine which product wins in each category
        
        Args:
            product1: First product
            product2: Second product
        
        Returns:
            Dictionary mapping categories to winner and reason
        """
        advantages = {}
        
        # Price comparison
        price1 = float(product1.price)
        price2 = float(product2.price)
        
        if price1 < price2:
            advantages['Price'] = {
                'winner': 1,
                'reason': f"{product1.name} is ${price2 - price1:.2f} cheaper"
            }
        elif price2 < price1:
            advantages['Price'] = {
                'winner': 2,
                'reason': f"{product2.name} is ${price1 - price2:.2f} cheaper"
            }
        else:
            advantages['Price'] = {
                'winner': 0,
                'reason': "Both products have the same price"
            }
        
        # Get specifications dictionaries
        specs1 = {spec.spec_key.lower(): spec.spec_value for spec in product1.specifications}
        specs2 = {spec.spec_key.lower(): spec.spec_value for spec in product2.specifications}
        
        # Compare RAM
        ram1 = self._find_spec_value(specs1, ['ram', 'memory'])
        ram2 = self._find_spec_value(specs2, ['ram', 'memory'])
        if ram1 or ram2:
            winner, reason = self._compare_numeric_specs(ram1, ram2, product1.name, product2.name, "RAM")
            advantages['RAM'] = {'winner': winner, 'reason': reason}
        
        # Compare Storage
        storage1 = self._find_spec_value(specs1, ['storage', 'ssd'])
        storage2 = self._find_spec_value(specs2, ['storage', 'ssd'])
        if storage1 or storage2:
            winner, reason = self._compare_numeric_specs(storage1, storage2, product1.name, product2.name, "Storage")
            advantages['Storage'] = {'winner': winner, 'reason': reason}
        
        # Compare Battery
        battery1 = self._find_spec_value(specs1, ['battery'])
        battery2 = self._find_spec_value(specs2, ['battery'])
        if battery1 or battery2:
            winner, reason = self._compare_numeric_specs(battery1, battery2, product1.name, product2.name, "Battery")
            advantages['Battery'] = {'winner': winner, 'reason': reason}
        
        # Compare Processor
        proc1 = self._find_spec_value(specs1, ['processor', 'cpu'])
        proc2 = self._find_spec_value(specs2, ['processor', 'cpu'])
        if proc1 and proc2:
            # Qualitative comparison based on known processor rankings
            proc1_score = self._rate_processor(proc1)
            proc2_score = self._rate_processor(proc2)
            
            if proc1_score > proc2_score:
                advantages['Processor'] = {'winner': 1, 'reason': f"{product1.name} has a more powerful processor"}
            elif proc2_score > proc1_score:
                advantages['Processor'] = {'winner': 2, 'reason': f"{product2.name} has a more powerful processor"}
            else:
                advantages['Processor'] = {'winner': 0, 'reason': "Similar processor performance"}
        
        # Brand reputation (if different brands)
        if product1.brand_id != product2.brand_id:
            advantages['Brand'] = {
                'winner': 0,
                'reason': f"Different brands: {product1.brand.name} vs {product2.brand.name} - personal preference"
            }
        
        return advantages
    
    def calculate_overall_score(self, product: Product, user_preferences: Dict[str, Any]) -> float:
        """
        Assign weighted score for recommendation (0-100)
        
        Args:
            product: Product to score
            user_preferences: User preferences for weighted scoring
        
        Returns:
            Overall score from 0 to 100
        """
        score = 50.0  # Base score
        category_name = product.category.name.lower()
        
        # Budget alignment (weight: 25%)
        budget = user_preferences.get('budget')
        if budget:
            try:
                budget_float = float(budget)
                price_float = float(product.price)
                
                if price_float <= budget_float:
                    # Within budget: higher score for better value
                    budget_ratio = price_float / budget_float
                    score += 25 * (1 - abs(budget_ratio - 0.8))  # Optimal at 80% of budget
                else:
                    # Over budget: penalty
                    score -= 15
            except (ValueError, TypeError):
                pass
        
        # Specification quality (weight: 40%)
        spec_score = 0
        for spec in product.specifications:
            key_lower = spec.spec_key.lower()
            
            # RAM scoring
            if 'ram' in key_lower:
                ram_value = self._extract_number(spec.spec_value)
                if ram_value:
                    benchmark = self.benchmarks.get(category_name, {}).get('ram', {})
                    if ram_value >= benchmark.get('excellent', 16):
                        spec_score += 10
                    elif ram_value >= benchmark.get('good', 8):
                        spec_score += 6
                    else:
                        spec_score += 2
            
            # Storage scoring
            if 'storage' in key_lower or 'ssd' in key_lower:
                storage_value = self._extract_number(spec.spec_value)
                if storage_value:
                    benchmark = self.benchmarks.get(category_name, {}).get('storage', {})
                    if storage_value >= benchmark.get('excellent', 512):
                        spec_score += 10
                    elif storage_value >= benchmark.get('good', 256):
                        spec_score += 6
                    else:
                        spec_score += 2
            
            # Premium features
            value_lower = spec.spec_value.lower()
            if any(keyword in value_lower for keyword in ['oled', 'amoled', '5g', 'wifi 6', 'rtx', 'm1', 'm2']):
                spec_score += 5
        
        score += min(40, spec_score)  # Cap at 40 points
        
        # Brand preference (weight: 10%)
        preferred_brand = user_preferences.get('preferred_brand')
        if preferred_brand and product.brand.name.lower() == preferred_brand.lower():
            score += 10
        
        # Usage type alignment (weight: 15%)
        usage_type = user_preferences.get('usage_type', '').lower()
        if usage_type == 'gaming':
            has_good_graphics = any('dedicated' in s.spec_value.lower() or 'nvidia' in s.spec_value.lower() 
                                   for s in product.specifications if 'graphics' in s.spec_key.lower())
            if has_good_graphics:
                score += 15
        elif usage_type in ['business', 'professional']:
            has_good_ram = any(self._extract_number(s.spec_value, 0) >= 16 
                              for s in product.specifications if 'ram' in s.spec_key.lower())
            if has_good_ram:
                score += 15
        
        # Normalize to 0-100 range
        return max(0, min(100, score))
    
    # Helper methods
    
    def _extract_number(self, text: str, default: float = None) -> float:
        """Extract first number from text string"""
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                pass
        return default
    
    def _find_spec_value(self, specs_dict: Dict, keywords: List[str]) -> str:
        """Find specification value by keyword match"""
        for key, value in specs_dict.items():
            if any(keyword in key for keyword in keywords):
                return value
        return None
    
    def _compare_numeric_specs(
        self, 
        value1: str, 
        value2: str, 
        name1: str, 
        name2: str, 
        spec_name: str
    ) -> Tuple[int, str]:
        """Compare two numeric specifications and return winner"""
        if not value1 and not value2:
            return 0, f"Neither product lists {spec_name}"
        if not value1:
            return 2, f"{name2} lists {spec_name}: {value2}"
        if not value2:
            return 1, f"{name1} lists {spec_name}: {value1}"
        
        num1 = self._extract_number(value1, 0)
        num2 = self._extract_number(value2, 0)
        
        if num1 > num2:
            return 1, f"{name1} has more {spec_name}: {value1} vs {value2}"
        elif num2 > num1:
            return 2, f"{name2} has more {spec_name}: {value2} vs {value1}"
        else:
            return 0, f"Both have equal {spec_name}: {value1}"
    
    def _rate_processor(self, processor_name: str) -> int:
        """Rate processor performance based on model name"""
        processor_lower = processor_name.lower()
        
        # Intel ratings
        if 'i9' in processor_lower or 'ultra 9' in processor_lower:
            return 9
        if 'i7' in processor_lower or 'ultra 7' in processor_lower:
            return 7
        if 'i5' in processor_lower or 'ultra 5' in processor_lower:
            return 5
        if 'i3' in processor_lower:
            return 3
        
        # AMD ratings
        if 'ryzen 9' in processor_lower:
            return 9
        if 'ryzen 7' in processor_lower:
            return 7
        if 'ryzen 5' in processor_lower:
            return 5
        
        # Apple ratings
        if 'm3' in processor_lower:
            return 9
        if 'm2' in processor_lower:
            return 8
        if 'm1' in processor_lower:
            return 7
        
        # Qualcomm Snapdragon (mobile)
        if 'snapdragon 8' in processor_lower or 'snapdragon 888' in processor_lower:
            return 8
        if 'snapdragon 7' in processor_lower:
            return 6
        
        return 5  # Default middle rating
    
    def _generate_winner_reason(
        self, 
        product1: Product, 
        product2: Product, 
        score1: float, 
        score2: float, 
        comparative_advantages: Dict
    ) -> str:
        """Generate explanation for why one product is recommended over the other"""
        score_diff = abs(score1 - score2)
        
        if score_diff < 5:
            return "Both products are very closely matched. Your final choice may come down to personal preference or brand loyalty."
        
        winner_product = product1 if score1 > score2 else product2
        winner_name = winner_product.name
        
        # Count advantages
        advantages_count = sum(1 for adv in comparative_advantages.values() 
                              if adv['winner'] == (1 if score1 > score2 else 2))
        
        if advantages_count >= 3:
            return f"{winner_name} is the recommended choice, winning in {advantages_count} key categories including performance, features, and value."
        elif score1 > score2 and float(product1.price) < float(product2.price):
            return f"{winner_name} offers better value for money with comparable or superior features at a lower price point."
        elif score2 > score1 and float(product2.price) < float(product1.price):
            return f"{winner_name} provides excellent value with strong performance at a more competitive price."
        else:
            return f"{winner_name} edges ahead with a better overall balance of features, performance, and price."
