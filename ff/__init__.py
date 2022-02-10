from understory import web, sql
from understory.web import tx
from sqlite3 import OperationalError
from pathlib import Path
import json

app = web.application(__name__, args={"concept": "\w+"})

json_dir = Path("FatalFrequenciesJSON")

concepts = {
    "antagonist_reactions": {"singular": "antagonist_reaction"},
    "challenges": {"singular": "challenge"},
    "characters": {"singular": "character"},
    "clues": {"singular": "clue"},
    "edges": {"singular": "edge"},
    "general_abilities": {"singular": "general_ability"},
    "investigative_abilities": {"singular": "investigative_ability"},
    "items": {"singular": "item"},
    "problems": {"singular": "problem"},
    "scenes": {"singular": "scene"},
    "sources": {"singular": "source"},
}

per_playthrough_state = {
    "playthroughs": "id INTEGER PRIMARY KEY, player TEXT NOT NULL, gm TEXT NOT NULL, status JSON",
    "clues_known": "tag TEXT, playthrough_id INTEGER, FOREIGN KEY(playthrough_id) REFERENCES playthroughs(id))",
    "scenes_visited": "tag TEXT, playthrough_id INTEGER, FOREIGN KEY(playthrough_id) REFERENCES playthroughs(id))",
}


def set_up_database():
    # get reference to database, creating it if necessary
    try:
        db = sql.db("ff.db")
    except OperationalError:
        pass

    # create varying tables
    for k, v in per_playthrough_state.items():
        try:
            db.create(k, v)
        except OperationalError:
            pass

    # create non-varying tables
    for c in concepts:
        try:
            db.create(c, "details JSON")
        except OperationalError:
            pass

    # fill database tables
    for c in concepts:
        p = json_dir / f"{c}.json"
        with open(p, "r", encoding="utf-8") as f:
            extracts = json.loads(f.read())
            for j in extracts:
                if not j.get("tag"):
                    print(f"WARNING no tag on {j}")
                if c == "clues":
                    j.pop("known")
                if c == "scenes":
                    j.pop("visited")
                with db.transaction as cur:
                    already_entered = cur.select(
                        c, where="json_extract(details, '$.tag') = ?", vals=(j["tag"],)
                    )
                    try:
                        # select() returns Results object; if any rows match query, there will be a list of Row objects inside its 0th index
                        already_entered[0]
                    except IndexError:
                        cur.insert(c, details=j)
    return db


db = set_up_database()


@app.wrap
def template(handler, app):
    """Wrap response with site-wide template."""
    yield
    if tx.response.headers.content_type == "text/html":
        tx.response.body = app.view.template(tx.response.body)


@app.control("")
class Home:
    def get(self):
        return app.view.home(concepts)


@app.control("gm/{concept}")
class Concept:
    def get(self):
        table_name = self.concept
        singular = concepts[self.concept]["singular"]
        return app.view.collection(singular, table_name, db.select(table_name))


@app.control("upload-clue")
class UploadClue:
    def post(self):
        tag, state = tx.request.body["tag"], tx.request.body["state"]
        # todo actually save the clue to the db with the current playthrough id
        return json.dumps({tag: "known" if state else "unknown"})


@app.control("gm")
class GM:
    def get(self):
        return app.view.gm(concepts)


@app.control("player")
class Player:
    def get(self):
        r = db.select(
            # todo adapt this to selected playthrough
            "playthroughs",
            what="id, status",
            where="player = 'test' AND gm = 'test'",
        )
        r = list(r)
        # todo if you have multiple playthroughs with the same gm AND player, return view.select_playthrough
        if len(r) == 1:
            info = r[0]
            pid = info["id"]
            status = info["status"]
            clues = db.select(
                "clues_known", what="tag", where="playthrough_id = ?", vals=(pid,)
            )
        else:
            status = "todo"
            clues = [
                "See #todo in Player() view implementation",
            ]

        return app.view.player(status, clues)
        # status  # Results object
        # status[0]  #  Row object
        # status[0][0]  #  thing actually contained in first Row

