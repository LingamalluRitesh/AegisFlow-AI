"""
Complex Event Processing (CEP) Deterministic Rule Engine
Evaluates dynamic boolean AST expressions against transaction payloads and hydrated feature vectors.
"""

import re
import operator
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from backend.core.types import ActionType
from backend.core.logging import get_logger

logger = get_logger("fraud.rule_engine")


class OperatorType(str):
    EQ = "=="
    NE = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    IN = "IN"
    NOT_IN = "NOT_IN"
    CONTAINS = "CONTAINS"
    REGEX = "REGEX"


_OP_FUNCS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "IN": lambda val, target_list: val in target_list,
    "NOT_IN": lambda val, target_list: val not in target_list,
    "CONTAINS": lambda val, substr: substr in str(val),
    "REGEX": lambda val, pattern: bool(re.search(pattern, str(val))),
}


class Condition(BaseModel):
    field: str = Field(..., description="Target feature or payload field, e.g. tx_count_5m")
    operator: str = Field(..., description="Comparison operator (==, >, <, IN, etc.)")
    value: Any = Field(..., description="Threshold or comparison target")

    def evaluate(self, context: Dict[str, Any]) -> bool:
        if self.field not in context:
            return False
        field_val = context[self.field]
        if field_val is None:
            return False

        op_func = _OP_FUNCS.get(self.operator.upper())
        if not op_func:
            return False

        try:
            if isinstance(self.value, (int, float)) and isinstance(field_val, (int, float)):
                return op_func(float(field_val), float(self.value))
            return op_func(field_val, self.value)
        except Exception:
            return False


class Rule(BaseModel):
    rule_id: str
    name: str
    description: str
    priority: int = 100
    conditions: List[Condition]
    action: ActionType = ActionType.BLOCK
    risk_score_boost: float = 0.5
    is_active: bool = True

    def evaluate(self, context: Dict[str, Any]) -> bool:
        if not self.is_active or not self.conditions:
            return False
        return all(cond.evaluate(context) for cond in self.conditions)


class ComplexEventRuleEngine:
    def __init__(self):
        self._rules: Dict[str, Rule] = {}

    def register_rule(self, rule: Rule) -> None:
        self._rules[rule.rule_id] = rule
        logger.info_ctx(f"Registered Fraud Rule: [{rule.rule_id}] {rule.name}")

    def evaluate_rules(self, context: Dict[str, Any]) -> List[Rule]:
        matched = []
        sorted_rules = sorted(self._rules.values(), key=lambda r: r.priority)
        for rule in sorted_rules:
            if rule.evaluate(context):
                matched.append(rule)
        return matched
