
# Hindi Localization QA Benchmark

## 1. Objective

Evaluate whether an AI agent can perform professional English-to-Hindi localization quality assurance.

## 2. Input Files

The agent will receive:

- source.csv: English source strings and their IDs.
- glossary.json: Approved English-to-Hindi terminology.

## 3. Task Instructions

For each source string:

1. Review the Hindi machine translation.
2. Compare it against the English source.
3. Check compliance with the supplied glossary.
4. Identify all applicable linguistic errors.
5. Explain each identified error.
6. Provide a corrected Hindi translation.

## 4. Error Categories

Use the following categories:

- TERMINOLOGY: Incorrect or inconsistent glossary usage.
- MEANING: Translation changes the original meaning.
- OMISSION: Important source information is missing.
- ADDITION: Information not present in the source is added.
- GRAMMAR: Significant grammatical errors.
- FORMAT: Placeholders or required formatting are changed.

## 5. Output Requirements

Return one JSON object for every input ID.

Each object must contain:

- id
- has_error
- error_types
- explanation
- corrected_translation

## 6. Important Rules

- Do not skip any input IDs.
- Do not invent information.
- Follow the approved glossary.
- Preserve all placeholders exactly.
- Use natural, professional Hindi.
- Return valid JSON only.

## 7. Success Criteria

The task is successful when all input records are evaluated, all applicable errors are identified, corrections are accurate, and the output follows the required JSON structure.
