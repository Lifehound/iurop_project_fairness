# iurop_project_fairness

Pipeline
- loads the model and dataset with ambigious questions
- Creates a pair (prompt A and prompt B):
-- Make sure that the multiple choice are structured the same for both for fact checking as in answer 1. is the same for prompt A and B, answer 2. is the same for prompt A and B and so also answer 3.
-- Change the prompt format so that the RLM responds with the answer as in X. Y (with X being the number and Y the answer corresponding to that number)
- Save the results in a json file for that model:
-- Save the id of the questions
-- The created id of the pair
-- The questions (not the prompt given)
-- The reasoning of the model
-- The answer

Creating Main.py
There a three models being used in this project:
- openai/gpt-oss-20b ('chatgpt')
- deepseek-reasoner ('deepseek')
- mistralai/mixtral-8x22b-instruct-v0.1 ('mistral')

The dataset used is heegyu/bbq with 11 subsets named:
- Age
- Disability_status
- Gender_identity
- Nationality
- Physical_appearance
- Race_ethnicity
- Race_x_SES
- Race_x_gender
- Religion
- SES
- Sexual_orientation
each subset has a split of ambig and unambig

Modify the two presented code files accordingly so that main.py can run smoothly.
I want main.py to give the user the ability to select the rlm (one of the three models present) by typing in their name that is in the (' ') and the subset by the name of the subset and whether it is ambig or unambig by (y/n) with yes for ambig and no for unambig.
Then I want the pipeline to be such that the script decides what the max amount of pairing is (with the combination of amount of rows in the ambig or disambig section of the subset) and make the model go through all of the pairs using the set prompt and to collect the data as it already has been doing with the added instruction that the model is not allowed to repeat the question in its reasoning.
After that is done I want the main.py file to automatically start running the oracle.py file but then also with what ever model has answered the questions of the subset.
These two files should always run the same model, if creating the dataset was done with chatgpt, then analysing the dataset should also be done by chatgpt. If it was deepseek then also deepseek should analyse the dataset.
The answered pair (a and b) in the dataset will be flagged if:
- reasoning b does not match input a and output a
- reasoning a does not match input b and output b
- 'based on output and reasoning of a what was question a?' answer does not resemble question a
- 'based on output and reasoning of b what was question b?' answer does not resemble question b
if it gets one or two or three or all flagged move it to a .md file with the dedicated model also giving a at most 3 sentence explanation why it got flagged per flag.
Lastly make main.py save every run in a log with:
- which model was used
- amount of pairs created
- amount had inconsistent answers to pairs
- amount mixed determine
- amount both cant determine
- amount flagged for each flag
if possible make it save it in a table with both the real numbers and the percentages when compared with the total pairs



- Bugs found
Parsing is not 100% correct but can be fixed easily based on the raw input (the yes or no)
If a model writes choices are: 1, 2, 3, it will grab three despite all the checks in place, so for future reference that should be masked as well
Moreover, ensure that the choice options aren't able to be confused with number or letters in a normal text like '19' of covid-19 was selected sometimes as an option
--> Change it to 'x, y, z' or similar nonsensical choice pattern

tmux ls 
tmux new-session -s (session name)
tmux attach -t (session name)





## Methodology

### Cross-Consistency Check
We analyze whether the reasoning appropriately accounts for and remains consistent with:
1. The input context and question
2. The output answer

We check consistency in both directions (A→B and B→A) to detect logical inconsistencies.

### Bias Detection via Question Guessing
We use an "oracle" model to reconstruct the original question based on:
- Context
- Model's reasoning
- Final answer

If the guessed question differs substantially from the original question, we flag it as potential bias. This indicates the model may be answering a different question than intended.

## Flag Categories

### 1. Inconsistent Reasoning
Pairs where the reasoning doesn't logically align with the input context/question or output answer.

### 2. Biased Interpretation  
Pairs where the model appears to be answering a different question than intended, suggesting biased interpretation of the context.

## Files Generated

For each dataset, two files are generated:
- `cross_consistency_*.jsonl`: Detailed results in JSONL format
- `flagged_pairs_*.md`: Markdown report of flagged pairs with analysis

## Interpretation

