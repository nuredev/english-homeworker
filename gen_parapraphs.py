import json
from typing import List, Dict, Union

import xerox

from compile import export

if __name__ == "__main__":
    paragraphs: List[str] = [""]

    with open("paragraphs.txt", "r") as fb:
        file_lines: List[str] = fb.readlines()

    for line in file_lines:
        line = line.replace("\n", "")
        if not line: paragraphs.append("")
        elif paragraphs[-1]: paragraphs[-1] += " " + line
        else: paragraphs[-1] += line

    with open("homework.json", "r") as fb:
        file_json: Dict[str, Union[str, Dict[str, Union[str, list, dict]]]] = json.load(fb)

    file_json["text"]["paragraphs"] = []

    for paragraph in paragraphs:
        sentences: dict = {}
        for sentence in paragraph.split(". "):
            xerox.copy(sentence)
            input(sentence)
            sentences = {
                **sentences,
                sentence: xerox.paste(),
            }
        file_json["text"]["paragraphs"].append(sentences)

    with open('homework.json', 'w') as fb:
        json.dump(file_json, fb, separators=(",", ": "), indent=4)

    export()
