# Copyright Sierra

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import time
import json


class EfficiencyMetrics(BaseModel):
    """Efficiency and resource consumption metrics"""
    # Timing metrics
    total_duration: float  # Total time in seconds
    avg_response_time: float  # Average time per response
    tool_call_duration: float  # Time spent on tool calls
    
    # Conversation metrics
    total_turns: int  # Total conversation turns
    avg_turns_per_task: float  # Average turns per task
    conversation_efficiency: float  # 0.0 to 1.0 efficiency score
    
    # Tool usage metrics
    total_tool_calls: int  # Total number of tool calls
    successful_tool_calls: int  # Number of successful tool calls
    tool_call_success_rate: float  # Success rate of tool calls
    tool_call_efficiency: float  # 0.0 to 1.0 efficiency score
    
    # Resource metrics
    total_tokens: int  # Total tokens used
    tokens_per_turn: float  # Average tokens per turn
    cost_estimate: float  # Estimated cost in USD
    
    # Transfer metrics
    transfer_to_human: bool  # Whether transferred to human
    transfer_rate: float  # Rate of transfers to human
    
    # Overall efficiency score
    overall_efficiency: float  # 0.0 to 1.0 overall efficiency


class EfficiencyTracker:
    """Track efficiency and resource metrics during evaluation"""
    
    def __init__(self):
        self.start_time = None
        self.tool_calls = []
        self.conversation_turns = 0
        self.total_tokens = 0
        self.transfer_to_human = False
        self.response_times = []
        self.current_response_start = None
        
    def start_evaluation(self):
        """Start tracking efficiency metrics"""
        self.start_time = time.time()
        self.tool_calls = []
        self.conversation_turns = 0
        self.total_tokens = 0
        self.transfer_to_human = False
        self.response_times = []
        self.current_response_start = None
        
    def start_response(self):
        """Start timing a response"""
        self.current_response_start = time.time()
        
    def end_response(self):
        """End timing a response"""
        if self.current_response_start:
            response_time = time.time() - self.current_response_start
            self.response_times.append(response_time)
            self.current_response_start = None
            
    def record_tool_call(self, tool_name: str, success: bool = True, 
                        duration: float = 0.0, tokens_used: int = 0):
        """Record a tool call"""
        # If no duration provided, estimate based on tool complexity
        if duration == 0.0:
            duration = self._estimate_tool_duration(tool_name)
            
        self.tool_calls.append({
            'name': tool_name,
            'success': success,
            'duration': duration,
            'tokens_used': tokens_used,
            'timestamp': time.time()
        })
        
    def record_turn(self, message: Dict[str, Any], tokens_used: int = 0, response_time: float = 0.0):
        """Record a conversation turn"""
        self.conversation_turns += 1
        
        # If no token count provided, estimate from content
        if tokens_used == 0:
            tokens_used = self._estimate_tokens(message)
        
        self.total_tokens += tokens_used
        
        # Record response time if provided
        if response_time > 0:
            self.response_times.append(response_time)
        elif message.get('role') == 'assistant':
            # Estimate response time based on content length (rough approximation)
            estimated_time = max(0.5, len(str(message.get('content', ''))) / 1000)  # ~1ms per character
            self.response_times.append(estimated_time)
        
        # Check for transfer to human
        if message.get('role') == 'assistant':
            content = message.get('content', '')
            if 'transfer_to_human' in content.lower() or 'human agent' in content.lower():
                self.transfer_to_human = True
                
    def calculate_metrics(self) -> EfficiencyMetrics:
        """Calculate comprehensive efficiency metrics"""
        
        if not self.start_time:
            return self._empty_metrics()
            
        total_duration = time.time() - self.start_time
        
        # Response time metrics
        avg_response_time = (
            sum(self.response_times) / len(self.response_times) 
            if self.response_times else 0.0
        )
        
        # Tool call metrics
        total_tool_calls = len(self.tool_calls)
        successful_tool_calls = sum(1 for call in self.tool_calls if call['success'])
        tool_call_success_rate = (
            successful_tool_calls / total_tool_calls 
            if total_tool_calls > 0 else 1.0
        )
        
        tool_call_duration = sum(call['duration'] for call in self.tool_calls)
        
        # Conversation efficiency
        conversation_efficiency = self._calculate_conversation_efficiency()
        
        # Tool call efficiency
        tool_call_efficiency = self._calculate_tool_call_efficiency()
        
        # Token metrics
        tokens_per_turn = self.total_tokens / self.conversation_turns if self.conversation_turns > 0 else 0
        
        # Cost estimation (rough estimate)
        cost_estimate = self._estimate_cost()
        
        # Overall efficiency score
        overall_efficiency = self._calculate_overall_efficiency(
            conversation_efficiency, tool_call_efficiency, tool_call_success_rate
        )
        
        return EfficiencyMetrics(
            total_duration=total_duration,
            avg_response_time=avg_response_time,
            tool_call_duration=tool_call_duration,
            total_turns=self.conversation_turns,
            avg_turns_per_task=self.conversation_turns,
            conversation_efficiency=conversation_efficiency,
            total_tool_calls=total_tool_calls,
            successful_tool_calls=successful_tool_calls,
            tool_call_success_rate=tool_call_success_rate,
            tool_call_efficiency=tool_call_efficiency,
            total_tokens=self.total_tokens,
            tokens_per_turn=tokens_per_turn,
            cost_estimate=cost_estimate,
            transfer_to_human=self.transfer_to_human,
            transfer_rate=1.0 if self.transfer_to_human else 0.0,
            overall_efficiency=overall_efficiency
        )
    
    def _calculate_conversation_efficiency(self) -> float:
        """Calculate conversation efficiency (0.0 to 1.0)"""
        if self.conversation_turns == 0:
            return 0.0
            
        # Optimal conversation length is 10-30 turns
        if self.conversation_turns <= 20:
            length_score = 1.0
        elif self.conversation_turns <= 40:
            length_score = 0.8
        elif self.conversation_turns <= 60:
            length_score = 0.6
        else:
            length_score = 0.4
            
        # Penalty for transfer to human
        transfer_penalty = 0.3 if self.transfer_to_human else 0.0
        
        return max(0.0, length_score - transfer_penalty)
    
    def _calculate_tool_call_efficiency(self) -> float:
        """Calculate tool call efficiency (0.0 to 1.0)"""
        if not self.tool_calls:
            return 0.5  # Neutral for no tool calls
            
        # Optimal tool call count is 5-15
        tool_count = len(self.tool_calls)
        if tool_count <= 10:
            count_score = 1.0
        elif tool_count <= 20:
            count_score = 0.8
        elif tool_count <= 30:
            count_score = 0.6
        else:
            count_score = 0.4
            
        # Success rate factor
        success_rate = sum(1 for call in self.tool_calls if call['success']) / len(self.tool_calls)
        
        return (count_score + success_rate) / 2
    
    def _estimate_cost(self) -> float:
        """Estimate cost based on token usage (rough estimate)"""
        # Rough cost estimation: $0.01 per 1K tokens
        return (self.total_tokens / 1000) * 0.01
    
    def _calculate_overall_efficiency(self, conversation_efficiency: float, 
                                    tool_call_efficiency: float, 
                                    tool_call_success_rate: float) -> float:
        """Calculate overall efficiency score"""
        return (conversation_efficiency * 0.4 + 
                tool_call_efficiency * 0.4 + 
                tool_call_success_rate * 0.2)
    
    def _estimate_tokens(self, message: Dict[str, Any]) -> int:
        """Estimate token count from message content"""
        content = message.get('content', '')
        if not content:
            return 0
            
        # Rough estimation: ~4 characters per token for English text
        # This is a simplified approximation
        char_count = len(str(content))
        
        # Add overhead for message structure and role
        role_overhead = 10  # "assistant: " or "user: " etc
        
        # Add overhead for tool calls if present
        tool_call_overhead = 0
        if 'tool_calls' in message and message['tool_calls']:
            tool_call_overhead = len(message['tool_calls']) * 50  # Rough estimate per tool call
            
        estimated_tokens = (char_count + role_overhead + tool_call_overhead) // 4
        return max(1, estimated_tokens)  # At least 1 token
    
    def _estimate_tool_duration(self, tool_name: str) -> float:
        """Estimate tool call duration based on tool complexity"""
        # Base duration estimates for different tool types
        tool_durations = {
            # Quick lookup tools
            'get_user_details': 0.1,
            'get_order_details': 0.1,
            'get_product_details': 0.1,
            'find_user_id_by_email': 0.1,
            'find_user_id_by_name_zip': 0.1,
            
            # Medium complexity tools
            'list_all_product_types': 0.3,
            'list_all_airports': 0.3,
            'search_direct_flight': 0.5,
            'search_onestop_flight': 0.5,
            
            # Complex database operations
            'exchange_delivered_order_items': 1.0,
            'return_delivered_order_items': 1.0,
            'modify_pending_order_items': 1.0,
            'modify_pending_order_address': 0.8,
            'modify_pending_order_payment': 0.8,
            'cancel_pending_order': 0.5,
            'book_reservation': 1.2,
            'update_reservation_flights': 1.0,
            'update_reservation_passengers': 0.8,
            'update_reservation_baggages': 0.8,
            'cancel_reservation': 0.5,
            
            # Communication tools
            'send_certificate': 0.5,
            'transfer_to_human_agents': 0.2,
            
            # Calculation tools
            'calculate': 0.1,
            'think': 0.1,
        }
        
        return tool_durations.get(tool_name, 0.5)  # Default 0.5 seconds for unknown tools
    
    def _empty_metrics(self) -> EfficiencyMetrics:
        """Return empty metrics when no data available"""
        return EfficiencyMetrics(
            total_duration=0.0,
            avg_response_time=0.0,
            tool_call_duration=0.0,
            total_turns=0,
            avg_turns_per_task=0.0,
            conversation_efficiency=0.0,
            total_tool_calls=0,
            successful_tool_calls=0,
            tool_call_success_rate=0.0,
            tool_call_efficiency=0.0,
            total_tokens=0,
            tokens_per_turn=0.0,
            cost_estimate=0.0,
            transfer_to_human=False,
            transfer_rate=0.0,
            overall_efficiency=0.0
        )
    
    def get_efficiency_summary(self) -> Dict[str, Any]:
        """Get human-readable efficiency summary"""
        metrics = self.calculate_metrics()
        
        return {
            "performance": {
                "total_duration_seconds": round(metrics.total_duration, 2),
                "avg_response_time_seconds": round(metrics.avg_response_time, 2),
                "total_turns": metrics.total_turns,
                "conversation_efficiency": round(metrics.conversation_efficiency, 3)
            },
            "tool_usage": {
                "total_tool_calls": metrics.total_tool_calls,
                "successful_tool_calls": metrics.successful_tool_calls,
                "success_rate": round(metrics.tool_call_success_rate, 3),
                "tool_efficiency": round(metrics.tool_call_efficiency, 3)
            },
            "resources": {
                "total_tokens": metrics.total_tokens,
                "tokens_per_turn": round(metrics.tokens_per_turn, 1),
                "estimated_cost_usd": round(metrics.cost_estimate, 4)
            },
            "transfers": {
                "transferred_to_human": metrics.transfer_to_human,
                "transfer_rate": round(metrics.transfer_rate, 3)
            },
            "overall": {
                "efficiency_score": round(metrics.overall_efficiency, 3)
            }
        }
