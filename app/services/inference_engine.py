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
            if operator == '==':
                return str(actual).lower() == str(expected).lower()
            elif operator == '!=':
                return str(actual).lower() != str(expected).lower()
            elif operator == '<':
                return float(actual) < float(expected)
            elif operator == '>':
                return float(actual) > float(expected)
            elif operator == '<=':
                return float(actual) <= float(expected)
            elif operator == '>=':
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
            
            all_conditions_met = True
            for condition in rule.conditions:
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
        
        # Get all active rules
        rules = Rule.query.filter_by(is_active=True).all()
        
        # Match rules against facts
        self.matched_rules = self.match_rules(rules, self.working_memory)
        
        return self.matched_rules
