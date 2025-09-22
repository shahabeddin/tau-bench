# τ+_bench: Enhanced Benchmark for Tool-Agent-User Interaction in Real-World Domains



**Original Paper**:
* [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)


We propose enhancements to the $\tau$-bench as described below.

## τ+_bench: Enhanced Evaluation System

**τ+_bench** is an enhanced version of the original τ-bench that introduces comprehensive multi-dimensional evaluation metrics beyond simple binary pass/fail scoring. This enhancement provides deeper insights into model performance, failure modes, and real-world deployment characteristics.

### Key Enhancements

#### 1. **Composite Performance Score (0.0-1.0)**
Replaces binary 0/1 scoring with weighted multi-dimensional evaluation:

- **Task Completion (40%)**: How well the task was completed
- **Efficiency (30%)**: How efficiently it was completed  
- **Policy Adherence (20%)**: How well policies were followed
- **User Satisfaction (10%)**: Quality of user interaction

#### 2. **Enhanced Error Analysis and Categorization**
Hierarchical error taxonomy with detailed analysis:

- **Policy Interpretation**: Rigid interpretation, context misunderstanding, policy violations
- **Tool Usage**: Wrong arguments, missing tools, tool failures
- **Conversation Flow**: Premature transfer, goal partial completion, inefficient flow
- **Context Understanding**: User intent misunderstanding, ambiguous request handling
- **System Errors**: Runtime errors, environment errors

Each error includes:
- Root cause analysis
- Suggested fixes
- Severity levels (low, medium, high, critical)
- Confidence scoring

#### 3. **Efficiency and Resource Metrics**
Comprehensive tracking of practical deployment metrics:

- **Timing Metrics**: Total duration, average response time, tool call duration
- **Conversation Metrics**: Total turns, conversation efficiency, transfer rates
- **Tool Usage**: Success rate, efficiency, call frequency
- **Resource Consumption**: Token usage, cost estimation, memory usage
- **Transfer Analysis**: Human escalation rates and patterns

### Enhanced Metrics Calculation

#### **Composite Score Calculation**
```python
overall_score = (
    task_completion * 0.4 +
    efficiency * 0.3 +
    policy_adherence * 0.2 +
    user_satisfaction * 0.1
)
```

#### **Efficiency Score Components**
- **Conversation Efficiency**: Based on optimal conversation length (10-30 turns = 1.0, 40+ turns = 0.4)
- **Tool Call Efficiency**: Optimal tool usage (5-15 calls = 1.0, 30+ calls = 0.4)
- **Transfer Penalty**: 30% penalty for premature human transfers
- **Success Rate Factor**: Tool call success rate weighting

#### **Token Estimation**
- **Character-based estimation**: ~4 characters per token for English text
- **Message overhead**: +10 tokens for role structure
- **Tool call overhead**: +50 tokens per tool call
- **Minimum tokens**: 1 token per message

#### **Timing Estimation**
- **Response times**: 0.5s base + 1ms per character for longer responses
- **Tool durations**: Based on complexity (0.1s for lookups, 1.2s for complex operations)
- **Realistic ranges**: 0.5s-3s for responses, 0.1s-1.2s for tool calls

## τ+_bench Enhanced Evaluation Results

### Model Performance Analysis

#### **Enhanced Metrics by Domain and Model**

| Model | Domain | Binary Success Rate | Composite Score | Efficiency Score | Transfer Rate | Avg Errors per Task |
|-------|--------|-------------------|-----------------|------------------|---------------|-------------------|
| **Grok-3-mini** | Retail | 0.572 | 0.830 | 0.860 | 0.309 | 1.42 |
| **Grok-3-mini** | Airline | 0.530 | 0.862 | 0.855 | 0.705 | 2.01 |
| **GPT-4o-mini** | Retail | 0.326 | 0.814 | 0.885 | 0.028 | 1.86 |
| **GPT-4o-mini** | Airline | 0.260 | 0.836 | 0.882 | 0.180 | 1.93 |

#### **Detailed Performance Breakdown**

##### **Retail Domain - Grok-3-mini**
- **Success Rate**: 57.2% (263/460 tasks completed successfully)
- **Composite Score**: 0.830 (excellent overall performance)
- **Efficiency**: 0.860 (very efficient task completion)
- **Transfer Rate**: 30.9% (moderate human escalation)
- **Error Rate**: 1.42 errors per task on average

**Fault Analysis (197 failed trajectories):**
- **Agent-caused failures**: 93.4% (184/197)
- **User-caused failures**: 1.52% (3/197)
- **Environment failures**: 5.08% (10/197)

