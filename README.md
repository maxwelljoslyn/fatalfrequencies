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
