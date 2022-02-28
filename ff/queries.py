from understory import web, sql
from understory.web import tx
from sqlite3 import OperationalError, IntegrityError

app = web.application(__name__, args={"concept": "\w+"})


def get_challenges(ctype):
    # "find_physical_injury(Challenge) :-
    #    challenge_type(Challenge, Type).
    #    general_ability_name(Type).
    #    general_ability_type(physical).
    #    challenge_extra_problem(Challenge, ExtraProblem).
    #    "
    pass


# https://linuxhint.com/subqueries-sqlite/
def get_clues(aslist=False, which="all", scene=None):
    if which == "all":
        query = tx.db.select("clues")
    elif which == "known":
        #        query = tx.db.execute(
        #            "SELECT * FROM clues "
        #            + "WHERE json_extract(details, '$.tag') IN (SELECT tag FROM clues_known), "
        #            # and session.playthrough_id == select playthrough_id from clues_known
        #        )
        #    # "json_extract(details, '$.tag') = ?"
        pass
    elif which == "unknown":
        pass
    else:
        raise ValueError(f"Invalid argument to `get_clues()`: `which`={which}")
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


# def leading_clues(current_scene, which='unknown'):
#    """Return clues that unlock leadouts from `current_scene`."""
#    if known:
#        return get_clues(which=which, current_scene=current_scene)
#    pass
