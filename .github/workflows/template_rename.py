#!/usr/bin/env python3

import os
import shutil
import sys


def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments!")

    repo_name = sys.argv[1]

    if not repo_name.endswith("-PCB"):
        raise ValueError("Incorrect repo name!")

    original_name = "ozelhd-template"

    try:
        new_name = repo_name.split("/", 1)[1][:-4]
    except IndexError:
        raise ValueError("Incorrect repo name!")

    if "-" not in new_name:
        raise ValueError("Incorrect repo name!")

    placeholder_pretty_name = "template_pretty_name"
    placeholder_repo = "template_repo"

    project_name = new_name.split("-", 1)[0].upper()
    pcb_name = (
        new_name.split("-", 1)[1]
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )

    pretty_name = f"{project_name} {pcb_name} Board"

    repo_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(sys.argv[0])
            )
        )
    )

    # Rename template files
    for root, dirs, files in os.walk(repo_root):
        for filename in files:
            new_filename = filename.replace(original_name, new_name)

            if new_filename != filename:
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)

    # Replace template README
    os.rename(
        os.path.join(repo_root, "README.md"),
        os.path.join(repo_root, "USAGE.md"),
    )

    os.rename(
        os.path.join(repo_root, "README.md.template"),
        os.path.join(repo_root, "README.md"),
    )

    # Replace pretty-name placeholder
    files_to_process = [
        os.path.join(repo_root, "README.md"),
    ]

    pcb_dir = os.path.join(repo_root, "PCB")

    for filename in os.listdir(pcb_dir):
        if filename.startswith("."):
            continue
        if ".kicad_" in filename:
            files_to_process.append(os.path.join(pcb_dir, filename))

    for path in files_to_process:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace(
            placeholder_pretty_name,
            pretty_name,
        )
        content = content.replace(
            placeholder_repo,
            repo_name,
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    # Save original PCB layout
    shutil.copyfile(
        os.path.join(
            pcb_dir,
            f"{new_name}-PCB.kicad_pcb",
        ),
        os.path.join(
            pcb_dir,
            ".original_pcb_layout",
        ),
    )


if __name__ == "__main__":
    main()