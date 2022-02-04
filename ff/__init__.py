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
    with open(Path(f"ff/json/{c}.json"), "r") as f:
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