**Agent Fault Types:**
- **Goal partially completed**: 89.67% (165/184)
- **Wrong tool arguments**: 8.7% (16/184)
- **Other issues**: 1.63% (3/184)

##### **Retail Domain - GPT-4o-mini**
- **Success Rate**: 32.6% (150/460 tasks completed successfully)
- **Composite Score**: 0.814 (excellent overall performance)
- **Efficiency**: 0.885 (very efficient task completion)
- **Transfer Rate**: 2.8% (very low human escalation)
- **Error Rate**: 1.86 errors per task on average

**Error Analysis (855 total errors):**
- **Tool failures**: 43.4% (371/855)
- **Wrong arguments**: 35.9% (307/855)
- **Rigid interpretation**: 8.8% (75/855)
- **Policy violations**: 7.3% (62/855)
- **Premature transfer**: 3.5% (30/855)

##### **Airline Domain - Grok-3-mini**
- **Success Rate**: 53.0% (106/200 tasks completed successfully)
- **Composite Score**: 0.862 (excellent overall performance)
- **Efficiency**: 0.855 (very efficient task completion)
- **Transfer Rate**: 70.5% (high human escalation rate)
- **Error Rate**: 2.01 errors per task on average

**Fault Analysis (94 failed trajectories):**
- **Agent-caused failures**: 81.91% (77/94)
- **User-caused failures**: 9.57% (9/94)
- **Environment failures**: 8.51% (8/94)

**Agent Fault Types:**
- **Goal partially completed**: 61.04% (47/77)
- **Wrong tool calls**: 1.3% (1/77)
- **Other issues**: 37.66% (29/77)

##### **Airline Domain - GPT-4o-mini**
- **Success Rate**: 26.0% (52/200 tasks completed successfully)
- **Composite Score**: 0.836 (excellent overall performance)
- **Efficiency**: 0.882 (very efficient task completion)
- **Transfer Rate**: 18.0% (low human escalation)
- **Error Rate**: 1.93 errors per task on average

**Error Analysis (385 total errors):**
- **Wrong arguments**: 35.1% (135/385)
- **Tool failures**: 32.5% (125/385)
- **Policy violations**: 13.5% (52/385)
- **Premature transfer**: 8.1% (31/385)
- **Rigid interpretation**: 6.8% (26/385)

#### **Key Insights**

##### **Model Comparison Across Domains**

**Retail Domain:**
1. **Success Rate**: Grok-3-mini significantly outperforms GPT-4o-mini (57.2% vs 32.6%)
2. **Composite Score**: Both models show excellent performance (0.830 vs 0.814)
3. **Efficiency**: GPT-4o-mini shows slightly higher efficiency (0.885 vs 0.860)
4. **Transfer Rate**: GPT-4o-mini has much lower human escalation (2.8% vs 30.9%)

**Airline Domain:**
1. **Success Rate**: Grok-3-mini significantly outperforms GPT-4o-mini (53.0% vs 26.0%)
2. **Composite Score**: Both models show excellent performance (0.862 vs 0.836)
3. **Efficiency**: GPT-4o-mini shows higher efficiency (0.882 vs 0.855)
4. **Transfer Rate**: GPT-4o-mini has much higher human escalation (70.5% vs 18.0%)

**Error Patterns:**
- **Grok-3-mini (Retail)**: "Goal partially completed" (89.7%) and "Wrong arguments" (8.7%)
- **GPT-4o-mini (Retail)**: "Tool failures" (43.4%) and "Wrong arguments" (35.9%)
- **Grok-3-mini (Airline)**: "Goal partially completed" (61.0%) and "Other issues" (37.7%)
- **GPT-4o-mini (Airline)**: "Wrong arguments" (35.1%) and "Tool failures" (32.5%)

##### **Domain Performance (Grok-3-mini)**
1. **Overall Performance**: Strong performance in both domains with composite scores above 0.83
2. **Efficiency**: Consistently high efficiency scores (~0.86) indicate effective task completion
3. **Transfer Patterns**: Airline domain has significantly higher human transfer rate (70.5% vs 30.9%), suggesting more complex scenarios
4. **Error Patterns**: "Goal partially completed" is the dominant failure mode, indicating the model often gets close but doesn't fully complete tasks
5. **Error Attribution**: Most failures are attributed to the agent rather than user or environment issues

##### **Model Strengths and Weaknesses**

