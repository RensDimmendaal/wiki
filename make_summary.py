import pathlib
import os  # needed to unlock __file__
import typing

ROOT = pathlib.Path(__file__).parent


class Summary:
    def __init__(self):
        self.text = ["# Table of Contents","\n"]

    def add_title(self, path: pathlib.Path) -> None:
        title = get_markdown_title(path)
        self.text.append(f"* [{title}]({path.relative_to(ROOT)})")

    def add_section(self, title: str) -> None:
        self.text.append("\n")
        self.text.append(f"## {title}")
        self.text.append("\n")

    def save(self, path:pathlib.Path) -> None:
        with open(path,'w') as f:
            for line in self.text:
                f.write(line)
                if line != "\n":
                    f.write("\n")


def find_markdown(path: pathlib.Path) -> typing.List[pathlib.Path]:
    return [child for child in path.iterdir() if child.suffix == ".md"]


def has_markdown_children(path: pathlib.Path) -> bool:
    return len(find_markdown(path)) > 0


def find_markdown_directories(path: pathlib.Path) -> typing.List[pathlib.Path]:
    dirs = (child for child in path.iterdir() if child.is_dir())
    md_dirs = (directory for directory in dirs if has_markdown_children(directory))
    return md_dirs


def get_markdown_title(path: pathlib.Path) -> str:
    txt = path.read_text().splitlines()
    try:
        return next(line.lstrip("# ") for line in txt if line.startswith("# "))
    except IndexError:
        raise RuntimeError(f"No title in: {path}")


def format_link(title: str, path: pathlib.Path) -> str:
    return f"* [{title}]({path.relative_to(root)})"


# find markdown files in root, except SUMMARY.md

if __name__ == "__main__":
    """Overwrite SUMMARY.md with the current structure."""

    summary = Summary()

    # add root level markdown files
    for md_path in sorted(find_markdown(ROOT)):
        # exclude SUMMARY.md because that's the file we're creating
        if not md_path.name.startswith("SUMMARY"):
            summary.add_title(md_path)

    # add directories
    for dir_path in sorted(find_markdown_directories(ROOT)):
        summary.add_section(dir_path.name.capitalize().replace('-',' '))
        for md_path in find_markdown(dir_path):
            summary.add_title(md_path)
        
    summary.save(ROOT / "SUMMARY.md")