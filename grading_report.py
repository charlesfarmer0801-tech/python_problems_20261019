"""Student-friendly pass/fail and grading feedback for submitted assignments."""
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


def _safe_markdown(value):
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _status(test):
    for key in ("failure", "error", "skipped"):
        node = test.find(key)
        if node is not None:
            return key, node
    return "passed", None


def _friendly_case(name):
    bracket = re.search(r"\[([^\]]+)\]$", name)
    if bracket:
        return bracket.group(1).replace("-", " ").capitalize()
    return name.replace("_", " ").capitalize()


def _feedback(node):
    text = (node.get("message", "") or (node.text or "")).strip()
    if not text:
        return "The test could not complete. Open the test log for details."
    text = re.sub(r"^(?:AssertionError|Failed):\s*", "", text)
    # Don't show the student's entire traceback in the friendly report.
    if "\n" in text and not text.startswith("Expected:"):
        text = text.splitlines()[0]
    return text[:700]


def _annotation(filename, title, message):
    # Escape GitHub Actions workflow command separators and newlines.
    def escape(value):
        return (str(value).replace("%", "%25").replace("\r", "%0D")
                .replace("\n", "%0A").replace(":", "%3A"))
    print(f"::error file={escape(filename)},title={escape(title)}::{escape(message[:400])}")


def build_report(xml_path, selection_path):
    if not selection_path.exists():
        return "## Python grading results\n\nCould not identify changed assignment files. Review the workflow logs.\n", []
    try:
        selected = json.loads(selection_path.read_text(encoding="utf-8"))
        if not isinstance(selected, list) or any(name not in PROBLEMS for name in selected):
            raise ValueError("Invalid assignment file list")
    except (OSError, ValueError) as exc:
        return f"## Python grading results\n\nCould not read selected assignments: {exc}\n", []

    if not selected:
        return (
            "## Python grading results\n\nNo assignment Python files changed. "
            "Submit edits to one or more existing assignment files.\n"
        ), []

    if not xml_path.exists():
        return "## Python grading results\n\nTests did not generate results. Check the workflow logs.\n", []
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as exc:
        return f"## Python grading results\n\nTest results could not be parsed: {exc}\n", []

    cases = {PROBLEMS[name][1]: [] for name in selected}
    for node in root.iter("testcase"):
        match = re.search(r"test_(\d{2})_", node.get("classname", ""))
        if not match or int(match.group(1)) not in cases:
            continue
        number = int(match.group(1))
        status, error = _status(node)
        cases[number].append((node.get("name", "test"), status, error))

    lines = [
        "## Python grading results", "",
        "Only the assignment files changed in this pull request are graded.",
        "",
        "| Submitted problem | Passed / Tested | Score |",
        "|---|---:|---:|",
    ]
    annotations = []
    total = 0.0
    for filename in selected:
        title, number = PROBLEMS[filename]
        records = cases[number]
        passed = sum(status == "passed" for _, status, _ in records)
        score = 10 * passed / len(records) if records else 0
        total += score
        lines.append(f"| {_safe_markdown(title)} | {passed}/{len(records)} | {score:.1f}/10 |")

    lines += ["", f"**Current submission: {total:.1f}/{len(selected)*10} points**", "",
              "For overall progress out of 100, see the grading comment on the pull request.", "",
              "---", ""]

    for filename in selected:
        title, number = PROBLEMS[filename]
        records = cases[number]
        lines += [f"### {title}", "", "| Test case | Result |", "|---|---|"]
        if not records:
            lines.append("| Tests could not be collected | ❌ Check workflow logs |")
        for name, status, _ in records:
            icon = "✅ Passed" if status == "passed" else ("⚪ Skipped" if status == "skipped" else "❌ Failed")
            lines.append(f"| {_safe_markdown(_friendly_case(name))} | {icon} |")
        lines.append("")
        for name, status, problem in records:
            if status not in ("failure", "error"):
                continue
            label = _friendly_case(name)
            explanation = _feedback(problem)
            lines.append(f"**❌ {label}**")
            lines.append("")
            for line in explanation.splitlines():
                if line.strip():
                    lines.append("> " + _safe_markdown(line))
            lines += ["", ""]
            annotations.append((filename, f"{title}: {label}", " | ".join(explanation.splitlines())))
        if not records:
            annotations.append((filename, title, "No tests were collected. Review the test runner logs."))

    lines += ["", "*These results are automated checks, not a replacement for instructor review.*"]
    return "\n".join(lines) + "\n", annotations



def write_pr_artifact(xml_path, selection_path, report):
    """Export a small, validated data file for a separate PR-comment workflow."""
    if not (xml_path.exists() and selection_path.exists()):
        return
    try:
        selection = json.loads(selection_path.read_text(encoding="utf-8"))
        root = ET.parse(xml_path).getroot()
    except (ValueError, OSError, ET.ParseError):
        return

    if (not isinstance(selection, list) or not selection
            or len(selection) != len(set(selection))
            or any(name not in PROBLEMS for name in selection)):
        return

    counts = {PROBLEMS[name][1]: [0, 0] for name in selection}
    for case in root.iter("testcase"):
        match = re.search(r"test_(\d{2})_", case.get("classname", ""))
        if not match:
            continue
        number = int(match.group(1))
        if number not in counts:
            continue
        counts[number][1] += 1
        if _status(case)[0] == "passed":
            counts[number][0] += 1

    # A pytest collection error still counts as zero for the submitted problem.
    # But if there is no XML at all (infrastructure failure), don't replace scores.
    scores = {
        name: round(10 * counts[PROBLEMS[name][1]][0] /
                    counts[PROBLEMS[name][1]][1], 6)
        if counts[PROBLEMS[name][1]][1] else 0
        for name in selection
    }
    target = Path("grading-feedback")
    target.mkdir(exist_ok=True)
    data = {
        "version": 1,
        "pr_number": int(os.environ.get("GRADE_PR_NUMBER", "0")),
        "head_sha": os.environ.get("GRADE_HEAD_SHA", ""),
        "scores": scores,
    }
    (target / "grade.json").write_text(
        json.dumps(data, sort_keys=True), encoding="utf-8"
    )
    (target / "details.md").write_text(report[:30000], encoding="utf-8")

def main():
    xml_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("results.xml")
    selection_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("grading_selection.json")
    report, annotations = build_report(xml_path, selection_path)
    print(report)
    write_pr_artifact(xml_path, selection_path, report)
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(report)
    for filename, title, message in annotations[:20]:
        _annotation(filename, title, message)
    if len(annotations) > 20:
        print(f"Additional failed tests: {len(annotations)-20}. See the full job summary.")


if __name__ == "__main__":
    main()
