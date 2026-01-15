from app.models.rule import Rule, RuleCondition
from app.models.product import Product, Category, Brand


class InferenceEngine:
    """Forward chaining inference engine for expert system"""
    
    def __init__(self):
        self.working_memory = {}
        self.matched_rules = []
    
    def add_fact(self, key, value):
        """Add user input to working memory"""
        self.working_memory[key] = value
    
    def evaluate_condition(self, condition, facts):
        """Evaluate a single rule condition against facts"""
        key = condition.condition_key
        operator = condition.operator
        expected = condition.condition_value
        actual = facts.get(key)
        
        if actual is None:
            return False
        
        try:
            # Map operator names to symbols for comparison
            if operator == 'equals' or operator == '==':
                return str(actual).lower() == str(expected).lower()
            elif operator == 'not_equals' or operator == '!=':
                return str(actual).lower() != str(expected).lower()
            elif operator == 'less_than' or operator == '<':
                return float(actual) < float(expected)
            elif operator == 'greater_than' or operator == '>':
                return float(actual) > float(expected)
            elif operator == 'less_equal' or operator == '<=':
                return float(actual) <= float(expected)
            elif operator == 'greater_equal' or operator == '>=':
                return float(actual) >= float(expected)
            elif operator == 'in':
                return str(actual).lower() in [v.strip().lower() for v in expected.split(',')]
            elif operator == 'contains':
                return expected.lower() in str(actual).lower()
        except (ValueError, TypeError):
            return False
        
        return False
    
    def match_rules(self, rules, facts):
        """Match all rules against current facts"""
        matched = []
        
        for rule in rules:
            if not rule.is_active:
                continue
            
            # Convert to list to get count and iterate
            conditions_list = list(rule.conditions)
            all_conditions_met = True
            for condition in conditions_list:
                if not self.evaluate_condition(condition, facts):
                    all_conditions_met = False
                    break
            
            if all_conditions_met:
                matched.append(rule)
        
        # Sort by priority (highest first)
        return sorted(matched, key=lambda r: r.priority, reverse=True)
    
    def infer(self, user_inputs):
        """Run inference engine with user inputs"""
        # Clear previous state
        self.working_memory = {}
        self.matched_rules = []
        
        # Add user inputs to working memory
        for key, value in user_inputs.items():
            self.add_fact(key, value)
        
        # Get all active rules, filtered by category if specified
        query = Rule.query.filter_by(is_active=True)
        
        # If user specified a category, only get rules for that category
        if 'category_id' in user_inputs and user_inputs['category_id']:
            query = query.filter(
                (Rule.category_id == user_inputs['category_id']) | 
                (Rule.category_id == None)  # Include generic rules with no category
            )
        
        rules = query.all()
        
        # Match rules against facts
        self.matched_rules = self.match_rules(rules, self.working_memory)
        
        return self.matched_rules
