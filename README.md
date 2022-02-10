## Introduction

This web application (still in development) is designed to help a game master (GM) run the *Fatal Frequencies* module for the Gumshoe One-2-One roleplaying game.

The app's database stores a large amount of information manually extracted from the module, which will be presented to the GM intelligently to help them remember what NPCs want, where items can be found, and what the player has already done. Inquiry into the effectiveness of this sort of "GM assistance" is the primary research goal of the project's lead.

## People

Project Lead: Devi Acharya, PhD Candidate
Software Development: Maxwell Joslyn, MS student
UI Design: Will Tate, BS student
Data Extraction: Michael Meacham, BS Student

## Installation Instructions

Download:

`git clone https://github.com/maxwelljoslyn/fatalfrequencies`

Install dependencies:

`poetry install`

Run:

`poetry run web serve ff:app --port 9090`

## Development Roadmap

JSON
- ✅Ingest JSON into the app (format seems to be stabilizing)
- ✅Do any necessary transformation on JSON (eg storing unchanging module data separately from changeable playthru data)
- ✅Ingest JSON to db

Database
- ✅able clues_known (tag)
- ✅able scenes_visited (tag)
- ✅playthroughs table, including ID, player, gm, and player character status

UI
- ✅Full (ugly) prototype of one+ UI view
- [✅Fstretch goal] Proof of concept “end to end” state change prototype
- generate graph of scene connections
- use `tag`s for edges, problems etc. to retrieve `name`s for display in UI

Logic Programming for Adaptive NPC Goals
- 🏗️Adapt Prolog statement writer to load from SQL, not JSON (including prefixing)
- ? install prolog interpreter for system if it's not already present
- start prolog interpreter on app startup
- web request interface around prolog interpreter a la Shi's code
- come up with representations of NPC goals

Playthroughs
- todo def new_playthrough()
- store playthrough id somewhere in app (session)
- remove checks for more than one playthrough e.g. in class Player (bc session storage will have that chosen, we won't need to check if player has been in more than one)
- add current scene to playthrough table
- if playthrough id not set in session, any view redirects to view.select_playthrough (show current scene, not only to help remember where they left off, but also to help partially disambiguate if the same two people play multiple through multiple times, as is especially likely while we are testing)
- add "select playthrough" link to home page
- figure out how best to store player path through scenes

Other
- inform GM when players in previous playthroughs did/didn't recover certain clues, etc.
