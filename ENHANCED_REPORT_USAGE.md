# Enhanced Metrics Report Generator

## Overview

The `generate_enhanced_report.py` script generates comprehensive reports from τ+_bench enhanced evaluation results. It analyzes performance metrics, error patterns, efficiency data, and provides actionable insights.

## Usage

### Basic Usage
```bash
python generate_enhanced_report.py <json_file>
```

### Save Report to File
```bash
python generate_enhanced_report.py <json_file> -o output_report.md
```

### Print Report to Console
```bash
python generate_enhanced_report.py <json_file> --print
```

### Examples

#### Generate report for Retail domain results
```bash
python generate_enhanced_report.py results/tool-calling-grok-3-mini-0.0_range_0--1_user-gpt-4.1-llm_0922001040.json
```

#### Generate report for Airline domain results
```bash
python generate_enhanced_report.py results/tool-calling-grok-3-mini-0.0_range_0--1_user-gpt-4.1-llm_0922011221.json
```

#### Save report with custom filename
```bash
python generate_enhanced_report.py results/tool-calling-grok-3-mini-0.0_range_0--1_user-gpt-4.1-llm_0922001040.json -o retail_analysis.md
```

## Report Sections

### 1. Enhanced Evaluation Metrics
- Binary Success Rate
- Composite Score (overall performance)
- Efficiency Score
- Transfer Rate (human escalation)
- Average Errors per Task

### 2. Task Statistics
- Total tasks processed
- Successful vs failed tasks
- Success rate percentage

### 3. Enhanced Metrics Details
- **Composite Score Breakdown**: Task completion, efficiency, policy adherence, user satisfaction
- **Efficiency Metrics**: Duration, turns, tool calls, tokens, response times

### 4. Error Analysis
- Total error count
- Error categories and distribution
- Error severities
- Most common error types

### 5. Failure Analysis
- Total failures
- Fault assignment (agent vs user vs environment)
- Fault types (if auto error identification data available)

### 6. Key Insights
- Performance assessment
- Efficiency evaluation
- Transfer rate analysis
- Error rate analysis

## Output Format

The script generates a Markdown report with:
- Clear section headers
- Emoji indicators for visual appeal
- Statistical summaries
- Percentage breakdowns
- Actionable insights

## Requirements

- Python 3.6+
- JSON results file from τ+_bench enhanced evaluation
- No additional dependencies (uses only standard library)

## File Structure

```
tau-bench/
├── generate_enhanced_report.py    # Main script
├── ENHANCED_REPORT_USAGE.md       # This usage guide
├── results/                       # JSON result files
│   ├── tool-calling-grok-3-mini-0.0_range_0--1_user-gpt-4.1-llm_0922001040.json
│   └── tool-calling-grok-3-mini-0.0_range_0--1_user-gpt-4.1-llm_0922011221.json
└── *_enhanced_report.md          # Generated reports
```

## Troubleshooting

### Common Issues

1. **File not found**: Ensure the JSON file path is correct
2. **Invalid JSON**: Check that the file is a valid JSON format
3. **No enhanced metrics**: Ensure the JSON file contains enhanced evaluation data

### Error Messages

- `File not found`: Check the file path
- `Invalid JSON`: Verify the file format
- `No enhanced metrics available`: The file doesn't contain enhanced evaluation results

## Example Output

```markdown
# τ+_bench Enhanced Evaluation Report
## Retail Domain - Grok-3-mini

## 📊 Enhanced Evaluation Metrics
============================================================
🏆 Binary Success Rate: 0.572
🎯 Composite Score: 0.830
⚡ Efficiency Score: 0.860
🔄 Transfer Rate: 0.309
❌ Avg Errors per Task: 1.42
============================================================
```

This script provides a comprehensive analysis of model performance using the enhanced τ+_bench evaluation system.
