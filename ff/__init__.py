import web
from web import tx
from sqlite3 import OperationalError, IntegrityError
from pathlib import Path
import json

# from collections import OrderedDict
from random import randint

# import queries
# from queries import current_scene, get_scenes, scene_depth

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
app = web.application(
    __name__,
    db=True,
    args={"concept": "\w+", "game": "\d+"},
    model={
        "games": {"player": "TEXT NOT NULL", "gm": "TEXT NOT NULL", "status": "JSON"},
        "clues_known": {
            "tag": "TEXT",
            "game_id": "INTEGER",
            # TODO shouldn't be able to have more than one row for a given pair (tag, game_id) ... how to enforce in database? for now, enforce in add_clue
            # FOREIGN KEY(game_id) REFERENCES games(rowid)",
        },
        "scenes_visited": {
            "tag": "TEXT",
            "game_id": "INTEGER",
            # TODO same uniqueness-of-pair issue as clues_known
            # FOREIGN KEY(game_id) REFERENCES games(rowid)",
        },
        **{k: {"details": "JSON"} for k in concepts},
    },
)


def current_scene():
    # todo calculate this from event log, as that materalizes
    # if no 'transition to scene' events in db for tis playthrough, current_scene is sadies story
    # else its the 'transition to scene' event with the biggest ID
    return "sadies_sob_story"


def get_scene(tag):
    return tx.db.select(
        "scenes",
        what="*",
        where="json_extract(details, '$.tag') = ?",
        vals=[tag],
    )[0][0]


def get_scenes(aslist=False):
    query = tx.db.select("scenes")
    innermost = [row[0] for row in query]
    if aslist:
        return innermost
    else:
        result = {}
        for d in innermost:
            tag = d["tag"]
            d.pop("tag")
            result[tag] = d
    return result


def get_visited_scenes(game):
    query = tx.db.select("scenes_visited", where="game_id = ?", vals=[game])
    return [row[0] for row in query]


def scene_depth(tag, scenes):
    if tag == "sadies_sob_story":
        return 1
    else:
        leadins = scenes[tag].get("lead_ins", [])
        if "sadies_sob_story" in leadins:
            return 2
        else:
            pred = leadins[0]
            return 1 + scene_depth(pred, scenes)


@app.control("")
class Home:
    def get(self):
        role = tx.user.session.get("role")
        game = tx.user.session.get("game")
        if game:
            games = []
        else:
            games = tx.db.select("games", what="rowid")
        if role:
            return app.view.join(games)
        else:
            return app.view.home()


@app.control("signin")
class SignIn:
    def post(self):
        role = web.form("role").role
        # todo fix hardcoded name by adding text field (or pick from existing players/gms) to home.html
        tx.user.session.update(role=role, name="test")
        raise web.SeeOther("/")


@app.control("signout")
class SignOut:
    def post(self):
        tx.user.session = {}
        raise web.SeeOther("/")


@app.control("join")
class Join:
    """Pick a game to play in."""

    def post(self):
        game = web.form("game").game
        tx.user.session["game"] = game
        raise web.SeeOther(f"games/{game}")


@app.control("leave")
class Leave:
    def post(self):
        tx.user.session.pop("game")
        raise web.SeeOther("/")


@app.control("games")
class Games:
    def get(self):
        return list(tx.db.select("games"))

    def post(self):
        with open(json_dir / "player_character.json", "r", encoding="utf-8") as f:
            starting_status = json.loads(f.read())
        game = tx.db.insert("games", player="test", gm="test", status=starting_status)
        tx.user.session["game"] = game
        raise web.SeeOther(f"games/{game}")


@app.control("games/{game}")
class Game:
    def get(self, game):
        status = tx.db.select("games", what="status", where="rowid = ?", vals=[game])[
            0
        ]["status"]
        role = tx.user.session.get("role")
        if role == "player":
            return app.view.player(status)
        else:
            scene = current_scene()
            return app.view.gm(scene, status)


@app.control("games/{game}/unvisited")
class UnvisitedScenes:
    def get(self, game):
        scenes = get_scenes()
        visited = get_visited_scenes(game)
        return {scene: info for scene, info in scenes.items() if scene not in visited}


@app.control("games/{game}/visited")
class VisitedScenes:
    def get(self, game):
        scenes = get_scenes()
        visited = get_visited_scenes(game)
        return {scene: info for scene, info in scenes.items() if scene in visited}


@app.control("concepts/{concept}")
class Concept:
    def get(self, concept):
        table_name = concept
        singular = concepts[concept]["singular"]
        if concept == "scenes":
            return get_scenes()
        else:
            return app.view.collection(singular, table_name, tx.db.select(table_name))


# @app.control("gm/current")
# class Current:
#    """Shows player status, current scene, play trace and other true-right-now info"""
#
#    def get(self):
#        s = tx.db.select(
#            "scenes",
#            what="*",
#            where="json_extract(details, '$.tag') = ?",
#            vals=[current_scene()],
#        )[0][0]
#        # replace leadout tags with whole scenes
#        for idx, each in enumerate(s["lead_outs"]):
#            lo = tx.db.select(
#                "scenes",
#                what="*",
#                where="json_extract(details, '$.tag') = ?",
#                vals=[each],
#            )[0][0]
#            s["lead_outs"][idx] = lo
#        # replace chunk clue tags with whole clues
#        for idx, chunk in enumerate(s["chunks"]):
#            for k, v in chunk.items():
#                if k == "clues":
#                    for which, unit in enumerate(v):
#                        clue = tx.db.select(
#                            "clues",
#                            what="*",
#                            where="json_extract(details, '$.tag') = ?",
#                            vals=[unit],
#                        )[0][0]
#                        s["chunks"][idx]["clues"][which] = clue
#        return app.view.current(s)


def add_clue(tag, game):
    query = tx.db.select(
        "clues_known", where="game_id = ? and  tag = ?", vals=[game, tag]
    )
    if len(query) == 0:
        tx.db.insert("clues_known", game_id=game, tag=tag)


def remove_clue(tag, game):
    tx.db.delete("clues_known", where="game_id = ? and  tag = ?", vals=[game, tag])


@app.control("games/{game}/upload-clue")
class UploadClue:
    def post(self, game):
        tag, state = tx.request.body.get("tag"), tx.request.body.get("state")
        if state is True:
            add_clue(tag, game)
        elif state is False:
            remove_clue(tag, game)
        else:
            raise web.BadRequest()
        return json.dumps({tag: "known" if state else "unknown"})


@app.control("filldatabase")
class FillDatabase:
    def get(self):
        for c in concepts:
            p = json_dir / f"{c}.json"
            with open(p, "r", encoding="utf-8") as f:
                extracts = json.loads(f.read())
                for j in extracts:
                    if not j.get("tag"):
                        print(f"WARNING no tag on {j}")
                    if c == "clues" and "known" in j:
                        j.pop("known")
                    if c == "scenes":
                        if "visited" in j:
                            j.pop("visited")
                        for conn in ("lead_ins", "lead_outs"):
                            if conn not in j:
                                j[conn] = []
                    with tx.db.transaction as cur:
                        already_entered = cur.select(
                            c,
                            where="json_extract(details, '$.tag') = ?",
                            vals=(j["tag"],),
                        )
                        try:
                            # select() returns Results object; if any rows match query, there will be a list of Row objects inside its 0th index
                            already_entered[0]
                        except IndexError:
                            cur.insert(c, details=j)
        return "Database filled"
