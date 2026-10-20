"""Render a score summary based on pytest-generated JUnit XML.

Each challenge is worth 10 points, split evenly across its test cases.
A test that errors or fails earns 0 points.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NAMES = [
    'Adding Numbers', 'List of Multiples', 'FizzBuzz', 'Basic Calculator',
    'Country Area', 'Find the Discount', 'Calculate the Profit',
    'Circle or Square', 'How Many Vowels', 'Calculating Damage',
]


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('results.xml')
    if not path.exists():
        message = '## Python grading results\n\nTests did not produce a results file. Review the job logs.\n'
    else:
        root = ET.parse(path).getroot()
        counts = {i: [0,0] for i in range(1,11)}
        for case in root.iter('testcase'):
            marker = case.attrib.get('classname','')
            match = re.search(r'test_(\d{2})_', marker)
            if not match:
                continue
            number = int(match.group(1))
            if number not in counts:
                continue
            counts[number][1] += 1
            if not any(case.find(tag) is not None for tag in ('failure','error','skipped')):
                counts[number][0] += 1
        lines = ['## Python grading results', '', '| Problem | Passed | Score |', '|---|---:|---:|']
        total = 0.0
        for i,name in enumerate(NAMES,1):
            passed,tests = counts[i]
            score = 10 * passed/tests if tests else 0
            total += score
            lines.append(f'| {i}. {name} | {passed}/{tests} | {score:.1f}/10 |')
        lines += ['', f'**Total: {total:.1f}/100 points**', '', 'Automated score reflects test cases only; instructor review may adjust the grade.']
        message = '\n'.join(lines)+'\n'
    print(message)
    summary = os.getenv('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary,'a',encoding='utf-8') as f:
            f.write(message)

if __name__ == '__main__':
    main()
