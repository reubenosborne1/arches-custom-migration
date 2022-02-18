import json
import uuid

file = "/home/rosborne/eamena_v3_data/v3resources-HERITAGE_PLACE.E27-2020-08-25.jsonl"
with open(file) as jsonl:
	json_list = list(jsonl)

period_json_list = [] 

# 1. Cycle through json in jsonl (each one is its own resource)
for resnum, json_str in enumerate(json_list):

	data = json.loads(json_str)

	# 2. Get EAMENA ID and append period tiles to new_data list for this resouce in the loop
	new_data = []
	for entity in (data['child_entities']):
		if "EAMENA-" in entity['label'] :
			EAMENAID = entity['label']
			
		for child1 in entity['child_entities']:
			if child1['entitytypeid'] == "PRODUCTION.E12":
				for child2 in child1['child_entities']:
					if child2['entitytypeid'] == 'DATE_INFERENCE_MAKING.I5':
						new_data.append(child2)
	v4tiles = []
	v4tile = {}
	v4_nodeids =  {
	  "DATE_INFERENCE_MAKING_ACTOR.E39": "DATE_INFERENCE_MAKING_ACTOR.E39",
	  "DATE_INFERENCE_MAKING_ACTOR_NAME.E41": "38cff73e-c77b-11ea-a292-02e7594ce0a0",
	  "CULTURAL_PERIOD_BELIEF.I2": "38cff734-c77b-11ea-a292-02e7594ce0a0",
	  "CULTURAL_PERIOD_TYPE.I4": "38cff73b-c77b-11ea-a292-02e7594ce0a0",
	  "CULTURAL_PERIOD_DETAIL_TYPE.E55": "38cff73c-c77b-11ea-a292-02e7594ce0a0",
	  "CULTURAL_PERIOD_CERTAINTY.I6": "38cff738-c77b-11ea-a292-02e7594ce0a0",
	  "V4-SUB-PERIOD-BELIEF":"38cff731-c77b-11ea-a292-02e7594ce0a0",
	  'CULTURAL_PERIOD_DETAIL_CERTAINTY.I6': "38cff73a-c77b-11ea-a292-02e7594ce0a0"

	 }
	for DATE_INFERENCE_MAKING in new_data:
		v4tile = {}
		for DATE_INFERENCE_MAKING_ACTOR in DATE_INFERENCE_MAKING['child_entities']:
			v4tile[v4_nodeids[DATE_INFERENCE_MAKING_ACTOR['entitytypeid']]] = DATE_INFERENCE_MAKING_ACTOR['value']
			for PERIOD_TILE in DATE_INFERENCE_MAKING_ACTOR['child_entities']:
				v4tile[v4_nodeids[PERIOD_TILE['entitytypeid']]] = PERIOD_TILE['value']
				if PERIOD_TILE['child_entities']:
					#print(PERIOD_TILE)
					for SUBPERIOD in PERIOD_TILE['child_entities']:
						v4tile[v4_nodeids[SUBPERIOD['entitytypeid']]] = SUBPERIOD['value']
						
		v4tiles.append(v4tile)

	tiles = []
	for data_dict in v4tiles:

		parent_id = str(uuid.uuid4())
		child_id = str(uuid.uuid4())
		try:
			actor_name = data_dict[v4_nodeids['DATE_INFERENCE_MAKING_ACTOR_NAME.E41']]
		except:
			actor_name = None

		try:
			certainty = data_dict[v4_nodeids['CULTURAL_PERIOD_CERTAINTY.I6']]
		except:
			certainty = None
			
		parent_tile = {
				'data': {
					v4_nodeids['DATE_INFERENCE_MAKING_ACTOR_NAME.E41']:actor_name ,
					v4_nodeids['CULTURAL_PERIOD_TYPE.I4']: data_dict[v4_nodeids['CULTURAL_PERIOD_TYPE.I4']],
					v4_nodeids['CULTURAL_PERIOD_CERTAINTY.I6']: certainty     
				},
				'nodegroup_id': v4_nodeids["CULTURAL_PERIOD_BELIEF.I2"],# Enter period nodeid
				'parenttile_id': "",# Correct parent tile id
				'provisionaledits': None,
				'resourceinstance_id': '',# Check this? Guess it is the id of this resource
				'sortorder': 0,
				'tileid': parent_id,
		}
		tiles.append(parent_tile)
		if v4_nodeids['CULTURAL_PERIOD_DETAIL_TYPE.E55'] in data_dict:
		 
			child_tile = {
					'data': {
						v4_nodeids['CULTURAL_PERIOD_DETAIL_TYPE.E55']: data_dict[v4_nodeids['CULTURAL_PERIOD_DETAIL_TYPE.E55']],
						v4_nodeids['CULTURAL_PERIOD_DETAIL_CERTAINTY.I6']: certainty     
					},
					'nodegroup_id': v4_nodeids["V4-SUB-PERIOD-BELIEF"],# Enter subperiod nodeid
					'parenttile_id': parent_id,
					'provisionaledits': None,
					'resourceinstance_id': '',# Check this? Guess it is the id of this resource
					'sortorder': 0,
					'tileid': child_id,
			}
			tiles.append(child_tile)
	finished_tiles = {'EAMENAID': EAMENAID,'tiles': tiles}
	finished_tiles = json.dumps(finished_tiles)
	period_json_list.append(finished_tiles)
	print(resnum)

with open((os.path.join(APP_ROOT, 'tiles/')) + 'period_tiles.jsonl', 'w') as outfile:
    for item in period_json_list:
        item= json.loads(item)
        json.dump(item, outfile)
        outfile.write('\n')
