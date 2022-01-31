from understory import web, sql
from understory.web import tx
from sqlite3 import OperationalError
from pathlib import Path
import json, textwrap

app = web.application(__name__)


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

for c, data in concepts.items():
    with open(Path(f"ff/json/{c}.json"), "r") as f:
        data["example"] = json.loads(f.read())

# create database

try:
    db = sql.db("ff.db")
except OperationalError:
    pass

# create database tables

for table in concepts:
    try:
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
            result.append("<fieldset>" + primitive_field_to_form(key) + "</fieldset>")
            # todo make this dang button work with some js
            result.append("<button type=button>Add Another</button>")
        elif isinstance(val, list):
            result.append(
                "<fieldset>" + "\n".join([form_fields(x) for x in val]) + "</fieldset>"
            )
            result.append("<button type=button>Add Another</button>")
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


@app.control("antagonist_reactions")
class AntagonistReactions:
    def get(self):
        table_name = "antagonist_reactions"
        singular = concepts["antagonist_reactions"]["singular"]
        ex = concepts["antagonist_reactions"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("challenges")
class Challenges:
    def get(self):
        table_name = "challenges"
        singular = concepts["challenges"]["singular"]
        ex = concepts["challenges"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("characters")
class Characters:
    def get(self):
        table_name = "characters"
        singular = concepts["characters"]["singular"]
        ex = concepts["characters"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("clues")
class Clues:
    def get(self):
        table_name = "clues"
        singular = concepts["clues"]["singular"]
        ex = concepts["clues"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("edges")
class Edges:
    def get(self):
        table_name = "edges"
        singular = concepts["edges"]["singular"]
        ex = concepts["edges"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("general_abilities")
class GeneralAbilities:
    def get(self):
        table_name = "general_abilities"
        singular = concepts["general_abilities"]["singular"]
        ex = concepts["general_abilities"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("investigative_abilities")
class InvestigativeAbilities:
    def get(self):
        table_name = "investigative_abilities"
        singular = concepts["investigative_abilities"]["singular"]
        ex = concepts["investigative_abilities"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("items")
class Items:
    def get(self):
        table_name = "items"
        singular = concepts["items"]["singular"]
        ex = concepts["items"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("problems")
class Problems:
    def get(self):
        table_name = "problems"
        singular = concepts["problems"]["singular"]
        ex = concepts["problems"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("scenes")
class Scenes:
    def get(self):
        table_name = "scenes"
        singular = concepts["scenes"]["singular"]
        ex = concepts["scenes"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


@app.control("sources")
class Sources:
    def get(self):
        table_name = "sources"
        singular = concepts["sources"]["singular"]
        ex = concepts["sources"]["example"]
        ex = form_fields(ex)
        return app.view.collection(singular, table_name, ex, db.select(table_name))


# ... but why write all that repetitive code? let's do some light metaprogramming and generate those classes
## for c in concepts:
# for c, data in concepts.items():
#
#    def get(self):
#        print(c)
#        table_name = c
#        # I could have used "for c, data in concepts.items()" but I want to ensure these always refer to the global concepts dict and I wasn't sure if would be the case that way
#        # global concepts
#        # singular = concepts[c]["singular"]
#        # schema = concepts[c]["example"].keys()
#        singular = data["singular"]
#        schema = data["example"].keys()
#        return app.view.collection(singular, table_name, schema, db.select(table_name))
#
#    # dynamically creating a class for each game concept
#    classname = c.title()
#    globals()[classname] = type(
#        classname,
#        (object,),
#        {
#            "get": get,
#        },
#    )
#    # decorate the class with web app route pattern
#    # can't use class decorator syntactic sugar b/c we aren't using a normal "def class"; instead, update the definition of the class in place
#    print(globals()[classname])
#    globals()[classname] = app.control(c)(globals()[classname])
#    # todo WTFFFF WHY ARE ALL THE ROUTES GOING TO SOURCES
#    print(c, classname, globals()[classname])
