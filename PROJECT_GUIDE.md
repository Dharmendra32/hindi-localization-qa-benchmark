# Hindi Localization QA Benchmark — Project Guide

**Author:** Dharmendra Singh  
**Repository:** <https://github.com/Dharmendra32/hindi-localization-qa-benchmark>  
**Focus:** English-to-Hindi localization quality assurance, terminology validation, Python testing, and AI-agent benchmark evaluation.

---

## 1. Project overview

The Hindi Localization QA Benchmark is a small Python project for checking whether an AI agent can review English-to-Hindi machine-translated (MT) strings, identify localization errors, and propose corrected Hindi translations.

The benchmark uses three kinds of data:

1. **Input data** — English source strings, their Hindi MT output, and an approved terminology glossary.
2. **Reference data** — human-prepared expected findings and corrections.
3. **Agent submission** — the JSON output produced by the AI agent being evaluated.

Python scripts validate the data, perform a deterministic terminology check, run unit tests, and compare an agent submission with the reference answers.

> **Scope note:** This is a controlled starter benchmark, not a complete automated measure of translation quality. Exact reference matching is useful for repeatable tests, but different valid Hindi phrasings may be marked as mismatches. Linguistic judgement is still needed when creating and reviewing reference answers.

## 2. What the benchmark evaluates

The task asks an AI agent to review each Hindi translation against its English source and the supplied glossary. The agent must identify applicable errors, explain them, and provide a corrected translation.

| Error category | Meaning | Example of what to look for |
|---|---|---|
| `TERMINOLOGY` | An unapproved or inconsistent term is used | Glossary says `खाता`, but the translation uses `अकाउंट` |
| `MEANING` | The translation changes the source meaning | “may” is translated as “must” |
| `OMISSION` | Important source information is missing | A condition or instruction is left untranslated |
| `ADDITION` | Information not present in the source is introduced | A new promise or condition is added |
| `GRAMMAR` | A significant grammatical problem affects the Hindi | Incorrect agreement or sentence construction |
| `FORMAT` | A placeholder or required formatting is changed | `{name}` is removed or altered |

The benchmark currently includes six sample records. It is intentionally small so the scripts and evaluation logic are easy to inspect and extend.

## 3. Repository structure

```text
linguistics_benchmark/
├── .github/
│   └── workflows/
│       └── ci.yml
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
├── PROJECT_GUIDE.md
└── task.md
```

### What each file does

- `task.md` describes the task instructions, error categories, output fields, and success criteria.
- `input/source.csv` contains record IDs, English source strings, and Hindi MT output.
- `input/glossary.json` contains approved English-to-Hindi terminology.
- `reference/expected_output.json` contains the expected error labels, explanations, and corrected translations.
- `output/agent_output.json` is the submission file evaluated by the benchmark.
- `tests/validate_inputs.py` checks input and reference data structure and consistency.
- `tests/check_terminology.py` performs a deterministic glossary-compliance check.
- `tests/test_terminology.py` contains unit tests for the terminology-checking helper functions.
- `tests/evaluate_agent.py` compares an agent submission with the reference answers.
- `.github/workflows/ci.yml` runs the checks automatically on GitHub Actions.

## 4. Input data

### 4.1 `input/source.csv`

The CSV file has three required columns: `id`, `source`, and `mt`.

```csv
id,source,mt
001,"Sign in to your account to continue.","जारी रखने के लिए अपने खाते में साइन इन करें।"
002,"Your password must contain at least 8 characters.","आपके पासवर्ड में कम से कम 8 वर्ण होने चाहिए।"
003,"Click the Settings icon to change your preferences.","अपनी प्राथमिकताएं बदलने के लिए सेटिंग आइकन पर क्लिक करें।"
004,"We couldn't find your account.","हम आपका अकाउंट नहीं खोज सके।"
005,"Please enter your email address.","कृपया अपना ईमेल पता दर्ज करें।"
006,"You can reset your password from the Settings page.","आप सेटिंग पृष्ठ से अपना पासवर्ड रीसेट कर सकते हैं।"
```

Each row is one segment to review. The `id` connects the source record to its corresponding reference answer and agent submission. IDs should be unique and should be preserved in the output.

### 4.2 `input/glossary.json`

The glossary is a JSON object in which each English key maps to an approved Hindi term.

```json
{
  "account": "खाता",
  "password": "पासवर्ड",
  "settings": "सेटिंग्स",
  "preferences": "प्राथमिकताएं",
  "email address": "ईमेल पता",
  "reset": "रीसेट"
}
```

The glossary is the terminology authority for this benchmark. If a term appears in the source, the Hindi translation should use the approved Hindi equivalent or a specifically documented accepted grammatical form.