**Grok-3-mini:**
- **Strengths**: Consistently higher success rates across both domains (57.2% retail, 53.0% airline)
- **Weaknesses**: High human transfer rates, especially in airline domain (70.5%)
- **Pattern**: Better at completing tasks but requires more human intervention for complex scenarios

**GPT-4o-mini:**
- **Strengths**: Lower human transfer rates, higher efficiency scores, more independent operation
- **Weaknesses**: Significantly lower success rates (32.6% retail, 26.0% airline)
- **Pattern**: More independent but struggles with task completion, especially in airline domain

**Domain-Specific Insights:**
- **Retail**: Both models show good composite scores (>0.81), but Grok-3-mini has 24.6% higher success rate
- **Airline**: Grok-3-mini has 27% higher success rate, but GPT-4o-mini has 52.5% lower transfer rate
- **Error Patterns**: Different failure modes suggest different model characteristics and optimization strategies

## Original τ-bench Leaderboard

### Airline

| Strategy       | Pass^1 | Pass^2 | Pass^3 | Pass^4 |
| -------------- | ------ | ------ | ------ | ------ |
| [TC (claude-3-5-sonnet-20241022)](https://www.anthropic.com/news/3-5-models-and-computer-use)      | **0.460**     | **0.326**     | **0.263**     | **0.225**     |
| [TC (gpt-4o)](https://platform.openai.com/docs/guides/function-calling)     | 0.420     | 0.273     | 0.220     | 0.200     |
| [TC (claude-3-5-sonnet-20240620)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)      | 0.360     | 0.224     | 0.169     | 0.139     |
| [TC (mistral-large-2407)](https://docs.mistral.ai/capabilities/function_calling/)     | ??     | ??     | ??     | ??     |
| [TC (gpt-4o-mini)](https://platform.openai.com/docs/guides/function-calling)     | 0.225     | 0.140     | 0.110     | 0.100     |
| [Act](https://arxiv.org/abs/2210.03629) (gpt-4o)     | 0.365 | 0.217 | 0.160 | 0.140     |
| [ReAct](https://arxiv.org/abs/2210.03629) (gpt-4o)     | 0.325 | 0.233 | 0.185 | 0.160     |

### Retail

| Strategy       | Pass^1 | Pass^2 | Pass^3 | Pass^4 |
| -------------- | ------ | ------ | ------ | ------ |
| [TC (claude-3-5-sonnet-20241022)](https://www.anthropic.com/news/3-5-models-and-computer-use)      | **0.692**     | **0.576**     | **0.509**     | **0.462**     |
| [TC (gpt-4o)](https://platform.openai.com/docs/guides/function-calling)     | 0.604     | 0.491     | 0.430     | 0.383     |
| [TC (claude-3-5-sonnet-20240620)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)      | 0.626     | 0.506     | 0.435     | 0.387     |
| [TC (mistral-large-2407)](https://docs.mistral.ai/capabilities/function_calling/)     | ??     | ??     | ??     | ??     |
| [TC (gpt-4o-mini)](https://platform.openai.com/docs/guides/function-calling)     | ??     | ??     | ??     | ??     |
| [Act](https://arxiv.org/abs/2210.03629) (gpt-4o)     | ??     | ??     | ??     | ??     |
| [ReAct](https://arxiv.org/abs/2210.03629) (gpt-4o)     | ??     | ??     | ??     | ??     |

*TC = `tool-calling` strategy (the function-calling strategy reported in the paper)

## Setup

1. Clone this repository:

```bash
git clone https://github.com/sierra-research/tau-bench && cd ./tau-bench
```

2. Install from source (which also installs required packages):

```bash
pip install -e .
```

3. Set up your OpenAI / Anthropic / Google / Mistral / AnyScale API keys as environment variables.

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...
```

## Run

### Basic Usage (with Enhanced Evaluation)

Run a tool-calling agent on the τ-retail environment with enhanced evaluation:

```bash
python run.py --agent-strategy tool-calling --env retail --model gpt-4o --model-provider openai --user-model gpt-4o --user-model-provider openai --user-strategy llm --max-concurrency 10
```

The enhanced evaluation system will automatically provide:
- Composite performance scores
- Detailed error analysis
- Efficiency and resource metrics
- Actionable recommendations

### Enhanced Metrics Output

The system now displays comprehensive metrics:

```
📊 ENHANCED EVALUATION METRICS
============================================================
🏆 Binary Success Rate: 0.567
🎯 Composite Score: 0.623
⚡ Efficiency Score: 0.745
🔄 Transfer Rate: 0.373
❌ Avg Errors per Task: 2.15
============================================================
```

### Running Specific Tasks

To run specific tasks, use the `--task-ids` flag:

```bash
python run.py --agent-strategy tool-calling --env retail --model gpt-4o --model-provider openai --user-model gpt-4o --user-model-provider openai --user-strategy llm --max-concurrency 10 --task-ids 2 4 6
```

## User Simulators

By default, we use `gpt-4o` as the user simulator with strategy `llm`. You can use other models by setting the `--user-model` flag, or other strategies by setting the `--user-strategy` flag.

### Tool-Calling Agent with Claude User Simulator

```bash
python run.py --agent-strategy tool-calling --env retail --model gpt-4o --model-provider openai --max-concurrency 10 --user-model claude-3-5-sonnet-20240620 --user-model-provider anthropic --user-strategy llm
```

### Other User Strategies

#### ReAct User Simulator
```bash
python run.py --agent-strategy tool-calling --env retail --model gpt-4o --model-provider openai --max-concurrency 10 --user-model gpt-4o --user-model-provider openai --user-strategy react
```

Example ReAct user response:
```md
Thought:
I should provide my name and zip code as I wasn't given an email address to use.

User Response:
Sure, my name is Yusuf Rossi, and my zip code is 19122.
```

#### Verify User Simulator
```bash
python run.py --agent-strategy tool-calling --env retail --model gpt-4o --model-provider openai --max-concurrency 10 --user-model gpt-4o --user-model-provider openai --user-strategy verify
```

This strategy uses a subsequent LLM verification step to check if the user simulator's response is satisfactory. If not, the user simulator will be prompted to generate a new response.

#### Reflection User Simulator
```bash
python run.py --agent-strategy tool-calling --env retail --model gpt-4o --model-provider openai --max-concurrency 10 --user-model gpt-4o --user-model-provider openai --user-strategy reflection
```

This strategy uses a subsequent LLM verification step to check if the user simulator's response is satisfactory. If not, the user simulator will be prompted to reflect on its response and generate a new response.

## Auto Error Identification

Often times, it is difficult and time consuming to manually identify specific error locations in trajectories as they can be long and the constraints can be complex. We have provided an auto error identification tool that can do the following:

1. Fault assignment: determine the entity that is responsible for the fault (user, agent, environment)
2. Fault type classification: classify the type of fault (goal_partially_completed, used_wrong_tool, used_wrong_tool_argument, took_unintended_action)

Both of the labels are accompanied with a description.

To run the auto error identification:

```bash
python auto_error_identification.py --env <airline/retail> --platform openai --results-path <the path to your results file here> --max-concurrency 16 --output-path test-auto-error-identification --max-num-failed-results 10
```

Please note that this feature utilizes an LLM, which may lead to inaccurate error identifications.

*Notice: If an error is raised due to the structure of your results file, you may have to rerun the benchmark to produce a new results file. We have recently [rewritten](https://github.com/sierra-research/tau-bench/commit/043b544371757ebb3762b3d02a6675dfe0c41798) the benchmark to be more type-safe and extensible.

## Historical Trajectories

τ-bench might be expensive to run. We have provided a set of historical trajectories for the airline and retail environments in `./historical_trajectories`.

If you would like to contribute your historical trajectories to this benchmark, please submit a PR!

## Enhanced Evaluation Features

### Real-Time Metrics Tracking
- Automatic token counting and estimation
- Response time measurement
- Tool call duration tracking
- Conversation flow analysis

### Comprehensive Error Analysis
- Hierarchical error categorization
- Root cause identification
- Suggested improvement actions
- Error severity assessment

### Resource Efficiency Analysis
- Token consumption tracking
- Cost estimation
- Memory usage patterns
- Performance bottleneck identification

### Actionable Insights
- Model-specific recommendations
- Performance optimization guidance
- Deployment readiness assessment
- Comparative analysis tools

## License

See `./LICENSE`.

## Contact

Please submit issues or pull requests if you find problems with the benchmark.

## Citation

```bibtex
@misc{yao2024tau,
      title={$\tau$-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains}, 
      author={Shunyu Yao and Noah Shinn and Pedram Razavi and Karthik Narasimhan},
      year={2024},
      eprint={2406.12045},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2406.12045}, 
}
@misc{barres2025tau2,
      title={$\tau^2$-Bench: Evaluating Conversational Agents in a Dual-Control Environment}, 
      author={Victor Barres and Honghua Dong and Soham Ray and Xujie Si and Karthik Narasimhan},
      year={2025},
      eprint={2506.07982},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2506.07982}, 
}
```