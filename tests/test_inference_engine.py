"""
Unit tests for Inference Engine
Tests the forward chaining logic and rule matching
"""
import pytest
from app.services.inference_engine import InferenceEngine


@pytest.mark.unit
class TestInferenceEngine:
    """Test cases for InferenceEngine"""
    
    def test_add_fact(self):
        """Test adding facts to working memory"""
        engine = InferenceEngine()
        engine.add_fact('budget', 1000)
        engine.add_fact('usage_type', 'gaming')
        
        assert engine.working_memory['budget'] == 1000
        assert engine.working_memory['usage_type'] == 'gaming'
    
    def test_evaluate_condition_equals(self):
        """Test equals operator"""
        engine = InferenceEngine()
        facts = {'usage_type': 'gaming'}
        
        # Mock condition object
        class MockCondition:
            condition_key = 'usage_type'
            operator = 'equals'
            condition_value = 'gaming'
        
        assert engine.evaluate_condition(MockCondition(), facts) is True
        
        MockCondition.condition_value = 'work'
        assert engine.evaluate_condition(MockCondition(), facts) is False
    
    def test_evaluate_condition_greater_than(self):
        """Test greater_than operator"""
        engine = InferenceEngine()
        facts = {'budget': 1000}
        
        class MockCondition:
            condition_key = 'budget'
            operator = 'greater_than'
            condition_value = '500'
        
        assert engine.evaluate_condition(MockCondition(), facts) is True
        
        MockCondition.condition_value = '1500'
        assert engine.evaluate_condition(MockCondition(), facts) is False
    
    def test_evaluate_condition_less_equal(self):
        """Test less_equal operator"""
        engine = InferenceEngine()
        facts = {'budget': 800}
        
        class MockCondition:
            condition_key = 'budget'
            operator = 'less_equal'
            condition_value = '800'
        
        assert engine.evaluate_condition(MockCondition(), facts) is True
        
        MockCondition.condition_value = '700'
        assert engine.evaluate_condition(MockCondition(), facts) is False
    
    def test_evaluate_condition_in_operator(self):
        """Test 'in' operator for multiple values"""
        engine = InferenceEngine()
        facts = {'usage_type': 'gaming'}
        
        class MockCondition:
            condition_key = 'usage_type'
            operator = 'in'
            condition_value = 'gaming, work, study'
        
        assert engine.evaluate_condition(MockCondition(), facts) is True
        
        facts['usage_type'] = 'creative'
        assert engine.evaluate_condition(MockCondition(), facts) is False
    
    def test_infer_with_rules(self, sample_rules, sample_categories):
        """Test inference with actual rules from database"""
        engine = InferenceEngine()
        
        smartphone_id = sample_categories['smartphone'].id
        
        user_inputs = {
            'category_id': smartphone_id,
            'usage_type': 'gaming',
            'budget': 500
        }
        
        matched_rules = engine.infer(user_inputs)
        
        assert len(matched_rules) > 0
        assert matched_rules[0].name == 'Gaming Smartphone'
    
    def test_infer_category_filtering(self, sample_rules, sample_categories):
        """Test that rules are filtered by category"""
        engine = InferenceEngine()
        
        smartphone_id = sample_categories['smartphone'].id
        
        user_inputs = {
            'category_id': smartphone_id,
            'usage_type': 'work',  # This won't match gaming rules
            'budget': 500
        }
        
        matched_rules = engine.infer(user_inputs)
        
        # Should not match laptop work rule
        for rule in matched_rules:
            assert rule.category_id == smartphone_id or rule.category_id is None
    
    def test_rule_priority_sorting(self, sample_rules, sample_categories):
        """Test that rules are sorted by priority"""
        engine = InferenceEngine()
        
        smartphone_id = sample_categories['smartphone'].id
        
        user_inputs = {
            'category_id': smartphone_id,
            'usage_type': 'gaming',
            'budget': 500
        }
        
        matched_rules = engine.infer(user_inputs)
        
        # Verify sorted descending by priority
        if len(matched_rules) > 1:
            for i in range(len(matched_rules) - 1):
                assert matched_rules[i].priority >= matched_rules[i+1].priority
