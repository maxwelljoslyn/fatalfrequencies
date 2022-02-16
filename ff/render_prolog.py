import json
import re
from pathlib import Path
from __init__ import json_dir, concepts

predicate_declarations = {
    "scene": [
        ":- dynamic(scene/1).",
        ":- dynamic(scene_name/2).",
        ":- dynamic(scene_type/2).",
        ":- dynamic(scene_visited/2).",
        ":- dynamic(scene_lead_outs/2).",
        ":- dynamic(scene_description/2).",
        ":- dynamic(scene_clues/2).",
        ":- dynamic(scene_characters/2).",
        ":- dynamic(scene_challenges/2).",
    ],
    "clue": [
        ":- dynamic(clue/1).",
        ":- dynamic(clue_desc/2).",
        ":- dynamic(clue_known/2).",
        ":- dynamic(clue_leads_to/2).",
    ],
    "source": [
        ":- dynamic(source/1).",
        ":- dynamic(source_name/2).",
        ":- dynamic(source_profession/2).",
        ":- dynamic(source_description/2).",
        ":- dynamic(source_investigative_abilities/2).",
    ],
    "problem": [
        ":- dynamic(problem/1).",
        ":- dynamic(problem_number/2).",
        ":- dynamic(problem_name/2).",
        ":- dynamic(problem_type/2).",
        ":- dynamic(problem_description/2).",
        ":- dynamic(problem_effect/2).",
    ],
    "item": [
        ":- dynamic(item/1).",
        ":- dynamic(item_name/2).",
        ":- dynamic(item_description/2).",
        ":- dynamic(item_type/2).",
    ],
    "edge": [
        ":- dynamic(edge/1).",
        ":- dynamic(edge_number/2).",
        ":- dynamic(edge_name/2).",
        ":- dynamic(edge_description/2).",
        ":- dynamic(edge_effect/2).",
    ],
    "challenge": [
        ":- dynamic(challenge/1).",
        ":- dynamic(challenge_name/2).",
        ":- dynamic(challenge_type/2).",
        ":- dynamic(challenge_advance/3).",
        ":- dynamic(challenge_hold/4).",
        ":- dynamic(challenge_setback/2).",
        ":- dynamic(challenge_extra_problem/2).",
    ],
    "character": [
        ":- dynamic(character/1).",
        ":- dynamic(character_name/2).",
        ":- dynamic(character_goal/2).",
        ":- dynamic(character_knows/2).",
        ":- dynamic(character_relationship_with/4).",
    ],
    "antagonist_reaction": [
        ":- dynamic(antagonist_reaction/1).",
    ],
    "investigative_ability": [
        ":- dynamic(investigative_ability/4).",
    ],
    "general_ability": [
        ":- dynamic(general_ability/4).",
    ],
    "player_status": [
        ":- dynamic(player_edge/1).",
        ":- dynamic(player_problem/1).",
        ":- dynamic(player_investigative_ability/1).",
        ":- dynamic(player_general_ability/2).",
        ":- dynamic(player_pushes/1).",
        ":- dynamic(player_item/1).",
    ],
}


def render_frontmatter():
    return "\n".join(
        [
            ":- set_prolog_flag(double_quotes, atom).",
            "current_prolog_flag(character_escapes, true).",
        ]
    )


def prologify(key, value):
    if isinstance(value, bool):
        value = str(value).lower()
    elif isinstance(value, str):
        if key == "description" or "'" in value or " " in value:
            value = f'"{value}"'
    elif isinstance(value, dict):
        # sort so that e.g. for character JSONs, all keys under "relationship_with" are inserted into Prolog relationship_with statement in same order each time
        elements = list(value.keys())
        elements.sort()
        value = ", ".join([prologify(e, value[e]) for e in elements])
    # todo move this into initial JSON load, which Prolog render is downstream of
    # special cases which I will inevitably catch one at a time
    if key == "profession":
        value = value.lower()
    return str(value)


# def render_dynamic(concept, key=None, num_args=1):
#    if key:
#        return f":- dynamic({concept}_{key}/{num_args})."
#    else:
#        return f":- dynamic({concept}/{num_args})."


def render_tag(concept, tag):
    return f"{concept}({tag}).\n"


def render_other(concept, tag, key, value):
    return f"{concept}_{key}({tag}, {prologify(key, value)}).\n"


def render_declarations():
    result = []
    for k, alist in predicate_declarations.items():
        result.append("\n".join(alist))
    return "\n".join(result)


def render_concept(location, concept, singular):
    with open(location, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        for d in data:
            tag = d.pop("tag")
            print(render_tag(singular, tag))
            for k, v in d.items():
                if isinstance(v, list):
                    for sub in v:
                        print(render_other(singular, tag, k, sub))
                else:
                    print(render_other(singular, tag, k, v))
            print(f"just rendered {k}")


def main():
    print(render_frontmatter())
    print(render_declarations())
    for concept, val in concepts.items():
        print(
            render_concept(
                json_dir / f"{concept}.json",
                concept,
                concepts[concept]["singular"],
            )
        )


if __name__ == "__main__":
    main()
