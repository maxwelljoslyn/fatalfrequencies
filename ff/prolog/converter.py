import json
import re

def check_in_item_tag(pred, item, item_type): 
	if pred in item:
		fWrite.write( item_type + "(" + str(item[pred]) + ").\n")
		return item[pred]

def check_in_item(pred, item): 
	if pred in item:
		fWrite.write( pred + "(" + tag + ", " + str(item[pred]) + ").\n")

def check_in_item_bool(pred, item): 
	if pred in item:
		if (item[pred] == False):  
			fWrite.write( pred + "(" + tag + ", false).\n")
		else: 
			fWrite.write( pred + "(" + tag + ", true).\n")

def check_in_item_arr(pred, item): 
	if pred in item:
		array = item[pred]
		for subitem in array: 
			fWrite.write( pred + "(" + tag + ", " + str(subitem) + ").\n")

def check_in_item_arr_obj(pred, item): 
	if pred in item:
		array = item[pred]
		for subitem in array: 
			obj = subitem
			result_string = pred + "(" + tag
			for obj_part in obj: 
				result_string = result_string + ", " +  str(obj[obj_part]) 
			result_string = result_string + ").\n"
			fWrite.write(result_string)

def check_in_item_obj(pred, item): 
	if pred in item:
		obj = item[pred]
		result_string = pred + "(" + tag
		for subitem in obj: 
			result_string = result_string + ", \"" +  str(obj[subitem]) + "\""
		result_string = result_string + ").\n"
		fWrite.write(result_string)
		

def check_in_item_quotes(pred, item): 
	if pred in item:
		fWrite.write( pred + "(" + tag + ", \"" + str(item[pred]) + "\").\n")

def check_in_item_arr_quotes(pred, item): 
	if pred in item:
		array = item[pred]
		for subitem in array: 
			fWrite.write( pred + "(" + tag + ", \"" + str(subitem) + "\").\n")


