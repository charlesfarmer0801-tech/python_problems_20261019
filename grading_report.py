"""Score only the problems submitted in the current pull request.

Every changed assignment is worth 10 points, divided among its pytest cases.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROBLEMS = {
    "adding_numbers.py": ("Adding Numbers", 1),
    "list_of_multiples.py": ("List of Multiples", 2),
    "fizz_buzz.py": ("FizzBuzz", 3),
    "basic_calculator.py": ("Basic Calculator", 4),
    "country_area.py": ("Get the Area of a Country", 5),
    "find_the_discount.py": ("Find the Discount", 6),
    "calc_the_profit.py": ("Calculate the Profit", 7),
    "circle_or_square.py": ("Circle or Square", 8),
    "how_many_vowels.py": ("How Many Vowels?", 9),
    "calc_damage.py": ("Calculating Damage", 10),
}


def build_report(xml_path, selection_path):
    if not selection_path.exists():
        return "## Python grading results\n\nCould not determine which assignment files changed. Check the job logs.\n"

    try:
        selection = json.loads(selection_path.read_text(encoding="utf-8"))
        if not isinstance(selection, list) or any(f not in PROBLEMS for f in selection):
            raise ValueError("Invalid assignment selection")
    except (ValueError, OSError) as exc:
        return f"## Python grading results\n\nCould not read the assignment selection: {exc}\n"

    if not selection:
        return (
            "## Python grading results\n\n"
            "**No assignment files were changed.** "
            "Modify an existing assignment .py file to submit a solution.\n"
        )

    if not xml_path.exists():
        return (
            "## Python grading results\n\n"
            "Tests did not produce results. Review the workflow logs. "
            f"Expected tests for: {', '.join(selection)}.\n"
        )

    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as exc:
        return f"## Python grading results\n\nInvalid test results XML: {exc}\n"

    counts = {PROBLEMS[name][1]: [0, 0] for name in selection}
    for case in root.iter("testcase"):
        match = re.search(r"test_(\d{2})_", case.get("classname", ""))
        if not match:
            continue
        number = int(match.group(1))
        if number not in counts:
            continue
        counts[number][1] += 1
        if not any(case.find(tag) is not None for tag in ("failure", "error", "skipped")):
            counts[number][0] += 1

    lines = [
        "## Python grading results",
        "",
        "Only assignment files changed in this pull request are graded.",
        "",
        "| Submitted problem | Tests passed | Score |",
        "|---|---:|---:|",
    ]
    total = 0.0
    for filename in selection:
        name, number = PROBLEMS[filename]
        passed, tested = counts[number]
        points = (10 * passed / tested) if tested else 0
        total += points
        lines.append(f"| {name} ({filename}) | {passed}/{tested} | {points:.1f}/10 |")

    maximum = 10 * len(selection)
    lines.extend([
        "",
        f"**Submitted score: {total:.1f}/{maximum} points**",
        "",
        "Unchanged assignment files are not graded or counted as zero.",
        "Scores reflect automated tests only; instructor review may adjust the grade.",
    ])
    return "\n".join(lines) + "\n"


def main():
    xml_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("results.xml")
    selection_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("grading_selection.json")
    report = build_report(xml_path, selection_path)
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as file:
            file.write(report)


if __name__ == "__main__":
    main()
