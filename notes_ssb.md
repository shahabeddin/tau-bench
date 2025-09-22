
## Retail -- grok-3-mini-0.0_range_0--1_user-gpt-4.1-llm
============================================================
📊 ENHANCED EVALUATION METRICS
============================================================
🏆 Binary Success Rate: 0.572
🎯 Composite Score: 0.830
⚡ Efficiency Score: 0.860
🔄 Transfer Rate: 0.309
❌ Avg Errors per Task: 1.42
============================================================
📈 Pass^k (Original Metrics)
  k=1: 0.5717391304347826
  k=2: 0.42608695652173895
  k=3: 0.3521739130434783
  k=4: 0.3130434782608696

Performing fault assignment analysis on 197 failed trajectories 
Performing fault type analysis on 184 failures that have been marked as being caused by the agent

Empty trajectory statistics:
  - Empty trajectories: 0 (0.0%)
  - Non-empty trajectories: 197 (100.0%)

Author fault distribution:
  - User: 3 (1.52%)
  - Agent: 184 (93.4%)
  - Environment (otherwise case): 10 (5.08%)

Fault type distribution (only failures marked as being caused by the agent):
  - Called wrong tool: 0 (0.0%)
  - Used wrong tool argument: 16 (8.7%)
  - Goal partially completed: 165 (89.67%)
  - Timeout or API error: 0 (0.0%)
  - Other: 3 (1.63%)

## Airline -- grok-3-mini-0.0_range_0--1_user-gpt-4.1
============================================================
📊 ENHANCED EVALUATION METRICS
============================================================
🏆 Binary Success Rate: 0.530
🎯 Composite Score: 0.862
⚡ Efficiency Score: 0.855
🔄 Transfer Rate: 0.705
❌ Avg Errors per Task: 2.01
============================================================
📈 Pass^k (Original Metrics)
  k=1: 0.53
  k=2: 0.45
  k=3: 0.41
  k=4: 0.38

Performing fault assignment analysis on 94 failed trajectories
Performing fault type analysis on 77 failures that have been marked as being caused by the agent

Empty trajectory statistics:
  - Empty trajectories: 0 (0.0%)
  - Non-empty trajectories: 94 (100.0%)

Author fault distribution:
  - User: 9 (9.57%)
  - Agent: 77 (81.91%)
  - Environment (otherwise case): 8 (8.51%)

Fault type distribution (only failures marked as being caused by the agent):
  - Called wrong tool: 1 (1.3%)
  - Used wrong tool argument: 0 (0.0%)
  - Goal partially completed: 47 (61.04%)
  - Timeout or API error: 0 (0.0%)

  