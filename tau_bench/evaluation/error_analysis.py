# Copyright Sierra

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel
from enum import Enum
import re


class ErrorCategory(str, Enum):
    """Hierarchical error categorization"""
    # Top level categories
    POLICY_INTERPRETATION = "policy_interpretation"
    TOOL_USAGE = "tool_usage"
    CONVERSATION_FLOW = "conversation_flow"
    CONTEXT_UNDERSTANDING = "context_understanding"
    SYSTEM_ERROR = "system_error"
    
    # Policy interpretation subcategories
    RIGID_INTERPRETATION = "rigid_interpretation"
    CONTEXT_MISUNDERSTANDING = "context_misunderstanding"
    POLICY_VIOLATION = "policy_violation"
    
    # Tool usage subcategories
    WRONG_ARGUMENTS = "wrong_arguments"
    MISSING_TOOLS = "missing_tools"
    TOOL_FAILURE = "tool_failure"
    
    # Conversation flow subcategories
    PREMATURE_TRANSFER = "premature_transfer"
    GOAL_PARTIAL_COMPLETION = "goal_partial_completion"
    INEFFICIENT_FLOW = "inefficient_flow"
    
    # Context understanding subcategories
    USER_INTENT_MISUNDERSTANDING = "user_intent_misunderstanding"
    AMBIGUOUS_REQUEST_HANDLING = "ambiguous_request_handling"
    
    # System error subcategories
    RUNTIME_ERROR = "runtime_error"
    ENVIRONMENT_ERROR = "environment_error"


