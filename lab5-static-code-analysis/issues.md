# Lab 5: Static Code Analysis

## Issues Identified and Fixed

| Issue | Type | Tool | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded password | Security | Bandit | Supervisor password was stored directly in the source code. | Read the password from an environment variable. |
| Unsafe eval() | Security | Bandit | eval() could execute arbitrary Python expressions. | Replaced it with a restricted arithmetic expression parser. |
| Weak MD5 hash | Security | Bandit | MD5 was used to generate SKU fingerprints. | Replaced MD5 with SHA-256. |
| Bare exception | Bug | Bandit, Flake8 | A bare except silently ignored all errors. | Added specific exception handling and logging. |
| Unused imports | Code quality | Pylint, Flake8 | Some imported modules were not used. | Removed unused imports and used logging where appropriate. |
| Mutable default argument | Bug | Code review | The history list was shared across calls. | Changed the default to None. |
| Unused variable | Code quality | Flake8 | total_units was calculated but never used. | Removed the unnecessary variable. |
| Poor formatting | Style | Flake8 | Several functions had incorrect spacing and lines exceeded the limit. | Reformatted the code. |
| Missing SKU handling | Bug | Code review | Accessing an unknown SKU could raise a KeyError. | Used dictionary get() with a default value. |
| Invalid SKU type | Validation | Code review | Numeric SKUs were accepted. | Added SKU type validation. |

## Results

- Original Pylint score: 4.48/10
- Updated Pylint score: 9.83/10
- Original Bandit findings: 5
- Updated Bandit findings: 0
- Flake8: Check the final report for the verified result.
