
from datetime import date


def format_visitor_name(name):
    """
    Formats a full name as 'Surname, Given names'.
    Handles empty and invalid inputs safely.
    """
    if not isinstance(name, str) or not name.strip():
        return ""

    parts = name.split()

    if len(parts) == 1:
        return parts[0].title()

    surname = parts[-1].title()
    given_names = ' '.join(parts[:-1]).title()

    return surname + ', ' + given_names


def parse_group_ages(text):
    """
    Parses space-separated ages into a list of integers.
    Ignores invalid entries and handles unexpected inputs.
    """
    if not isinstance(text, str) or not text.strip():
        return []

    ages = []

    for age in text.split():
        try:
            value = int(age)
            if value >= 0:
                ages.append(value)
        except ValueError:
            continue

    return ages


def parse_visit_date(text):
    """
    Parses a YYYY-MM-DD date into a (year, month, day) tuple.
    Returns None for invalid dates or inputs.
    """
    if not isinstance(text, str):
        return None

    try:
        year, month, day = map(int, text.strip().split('-'))

        date(year, month, day)

        return year, month, day

    except (ValueError, TypeError, OverflowError):
        return None


def main():
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    print("Name on ticket:", format_visitor_name(value))

    print("\n==== Running parse_group_ages ====")
    value = input("Enter the ages in the group separated by spaces (e.g. 34 12 70): ")
    print("Group ages:", parse_group_ages(value))

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    print("Visit date (year, month, day):", parse_visit_date(value))


if __name__ == "__main__":
    main()


