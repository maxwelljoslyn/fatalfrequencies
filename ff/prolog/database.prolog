:- set_prolog_flag(double_quotes, atom).
current_prolog_flag(character_escapes, true).


:- dynamic(scene/1).
:- dynamic(scene_name/2).
:- dynamic(scene_type/2).
:- dynamic(scene_visited/2).
:- dynamic(scene_lead_outs/2).
:- dynamic(scene_description/2).
:- dynamic(scene_clues/2).
:- dynamic(scene_characters/2).
:- dynamic(scene_challenges/2).

scene(sadies_sob_story).
scene_name(sadies_sob_story, "Sadie's Sob Story").
scene_type(sadies_sob_story, introduction).
scene_visited(sadies_sob_story, false).
scene_lead_outs(sadies_sob_story, what_the_cops_know).
scene_lead_outs(sadies_sob_story, fullers_electrical_repair).
scene_lead_outs(sadies_sob_story, the_peculiar_death_of_myron_fink).
scene_description(sadies_sob_story, "The scenario starts off for Vivian Sinclair on a Monday morning after she’s turned in her most recent story. Invite the player to describe it, if she likes. She may rest on her laurels and joke around with the guys in the Herald Tribune’s newsroom, or she may already be scouring a pile of newspaper clippings and notes for her next lead. Around 9 a.m., she gets a telephone call from downstairs.").
scene_description(sadies_sob_story, "Use this as an opportunity to establish Viv’s newsroom and how she meets with interested parties. Does she have the receptionist send them up to her desk in a smoky room full of (mostly) men bent over typewriters and paper-strewn desks? Or does she meet with her Sources and sometime- clients in another location, such as a restaurant across the street? Have the player take a moment to describe something important that Viv keeps at her desk in the newsroom, or her regular order at the restaurant.").
scene_clues(sadies_sob_story, someone_in_georges).
scene_clues(sadies_sob_story, george_works_as).
scene_characters(sadies_sob_story, sadie_cain).


:- dynamic(clue/1).
:- dynamic(clue_desc/2).
:- dynamic(clue_known/2).
:- dynamic(clue_leads_to/2).

clue(someone_in_georges).
clue_desc(someone_in_georges, "Someone in George’s apartment building was murdered the day before he disappeared. She gives an address and third-story apartment number near the Brooklyn Navy Yard.").
clue_known(someone_in_georges, false).
clue(george_works_as).
clue_desc(george_works_as, "(Core, 'Fuller’s Electrical Repair') George works as an electrical repairman at Fuller’s Electrical Repair, just a couple blocks north of Fulton Street in downtown Brooklyn.").
clue_known(george_works_as, false).
clue_leads_to(george_works_as, fullers_electrical_repair).


:- dynamic(source/1).
:- dynamic(source_name/2).
:- dynamic(source_profession/2).
:- dynamic(source_description/2).
:- dynamic(source_investigative_abilities/2).

source(annette_rice).
source_name(annette_rice, "Annette (Nettie) Rice").
source_profession(annette_rice, "Professor").
source_description(annette_rice, "If, during her time at Hunter College, someone had asked Viv which professor she’d be closest friends with in a decade, she’d never have named Nettie Rice.").
source_investigative_abilities(annette_rice, astronomy).
source_investigative_abilities(annette_rice, biology).
source_investigative_abilities(annette_rice, chemistry).
source_investigative_abilities(annette_rice, languages).
source_investigative_abilities(annette_rice, physics).


:- dynamic(problem/1).
:- dynamic(problem_number/2).
:- dynamic(problem_name/2).
:- dynamic(problem_type/2).
:- dynamic(problem_description/2).
:- dynamic(problem_effect/2).

problem(sucker_for_a_pretty_face).
problem_number(sucker_for_a_pretty_face, 1).
problem_name(sucker_for_a_pretty_face, "Sucker for a Pretty Face").
problem_type(sucker_for_a_pretty_face, continuity).
problem_description(sucker_for_a_pretty_face, "You change lovers as frequently as clothes.").
problem(wrenched_ankle).
problem_number(wrenched_ankle, 8).
problem_name(wrenched_ankle, "Wrenched Ankle").
problem_effect(wrenched_ankle, "-2 on your next Athletics, Fighting, or other General/Physical test or Take Time and then discard this Problem").


:- dynamic(item/1).
:- dynamic(item_name/2).
:- dynamic(item_description/2).
:- dynamic(item_type/2).

item(gun).
item_name(gun, "A Gun").
item_description(gun, "A gun you got from a friend").
item_type(gun, weapon).


:- dynamic(edge/1).
:- dynamic(edge_number/2).
:- dynamic(edge_name/2).
:- dynamic(edge_description/2).
:- dynamic(edge_effect/2).

edge(ice_queen).
edge_number(ice_queen, 1).
edge_name(ice_queen, "Ice Queen").
edge_description(ice_queen, "You're getting better at prioritizing things that matter.").
edge_effect(ice_queen, "Spend to get an extra die on Cool or Stability or a +2 on a General/Mental test, then discard").


:- dynamic(challenge/1).
:- dynamic(challenge_name/2).
:- dynamic(challenge_type/2).
:- dynamic(challenge_advance/3).
:- dynamic(challenge_hold/4).
:- dynamic(challenge_setback/2).
:- dynamic(challenge_extra_problem/2).

challenge(other_peoples_mail).
challenge_name(other_peoples_mail, "Other People's Mail").
challenge_type(other_peoples_mail, "filch").
challenge_advance(other_peoples_mail, "4", "You successfully purloin the letter. Grants access to alternate scene 'The Psychical Investigator'.").
challenge_hold(other_peoples_mail, "2", "3", "As your fingers brush the edge of the letter, Fuller makes eye contact and his eyes begin to move downward. If you decide to play it off by deliberately noticing the letter’s address, you may spend a Push to convince him you’ll give the letter to Preston’s fiancée. He demurs to this suggestion, but may later change his mind. Grants access to alternate scene 'The Psychical Investigator'.").
challenge_setback(other_peoples_mail, "Fuller sees you tip the letter into your handbag. After snatching it back, he roughly escorts you out of the building and threatens to call the police if you set foot inside again. If you have not yet spoken to Charlie Fitzpatrick, she follows you onto the street to see if you know something about George.").
challenge_extra_problem(other_peoples_mail, fuller_becomes_suspicious).


:- dynamic(character/1).
:- dynamic(character_name/2).
:- dynamic(character_goal/2).
:- dynamic(character_knows/2).
:- dynamic(character_relationship_with/4).

character(sadie_cain).
character_name(sadie_cain, "Sadie Cain").
character_goal(sadie_cain, "Find missing husband").
character_knows(sadie_cain, george_preston).
character_relationship_with(sadie_cain, george_preston, married, positive).


:- dynamic(investigative_ability/4).

investigative_ability(accounting, "Accounting", "You understand bookkeeping and accountancy procedures; you can read and keep financial records.", academic).


:- dynamic(general_ability/5).

general_ability(athletics, "Athletics", "Athletics allows you to perform general acts of physical derring-do, from running to jumping to throwing bundles of dynamite to dodging oncoming objects.", physical, 1).


:- dynamic(player_edge/1).
:- dynamic(player_problem/1).
:- dynamic(player_investigative_ability/1).
:- dynamic(player_general_ability/2).
:- dynamic(player_pushes/1).
:- dynamic(player_item/1).

player_edge(ice_queen).
player_problem(sucker_for_a_pretty_face).
player_investigative_ability(accounting).
player_investigative_ability(assess_honesty).
player_general_ability(athletics).
player_pushes(4).
