# Hindi Localization QA Benchmark

A Python-based benchmark designed to evaluate AI agents on English-to-Hindi localization quality assurance tasks.

## Project Overview

This project evaluates whether an AI agent can identify and correct common localization errors in Hindi machine-translated content.

The benchmark focuses on linguistic accuracy, terminology compliance, meaning preservation, and output consistency.

## Key Features

- **Terminology validation:** Checks whether approved glossary terms are used correctly.
- **Error detection:** Evaluates terminology, meaning, omission, addition, grammar, and formatting errors.
- **Translation correction:** Compares corrected Hindi translations against reference answers.
- **Input validation:** Checks CSV, JSON, required fields, and matching record IDs.
- **Automated testing:** Uses Python's unittest framework.
- **Benchmark evaluation:** Measures AI agent performance against reference outputs.

## Project Structure

```text
linguistics_benchmark/
├── input/
│   ├── glossary.json
│   └── source.csv
├── output/
│   └── agent_output.json
├── reference/
│   └── expected_output.json
├── tests/
│   ├── check_terminology.py
│   ├── evaluate_agent.py
│   ├── test_terminology.py
│   └── validate_inputs.py
├── .gitignore
├── README.md
└── task.md
```

## Requirements

- Python 3.10 or later
- No external Python packages required.

## How to Run

Clone the repository:

```bash
git clone https://github.com/Dharmendra32/hindi-localization-qa-benchmark.git
cd hindi-localization-qa-benchmark
```

### 1. Validate Input Files

```bash
python tests/validate_inputs.py
```

Checks the input CSV, glossary, reference JSON, and record IDs.

### 2. Run Terminology Checks

```bash
python tests/check_terminology.py
```

Identifies translations that do not follow the approved terminology.

### 3. Run Unit Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Executes automated tests for terminology-checking functions.

### 4. Evaluate an AI Agent Submission

Place the agent's JSON response in:

`output/agent_output.json`

Then execute:

```bash
python tests/evaluate_agent.py
```

The evaluator measures:

- Error detection accuracy
- Error category accuracy
- Corrected translation accuracy
- Missing and extra record IDs

## Error Categories

| Category | Description |
|---|---|
| TERMINOLOGY | Incorrect or inconsistent glossary usage |
| MEANING | Changes to the original meaning |
| OMISSION | Missing source information |
| ADDITION | Unnecessary information added |
| GRAMMAR | Significant grammatical errors |
| FORMAT | Changes to placeholders or required formatting |

## Technologies Used

- Python
- CSV and JSON processing
- Regular expressions
- Unit testing
- Git and GitHub
- Localization QA methodologies

## Current Limitations

The terminology checker uses deterministic string matching and predefined accepted variants. It does not fully understand Hindi morphology, context, or semantic equivalence.

The reference evaluator uses exact comparison for corrected translations. This makes it suitable for a controlled benchmark but does not independently establish whether an unseen translation is linguistically correct.

## Future Improvements

- Add semantic translation evaluation.
- Improve Hindi morphology and contextual terminology checks.
- Introduce placeholder and formatting validation.
- Expand the benchmark with more linguistic error examples.
- Add automated GitHub Actions testing.
- Develop support for additional language pairs.

## Author

**Dharmendra Singh**

Localization | Machine Translation | Linguistic QA | Language AI

GitHub: [Dharmendra32](https://github.com/Dharmendra32)

## Detailed Documentation

For a complete explanation of the project architecture, Python scripts, testing methodology, benchmark evaluation, and GitHub Actions setup, see:

[Read the Complete Project Guide](PROJECT_GUIDE.md)
