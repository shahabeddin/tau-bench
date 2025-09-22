#!/usr/bin/env python3
"""
Enhanced Metrics Report Generator for τ+_bench

This script reads the enhanced evaluation results from JSON files and generates
a comprehensive report showing performance metrics, error analysis, and insights.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import statistics


class EnhancedMetricsReporter:
    """Generate comprehensive reports from enhanced evaluation results"""
    
    def __init__(self, json_file_path: str):
        self.json_file_path = Path(json_file_path)
        self.results = self._load_results()
        self.domain = self._detect_domain()
        
    def _load_results(self) -> List[Dict[str, Any]]:
        """Load results from JSON file"""
        try:
            with open(self.json_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File {self.json_file_path} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.json_file_path}: {e}")
            sys.exit(1)
    
    def _detect_domain(self) -> str:
        """Detect domain from filename or content"""
        filename = self.json_file_path.name.lower()
        if 'retail' in filename:
            return 'Retail'
        elif 'airline' in filename:
            return 'Airline'
        else:
            return 'Unknown'
    
    def _calculate_basic_metrics(self) -> Dict[str, Any]:
        """Calculate basic performance metrics"""
        total_tasks = len(self.results)
        successful_tasks = sum(1 for r in self.results if r.get('reward', 0) == 1.0)
        failed_tasks = total_tasks - successful_tasks
        
        # Enhanced evaluation metrics
        enhanced_results = [r for r in self.results if r.get('enhanced_evaluation')]
        
        if not enhanced_results:
            return {
                'total_tasks': total_tasks,
                'successful_tasks': successful_tasks,
                'failed_tasks': failed_tasks,
                'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
                'has_enhanced_metrics': False
            }
        
        # Composite scores
        composite_scores = [r['enhanced_evaluation']['composite_score']['overall_score'] 
                          for r in enhanced_results]
        avg_composite_score = statistics.mean(composite_scores)
        
        # Efficiency metrics
        efficiency_scores = [r['enhanced_evaluation']['efficiency_metrics']['overall_efficiency'] 
                           for r in enhanced_results]
        avg_efficiency = statistics.mean(efficiency_scores)
        
        # Transfer rate
        transfer_count = sum(1 for r in enhanced_results 
                           if r['enhanced_evaluation']['efficiency_metrics']['transfer_to_human'])
        transfer_rate = transfer_count / len(enhanced_results)
        
        # Error analysis
        total_errors = sum(len(r['enhanced_evaluation']['errors']) for r in enhanced_results)
        avg_errors_per_task = total_errors / len(enhanced_results)
        
        return {
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'failed_tasks': failed_tasks,
            'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
            'has_enhanced_metrics': True,
            'avg_composite_score': avg_composite_score,
            'avg_efficiency': avg_efficiency,
            'transfer_rate': transfer_rate,
            'avg_errors_per_task': avg_errors_per_task,
            'total_errors': total_errors
        }
    
    def _analyze_errors(self) -> Dict[str, Any]:
        """Analyze error patterns and categories"""
        enhanced_results = [r for r in self.results if r.get('enhanced_evaluation')]
        if not enhanced_results:
            return {}
        
        all_errors = []
        for result in enhanced_results:
            all_errors.extend(result['enhanced_evaluation']['errors'])
        
        if not all_errors:
            return {'total_errors': 0}
        
        # Error categories
        error_categories = Counter(error['category'] for error in all_errors)
        
        # Error severities
        error_severities = Counter(error['severity'] for error in all_errors)
        
        # Most common error types
        most_common_category = error_categories.most_common(1)[0] if error_categories else None
        most_common_severity = error_severities.most_common(1)[0] if error_severities else None
        
        return {
            'total_errors': len(all_errors),
            'error_categories': dict(error_categories),
            'error_severities': dict(error_severities),
            'most_common_category': most_common_category,
            'most_common_severity': most_common_severity
        }
    
    def _analyze_efficiency_metrics(self) -> Dict[str, Any]:
        """Analyze detailed efficiency metrics"""
        enhanced_results = [r for r in self.results if r.get('enhanced_evaluation')]
        if not enhanced_results:
            return {}
        
        # Aggregate efficiency metrics
        total_duration = sum(r['enhanced_evaluation']['efficiency_metrics']['total_duration'] 
                           for r in enhanced_results)
        total_turns = sum(r['enhanced_evaluation']['efficiency_metrics']['total_turns'] 
                         for r in enhanced_results)
        total_tool_calls = sum(r['enhanced_evaluation']['efficiency_metrics']['total_tool_calls'] 
                              for r in enhanced_results)
        total_tokens = sum(r['enhanced_evaluation']['efficiency_metrics']['total_tokens'] 
                          for r in enhanced_results)
        
        # Averages
        avg_response_time = statistics.mean(r['enhanced_evaluation']['efficiency_metrics']['avg_response_time'] 
                                          for r in enhanced_results)
        avg_turns_per_task = statistics.mean(r['enhanced_evaluation']['efficiency_metrics']['avg_turns_per_task'] 
                                           for r in enhanced_results)
        avg_tokens_per_task = statistics.mean(r['enhanced_evaluation']['efficiency_metrics']['total_tokens'] 
                                            for r in enhanced_results)
        
        # Tool call success rate
        successful_tool_calls = sum(r['enhanced_evaluation']['efficiency_metrics']['successful_tool_calls'] 
                                  for r in enhanced_results)
        tool_call_success_rate = successful_tool_calls / total_tool_calls if total_tool_calls > 0 else 0
        
        return {
            'total_duration': total_duration,
            'total_turns': total_turns,
            'total_tool_calls': total_tool_calls,
            'total_tokens': total_tokens,
            'avg_response_time': avg_response_time,
            'avg_turns_per_task': avg_turns_per_task,
            'avg_tokens_per_task': avg_tokens_per_task,
            'tool_call_success_rate': tool_call_success_rate
        }
    
    def _analyze_failures(self) -> Dict[str, Any]:
        """Analyze failure patterns from auto error identification"""
        failed_results = [r for r in self.results if r.get('reward', 0) != 1.0]
        
        if not failed_results:
            return {'total_failures': 0}
        
        # Check if we have auto error identification data
        has_auto_error_data = any('fault_assignment' in r.get('info', {}) for r in failed_results)
        
        if not has_auto_error_data:
            return {
                'total_failures': len(failed_results),
                'has_auto_error_data': False
            }
        
        # Analyze fault assignments
        fault_assignments = []
        fault_types = []
        
        for result in failed_results:
            info = result.get('info', {})
            if 'fault_assignment' in info:
                fault_assignments.append(info['fault_assignment'])
            if 'fault_type' in info:
                fault_types.append(info['fault_type'])
        
        fault_assignment_counts = Counter(fault_assignments)
        fault_type_counts = Counter(fault_types)
        
        return {
            'total_failures': len(failed_results),
            'has_auto_error_data': True,
            'fault_assignments': dict(fault_assignment_counts),
            'fault_types': dict(fault_type_counts)
        }
    
    def generate_report(self) -> str:
        """Generate comprehensive report"""
        basic_metrics = self._calculate_basic_metrics()
        error_analysis = self._analyze_errors()
        efficiency_metrics = self._analyze_efficiency_metrics()
        failure_analysis = self._analyze_failures()
        
        report = []
        report.append(f"# τ+_bench Enhanced Evaluation Report")
        report.append(f"## {self.domain} Domain - Grok-3-mini")
        report.append(f"**Source File**: {self.json_file_path.name}")
        report.append("")
        
        # Basic Performance Metrics
        report.append("## 📊 Enhanced Evaluation Metrics")
        report.append("=" * 60)
        report.append(f"🏆 Binary Success Rate: {basic_metrics['success_rate']:.3f}")
        
        if basic_metrics['has_enhanced_metrics']:
            report.append(f"🎯 Composite Score: {basic_metrics['avg_composite_score']:.3f}")
            report.append(f"⚡ Efficiency Score: {basic_metrics['avg_efficiency']:.3f}")
            report.append(f"🔄 Transfer Rate: {basic_metrics['transfer_rate']:.3f}")
            report.append(f"❌ Avg Errors per Task: {basic_metrics['avg_errors_per_task']:.2f}")
        else:
            report.append("⚠️  No enhanced metrics available")
        
        report.append("=" * 60)
        report.append("")
        
        # Task Statistics
        report.append("## 📈 Task Statistics")
        report.append(f"- **Total Tasks**: {basic_metrics['total_tasks']}")
        report.append(f"- **Successful Tasks**: {basic_metrics['successful_tasks']}")
        report.append(f"- **Failed Tasks**: {basic_metrics['failed_tasks']}")
        report.append("")
        
        # Enhanced Metrics Details
        if basic_metrics['has_enhanced_metrics']:
            report.append("## 🔍 Enhanced Metrics Details")
            
            # Composite Score Breakdown
            enhanced_results = [r for r in self.results if r.get('enhanced_evaluation')]
            task_completion_scores = [r['enhanced_evaluation']['composite_score']['task_completion'] 
                                    for r in enhanced_results]
            policy_adherence_scores = [r['enhanced_evaluation']['composite_score']['policy_adherence'] 
                                     for r in enhanced_results]
            user_satisfaction_scores = [r['enhanced_evaluation']['composite_score']['user_satisfaction'] 
                                      for r in enhanced_results]
            
            report.append("### Composite Score Breakdown")
            report.append(f"- **Task Completion**: {statistics.mean(task_completion_scores):.3f}")
            report.append(f"- **Efficiency**: {basic_metrics['avg_efficiency']:.3f}")
            report.append(f"- **Policy Adherence**: {statistics.mean(policy_adherence_scores):.3f}")
            report.append(f"- **User Satisfaction**: {statistics.mean(user_satisfaction_scores):.3f}")
            report.append("")
            
            # Efficiency Metrics
            if efficiency_metrics:
                report.append("### Efficiency Metrics")
                report.append(f"- **Total Duration**: {efficiency_metrics['total_duration']:.2f} seconds")
                report.append(f"- **Total Turns**: {efficiency_metrics['total_turns']}")
                report.append(f"- **Total Tool Calls**: {efficiency_metrics['total_tool_calls']}")
                report.append(f"- **Total Tokens**: {efficiency_metrics['total_tokens']:,}")
                report.append(f"- **Avg Response Time**: {efficiency_metrics['avg_response_time']:.3f} seconds")
                report.append(f"- **Avg Turns per Task**: {efficiency_metrics['avg_turns_per_task']:.1f}")
                report.append(f"- **Avg Tokens per Task**: {efficiency_metrics['avg_tokens_per_task']:.0f}")
                report.append(f"- **Tool Call Success Rate**: {efficiency_metrics['tool_call_success_rate']:.3f}")
                report.append("")
        
        # Error Analysis
        if error_analysis and error_analysis.get('total_errors', 0) > 0:
            report.append("## ❌ Error Analysis")
            report.append(f"- **Total Errors**: {error_analysis['total_errors']}")
            
            if error_analysis.get('error_categories'):
                report.append("### Error Categories")
                for category, count in error_analysis['error_categories'].items():
                    percentage = (count / error_analysis['total_errors']) * 100
                    report.append(f"- **{category}**: {count} ({percentage:.1f}%)")
            
            if error_analysis.get('error_severities'):
                report.append("### Error Severities")
                for severity, count in error_analysis['error_severities'].items():
                    percentage = (count / error_analysis['total_errors']) * 100
                    report.append(f"- **{severity}**: {count} ({percentage:.1f}%)")
            
            if error_analysis.get('most_common_category'):
                category, count = error_analysis['most_common_category']
                report.append(f"- **Most Common Category**: {category} ({count} occurrences)")
            
            report.append("")
        
        # Failure Analysis
        if failure_analysis and failure_analysis.get('total_failures', 0) > 0:
            report.append("## 🔍 Failure Analysis")
            report.append(f"- **Total Failures**: {failure_analysis['total_failures']}")
            
            if failure_analysis.get('has_auto_error_data'):
                if failure_analysis.get('fault_assignments'):
                    report.append("### Fault Assignment")
                    for assignment, count in failure_analysis['fault_assignments'].items():
                        percentage = (count / failure_analysis['total_failures']) * 100
                        report.append(f"- **{assignment}**: {count} ({percentage:.1f}%)")
                
                if failure_analysis.get('fault_types'):
                    report.append("### Fault Types")
                    for fault_type, count in failure_analysis['fault_types'].items():
                        percentage = (count / failure_analysis['total_failures']) * 100
                        report.append(f"- **{fault_type}**: {count} ({percentage:.1f}%)")
            else:
                report.append("- **Auto Error Identification**: Not available")
            
            report.append("")
        
        # Key Insights
        report.append("## 💡 Key Insights")
        
        if basic_metrics['has_enhanced_metrics']:
            if basic_metrics['avg_composite_score'] >= 0.8:
                report.append("✅ **Excellent Performance**: Composite score above 0.8 indicates strong overall performance")
            elif basic_metrics['avg_composite_score'] >= 0.6:
                report.append("⚠️  **Good Performance**: Composite score above 0.6 indicates decent performance")
            else:
                report.append("❌ **Needs Improvement**: Composite score below 0.6 indicates performance issues")
            
            if basic_metrics['avg_efficiency'] >= 0.8:
                report.append("✅ **High Efficiency**: Efficiency score above 0.8 indicates very efficient task completion")
            elif basic_metrics['avg_efficiency'] >= 0.6:
                report.append("⚠️  **Moderate Efficiency**: Efficiency score above 0.6 indicates reasonable efficiency")
            else:
                report.append("❌ **Low Efficiency**: Efficiency score below 0.6 indicates efficiency issues")
            
            if basic_metrics['transfer_rate'] >= 0.5:
                report.append("⚠️  **High Transfer Rate**: More than 50% of tasks require human intervention")
            elif basic_metrics['transfer_rate'] >= 0.3:
                report.append("ℹ️  **Moderate Transfer Rate**: Some tasks require human intervention")
            else:
                report.append("✅ **Low Transfer Rate**: Most tasks completed without human intervention")
            
            if basic_metrics['avg_errors_per_task'] <= 1.0:
                report.append("✅ **Low Error Rate**: Few errors per task on average")
            elif basic_metrics['avg_errors_per_task'] <= 2.0:
                report.append("⚠️  **Moderate Error Rate**: Some errors per task on average")
            else:
                report.append("❌ **High Error Rate**: Many errors per task on average")
        
        report.append("")
        report.append("---")
        report.append(f"*Report generated from {self.json_file_path.name}*")
        
        return "\n".join(report)
    
    def save_report(self, output_file: Optional[str] = None) -> str:
        """Generate and save report to file"""
        report = self.generate_report()
        
        if output_file:
            output_path = Path(output_file)
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_path}")
        else:
            # Auto-generate filename
            base_name = self.json_file_path.stem
            output_path = self.json_file_path.parent / f"{base_name}_enhanced_report.md"
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_path}")
        
        return str(output_path)


def main():
    parser = argparse.ArgumentParser(description='Generate enhanced metrics report from τ+_bench results')
    parser.add_argument('json_file', help='Path to the JSON results file')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('--print', action='store_true', help='Print report to console')
    
    args = parser.parse_args()
    
    # Generate report
    reporter = EnhancedMetricsReporter(args.json_file)
    
    if args.print:
        print(reporter.generate_report())
    else:
        output_file = reporter.save_report(args.output)
        print(f"Enhanced metrics report generated successfully!")


if __name__ == "__main__":
    main()
