# Bias Analysis in Language Models using BBQ Dataset

A comprehensive pipeline for detecting and analyzing biases in Large Language Models (LLMs) using the Bias Benchmark for QA (BBQ) dataset. This system performs cross-consistency checks and question-guessing tasks to identify inconsistent reasoning and biased interpretations in model responses across various demographic dimensions.

## Overview

This project implements a two-stage analysis pipeline:

1. **Dataset Creation**: Query LLMs with paired questions from the BBQ dataset to generate model responses  
2. **Oracle Analysis**: Use a secondary "oracle" model to analyze the consistency and bias in the original model's reasoning  

The system identifies four types of flags:

- **Flag 1**: Reasoning B doesn't match Input A/Output A  
- **Flag 2**: Reasoning A doesn't match Input B/Output B  
- **Flag 3**: Failed to correctly guess Question A from reasoning  
- **Flag 4**: Failed to correctly guess Question B from reasoning  

## Project Structure
<pre lang="markdown">
├── deepseek-reasoner_results
├── mistralai_mixtral-8x22b-instruct-v0.1_results
├── openai_gpt-oss-20b_results
├── main.py # Main pipeline orchestrator
├── model_creating_dataset.py # Stage 1: Dataset creation from BBQ
├── oracle.py # Stage 2: Cross-consistency analysis
├── requirements.txt # Dependencies
└── logs/ # Analysis results and summaries </pre>

## Installation
### Clone the repository
> git clone <repository-url>
> cd <repository-name>

### Install dependencies
> pip install -r requirements.txt

# Basic Usage
Run the complete pipeline:
> python3 main.py

The interactive CLI will guide you through:

>1. Model selection (ChatGPT, DeepSeek, or Mistral)

>2. BBQ subset selection 
>Available BBQ subsets:
>   1. Age
>   2. Disability_status
>   3. Gender_identity
>   4. Nationality
>   5. Physical_appearance
>   6. Race_ethnicity
>   7. Race_x_SES
>   8. Race_x_gender
>   9. Religion
>  10. SES
>  11. Sexual_orientation

>Context ambiguity setting (ambiguous/unambiguous)

>Number of pairs to analyze

Available models:
| Key        | Model                    | Provider   |
| ---------- | ------------------------ | ---------- |
| `chatgpt`  | GPT-4 via nscale         | OpenAI     |
| `deepseek` | DeepSeek Reasoner        | DeepSeek   |
| `mistral`  | Mixtral 8x22B via nscale | Mistral AI |

Context conditions:
Context Conditions
>ambig: Ambiguous contexts (multiple plausible interpretations)
>disambig: Unambiguous contexts (clear single interpretation)

# Pipeline
<pre lang="markdown">
DATA SOURCE
│
├── BBQ Dataset
│   ├── Demographic Subset Selection
│   │   (Age/Gender/Race/etc.)
│   └── Context Condition
│       (Ambiguous/Unambiguous)
│
├── DATASET CREATION MODULE
│   ├── Context Matching
│   │   (Identify shared narratives)
│   ├── Question Pairing
│   │   (A→B question mapping)
│   ├── Prompt Template
│   │   (Chain-of-thought format)
│   ├── Model Querying
│   │   (GPT/DeepSeek/Mixtral)
│   ├── Response Parsing
│   │   (Reasoning + Answer extraction)
│   ├── Pair Classification
│   │   (Consistent/Mixed/Both)
│   └── File Output
│       (consistent.jsonl, mixed.jsonl)
│
├── ORACLE ANALYSIS MODULE
│   ├── Cross-Consistency Check
│   │   │
│   │   ├── A→B Validation
│   │   │   (Reasoning B ↔ Answer A)
│   │   └── B→A Validation
│   │       (Reasoning A ↔ Answer B)
│   │
│   ├── Question Guessing Task
│   │   │
│   │   ├── Context + Reasoning A
│   │   │   (Guess: Q_A vs Q_B)
│   │   └── Context + Reasoning B
│   │       (Guess: Q_B vs Q_A)
│   │
│   ├── Flag Detection
│   │   │
│   │   ├── Flag 1: A→B Inconsistency
│   │   ├── Flag 2: B→A Inconsistency
│   │   ├── Flag 3: Q_A Bias
│   │   └── Flag 4: Q_B Bias
│   │
│   └── Results Generation
│       (JSONL + Markdown reports)
│
├── STATISTICAL AGGREGATION
│   ├── Metric Calculation
│   │   (Consistency rate, Flag counts)
│   ├── Significance Testing
│   │   (p-values, Confidence intervals)
│   └── Visualization Data
│       (Charts-ready datasets)
│
└── OUTPUT ARTIFACTS
    ├── Raw Model Responses
    ├── Oracle Analysis Reports
    └── Statistical Summaries </pre>

## Output Files
The system generates comprehensive outputs.
### Dataset Creation Results:
>{model}_results/{subset}_{condition}_consistent.jsonl — Consistent response pairs
>{model}_results/{subset}_{condition}_mixed_cant_determine.jsonl — Mixed response pairs
### Oracle Analysis Results:
>cross_consistency_*.jsonl — Detailed cross-consistency results
>flagged_pairs_*.md — Markdown report of flagged inconsistencies
>BIAS_ANALYSIS_*.md — Summary statistics and analysis
### Log Files
>logs/run_*.json — Complete run metadata and statistics
>logs/run_summary_*.md — Formatted summary reports

# Technical Details
### Prompt Engineering:
The system uses carefully designed prompts to:
- Encourage chain-of-thought reasoning
- Prevent question repetition in reasoning
- Extract structured JSON responses
- Maintain consistent output formatting

### Bias Detection Methodology
Cross-Consistency Analysis: Reasoning for question A should logically support answer B when swapped
Question Disambiguation: Reasoning should not reveal which specific question was asked
Statistical Aggregation: Calculate flag rates across demographic dimensions

### API Integration
Supports multiple LLM providers through OpenAI-compatible APIs:
- DeepSeek API for DeepSeek Reasoner
- NScale API for ChatGPT
- NScale API for Mixtral and other open-source models

### Metrics and Statistics
The analysis provides:
- Consistency Rate: Percentage of fully consistent pairs
- Bias Rate: Percentage showing biased interpretation
- Flag Distribution: Breakdown of four flag types
- Demographic Comparisons: Bias patterns across different subsets
- Context Effects: Differences between ambiguous vs unambiguous contexts

## Research Applications
This tool enables researchers to:
- Compare bias profiles across different LLMs
- Measure improvements in model updates
- Identify specific demographic vulnerabilities
- Understand reasoning inconsistency patterns
- Benchmark model fairness across multiple dimensions

## License
This project is for research purposes. Please ensure compliance with:
- BBQ dataset usage terms
- Respective API provider terms of service
- Ethical AI research guidelines

## Support
For issues and questions:
- Check the existing issues on GitHub
- Review the example outputs in the logs/ directory
- Ensure your API keys are properly configured
- Verify dataset availability from Hugging Face

## Citation
If you use this tool in your research, please cite:
@software{llm_bias_analyzer,
  title = {LLM Bias Analysis Pipeline with BBQ Dataset},
  author = {Emily Heugen},
  year = {2025}

