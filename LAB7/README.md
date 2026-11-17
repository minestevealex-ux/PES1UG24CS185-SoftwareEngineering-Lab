
# L6_L7_54 - Museum Admission

## Lab 7: Fuzz Testing for Input Validation Bugs

### Objective

To apply property-based fuzz testing using the Hypothesis library to identify input validation bugs in a Python application and improve its robustness by fixing the discovered issues.

### Project Structure

```text
LAB7/
├── museum_admission_parser.py
├── test_museum_admission_parser.py
├── Lab7_FuzzTesting_Evidence.pdf
└── README.md
```

### Requirements

- Python 3.8+
- Hypothesis
- Pytest

### Installation

Install the required dependencies:

```bash
pip install hypothesis pytest
```

### Execution

Navigate to the LAB7 directory:

```bash
cd LAB7
```

Run the original/fixed application:

```bash
python museum_admission_parser.py
```

Run the fuzz tests:

```bash
python -m pytest test_museum_admission_parser.py -v
```

### Functions Tested

1. `format_visitor_name()` - Formats visitor names into surname-first format and handles empty or invalid inputs.

2. `parse_group_ages()` - Parses space-separated group ages into integers while handling invalid entries and unexpected inputs.

3. `parse_visit_date()` - Parses dates in YYYY-MM-DD format and validates calendar dates.

### Fuzz Testing

Hypothesis was used to generate unexpected and edge-case inputs automatically.

The tests were designed to identify crashes caused by invalid inputs, including:

- Empty strings and None values.
- Unexpected data types.
- Non-numeric age values.
- Invalid date formats.
- Impossible calendar dates.

### Bugs Fixed

- Added input type and empty-value validation.
- Added exception handling for invalid age values.
- Added validation for negative ages.
- Added proper calendar date validation.
- Ensured the functions handle unexpected inputs without crashing.

### Test Results

All three Hypothesis fuzz tests passed after fixing the application.

```text
3 passed
```

### Screenshots and Evidence

`Lab7_FuzzTesting_Evidence.pdf` contains the screenshots documenting:

- SS1: Original application execution.
- SS2: Failing fuzz tests on the buggy application.
- SS3: Execution of the fixed application.
- SS4: Successful fuzz tests after fixing the bugs.

### Deliverables

1. Fixed `museum_admission_parser.py`.
2. Updated `test_museum_admission_parser.py`.
3. `Lab7_FuzzTesting_Evidence.pdf`.