class ErrorSeverity(str, Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorAnalysis(BaseModel):
    """Detailed error analysis for a task"""
    category: ErrorCategory
    subcategory: Optional[str] = None
    severity: ErrorSeverity
    description: str
    root_cause: str
    suggested_fix: str
    confidence: float  # 0.0 to 1.0


class ErrorAnalyzer:
    """Enhanced error analysis and categorization system"""
    
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
        
    def _initialize_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize patterns for error detection"""
        return {
            "policy_rigid": {
                "patterns": [
                    r"based on our policies",
                    r"unfortunately.*cannot",
                    r"not possible.*policy",
                    r"against.*policy"
                ],
                "category": ErrorCategory.RIGID_INTERPRETATION,
                "severity": ErrorSeverity.MEDIUM
            },
            "premature_transfer": {
                "patterns": [
                    r"transfer.*human",
                    r"human agent",
                    r"escalate.*case"
                ],
                "category": ErrorCategory.PREMATURE_TRANSFER,
                "severity": ErrorSeverity.HIGH
            },
            "tool_failure": {
                "patterns": [
                    r"error.*tool",
                    r"failed.*call",
                    r"tool.*not.*found"
                ],
                "category": ErrorCategory.TOOL_FAILURE,
                "severity": ErrorSeverity.MEDIUM
            },
            "context_confusion": {
                "patterns": [
                    r"i.*not.*understand",
                    r"unclear.*request",
                    r"could.*clarify"
                ],
                "category": ErrorCategory.USER_INTENT_MISUNDERSTANDING,
                "severity": ErrorSeverity.MEDIUM
            },
            "policy_violation": {
                "patterns": [
                    r"i.*recommend",
                    r"you.*should",
                    r"better.*to",
                    r"i.*think.*you"
                ],
                "category": ErrorCategory.POLICY_VIOLATION,
                "severity": ErrorSeverity.LOW
            }
        }
    
    def analyze_error(self, 
                     binary_reward: float,
                     conversation: List[Dict[str, Any]], 
                     task_actions: List[Dict[str, Any]],
                     actual_actions: List[Dict[str, Any]],
                     error_info: Optional[Dict[str, Any]] = None) -> List[ErrorAnalysis]:
        """Analyze errors in a task and return detailed error analysis"""
        
        if binary_reward == 1.0:
            return []  # No errors for successful tasks
            
        errors = []
        
        # Analyze conversation for error patterns
        conversation_errors = self._analyze_conversation_errors(conversation)
        errors.extend(conversation_errors)
        
        # Analyze action sequence errors
        action_errors = self._analyze_action_errors(task_actions, actual_actions)
        errors.extend(action_errors)
        
        # Analyze tool usage errors
        tool_errors = self._analyze_tool_errors(actual_actions, conversation)
        errors.extend(tool_errors)
        
        # Analyze goal completion errors
        goal_errors = self._analyze_goal_completion_errors(task_actions, actual_actions, conversation)
        errors.extend(goal_errors)
        
        # Analyze system errors if present
        if error_info and 'error' in error_info:
            system_errors = self._analyze_system_errors(error_info)
            errors.extend(system_errors)
            
        return errors
    
    def _analyze_conversation_errors(self, conversation: List[Dict[str, Any]]) -> List[ErrorAnalysis]:
        """Analyze conversation for error patterns"""
        errors = []
        
        for message in conversation:
            if message.get('role') == 'assistant':
                content = message.get('content', '')
                
                # Check for error patterns
                for error_type, error_config in self.error_patterns.items():
                    for pattern in error_config['patterns']:
                        if re.search(pattern, content, re.IGNORECASE):
                            errors.append(ErrorAnalysis(
                                category=error_config['category'],
                                severity=error_config['severity'],
                                description=f"Detected {error_type} pattern in conversation",
                                root_cause=f"Pattern '{pattern}' matched in assistant response",
                                suggested_fix=self._get_suggested_fix(error_type),
                                confidence=0.8
                            ))
                            
        return errors
    
    def _analyze_action_errors(self, task_actions: List[Dict[str, Any]], 
                             actual_actions: List[Dict[str, Any]]) -> List[ErrorAnalysis]:
        """Analyze action sequence for errors"""
        errors = []
        
        if not task_actions or not actual_actions:
            return errors
            
        # Check for missing required actions
        task_action_names = {action.get('name', '') for action in task_actions}
        actual_action_names = {action.get('name', '') for action in actual_actions}
        
        missing_actions = task_action_names - actual_action_names
        if missing_actions:
            errors.append(ErrorAnalysis(
                category=ErrorCategory.MISSING_TOOLS,
                severity=ErrorSeverity.HIGH,
                description=f"Missing required actions: {list(missing_actions)}",
                root_cause="Agent failed to execute all required actions",
                suggested_fix="Ensure all required actions are executed in correct sequence",
                confidence=0.9
            ))
            
        # Check for wrong actions
        wrong_actions = actual_action_names - task_action_names
        if wrong_actions:
            errors.append(ErrorAnalysis(
                category=ErrorCategory.WRONG_ARGUMENTS,
                severity=ErrorSeverity.MEDIUM,
                description=f"Executed unnecessary actions: {list(wrong_actions)}",
                root_cause="Agent executed actions not required for the task",
                suggested_fix="Review task requirements and only execute necessary actions",
                confidence=0.8
            ))
            
        return errors
    
    def _analyze_tool_errors(self, actual_actions: List[Dict[str, Any]], 
                           conversation: List[Dict[str, Any]]) -> List[ErrorAnalysis]:
        """Analyze tool usage for errors"""
        errors = []
        
        # Check for tool call failures in conversation
        for message in conversation:
            if message.get('role') == 'tool':
                content = message.get('content', '')
                if 'error' in content.lower() or 'failed' in content.lower():
                    errors.append(ErrorAnalysis(
                        category=ErrorCategory.TOOL_FAILURE,
                        severity=ErrorSeverity.MEDIUM,
                        description=f"Tool call failed: {content[:100]}...",
                        root_cause="Tool execution returned an error",
                        suggested_fix="Check tool parameters and retry with correct arguments",
                        confidence=0.9
                    ))
                    
        return errors
    
    def _analyze_goal_completion_errors(self, task_actions: List[Dict[str, Any]], 
                                      actual_actions: List[Dict[str, Any]],
                                      conversation: List[Dict[str, Any]]) -> List[ErrorAnalysis]:
        """Analyze goal completion errors"""
        errors = []
        
        # Check if task was partially completed
        if task_actions and actual_actions:
            task_action_names = {action.get('name', '') for action in task_actions}
            actual_action_names = {action.get('name', '') for action in actual_actions}
            
            matching_actions = len(task_action_names.intersection(actual_action_names))
            total_required = len(task_action_names)
            
            if matching_actions > 0 and matching_actions < total_required:
                completion_ratio = matching_actions / total_required
                
                errors.append(ErrorAnalysis(
                    category=ErrorCategory.GOAL_PARTIAL_COMPLETION,
                    severity=ErrorSeverity.HIGH if completion_ratio < 0.5 else ErrorSeverity.MEDIUM,
                    description=f"Task partially completed ({completion_ratio:.1%} of required actions)",
                    root_cause="Agent failed to complete all required actions",
                    suggested_fix="Review task requirements and ensure all actions are completed",
                    confidence=0.9
                ))
                
        return errors
    
    def _analyze_system_errors(self, error_info: Dict[str, Any]) -> List[ErrorAnalysis]:
        """Analyze system errors"""
        errors = []
        
        error_message = error_info.get('error', '')
        traceback_info = error_info.get('traceback', '')
        
        errors.append(ErrorAnalysis(
            category=ErrorCategory.RUNTIME_ERROR,
            severity=ErrorSeverity.CRITICAL,
            description=f"System error occurred: {error_message}",
            root_cause="Runtime exception during task execution",
            suggested_fix="Check system configuration and error handling",
            confidence=1.0
        ))
        
        return errors
    
    def _get_suggested_fix(self, error_type: str) -> str:
        """Get suggested fix for error type"""
        fixes = {
            "policy_rigid": "Review policy interpretation and consider edge cases",
            "premature_transfer": "Try alternative approaches before transferring to human",
            "tool_failure": "Verify tool parameters and retry with correct arguments",
            "context_confusion": "Ask clarifying questions to better understand user intent",
            "policy_violation": "Avoid subjective recommendations and stick to facts"
        }
        return fixes.get(error_type, "Review and improve error handling")
    
    def get_error_summary(self, errors: List[ErrorAnalysis]) -> Dict[str, Any]:
        """Get summary statistics for errors"""
        if not errors:
            return {"total_errors": 0, "by_category": {}, "by_severity": {}}
            
        by_category = {}
        by_severity = {}
        
        for error in errors:
            category = error.category.value
            severity = error.severity.value
            
            by_category[category] = by_category.get(category, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
            
        return {
            "total_errors": len(errors),
            "by_category": by_category,
            "by_severity": by_severity,
            "most_common_category": max(by_category.items(), key=lambda x: x[1])[0] if by_category else None,
            "most_common_severity": max(by_severity.items(), key=lambda x: x[1])[0] if by_severity else None
        }