A glossary needs clear rules for inflected forms. For example, `खाते` may be an acceptable grammatical form of `खाता` in a sentence such as `अपने खाते में`. This project currently handles that example with a small manually maintained accepted-variants dictionary in the terminology checker.

## 5. Agent output and reference format

Both `reference/expected_output.json` and `output/agent_output.json` use a JSON array containing one object per source ID.

Example record:

```json
{
  "id": "003",
  "has_error": true,
  "error_types": ["TERMINOLOGY"],
  "explanation": "The translation uses 'सेटिंग' instead of the approved glossary term 'सेटिंग्स'.",
  "corrected_translation": "अपनी प्राथमिकताएं बदलने के लिए सेटिंग्स आइकन पर क्लिक करें।"
}
```

The required fields are:

| Field | Expected type | Purpose |
|---|---|---|
| `id` | String | Links the result to the input segment |
| `has_error` | Boolean | Indicates whether an error was identified |
| `error_types` | Array of strings | Lists applicable error categories |
| `explanation` | String | Explains the finding |
| `corrected_translation` | String | Supplies the corrected Hindi translation |

Use JSON strings for IDs, including IDs with leading zeroes. Do not return comments or trailing commas in JSON. Preserve placeholders and required formatting exactly.

## 6. Input validation

Run the input validator before evaluating a submission:

```powershell
python tests/validate_inputs.py
```

The validator checks:

- The CSV contains the required `id`, `source`, and `mt` columns.
- Source IDs are unique.
- Required source fields are not blank.
- The glossary is a non-empty JSON object with non-empty string terms and translations.
- Reference records contain the required fields.
- `has_error` is a Boolean and `error_types` is a list.
- Error categories belong to the allowed set.
- `has_error` agrees with whether `error_types` is empty.
- Reference IDs are unique and match the source IDs.

The script uses Python's built-in `csv`, `json`, `pathlib`, and `re` modules, so no third-party package installation is needed.

### Important validation limitation

The current validator is designed for the known project schema. It can be made more defensive by checking that the top-level reference JSON value is a list, checking the types of every field, and handling malformed or missing files with clear error messages. These are useful next improvements before treating the project as a robust external benchmark.

## 7. Deterministic terminology checker

Run:

```powershell
python tests/check_terminology.py
```

The checker:

1. Loads the glossary JSON.
2. Loads the source CSV.
3. Checks whether each English glossary term appears in the source string.
4. If it does, checks whether the approved Hindi term appears in the MT output.
5. Reports records where the expected term is not found.

A regular expression with word boundaries is used for English term matching:

```python
pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
return re.search(pattern, source, re.IGNORECASE) is not None
```

`re.escape()` treats glossary terms as literal text. `re.IGNORECASE` makes English matching case-insensitive. The lookbehind and lookahead help prevent a short term from matching as part of a larger word.

The project has a manually defined accepted-variants dictionary for the `account` term:

```python
APPROVED_VARIANTS = {
    "account": ["खाता", "खाते"],
}
```

This allows the checker to accept the inflected form `खाते` in the first sample record while still flagging `अकाउंट` in record `004`.

### Current sample findings

The sample data is designed to produce three terminology violations:

- ID `003`: `सेटिंग` is used instead of `सेटिंग्स`.
- ID `004`: `अकाउंट` is used instead of `खाता`.
- ID `006`: `सेटिंग` is used instead of `सेटिंग्स`.

### Limitations of string matching

This checker does not understand Hindi morphology, syntax, or context. It checks for the presence of text, not whether a term is used correctly in every grammatical context. It may also miss a violation if an unapproved form happens to contain the approved string. A more advanced version could use token-aware matching, morphology rules, contextual checks, and human-reviewed exceptions.

## 8. Unit tests

Run the tests with:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The current test file checks helper-function behaviour, including:

- Finding an English term in a source sentence.
- Matching English terms without case sensitivity.
- Avoiding a match inside a larger concatenated word.
- Accepting an approved Hindi form.
- Rejecting an unapproved Hindi form.

A successful run currently reports five passing tests. Unit tests check small pieces of logic independently; they do not prove that the benchmark detects every possible localization issue.

## 9. Reference-based benchmark evaluator

Run:

```powershell
python tests/evaluate_agent.py
```

The evaluator loads the reference answers and the agent submission, maps each list by `id`, and compares three dimensions:

1. **Error detection:** Does `has_error` match the reference?
2. **Error categories:** Does the set of submitted `error_types` match the reference categories?
3. **Corrected translation:** Does `corrected_translation` exactly match the reference string?

It also reports missing and extra IDs. Each dimension is scored as a count and percentage.

### Example scoring interpretation

If six records are expected and five error-detection decisions match, the score is:

```text
error_detection: 5/6 (83.3%)
```

The final result is `PASS` only when there are no missing or extra IDs and all three score dimensions match every reference record.

