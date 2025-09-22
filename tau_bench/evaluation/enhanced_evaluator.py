# Copyright Sierra

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
import time

from .composite_scoring import CompositeScorer, CompositeScore
from .error_analysis import ErrorAnalyzer, ErrorAnalysis
from .efficiency_metrics import EfficiencyTracker, EfficiencyMetrics


class EnhancedEvaluationResult(BaseModel):
    """Enhanced evaluation result with composite scoring and detailed analysis"""
    # Original binary result
    binary_reward: float
    
    # Enhanced scoring
    composite_score: CompositeScore
    
    # Error analysis
    errors: List[ErrorAnalysis]
    error_summary: Dict[str, Any]
    
    # Efficiency metrics
    efficiency_metrics: EfficiencyMetrics
    
    # Additional metadata
    task_id: int
    trial: int
    evaluation_timestamp: float


class EnhancedEvaluator:
    """Main evaluator that combines all enhanced evaluation components"""
    
    def __init__(self):
        self.composite_scorer = CompositeScorer()
        self.error_analyzer = ErrorAnalyzer()
        self.efficiency_tracker = EfficiencyTracker()
        # Link the efficiency tracker to the composite scorer
        self.composite_scorer.efficiency_tracker = self.efficiency_tracker
        
    def start_evaluation(self, task_id: int, trial: int):
        """Start evaluation for a new task"""
        self.composite_scorer.start_evaluation()
        self.efficiency_tracker.start_evaluation()
        self.current_task_id = task_id
        self.current_trial = trial
        # Reset conversation processed flag
        self._conversation_processed = False
        
    def record_tool_call(self, tool_name: str, success: bool = True, 
                        duration: float = 0.0, tokens_used: int = 0):
        """Record a tool call during evaluation"""
        self.composite_scorer.record_tool_call(tool_name, success)
        self.efficiency_tracker.record_tool_call(tool_name, success, duration, tokens_used)
        
    def record_turn(self, message: Dict[str, Any], tokens_used: int = 0):
        """Record a conversation turn during evaluation"""
        self.composite_scorer.record_turn(message)
        self.efficiency_tracker.record_turn(message, tokens_used)
        
    def start_response(self):
        """Start timing a response"""
        self.efficiency_tracker.start_response()
        
    def end_response(self):
        """End timing a response"""
        self.efficiency_tracker.end_response()
        
    def evaluate_task(self, 
                     binary_reward: float,
                     conversation: List[Dict[str, Any]],
                     task_actions: List[Dict[str, Any]],
                     actual_actions: List[Dict[str, Any]],
                     error_info: Optional[Dict[str, Any]] = None) -> EnhancedEvaluationResult:
        """Evaluate a completed task with enhanced metrics"""
        
        # Process conversation to extract efficiency data
        self._process_conversation(conversation)
        
        # Calculate composite score
        composite_score = self.composite_scorer.calculate_composite_score(
            binary_reward, task_actions, actual_actions, conversation
        )
        
        # Analyze errors
        errors = self.error_analyzer.analyze_error(
            binary_reward, conversation, task_actions, actual_actions, error_info
        )
        error_summary = self.error_analyzer.get_error_summary(errors)
        
        # Calculate efficiency metrics
        efficiency_metrics = self.efficiency_tracker.calculate_metrics()
        
        return EnhancedEvaluationResult(
            binary_reward=binary_reward,
            composite_score=composite_score,
            errors=errors,
            error_summary=error_summary,
            efficiency_metrics=efficiency_metrics,
            task_id=self.current_task_id,
            trial=self.current_trial,
            evaluation_timestamp=time.time()
        )
    
    def _process_conversation(self, conversation: List[Dict[str, Any]]):
        """Process conversation to extract efficiency metrics"""
        if not conversation:
            return
            
        # Check if we've already processed this conversation
        if hasattr(self, '_conversation_processed') and self._conversation_processed:
            return
            
        for message in conversation:
            # Record the turn with token estimation
            self.record_turn(message)
            
            # Extract tool calls from the message
            if 'tool_calls' in message and message['tool_calls']:
                for tool_call in message['tool_calls']:
                    tool_name = tool_call.get('function', {}).get('name', 'unknown')
                    self.record_tool_call(tool_name, success=True)
            
            # Check for tool responses
            if message.get('role') == 'tool':
                # This is a tool response, we can infer the tool was called
                # We don't have the tool name here, so we'll estimate
                self.record_tool_call('unknown_tool', success=True)
        
        # Mark conversation as processed
        self._conversation_processed = True
    
    def get_evaluation_summary(self, results: List[EnhancedEvaluationResult]) -> Dict[str, Any]:
        """Get comprehensive evaluation summary for multiple tasks"""
        
        if not results:
            return {"error": "No results to summarize"}
            
        # Basic statistics
        total_tasks = len(results)
        binary_success_rate = sum(1 for r in results if r.binary_reward == 1.0) / total_tasks
        
        # Composite score statistics
        composite_scores = [r.composite_score.overall_score for r in results]
        avg_composite_score = sum(composite_scores) / len(composite_scores)
        
        # Error statistics
        all_errors = []
        for result in results:
            all_errors.extend(result.errors)
        
        error_summary = self.error_analyzer.get_error_summary(all_errors)
        
        # Efficiency statistics
        efficiency_scores = [r.efficiency_metrics.overall_efficiency for r in results]
        avg_efficiency = sum(efficiency_scores) / len(efficiency_scores)
        
        transfer_rate = sum(1 for r in results if r.efficiency_metrics.transfer_to_human) / total_tasks
        
        # Performance by category
        performance_categories = {
            "task_completion": {
                "avg_score": sum(r.composite_score.task_completion for r in results) / total_tasks,
                "description": "How well tasks were completed"
            },
            "efficiency": {
                "avg_score": sum(r.composite_score.efficiency for r in results) / total_tasks,
                "description": "How efficiently tasks were completed"
            },
            "policy_adherence": {
                "avg_score": sum(r.composite_score.policy_adherence for r in results) / total_tasks,
                "description": "How well policies were followed"
            },
            "user_satisfaction": {
                "avg_score": sum(r.composite_score.user_satisfaction for r in results) / total_tasks,
                "description": "Quality of user interaction"
            }
        }
        
        return {
            "overview": {
                "total_tasks": total_tasks,
                "binary_success_rate": round(binary_success_rate, 3),
                "avg_composite_score": round(avg_composite_score, 3),
                "avg_efficiency": round(avg_efficiency, 3),
                "transfer_rate": round(transfer_rate, 3)
            },
            "performance_breakdown": performance_categories,
            "error_analysis": error_summary,
            "efficiency_metrics": {
                "avg_turns": sum(r.efficiency_metrics.total_turns for r in results) / total_tasks,
                "avg_tool_calls": sum(r.efficiency_metrics.total_tool_calls for r in results) / total_tasks,
                "avg_tokens": sum(r.efficiency_metrics.total_tokens for r in results) / total_tasks,
                "avg_cost": sum(r.efficiency_metrics.cost_estimate for r in results) / total_tasks
            },
            "recommendations": self._generate_recommendations(results, error_summary)
        }
    
    def _generate_recommendations(self, results: List[EnhancedEvaluationResult], 
                                error_summary: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on evaluation results"""
        
        recommendations = []
        
        # Check for common error patterns
        if error_summary.get('total_errors', 0) > 0:
            most_common_category = error_summary.get('most_common_category')
            if most_common_category == 'policy_interpretation':
                recommendations.append("Improve policy interpretation flexibility - consider edge cases")
            elif most_common_category == 'premature_transfer':
                recommendations.append("Reduce premature transfers to human - try alternative approaches first")
            elif most_common_category == 'tool_usage':
                recommendations.append("Improve tool usage accuracy - verify parameters before calling")
                
        # Check efficiency issues
        avg_efficiency = sum(r.efficiency_metrics.overall_efficiency for r in results) / len(results)
        if avg_efficiency < 0.6:
            recommendations.append("Improve overall efficiency - reduce conversation length and tool calls")
            
        # Check transfer rate
        transfer_rate = sum(1 for r in results if r.efficiency_metrics.transfer_to_human) / len(results)
        if transfer_rate > 0.3:
            recommendations.append("Reduce transfer rate - improve problem-solving capabilities")
            
        # Check policy adherence
        avg_policy_adherence = sum(r.composite_score.policy_adherence for r in results) / len(results)
        if avg_policy_adherence < 0.7:
            recommendations.append("Improve policy adherence - avoid subjective recommendations")
            
        return recommendations
    
    def export_detailed_results(self, results: List[EnhancedEvaluationResult], 
                              filename: str) -> None:
        """Export detailed results to JSON file"""
        
        export_data = {
            "evaluation_metadata": {
                "total_tasks": len(results),
                "evaluation_timestamp": time.time(),
                "evaluator_version": "1.0.0"
            },
            "summary": self.get_evaluation_summary(results),
            "detailed_results": [
                {
                    "task_id": r.task_id,
                    "trial": r.trial,
                    "binary_reward": r.binary_reward,
                    "composite_score": r.composite_score.dict(),
                    "errors": [error.dict() for error in r.errors],
                    "efficiency_metrics": r.efficiency_metrics.dict()
                }
                for r in results
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        print(f"Detailed results exported to {filename}")
