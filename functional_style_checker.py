import os
import re
from typing import List, Tuple

def read_file(file_path: str) -> List[str]:
    """Reads the content of the file and returns lines as a list."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return file.readlines()

def analyze_file_structure(lines: List[str]) -> Tuple[int, List[str], List[str], List[str]]:
    """Analyzes the file structure and extracts information."""
    imports = []
    classes = []
    functions = []

    for line in lines:
        if line.strip().startswith('import') or line.strip().startswith('from'):
            imports.append(line.strip())
        elif line.strip().startswith('class '):
            match = re.match(r'class (\w+)', line.strip())
            if match:
                classes.append(match.group(1))
        elif line.strip().startswith('def '):
            match = re.match(r'def (\w+)', line.strip())
            if match:
                functions.append(match.group(1))

    return len(lines), imports, classes, functions

def extract_docstrings(lines: List[str]) -> dict:
    """Extracts DocStrings for classes and functions."""
    docstrings = {}
    current_element = None

    for i, line in enumerate(lines):
        if line.strip().startswith('class ') or line.strip().startswith('def '):
            match = re.match(r'(class|def) (\w+)', line.strip())
            if match:
                current_element = match.group(2)
                docstrings[current_element] = "DocString not found"
        elif '"""' in line and current_element:
            doc_line = line.strip().split('"""')[1] if '"""' in line else ""
            docstrings[current_element] = doc_line or """\n""".join(lines[i + 1:i + 3])
            current_element = None

    return docstrings

def check_type_annotations(lines: List[str]) -> List[str]:
    """Checks for functions without type annotations."""
    non_compliant = []
    for line in lines:
        if line.strip().startswith('def '):
            if '->' not in line and ':' not in line:
                match = re.match(r'def (\w+)', line.strip())
                if match:
                    non_compliant.append(match.group(1))
    return non_compliant

def check_naming_conventions(classes: List[str], functions: List[str]) -> Tuple[List[str], List[str]]:
    """Checks naming conventions for classes and functions."""
    non_compliant_classes = [cls for cls in classes if not cls[0].isupper()]
    non_compliant_functions = [fn for fn in functions if '_' not in fn and fn.islower() is False]
    return non_compliant_classes, non_compliant_functions

def generate_report(file_path: str, analysis: dict) -> None:
    """Generates a report and saves it to a file."""
    report_path = os.path.join(os.path.dirname(file_path), f"style_report_{os.path.basename(file_path)}.txt")
    with open(report_path, 'w') as report:
        report.write("File Structure\n")
        report.write(f"Total lines: {analysis['total_lines']}\n\n")
        
        report.write("Imports\n")
        report.write("\n".join(analysis['imports']) + "\n\n")

        report.write("Classes\n")
        report.write("\n".join(analysis['classes']) + "\n\n")

        report.write("Functions\n")
        report.write("\n".join(analysis['functions']) + "\n\n")

        report.write("DocStrings\n")
        for key, doc in analysis['docstrings'].items():
            report.write(f"{key}: {doc}\n")
        report.write("\n")

        report.write("Type Annotation Check\n")
        if analysis['type_annotations']:
            report.write("\n".join(analysis['type_annotations']) + "\n\n")
        else:
            report.write("All functions and methods use type annotations.\n\n")

        report.write("Naming Convention Check\n")
        if analysis['non_compliant_classes']:
            report.write("Non-Compliant Classes\n")
            report.write("\n".join(analysis['non_compliant_classes']) + "\n\n")
        if analysis['non_compliant_functions']:
            report.write("Non-Compliant Functions\n")
            report.write("\n".join(analysis['non_compliant_functions']) + "\n\n")
        if not analysis['non_compliant_classes'] and not analysis['non_compliant_functions']:
            report.write("All classes and functions adhere to naming conventions.\n\n")

def main():
    file_path = input("Enter the Python file path: ").strip()
    try:
        lines = read_file(file_path)
        total_lines, imports, classes, functions = analyze_file_structure(lines)
        docstrings = extract_docstrings(lines)
        type_annotations = check_type_annotations(lines)
        non_compliant_classes, non_compliant_functions = check_naming_conventions(classes, functions)

        analysis = {
            'total_lines': total_lines,
            'imports': imports,
            'classes': classes,
            'functions': functions,
            'docstrings': docstrings,
            'type_annotations': type_annotations,
            'non_compliant_classes': non_compliant_classes,
            'non_compliant_functions': non_compliant_functions
        }

        generate_report(file_path, analysis)
        print(f"Report generated: style_report_{os.path.basename(file_path)}.txt")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
