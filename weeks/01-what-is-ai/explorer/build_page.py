"""python3 build_page.py - embed data.json into index.template.html and write index.html."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
PLACEHOLDER = "__DATA__"


def build():
    data = json.loads((HERE / "data.json").read_text(encoding="utf-8"))
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=True).replace("</", "<\\/")
    template = (HERE / "index.template.html").read_text(encoding="utf-8")
    assert template.count(PLACEHOLDER) == 1, "template must contain the __DATA__ placeholder exactly once"
    (HERE / "index.html").write_text(template.replace(PLACEHOLDER, blob), encoding="utf-8")


if __name__ == "__main__":
    build()
    print("wrote index.html")