def convert_scenes():
	# opens the JSON file with the data and saves it to a JSON object
	with open('scenes.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(scene/1).\n")
	fWrite.write(":- dynamic(scene_name/2).\n")
	fWrite.write(":- dynamic(scene_type/2).\n")
	fWrite.write(":- dynamic(scene_visited/2).\n")
	fWrite.write(":- dynamic(scene_lead_outs/2).\n")
	fWrite.write(":- dynamic(scene_description/2).\n")
	fWrite.write(":- dynamic(scene_clues/2).\n")
	fWrite.write(":- dynamic(scene_characters/2).\n")
	fWrite.write(":- dynamic(scene_challenges/2).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "scene")
		
		pred = "scene_name"
		check_in_item_quotes(pred, item)

		pred = "scene_type"
		check_in_item(pred, item)

		pred = "scene_visited"
		check_in_item_bool(pred, item)

		pred = "scene_lead_ins"
		check_in_item_arr(pred, item)
		
		pred = "scene_lead_outs"
		check_in_item_arr(pred, item)

		pred = "scene_description"
		check_in_item_arr_quotes(pred, item)

		pred = "scene_clues"
		check_in_item_arr(pred, item)

		pred = "scene_characters"
		check_in_item_arr(pred, item)

		pred = "scene_challenges"
		check_in_item_arr(pred, item)

def convert_clues():
	# opens the JSON file with the data and saves it to a JSON object
	with open('clues.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(clue/1).\n")
	fWrite.write(":- dynamic(clue_desc/2).\n")
	fWrite.write(":- dynamic(clue_known/2).\n")
	fWrite.write(":- dynamic(clue_leads_to/2).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "clue")
		
		pred = "clue_desc"
		check_in_item_quotes(pred, item)

		pred = "clue_known"
		check_in_item_bool(pred, item)

		pred = "clue_leads_to"
		check_in_item(pred, item)

def convert_sources():
	# opens the JSON file with the data and saves it to a JSON object
	with open('sources.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(source/1).\n")
	fWrite.write(":- dynamic(source_name/2).\n")
	fWrite.write(":- dynamic(source_profession/2).\n")
	fWrite.write(":- dynamic(source_description/2).\n")
	fWrite.write(":- dynamic(source_investigative_abilities/2).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "source")
		
		pred = "source_name"
		check_in_item_quotes(pred, item)

		pred = "source_profession"
		check_in_item_quotes(pred, item)

		pred = "source_description"
		check_in_item_quotes(pred, item)

		pred = "source_investigative_abilities"
		check_in_item_arr(pred, item)

def convert_problems():
	# opens the JSON file with the data and saves it to a JSON object
	with open('problems.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(problem/1).\n")
	fWrite.write(":- dynamic(problem_number/2).\n")
	fWrite.write(":- dynamic(problem_name/2).\n")
	fWrite.write(":- dynamic(problem_type/2).\n")
	fWrite.write(":- dynamic(problem_description/2).\n")
	fWrite.write(":- dynamic(problem_effect/2).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "problem")

		pred = "problem_number"
		check_in_item(pred, item)
		
		pred = "problem_name"
		check_in_item_quotes(pred, item)

		pred = "problem_type"
		check_in_item(pred, item)

		pred = "problem_description"
		check_in_item_quotes(pred, item)

		pred = "problem_effect"
		check_in_item_quotes(pred, item)

def convert_items():
	# opens the JSON file with the data and saves it to a JSON object
	with open('items.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(item/1).\n")
	fWrite.write(":- dynamic(item_name/2).\n")
	fWrite.write(":- dynamic(item_description/2).\n")
	fWrite.write(":- dynamic(item_type/2).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "item")
		
		pred = "item_name"
		check_in_item_quotes(pred, item)

		pred = "item_description"
		check_in_item_quotes(pred, item)

		pred = "item_type"
		check_in_item(pred, item)

def convert_edges():
	# opens the JSON file with the data and saves it to a JSON object
	with open('edges.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(edge/1).\n")
	fWrite.write(":- dynamic(edge_number/2).\n")
	fWrite.write(":- dynamic(edge_name/2).\n")
	fWrite.write(":- dynamic(edge_description/2).\n")
	fWrite.write(":- dynamic(edge_effect/2).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "edge")

		pred = "edge_number"
		check_in_item(pred, item)
		
		pred = "edge_name"
		check_in_item_quotes(pred, item)

		pred = "edge_description"
		check_in_item_quotes(pred, item)

		pred = "edge_effect"
		check_in_item_quotes(pred, item)

def convert_challenges():
	# opens the JSON file with the data and saves it to a JSON object
	with open('challenges.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(challenge/1).\n")
	fWrite.write(":- dynamic(challenge_name/2).\n")
	fWrite.write(":- dynamic(challenge_type/2).\n")
	fWrite.write(":- dynamic(challenge_advance/3).\n")
	fWrite.write(":- dynamic(challenge_hold/4).\n")
	fWrite.write(":- dynamic(challenge_setback/2).\n")
	fWrite.write(":- dynamic(challenge_extra_problem/2).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "challenge")
		
		pred = "challenge_name"
		check_in_item_quotes(pred, item)

		pred = "challenge_type"
		check_in_item_quotes(pred, item)

		pred = "challenge_advance"
		check_in_item_obj(pred, item)

		pred = "challenge_hold"
		check_in_item_obj(pred, item)

		pred = "challenge_setback"
		check_in_item_obj(pred, item)

		pred = "challenge_extra_problem"
		check_in_item(pred, item)

def convert_characters():
	# opens the JSON file with the data and saves it to a JSON object
	with open('characters.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(character/1).\n")
	fWrite.write(":- dynamic(character_name/2).\n")
	fWrite.write(":- dynamic(character_goal/2).\n")
	fWrite.write(":- dynamic(character_knows/2).\n")
	fWrite.write(":- dynamic(character_relationship_with/4).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 
		tag = check_in_item_tag(pred, item, "character")
		
		pred = "character_name"
		check_in_item_quotes(pred, item)

		pred = "character_goal"
		check_in_item_quotes(pred, item)

		pred = "character_knows"
		check_in_item_arr(pred, item)

		pred = "character_relationship_with"
		check_in_item_arr_obj(pred, item)

def convert_investigative_abilities():
	# opens the JSON file with the data and saves it to a JSON object
	with open('investigative_abilities.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(investigative_ability/4).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 

		result_string = "investigative_ability(" + str(item["tag"]) + ", \"" +  str(item["investigative_ability_name"]) + "\", \"" + str(item["investigative_ability_description"]) + "\", " + str(item["investigative_ability_type"]) + ")."
		fWrite.write( result_string + "\n")

def convert_general_abilities():
	# opens the JSON file with the data and saves it to a JSON object
	with open('general_abilities.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(general_ability/5).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	for item in data:
		pred = "tag" 
		global tag 

		result_string = "general_ability(" + str(item["tag"]) + ", \"" +  str(item["general_ability_name"]) + "\", \"" + str(item["general_ability_description"]) + "\", " + str(item["general_ability_type"]) + ", " + str(item["general_ability_skill_value"]) + ")."
		fWrite.write(result_string + "\n")

def convert_player_character():
	# opens the JSON file with the data and saves it to a JSON object
	with open('player_character.json') as data_file:
	    data = json.load(data_file)

	# add in the predicate definitions 
	fWrite.write(":- dynamic(player_edge/1).\n")
	fWrite.write(":- dynamic(player_problem/1).\n")
	fWrite.write(":- dynamic(player_investigative_ability/1).\n")
	fWrite.write(":- dynamic(player_general_ability/2).\n")
	fWrite.write(":- dynamic(player_pushes/1).\n")
	fWrite.write(":- dynamic(player_item/1).\n")
	fWrite.write("\n")
	# runs through each element in JSON object and extracts the data, writing it to file
	
	for item in data["player_edge"]: 
		fWrite.write("player_edge(" + item + ").\n")

	for item in data["player_problem"]: 
		fWrite.write("player_problem(" + item + ").\n")

	for item in data["player_investigative_ability"]: 
		fWrite.write("player_investigative_ability(" + item + ").\n")

	for item in data["player_general_ability"]: 
		fWrite.write("player_general_ability(" + item + ").\n")

	fWrite.write("player_pushes(" + str(data["player_pushes"]) + ").\n")

	for item in data["player_item"]: 
		fWrite.write("player_item(" + str(item) + ").\n")


def add_front_matter(): 
	fWrite.write(":- set_prolog_flag(double_quotes, atom).\n")
	fWrite.write("current_prolog_flag(character_escapes, true).\n")

tag = ""
# file to which we will be writing 
fWrite = open('database.prolog', 'w')
add_front_matter()
fWrite.write("\n\n")
convert_scenes()
fWrite.write("\n\n")
convert_clues()
fWrite.write("\n\n")
convert_sources()
fWrite.write("\n\n")
convert_problems()
fWrite.write("\n\n")
convert_items()
fWrite.write("\n\n")
convert_edges()
fWrite.write("\n\n")
convert_challenges()
fWrite.write("\n\n")
convert_characters()
fWrite.write("\n\n")
convert_investigative_abilities()
fWrite.write("\n\n")
convert_general_abilities()
fWrite.write("\n\n")
convert_player_character()
fWrite.close()

