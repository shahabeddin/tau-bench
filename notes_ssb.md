# Grok-3-mini
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

# GPT-4o-mini
## Retail

============================================================
📊 ENHANCED EVALUATION METRICS
============================================================
🏆 Binary Success Rate: 0.326
🎯 Composite Score: 0.814
⚡ Efficiency Score: 0.885
🔄 Transfer Rate: 0.028
❌ Avg Errors per Task: 1.86
============================================================
📈 Pass^k (Original Metrics)
  k=1: 0.32608695652173914
  k=2: 0.21449275362318848
  k=3: 0.16956521739130434
  k=4: 0.14782608695652175

📄 Results saved to results/tool-calling-gpt-4o-mini-0.0_range_0--1_user-gpt-4.1-mini-llm_0922030422.json

Found 310 failed trajectories
Performing fault assignment analysis on 310 failed trajectories with a max concurrency of 16...
Performing fault type analysis on 295 failures that have been marked as being caused by the agent with a max concurrency of 16...
Reviewed 310 trajectories:

Empty trajectory statistics:
  - Empty trajectories: 0 (0.0%)
  - Non-empty trajectories: 310 (100.0%)

Author fault distribution:
  - User: 7 (2.26%)
  - Agent: 295 (95.16%)
  - Environment (otherwise case): 8 (2.58%)

Fault type distribution (only failures marked as being caused by the agent):
  - Called wrong tool: 0 (0.0%)
  - Used wrong tool argument: 34 (11.53%)
  - Goal partially completed: 250 (84.75%)
  - Timeout or API error: 0 (0.0%)
  - Other: 11 (3.73%)

  ## Airline

  ============================================================
📊 ENHANCED EVALUATION METRICS
============================================================
🏆 Binary Success Rate: 0.260
🎯 Composite Score: 0.836
⚡ Efficiency Score: 0.882
🔄 Transfer Rate: 0.180
❌ Avg Errors per Task: 1.93
============================================================
📈 Pass^k (Original Metrics)
  k=1: 0.26
  k=2: 0.14666666666666667
  k=3: 0.105
  k=4: 0.08

📄 Results saved to results/tool-calling-gpt-4o-mini-0.0_range_0--1_user-gpt-4.1-mini-llm_0922033728.json

Found 148 failed trajectories
Performing fault assignment analysis on 148 failed trajectories with a max concurrency of 16...
Performing fault type analysis on 110 failures that have been marked as being caused by the agent with a max concurrency of 16...
Reviewed 148 trajectories:

Empty trajectory statistics:
  - Empty trajectories: 0 (0.0%)
  - Non-empty trajectories: 148 (100.0%)

Author fault distribution:
  - User: 25 (16.89%)
  - Agent: 110 (74.32%)
  - Environment (otherwise case): 13 (8.78%)

Fault type distribution (only failures marked as being caused by the agent):
  - Called wrong tool: 0 (0.0%)
  - Used wrong tool argument: 0 (0.0%)
  - Goal partially completed: 66 (60.0%)
  - Timeout or API error: 0 (0.0%)
  - Other: 44 (40.0%)
