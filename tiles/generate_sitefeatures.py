import json
import uuid

file = "/home/rosborne/eamena_v3_data/v3resources-HERITAGE_PLACE.E27-2020-08-25.jsonl"
with open(file) as jsonl:
	json_list = list(jsonl)

sfa_json_list = [] 

# 1. Cycle through json in jsonl (each one is its own resource)
for resnum, json_str in enumerate(json_list):

	data = json.loads(json_str)
	new_data = []
	for entity in (data['child_entities']):
		#print(json.dumps(entity, indent=2))
		if "EAMENA-" in entity['label'] :
			EAMENAID = entity['label']
			
		for child1 in entity['child_entities']:
			if child1['entitytypeid'] == "FEATURE_ASSIGNMENT.E13":
				for child2 in child1['child_entities']:
					if child2['entitytypeid'] == "FEATURE_SHAPE_TYPE.E55":
			
			
						new_data.append(child1)
	v4tiles = []

	v4_nodeids =  {
	"SITE_FEATURE_ASSIGMENT": "34cfea13-c2c0-11ea-9026-02e7594ce0a0",
	"SITE_FEATURE_FORM_TYPE_BELIEF": "34cfe9b0-c2c0-11ea-9026-02e7594ce0a0",
	"FEATURE_FORM_TYPE.I4":"34cfea9a-c2c0-11ea-9026-02e7594ce0a0",
	"FEATURE_FORM_TYPE_CERTAINTY.I6":"34cfea59-c2c0-11ea-9026-02e7594ce0a0",
	"FEATURE_SHAPE_TYPE.E55": "34cfea19-c2c0-11ea-9026-02e7594ce0a0",
	"FEATURE_ARRANGEMENT_TYPE.E55": "34cfe9e9-c2c0-11ea-9026-02e7594ce0a0",
	"FEATURE_NUMBER_TYPE.E55":"34cfe9f8-c2c0-11ea-9026-02e7594ce0a0",}

	for data in new_data:
		v4tile = {}
		for level1 in data['child_entities']:
			if level1["entitytypeid"] =="FEATURE_SHAPE_TYPE.E55":
				v4tile[level1["entitytypeid"]] = level1["value"]
			if level1["entitytypeid"] =="FEATURE_ARRANGEMENT_TYPE.E55":
				v4tile[level1["entitytypeid"]] = level1["value"]
			if level1["entitytypeid"] =="FEATURE_NUMBER_TYPE.E55":
				v4tile[level1["entitytypeid"]] = level1["value"]
			if level1['child_entities']:
				for level2 in level1['child_entities']:
					if level2["entitytypeid"] =="FEATURE_FORM_TYPE.I4":
						v4tile[level2["entitytypeid"]] = level2["value"]
					if level2["entitytypeid"] =="FEATURE_FORM_TYPE_CERTAINTY.I6":
						v4tile[level2["entitytypeid"]] = level2["value"]
		v4tiles.append(v4tile)

	tiles = []
	for data_dict in v4tiles:

		grandparent_tile = str(uuid.uuid4())

		SFA_tile = {
				'data': {},
				'nodegroup_id': v4_nodeids["SITE_FEATURE_ASSIGMENT"],
				'parenttile_id': "",# Correct parent tile id
				'provisionaledits': None,
				'resourceinstance_id': '',# Check this? Guess it is the id of this resource
				'sortorder': 0,
				'tileid': grandparent_tile,
		}

		tiles.append(SFA_tile)

		parent_id = str(uuid.uuid4())

		try:
			form = data_dict['FEATURE_FORM_TYPE.I4']
		except:
			form = None
		
		try:
			certainty = data_dict["FEATURE_FORM_TYPE_CERTAINTY.I6"]
		except:
			certainty = None

			
		parent_tile = {
				'data': {
					v4_nodeids['FEATURE_FORM_TYPE.I4']: form,
					v4_nodeids["FEATURE_FORM_TYPE_CERTAINTY.I6"]: certainty,    
				},
				'nodegroup_id': v4_nodeids["SITE_FEATURE_FORM_TYPE_BELIEF"],
				'parenttile_id': grandparent_tile,
				'provisionaledits': None,
				'resourceinstance_id': '',# Check this? Guess it is the id of this resource
				'sortorder': 0,
				'tileid': parent_id,
		}
		tiles.append(parent_tile)
		if "FEATURE_NUMBER_TYPE.E55" in data_dict:
			child_id = str(uuid.uuid4())
			child_tile = {
					'data': {
						v4_nodeids["FEATURE_NUMBER_TYPE.E55"]: data_dict["FEATURE_NUMBER_TYPE.E55"],
					},
					'nodegroup_id': v4_nodeids["FEATURE_NUMBER_TYPE.E55"],# Enter shape/number/arrangement
					'parenttile_id': parent_id,
					'provisionaledits': None,
					'resourceinstance_id': '',# Check this? Guess it is the id of this resource
					'sortorder': 0,
					'tileid': child_id,
			}
			tiles.append(child_tile)
			
		if "FEATURE_SHAPE_TYPE.E55" in data_dict:
			child_id = str(uuid.uuid4())
			child_tile = {
					'data': {
						v4_nodeids["FEATURE_SHAPE_TYPE.E55"]: data_dict["FEATURE_SHAPE_TYPE.E55"],
					},
					'nodegroup_id': v4_nodeids["FEATURE_SHAPE_TYPE.E55"],# Enter shape/number/arrangement
					'parenttile_id': parent_id,
					'provisionaledits': None,
					'resourceinstance_id': '',# Check this? Guess it is the id of this resource
					'sortorder': 0,
					'tileid': child_id,
			}
			tiles.append(child_tile)
			
		if "FEATURE_ARRANGEMENT_TYPE.E55" in data_dict:
			child_id = str(uuid.uuid4())
			child_tile = {
					'data': {
						v4_nodeids["FEATURE_ARRANGEMENT_TYPE.E55"]: data_dict["FEATURE_ARRANGEMENT_TYPE.E55"],
					},
					'nodegroup_id': v4_nodeids["FEATURE_ARRANGEMENT_TYPE.E55"],# Enter shape/number/arrangement
					'parenttile_id': parent_id,
					'provisionaledits': None,
					'resourceinstance_id': '',# Check this? Guess it is the id of this resource
					'sortorder': 0,
					'tileid': child_id,
			}
			tiles.append(child_tile)
		
	# General - replace the data nodes!
	finished_tiles = {'EAMENAID': EAMENAID,'tiles': tiles}
	finished_tiles = json.dumps(finished_tiles)
	sfa_json_list.append(finished_tiles)
	print(resnum)

with open((os.path.join(APP_ROOT, 'tiles/')) + 'sfftb_tiles.jsonl', 'w') as outfile:
	for item in sfa_json_list:
		item = json.loads(item)
		json.dump(item, outfile)
		outfile.write('\n')


