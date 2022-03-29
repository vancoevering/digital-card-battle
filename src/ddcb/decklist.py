import json
from pathlib import Path

from . import PKG_ROOT


def main():
    text_decklist_to_json(PKG_ROOT / "go-go-dinosaur-deck.txt")


def text_decklist_to_json(path):
    path = Path(path)
    decklist = load_text_decklist(path)
    write_decklist(decklist, path.with_suffix(".json"))


def load_text_decklist(path):
    decklist = []
    with open(path, "r") as fp:
        for line in fp.readlines():
            line = clean_str(line)
            count, name = parse_decklist_line(line)
            decklist.extend([name]*count)
    return decklist


def write_decklist(decklist: list, path):
    with open(path, "w") as fp:
        json.dump(decklist, fp, indent=4)


def parse_decklist_line(line: str):
    count, name = line.split(maxsplit=1)
    count = int(count)
    name = str_to_card_name(name)
    return count, name


def str_to_card_name(s: str):
    s = clean_str(s)
    s = replace_icons(s)
    return s


def clean_str(s: str):
    return " ".join(s.split())


def replace_icons(s: str):
    new_str = s.lower()
    for icon in ("o", "triangle", "x"):
        if new_str.endswith(icon):
            new_str = new_str[:-len(icon)] + f"[{icon}]"
    return new_str


if __name__ == '__main__':
    main()