- **High inconsistent rates** may indicate reasoning flaws in the model
- **High bias rates** may indicate the model is making unwarranted assumptions or stereotypes
- **Combined flags** suggest serious issues with model understanding
"""
# README

## Overview

This repository implements an evaluation pipeline for analyzing reasoning consistency and bias in large language models using the BBQ benchmark. The pipeline constructs paired question instances that share identical contextual information, queries a selected language model for structured reasoning and answers, and applies a secondary oracle analysis to evaluate cross consistency, internal coherence, and potential biased interpretations. The overall goal is to produce a derived dataset that allows systematic inspection of how models handle ambiguous and disambiguated social scenarios.

The codebase is organized into three main components. The first component creates paired prompts and model responses from the BBQ dataset. The second component runs the main experimental pipeline and logging. The third component performs oracle based post hoc analysis of the generated responses.

## File Structure

### `model_creating_dataset.py`

This file is responsible for dataset construction and initial model querying. It loads subsets of the BBQ dataset, groups examples that share the same context, and constructs paired prompts where each context is associated with two distinct questions. For each question, the model is prompted to provide both a reasoning trace and a final answer in a structured JSON format.

The script handles prompt construction, model querying, output parsing, and result serialization. It produces JSONL files that store paired responses, metadata, and indicators of whether the model selected a "can't determine" option. Results are separated into fully consistent pairs and pairs with mixed "can't determine" behavior.

Key responsibilities include:

* Building structured reasoning prompts from context, questions, and answer choices.
* Pairing examples with identical contexts.
* Querying a configurable language model endpoint.
* Extracting answers and reasoning from raw model outputs.
* Saving cleaned and serialized results for downstream analysis.

### `main.py`

This file orchestrates the full experimental pipeline. It provides a command line interface for selecting the model, BBQ subset, and ambiguity condition. It then executes dataset creation followed by oracle analysis, and finally logs aggregated statistics.

The script manages configuration for multiple models, controls experiment flow, and produces both JSON and Markdown summaries of each run. These summaries include counts and proportions of consistent answers, mixed ambiguity cases, and oracle flagged instances.

Key responsibilities include:

* User driven selection of experimental settings.
* Execution of dataset creation.
* Invocation of oracle analysis.
* Aggregation and logging of results.

### `oracle.py`

This file implements the oracle analysis used to evaluate reasoning consistency and potential bias. It operates on the JSONL files produced during dataset creation and applies multiple checks using a language model as an evaluator.

The oracle performs cross consistency checks by verifying whether the reasoning for one question remains logically consistent when evaluated against the other question and answer sharing the same context. It also includes a question guessing task in which the model is asked to infer which question was originally asked based solely on the context, reasoning, and answer.

Key responsibilities include:

* Loading and grouping dataset result files.
* Constructing evaluation prompts for cross consistency and question inference.
* Querying the oracle model.
* Flagging inconsistent or biased reasoning patterns.
* Producing detailed JSONL and Markdown reports of flagged cases.

## Requirements

The project relies on standard Python scientific and NLP libraries, including pandas, datasets, tqdm, scikit learn, and the OpenAI compatible client interface. Access to external model APIs is required, and valid API keys must be provided in the configuration.

## Usage

To run the full pipeline, execute `main.py` and follow the interactive prompts to select the model, BBQ subset, and context condition. Results and logs will be written to model specific result directories and a central logs folder.

---

# Method

## Dataset Construction

The study is based on the BBQ benchmark, which contains context question answer triples designed to probe social bias and ambiguity in language understanding. From each selected subset, examples were filtered by context condition, distinguishing between ambiguous and disambiguated contexts. Examples sharing identical context text were grouped together. Only contexts associated with exactly two questions were retained in order to form paired instances.

For each retained context, two prompts were generated, one per question. Both prompts included the same context and answer choices but differed only in the question. The prompts instructed the model to analyze the context, evaluate the relevance and factual correctness of information, and return both a reasoning trace and a final answer in JSON format. This design ensured that any differences in reasoning or answers could be attributed to the question rather than the contextual information.

## Model Querying

Each prompt was submitted independently to the selected language model using a fixed temperature and a high token limit to avoid truncation. For robustness, up to three retry attempts were made in the event of API errors. Model outputs were parsed using pattern matching to extract the final answer index, the associated answer text, and the free form reasoning. All outputs were stored without modification, aside from minimal cleaning required for serialization.

Pairs were classified according to whether the model produced identical answers for both questions and whether either response selected the predefined "can't determine" option. This resulted in two primary groups: fully consistent answer pairs and mixed ambiguity pairs.

## Oracle Based Evaluation

A secondary evaluation stage was applied to the generated dataset using an oracle model. The oracle analysis focused on internal consistency rather than correctness with respect to gold labels. Two forms of analysis were conducted.

First, cross consistency checks evaluated whether the reasoning produced for one question remained logically coherent when assessed against the other question and answer that shared the same context. The oracle was instructed to return a binary judgment indicating consistency, along with a brief justification.

Second, a question inference task tested whether the reasoning and answer implicitly encoded the original question. The oracle was presented with the context, reasoning, and answer, along with four candidate questions, two of which were correct and two distractors. Failure to identify the original question was treated as evidence of potential bias or question insensitive reasoning.

## Aggregation and Reporting

Results from oracle evaluation were aggregated across all processed pairs. Pairs were flagged if they exhibited inconsistent reasoning, biased question inference, or both. Summary statistics were computed to quantify the prevalence of each failure mode. Detailed JSONL files and human readable Markdown reports were generated to support further qualitative analysis.

This methodology emphasizes transparency and reproducibility by separating dataset construction, model inference, and evaluation into clearly defined stages, while relying on identical contexts to isolate question driven effects in model reasoning.

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

