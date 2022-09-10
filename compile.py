import json
import os
import pathlib
from typing import Union, List, Dict


def read(*file_path: str, parse_json: bool = False) -> Union[List[str], Dict[str, Union[str, list, dict]]]:
    with open(os.path.join(pathlib.Path(__file__).parent.resolve(), *file_path), "r") as fb:
        if parse_json: return json.load(fb)
        return fb.readlines()


def write(*file_path: str, content: List[str], parse_json: bool = False):
    with open(os.path.join(pathlib.Path(__file__).parent.resolve(), *file_path), "w") as fb:
        if parse_json: json.dump(content, fb)
        else: fb.writelines(content)


def opening(tag_name: str, **kwargs) -> str:
    return f"<{tag_name} " + " ".join([f'{kwarg.replace("__", "").replace("_", "-")}="{kwargs.get(kwarg)}"' for kwarg in kwargs]) + ">\n"


def insert(content: str) -> str:
    return content + "\n"


def closing(tag_name: str) -> str:
    return f"</{tag_name}>\n"


def generate_body(document: dict) -> str:
    output: str = "<article>- Зажми Ctrl и нажми/выдели текст (выделяй сверху вниз!)<br/>- Проскроль или нажми на " \
                  "перевод чтобы закрыть его.</article>"
    if document.get("text"):
        output += opening("article", __class="text")
        output += opening("header", __data_translation=document.get("text").get("title_translated"))
        output += insert(document.get("text").get("title"))
        output += closing("header")
        for paragraph in document.get("text").get("paragraphs"):
            output += opening("p")
            for sentence in paragraph:
                output += opening("span", __data_translation=paragraph.get(sentence))
                output += insert(sentence + ".")
                output += closing("span")
            output += closing("p")
        output += closing("article")
    if document.get("tasks"):
        for task in document.get("tasks"):
            output += opening("article", __class=task.get("type"))
            match task.get("type"):
                case "word_list":
                    output += opening("header")
                    output += opening("b")
                    output += insert(task.get("category"))
                    output += closing("b")
                    output += insert(task.get("title"))
                    output += closing("header")
                    output += opening("table")

                    output += opening("tr")
                    output += opening("th")
                    output += insert("<b>#</b>")
                    output += closing("th")
                    output += opening("th")
                    output += insert("<b>Original</b>")
                    output += closing("th")
                    output += opening("th")
                    output += insert("<b>Translated</b>")
                    output += closing("th")
                    output += closing("tr")

                    for index, word in enumerate(task.get("words"), start=1):
                        output += opening("tr")
                        output += opening("th")
                        output += insert(str(index))
                        output += closing("th")
                        output += opening("th")
                        output += insert(word)
                        output += closing("th")
                        output += opening("th")
                        output += insert(task.get("words").get(word))
                        output += closing("th")
                        output += closing("tr")

                    output += closing("table")

                case "answer_questions":
                    output += opening("header")
                    output += insert(task.get("title"))
                    output += closing("header")

                    output += opening("div")
                    index = 0
                    for question in task.get("questions"):
                        output += opening("div")
                        output += opening("span", __data_translation=list(task.get("translations"))[index])
                        output += insert(question)
                        output += closing("span")
                        output += opening("span", __data_translation=task.get("translations").get(list(task.get("translations"))[index]))
                        output += insert(task.get("questions").get(question))
                        output += closing("span")
                        output += closing("div")
                        index += 1
                    output += closing("div")

                case "true_or_false":
                    output += opening("header")
                    output += insert(task.get("title"))
                    output += closing("header")

                    output += opening("div")
                    index: int = 0
                    for statement in task.get("statements"):
                        output += opening("span", __data_translation=task.get("translations")[index], __value=str(task.get("statements").get(statement)))
                        output += insert(statement)
                        output += closing("span")
                        index += 1
                    output += closing("div")

                case "complete_sentences":
                    output += opening("header")
                    output += insert(task.get("title"))
                    output += closing("header")

                    output += opening("div", __class="cs_words")
                    for word in task.get("words").split(", "):
                        output += opening("span")
                        output += insert(word)
                        output += closing("span")
                    output += closing("div")

                    output += opening("div", __class="cs_sentences")
                    for sentence in task.get("sentences"):
                        output += opening("span", __data_translation=task.get("sentences").get(sentence))
                        output += insert(sentence)
                        output += closing("span")
                    output += closing("div")

            output += closing("article")
    return output


def export():
    print("[Process] Collecting necessary files...")
    json_document = read("homework.json", parse_json=True)
    html_document = read("source", "index.html")
    css_document = read("source", "styles.css")
    js_document = read("source", "script.js")
    file_name = f"English_{json_document.get('date').replace(' ', '-').replace(',', '')}.html"

    write("export", file_name, content=[
        line.replace(
            "@Date", json_document.get("date")
        ).replace(
            "@Styles", "<style>\n" + "".join([f"        {i}" for i in css_document]) + "\n    </style>"
        ).replace(
            "@Script", "<script>\n" + "".join([f"        {i}" for i in js_document]) + "\n    </script>"
        ).replace(
            "@Body", generate_body(json_document)
        )
        for line in html_document
    ])

    print(f"[Done] Exported as \"{file_name}\"")


if __name__ == "__main__":
    export()
