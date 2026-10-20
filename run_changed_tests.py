"""Run only tests for Python assignment files changed in the pull request.

The student checkout is GitHub's PR merge commit. HEAD^1 is the current
base branch, so comparing HEAD^1..HEAD identifies the submitted changes.
"""
import json
import subprocess
import sys
from pathlib import Path

ASSIGNMENTS = {
    "adding_numbers.py": "test_01_adding_numbers.py",
    "list_of_multiples.py": "test_02_list_of_multiples.py",
    "fizz_buzz.py": "test_03_fizz_buzz.py",
    "basic_calculator.py": "test_04_basic_calculator.py",
    "country_area.py": "test_05_country_area.py",
    "find_the_discount.py": "test_06_find_the_discount.py",
    "calc_the_profit.py": "test_07_calc_the_profit.py",
    "circle_or_square.py": "test_08_circle_or_square.py",
    "how_many_vowels.py": "test_09_how_many_vowels.py",
    "calc_damage.py": "test_10_calc_damage.py",
}

GRADER_DIR = Path(__file__).resolve().parent
SELECTION_PATH = Path("grading_selection.json")


def main():
    student_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "student").resolve()

    # Use null-delimited names to safely handle filenames containing spaces.
    result = subprocess.run(
        ["git", "-C", str(student_dir), "diff", "--name-only", "-z",
         "HEAD^1", "HEAD", "--"],
        stdout=subprocess.PIPE,
        check=True,
    )
    changed = {name.decode("utf-8") for name in result.stdout.split(b"\0") if name}
    selected = [name for name in ASSIGNMENTS if name in changed]
    SELECTION_PATH.write_text(json.dumps(selected, indent=2), encoding="utf-8")

    if not selected:
        print("No assignment Python files changed in this pull request.")
        print("Submit edits to one or more existing assignment .py files.")
        return 2

    print("Grading only changed assignment files:", flush=True)
    for name in selected:
        print(f"  - {name}", flush=True)

    test_paths = [str(GRADER_DIR / "tests" / ASSIGNMENTS[name]) for name in selected]
    command = [
        sys.executable, "-m", "pytest",
        *test_paths,
        "-v", "--timeout=5", "--timeout-method=signal",
        "--junitxml=results.xml",
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