### Exact-match limitation

The current correction score uses exact string equality. A linguistically valid alternative Hindi translation may therefore receive a mismatch if it differs from the reference punctuation, wording, or spacing. For a larger benchmark, consider combining exact match with human evaluation, terminology checks, semantic similarity, and structured error-specific scoring. Do not interpret this exact-match score as a complete measure of translation quality.

## 10. Running the full project locally

Open PowerShell in the project directory:

```powershell
cd "C:\Users\Dharmendra Singh\linguistics_benchmark"
```

Run the checks in this order:

```powershell
python tests/validate_inputs.py
python tests/check_terminology.py
python -m unittest discover -s tests -p "test_*.py" -v
python tests/evaluate_agent.py
```

The evaluator expects a valid submission at `output/agent_output.json`. To run a baseline comparison, that file can contain a copy of the reference answers. This verifies the evaluator's comparison path, but it is **not** evidence that an independent AI agent achieved a perfect score.

To restore the baseline file from the reference answers in PowerShell:

```powershell
Copy-Item reference\expected_output.json output\agent_output.json -Force
```

Then rerun the evaluator:

```powershell
python tests/evaluate_agent.py
```

For a meaningful benchmark result, replace the baseline with an independently generated agent submission before evaluating it.

## 11. GitHub Actions continuous integration

The workflow file is:

```text
.github/workflows/ci.yml
```

It runs on:

- Pushes to the `main` branch.
- Pull requests targeting `main`.
- Manual runs using the GitHub Actions interface (`workflow_dispatch`).

The workflow checks out the repository, sets up Python 3.12 on an Ubuntu runner, and runs input validation, terminology checks, unit tests, and reference-based evaluation.

To inspect a run, open the repository on GitHub, select **Actions**, and open the latest `Hindi Localization QA Benchmark CI` run.

A green check means the configured commands completed successfully. It does not mean that every possible Hindi localization error is detected. The workflow also depends on `output/agent_output.json` being a valid submission file.

## 12. Git workflow used to publish the project

The local repository was initialized and connected to GitHub with these commands:

```powershell
git init
git status
git add .
git commit -m "Initial commit: Hindi Localization QA Benchmark"
git branch -M main
git remote add origin https://github.com/Dharmendra32/hindi-localization-qa-benchmark.git
git push -u origin main
```

For later changes, the usual workflow is:

```powershell
git status
git add README.md
git commit -m "Update project documentation"
git push
```

Replace `README.md` in the `git add` command with the file or folder you actually changed. Review `git status` before committing so you know what will be included.

## 13. Troubleshooting

### `python` is not recognised

Check that Python is installed and added to PATH. On Windows, this may also work:

```powershell
py --version
```

### `FileNotFoundError`

Confirm that PowerShell is in the project root and that the expected file exists:

```powershell
Get-Location
Get-ChildItem
```

### `ModuleNotFoundError`

The current scripts use Python standard-library modules. Check that the command is being run with the expected Python interpreter. If future dependencies are added, document them and add a dependency file such as `requirements.txt`.

### Git says `pathspec ... did not match any files`

The file may not exist in the current directory or may have a different extension. Check with:

```powershell
Get-ChildItem -Force
```

### GitHub Actions fails

Open the failed workflow run, expand the failed step, and read the first relevant error message. Reproduce the same command locally before changing the workflow.

## 14. Future development roadmap

Potential next improvements include:

1. Harden validation against malformed JSON, missing fields, duplicate submission IDs, and incorrect data types.
2. Add placeholder and formatting validation, including `{name}`, `%s`, HTML tags, and ICU-style messages.
3. Improve Hindi terminology handling with morphology-aware matching and reviewed grammatical variants.
4. Add test cases for meaning changes, omissions, additions, grammar, and formatting—not only terminology.
5. Add larger, balanced datasets with documented annotation guidelines.
6. Separate benchmark scoring from the reference data and report per-category precision, recall, and F1 where appropriate.
7. Add semantic or human-reviewed evaluation for valid alternative translations.
8. Add more language pairs only after defining language-specific terminology and evaluation rules.

## 15. Skills demonstrated

This project brings together practical skills in:

- English-to-Hindi localization and linguistic quality assurance.
- Terminology management and glossary compliance.
- Python scripting and file processing with CSV and JSON.
- Regular expressions and deterministic text checks.
- Unit testing with `unittest`.
- Reference-based evaluation of AI-agent outputs.
- Git, GitHub, and GitHub Actions CI workflows.

The project is a practical demonstration of applying localization domain knowledge to a reproducible Python-based evaluation workflow.

---

**Author:** Dharmendra Singh  
**GitHub repository:** <https://github.com/Dharmendra32/hindi-localization-qa-benchmark>
