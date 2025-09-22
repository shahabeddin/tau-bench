# Copyright Sierra

from typing import Dict, Any, List, Optional, ClassVar
from pydantic import BaseModel
import re
import time


class CompositeScore(BaseModel):
    """Composite performance score with multiple dimensions"""
    task_completion: float  # 0.0 to 1.0 - Did the task get completed?
    efficiency: float       # 0.0 to 1.0 - How efficiently was it completed?
    policy_adherence: float # 0.0 to 1.0 - Did it follow policies correctly?
    user_satisfaction: float # 0.0 to 1.0 - Was the conversation helpful?
    overall_score: float    # Weighted composite score
    
    # Weights for composite scoring
    TASK_COMPLETION_WEIGHT: ClassVar[float] = 0.4
    EFFICIENCY_WEIGHT: ClassVar[float] = 0.3
    POLICY_ADHERENCE_WEIGHT: ClassVar[float] = 0.2
    USER_SATISFACTION_WEIGHT: ClassVar[float] = 0.1


class CompositeScorer:
    """Enhanced scoring system that replaces binary 0/1 with composite scores"""
    
    def __init__(self):
        self.start_time = None
        self.tool_calls = []
        self.conversation_turns = 0
        self.transfer_to_human = False
        self.efficiency_tracker = None  # Will be set by the enhanced evaluator
        
    def start_evaluation(self):
        """Start timing for efficiency metrics"""
        self.start_time = time.time()
        self.tool_calls = []
        self.conversation_turns = 0
        self.transfer_to_human = False
        
    def record_tool_call(self, tool_name: str, success: bool = True):
        """Record a tool call for efficiency analysis"""
        self.tool_calls.append({
            'name': tool_name,
            'success': success,
            'timestamp': time.time()
        })
        
    def record_turn(self, message: Dict[str, Any]):
        """Record a conversation turn"""
        self.conversation_turns += 1
        
        # Check for transfer to human
        if message.get('role') == 'assistant':
            content = message.get('content', '')
            if content and isinstance(content, str):
                if 'transfer_to_human' in content.lower() or 'human agent' in content.lower():
                    self.transfer_to_human = True
                
    def calculate_composite_score(self, 
                                binary_reward: float, 
                                task_actions: List[Dict[str, Any]], 
                                actual_actions: List[Dict[str, Any]],
                                conversation: List[Dict[str, Any]]) -> CompositeScore:
        """Calculate composite performance score"""
        
        # 1. Task Completion Score (0.0 to 1.0)
        task_completion = self._calculate_task_completion(binary_reward, task_actions, actual_actions)
        
        # 2. Efficiency Score (0.0 to 1.0) - use pre-calculated efficiency from tracker
        efficiency = self._calculate_efficiency_score_from_tracker()
        
        # 3. Policy Adherence Score (0.0 to 1.0)
        policy_adherence = self._calculate_policy_adherence(conversation, actual_actions)
        
        # 4. User Satisfaction Score (0.0 to 1.0)
        user_satisfaction = self._calculate_user_satisfaction(conversation)
        
        # 5. Calculate weighted composite score
        overall_score = (
            task_completion * CompositeScore.TASK_COMPLETION_WEIGHT +
            efficiency * CompositeScore.EFFICIENCY_WEIGHT +
            policy_adherence * CompositeScore.POLICY_ADHERENCE_WEIGHT +
            user_satisfaction * CompositeScore.USER_SATISFACTION_WEIGHT
        )
        
        return CompositeScore(
            task_completion=task_completion,
            efficiency=efficiency,
            policy_adherence=policy_adherence,
            user_satisfaction=user_satisfaction,
            overall_score=overall_score
        )
    
    def _calculate_task_completion(self, binary_reward: float, 
                                 task_actions: List[Dict[str, Any]], 
                                 actual_actions: List[Dict[str, Any]]) -> float:
        """Calculate how well the task was completed (0.0 to 1.0)"""
        if binary_reward == 1.0:
            return 1.0
            
        # For failed tasks, calculate partial completion
        if not task_actions or not actual_actions:
            return 0.0
            
        # Count matching actions
        task_action_names = {action.get('name', '') for action in task_actions}
        actual_action_names = {action.get('name', '') for action in actual_actions}
        
        # Calculate overlap
        matching_actions = len(task_action_names.intersection(actual_action_names))
        total_required = len(task_action_names)
        
        if total_required == 0:
            return 0.0
            
        completion_ratio = matching_actions / total_required
        
        # Apply penalty for wrong actions
        wrong_actions = len(actual_action_names - task_action_names)
        penalty = min(0.5, wrong_actions * 0.1)  # Max 50% penalty
        
        return max(0.0, completion_ratio - penalty)
    
    def _calculate_efficiency_score(self, conversation: List[Dict[str, Any]]) -> float:
        """Calculate efficiency based on conversation length and tool usage (0.0 to 1.0)"""
        if not conversation:
            return 0.0
            
        # Base efficiency on conversation length (shorter is better)
        # Typical good conversation: 10-30 turns
        # Penalty for very long conversations
        turn_count = len(conversation)
        
        if turn_count <= 20:
            length_score = 1.0
        elif turn_count <= 40:
            length_score = 0.8
        elif turn_count <= 60:
            length_score = 0.6
        else:
            length_score = 0.4
            
        # Tool usage efficiency
        tool_call_count = len(self.tool_calls)
        if tool_call_count == 0:
            tool_score = 0.5  # Neutral for no tool calls
        elif tool_call_count <= 10:
            tool_score = 1.0
        elif tool_call_count <= 20:
            tool_score = 0.8
        else:
            tool_score = 0.6
            
        # Transfer to human penalty
        transfer_penalty = 0.3 if self.transfer_to_human else 0.0
        
        return max(0.0, (length_score + tool_score) / 2 - transfer_penalty)
    
    def _calculate_policy_adherence(self, conversation: List[Dict[str, Any]], 
                                  actual_actions: List[Dict[str, Any]]) -> float:
        """Calculate how well policies were followed (0.0 to 1.0)"""
        if not conversation:
            return 0.0
            
        score = 1.0
        
        # Check for policy violations in conversation
        for message in conversation:
            if message.get('role') == 'assistant':
                content = message.get('content', '')
                if not content or not isinstance(content, str):
                    continue
                content = content.lower()
                
                # Penalty for making up information
                if any(phrase in content for phrase in [
                    'i think', 'i believe', 'probably', 'might be', 'could be'
                ]):
                    score -= 0.1
                    
                # Penalty for subjective recommendations
                if any(phrase in content for phrase in [
                    'i recommend', 'you should', 'i suggest', 'better to'
                ]):
                    score -= 0.1
                    
                # Penalty for providing information not from tools
                if 'based on our records' in content and not self.tool_calls:
                    score -= 0.2
                    
        # Check for proper confirmation before consequential actions
        consequential_actions = ['exchange_delivered_order_items', 'return_delivered_order_items', 
                               'modify_pending_order_items', 'cancel_pending_order']
        
        for action in actual_actions:
            if action.get('name') in consequential_actions:
                # Check if there was confirmation in previous messages
                confirmed = False
                for message in conversation[-5:]:  # Check last 5 messages
                    if message.get('role') == 'user':
                        content = message.get('content', '')
                        if content and isinstance(content, str) and 'yes' in content.lower():
                            confirmed = True
                            break
                        
                if not confirmed:
                    score -= 0.2
                    
        return max(0.0, score)
    
    def _calculate_user_satisfaction(self, conversation: List[Dict[str, Any]]) -> float:
        """Calculate user satisfaction based on conversation quality (0.0 to 1.0)"""
        if not conversation:
            return 0.0
            
        score = 1.0
        
        # Check for helpful and clear communication
        for message in conversation:
            if message.get('role') == 'assistant':
                content = message.get('content', '')
                if not content or not isinstance(content, str):
                    continue
                content = content.lower()
                
                # Positive indicators
                if any(phrase in content for phrase in [
                    'i can help', 'let me assist', 'i understand', 'thank you'
                ]):
                    score += 0.05
                    
                # Negative indicators
                if any(phrase in content for phrase in [
                    'i cannot', 'unable to', 'not possible', 'sorry, but'
                ]):
                    score -= 0.1
                    
                # Check for clear explanations
                if len(content) < 20:  # Very short responses
                    score -= 0.1
                elif len(content) > 500:  # Very long responses
                    score -= 0.05
                    
        # Penalty for transfer to human without trying
        if self.transfer_to_human and len(conversation) < 10:
            score -= 0.3
            
        return max(0.0, min(1.0, score))
    
    def _calculate_efficiency_score_from_tracker(self) -> float:
        """Calculate efficiency score using the efficiency tracker data"""
        if not self.efficiency_tracker:
            return 0.5  # Default neutral score
        
        metrics = self.efficiency_tracker.calculate_metrics()
        return metrics.overall_efficiency
