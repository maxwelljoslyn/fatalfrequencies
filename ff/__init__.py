from understory import web, sql
from understory.web import tx
from sqlite3 import OperationalError
from pathlib import Path
import json, textwrap

app = web.application(__name__, args={"concept": "\w+"})


concepts = {
    "antagonist_reactions": {"singular": "antagonist_reaction", "example": None},
    "challenges": {"singular": "challenge", "example": None},
    "characters": {"singular": "character", "example": None},
    "clues": {"singular": "clue", "example": None},
    "edges": {"singular": "edge", "example": None},
    "general_abilities": {"singular": "general_ability", "example": None},
    "investigative_abilities": {"singular": "investigative_ability", "example": None},
    "items": {"singular": "item", "example": None},
    "problems": {"singular": "problem", "example": None},
    "scenes": {"singular": "scene", "example": None},
    "sources": {"singular": "source", "example": None},
}

# todo create playthrough db with player_character table, pushes table (count INT), clues table (if a "tag" is in here, that clue's known), scenes (if "tag" in here, that scene's visited), edges/problems (if its in here it's possessed) etc.
# todo intitalize playthrough db with ice_queen, 4 pushes, etc.
# todo integrate with devi's ffjson repo

for c, data in concepts.items():
    with open(Path(f"ff/json/{c}.json"), "r", encoding='utf-8') as f:
        data["example"] = json.loads(f.read())

try:
    # create database
    db = sql.db("ff.db")
except OperationalError:
    pass

for table in concepts:
    try:
        # create database tables
        db.create(table, "details JSON")
    except OperationalError:
        pass


def preprocess_json(d):
    result = {}

    def primitive(x):
        return not isinstance(x, list) and not isinstance(x, dict)

    for key, val in d.items():
        if primitive(val):
            result[key] = "primitive"
        elif isinstance(val, list):
            if not val:
                # empty and will eventually hold tags, ie strings, ie primitives
                result[key] = "primitive list"
            elif primitive(val[0]):
                result[key] = "primitive list"
            else:
                result[key] = [preprocess_json(x) for x in val]
        else:
            result[key] = preprocess_json(val)
    return result


def primitive_field_to_form(field):
    if field in ("trigger", "reaction", "description"):
        return f"<label for={field}>{field.title()}</label><textarea id={field} name={field} rows=5 cols=33></textarea>"
    else:
        # todo add is_number clause to preprocess_json, form_fields, and this function... so I can add type=number HTML fields for challenge thresholds (the only place that need it)
        return f"<label>{field.title()}<input type=text name={field}></input></label>"


def form_fields(d):
    d = preprocess_json(d)
    result = []
    for key, val in d.items():
        if val == "primitive":
            result.append(primitive_field_to_form(key))
        elif val == "primitive list":
            result.append(
                f"<fieldset><legend>{key.title()}</legend>"
                + primitive_field_to_form(key)
                + "</fieldset>"
            )
        elif isinstance(val, list):
            result.append(
                f"<fieldset> <legend> {key.title()} </legend>"
                + "\n".join([form_fields(x) for x in val])
                + "</fieldset>"
            )
        else:
            result.append(
                f"<fieldset><legend>{key.title()}</legend>"
                + form_fields(val)
                + "</fieldset>"
            )
    return "\n".join(result)


@app.wrap
def template(handler, app):
    """Wrap response with site-wide template."""
    yield
    if tx.response.headers.content_type == "text/html":
        tx.response.body = app.view.template(tx.response.body)


@app.control("upload")
class Upload:
    def post(self):
        form = web.form()
        table = form.pop("table_name")
        db.insert(table, {"details": form})


@app.control("")
class Home:
    def get(self):
        return app.view.home(concepts)


@app.control("{concept}")
class Concept:
    def get(self):
        # self.concept == "sources"
        table_name = self.concept
        singular = concepts[self.concept]["singular"]
        ex = concepts[self.concept]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))
