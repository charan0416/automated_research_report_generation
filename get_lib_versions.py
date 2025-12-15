import importlib.metadata
import re

REQUIREMENTS_PATH = "requirements.txt"

def get_installed_version(pkg_name):
    try:
        return importlib.metadata.version(pkg_name)
    except importlib.metadata.PackageNotFoundError:
        return None

def normalize_package_name(pkg_line):
    """Handles editable installs, extras, and version stripping."""
    pkg_line = pkg_line.strip()
    if pkg_line.startswith("-e") or pkg_line.startswith("--"):
        return None  # Ignore editable installs or options
    pkg_name = re.split(r"[=<>!]", pkg_line)[0].strip()
    return pkg_name

def update_requirements_file():
    with open(REQUIREMENTS_PATH, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        original_line = line.strip()

        if original_line.startswith("-e") or original_line.startswith("--") or original_line == "":
            new_lines.append(original_line)
            continue

        pkg_name = normalize_package_name(original_line)
        version = get_installed_version(pkg_name)

        if version:
            new_lines.append(f"{pkg_name}=={version}")
        else:
            print(f"{pkg_name} not installed, skipping.")
            new_lines.append(original_line)

    with open(REQUIREMENTS_PATH, "w") as f:
        f.write("\n".join(new_lines) + "\n")

    print("requirements.txt updated successfully with installed versions.")

if __name__ == "__main__":
    update_requirements_file()
