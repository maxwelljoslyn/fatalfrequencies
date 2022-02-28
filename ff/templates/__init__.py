import re
import web
from web import tx

__all__ = ["tx", "render_scene"]


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)


def render_scene(tag, info):
    # "&#10144;"
    scenetype = info["type"]
    title = titlecase(info["name"])
    depth = info["depth"]
    leadins = ["#" + x for x in info["lead_ins"]]
    leadouts = ["#" + x for x in info["lead_outs"]]
    if leadins:
        leadins = "data-leadins=" + " ".join(leadins)
    else:
        leadins = ""
    if leadouts:
        leadouts = "data-leadouts=" + " ".join(leadouts)
    else:
        leadouts = ""
    return " ".join(
        [
            "<div",
            f'id={tag} class="scene-type-{scenetype} depth-{depth}"',
            ">",
            f"<span class=linepoint id=line-end-{tag}></span>",
            # f"{leadins}",
            # f"{leadouts}",
            f'<span style="position:relative; z-index:100;">{title}</span>',
            f"<span class=linepoint id=line-start-{tag}></span>",
            "</div>",
        ]
    )
