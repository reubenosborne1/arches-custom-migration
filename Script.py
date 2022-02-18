import json
import uuid
import os
import inspect
import pandas as pd
import multiprocessing as mp

APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

in_file = APP_ROOT + '/input/HERITAGE_PLACES_UNSUCESSFUL.jsonl'
out_file = APP_ROOT + '/output/HERITAGE_PLACES-output.jsonl'
outputfile = open(out_file, 'w')

grid_file = APP_ROOT + '/mappings/grid_mapping.csv'
people_file = APP_ROOT + '/mappings/personorg_mapping.csv'


# NodeGroup Assignment
AS = '34cfea2e-c2c0-11ea-9026-02e7594ce0a0'
ASSESSMENT_INVESTIGATOR = '34cfea8a-c2c0-11ea-9026-02e7594ce0a0'
RS = '34cfe98f-c2c0-11ea-9026-02e7594ce0a0'
AA = "34cfe9b3-c2c0-11ea-9026-02e7594ce0a0"
SFA = "34cfea13-c2c0-11ea-9026-02e7594ce0a0"
SFIB = "34cfe9fe-c2c0-11ea-9026-02e7594ce0a0"
SFFTB = "34cfe9b0-c2c0-11ea-9026-02e7594ce0a0"
EAMENA_NUMBER = '34cfe992-c2c0-11ea-9026-02e7594ce0a0'
CPB = '38cff734-c77b-11ea-a292-02e7594ce0a0'
CSPB ='38cff731-c77b-11ea-a292-02e7594ce0a0'
SITE_FEATURE_FORM_TYPE_BELIEF= "34cfe9b0-c2c0-11ea-9026-02e7594ce0a0"
FEATURE_FORM_TYPE="34cfea9a-c2c0-11ea-9026-02e7594ce0a0"
FEATURE_FORM_TYPE_CERTAINTY="34cfea59-c2c0-11ea-9026-02e7594ce0a0"
FEATURE_SHAPE_TYPE= "34cfea19-c2c0-11ea-9026-02e7594ce0a0"
FEATURE_ARRANGEMENT_TYPE= "34cfe9e9-c2c0-11ea-9026-02e7594ce0a0"
FEATURE_NUMBER_TYPE="34cfe9f8-c2c0-11ea-9026-02e7594ce0a0"
BUILD_COMPONENT = "3d218500-c385-11ea-9026-02e7594ce0a0"
HERITAGE_PLACE_RESOURCE_INSTANCE = "34cfe9e3-c2c0-11ea-9026-02e7594ce0a0"
CERTAINTY_OBSERVATION = '34cfe9a4-c2c0-11ea-9026-02e7594ce0a0'
SITE_MORPHOLOGY = '34cfe9e6-c2c0-11ea-9026-02e7594ce0a0'
ARCHAEOLOGICAL_TIMESPACE = '34cfe9cb-c2c0-11ea-9026-02e7594ce0a0'
MATERIAL = '34cfe9c5-c2c0-11ea-9026-02e7594ce0a0'
MEASUREMENTS = '34cfe9f2-c2c0-11ea-9026-02e7594ce0a0'
RELATED_GEOARCHAEOLOGY = "34cfe9ec-c2c0-11ea-9026-02e7594ce0a0"
DESIGNATION = "d9abdfdb-c6a3-11ea-a292-02e7594ce0a0"
DESCRIPTION = "34cfe9c8-c2c0-11ea-9026-02e7594ce0a0"
NAME = '34cfe9dd-c2c0-11ea-9026-02e7594ce0a0'
PLACE_TYPE = '34cfe9ef-c2c0-11ea-9026-02e7594ce0a0'
ASSIGNMENT = '34cfe9ad-c2c0-11ea-9026-02e7594ce0a0'
CONDITION_ASSIGNMENT = "34cfe9b9-c2c0-11ea-9026-02e7594ce0a0"
CONDITION_STATE = "34cfea6f-c2c0-11ea-9026-02e7594ce0a0"
DISTURBANCES = "34cfe9aa-c2c0-11ea-9026-02e7594ce0a0"
DISTURBANCE = "34cfe9c2-c2c0-11ea-9026-02e7594ce0a0"
CAUSE = "34cfe99e-c2c0-11ea-9026-02e7594ce0a0"
EFFECT = "34cfe9ce-c2c0-11ea-9026-02e7594ce0a0"
TOPOGRAPHY = '34cfea28-c2c0-11ea-9026-02e7594ce0a0'
LAND_COVER = '34cfea25-c2c0-11ea-9026-02e7594ce0a0'
MARINE_ENV = '34cfe998-c2c0-11ea-9026-02e7594ce0a0'
DEPTH = '34cfea1f-c2c0-11ea-9026-02e7594ce0a0'
SURFICIAL_GEOGRAPHY = '34cfea22-c2c0-11ea-9026-02e7594ce0a0'
BEDROCK_GEOGRAPHY = '34cfea2b-c2c0-11ea-9026-02e7594ce0a0'
GRIDID = "34cfea5d-c2c0-11ea-9026-02e7594ce0a0"
GEOGRAPHY = '34cfe9b6-c2c0-11ea-9026-02e7594ce0a0'
GEOMETRY = '3080eebe-c2c5-11ea-9026-02e7594ce0a0'
GEOMETRIC_PLACE_EXPESSION = '5348cf67-c2c5-11ea-9026-02e7594ce0a0'


# Open files
with open(in_file) as jsonl:
	json_list = list(jsonl)

with open((os.path.join(APP_ROOT, 'tiles/')) + 'period_tiles.jsonl') as period_jsonl:
	period_list = list(period_jsonl)

with open((os.path.join(APP_ROOT, 'tiles/')) + 'sitefeatures_tiles.jsonl') as sfftb_jsonl:
	sfftb_list = list(sfftb_jsonl)

with open((os.path.join(APP_ROOT, 'tiles/')) + 'disturbances_tiles.jsonl') as disturbances_jsonl:
	disturbance_resources = list(disturbances_jsonl)

grid_sqaures = pd.read_csv(grid_file)
people_data = pd.read_csv(people_file)

records = len(json_list)
 

def migrate(x, q):

	json_str = json_list[x] 

	

	data = json.loads(json_str)

	# Create tile lists & grab eamenaid / resource uuid
	AS_tiles = []
	AA_tiles = []
	RS_tiles = []
	CONDITION_ASSIGNMENT_TILE = []
	Geometry_tiles = []
	Geography_tiles = []
	for tile in data['tiles']:

		if tile['nodegroup_id'] == AS:
			AS_tiles.append(tile['tileid'])

		if tile['nodegroup_id'] == AA:
			AA_tiles.append(tile['tileid'])

		if tile['nodegroup_id'] == RS:
			RS_tiles.append(tile['tileid'])

		if tile['nodegroup_id'] == CONDITION_ASSIGNMENT:
			CONDITION_ASSIGNMENT_TILE.append(tile['tileid'])

		if tile['nodegroup_id'] == GEOMETRY:
			Geometry_tiles.append(tile['tileid'])

		if tile['nodegroup_id'] == GEOGRAPHY:
			Geography_tiles.append(tile['tileid'])

		if tile['nodegroup_id'] == EAMENA_NUMBER: 
			EAMENAID = tile['data'][EAMENA_NUMBER]
			RESOURCEID = tile['resourceinstance_id']


	# Find children tiles & nodes + Create geometry tile types
	AA_children_tiles = []
	AA_children_nodes = []
	RS_children_tiles = []
	polygon_tile = None
	point_tile = None
	other_tile = None
	for tile in data['tiles'][:]: 

		if tile['tileid'] in AS_tiles:

			try:
				actor_name_str = tile['data'][ASSESSMENT_INVESTIGATOR]

			except:
				actor_name_str = None
			if actor_name_str:
				try:
					actor_name_uuid = str(people_data['ResourceID'][people_data['Name'] == actor_name_str].values[0])
				except: 
					actor_name_uuid = None
				tile['data'][ASSESSMENT_INVESTIGATOR] = actor_name_uuid

		if tile['parenttile_id'] in AA_tiles:
			AA_children_tiles.append(tile['tileid'])
			AA_children_nodes.append(tile['nodegroup_id'])

		if tile['parenttile_id'] in RS_tiles:
			RS_children_tiles.append(tile['tileid'])

		if tile['tileid'] in Geometry_tiles:
			if GEOMETRIC_PLACE_EXPESSION in tile['data']:
				if tile['data'][GEOMETRIC_PLACE_EXPESSION]['features'][0]['geometry']['type'] == 'MultiPolygon':
					polygon_tile = tile['tileid']
				elif tile['data'][GEOMETRIC_PLACE_EXPESSION]['features'][0]['geometry']['type'] == 'Point':
					point_tile = tile['tileid']
				else: 
					other_tile = tile['tileid']

	# Assign Parent tiles   
	try:
		AA_parent_tile = AA_tiles[0]
	except: 
		AA_parent_tile = None
	try:
		RS_parent_tile = RS_tiles[0]
	except:
		RS_parent_tile = None
	try:
		CA_parent_tile = CONDITION_ASSIGNMENT_TILE[0]
	except:
		CA_parent_tile = None

	# Delete all but first tile & then assign children to this one parent
	for tile in data['tiles'][:]:

		if tile['tileid'] in AA_tiles[1:]:
			data['tiles'].remove(tile)

		if tile['nodegroup_id'] in AA_children_nodes:
			tile['parenttile_id'] = AA_parent_tile

		if tile['tileid'] in RS_tiles[1:]:
			data['tiles'].remove(tile)

		if tile['tileid'] in RS_children_tiles:
			tile['parenttile_id'] = RS_parent_tile

		if tile['parenttile_id'] in CONDITION_ASSIGNMENT_TILE[1:]:
			tile['parenttile_id'] = CA_parent_tile

		if tile['tileid'] in CONDITION_ASSIGNMENT_TILE[1:]:
			data['tiles'].remove(tile)

		# If there is more than one tile, combine to this priority 1. polygon tile 2. point tile 3. other tile
		if tile['tileid'] in Geometry_tiles:
			if GEOMETRIC_PLACE_EXPESSION not in tile['data']:
				for tile2 in data['tiles']:
					if polygon_tile: 
						if tile2['tileid'] == polygon_tile:
							for data_uuid in tile['data']:
								tile2['data'][data_uuid] = tile['data'][data_uuid]
					elif point_tile:
						if tile2['tileid'] == point_tile:
							for data_uuid in tile['data']:
								tile2['data'][data_uuid] = tile['data'][data_uuid]
					elif other_tile:
						if tile2['tileid'] == other_tile:
							for data_uuid in tile['data']:
								tile2['data'][data_uuid] = tile['data'][data_uuid]
				data['tiles'].remove(tile)

		try:
			geog_tile = Geography_tiles[0]
		except:
			geog_tile = None

		if geog_tile:
			if tile['tileid'] in Geography_tiles[0]:
				for tile2 in data['tiles']:
					if tile2['tileid'] in Geography_tiles[1:]:
						for uuid in tile2['data']:
							tile['data'][uuid] = tile2['data'][uuid]
						data['tiles'].remove(tile2)

				try:
					grid_id_str = tile['data'][GRIDID]
				except:
					grid_id_str = None

				if grid_id_str:
					try:
						grid_id_uuid = str(grid_sqaures['ResourceID'][grid_sqaures['Grid ID'] == grid_id_str].values[0])
					except: 
						grid_id_uuid = None
					tile['data'][GRIDID] = grid_id_uuid

	# --- Delete tiles that we've manually migrated ---
	for tile in data['tiles'][:]:
		# Periods
		if tile['nodegroup_id'] == CPB:
			data['tiles'].remove(tile)
		if tile['nodegroup_id'] == CSPB:
			data['tiles'].remove(tile)

		# Site features
		if tile['nodegroup_id'] == FEATURE_SHAPE_TYPE:
			data['tiles'].remove(tile)
		if tile['nodegroup_id'] == FEATURE_ARRANGEMENT_TYPE:
			data['tiles'].remove(tile)
		if tile['nodegroup_id'] == FEATURE_NUMBER_TYPE:
			data['tiles'].remove(tile)
		if tile['nodegroup_id'] == SITE_FEATURE_FORM_TYPE_BELIEF:
			data['tiles'].remove(tile)

		# Disturbances
		if tile['nodegroup_id'] == DISTURBANCES:
			data['tiles'].remove(tile)
		if tile['nodegroup_id'] == DISTURBANCE:
			data['tiles'].remove(tile)
		if tile['nodegroup_id'] == CAUSE:
			data['tiles'].remove(tile)
		if tile['nodegroup_id'] == EFFECT:
			data['tiles'].remove(tile)

	# --- Manual Period migration ---
	# Cycle through Period tiles file, find correct record and append to data
	for res_period in period_list:
		res_period = json.loads(res_period)
		if res_period['EAMENAID'] == EAMENAID:
			for period_tile in res_period['tiles']:
				period_tile['resourceinstance_id'] = RESOURCEID
				if period_tile['nodegroup_id'] == CPB:
					period_tile['parenttile_id'] = AA_parent_tile
			data['tiles'] = data['tiles'] + res_period['tiles']

	# --------- End --------- 

	# --- Start Manual Site Features Migration ---

	# Cycle through SF tiles file, find correct record and append to data 
	for sfftb_resource in sfftb_list:
		sfftb_resource = json.loads(sfftb_resource)
		if sfftb_resource['EAMENAID'] == EAMENAID:
			for sfftb_tile in sfftb_resource['tiles']:
				sfftb_tile['resourceinstance_id'] = RESOURCEID
				if sfftb_tile['nodegroup_id'] == SFA:
					sfftb_tile['parenttile_id'] = AA_parent_tile
			data['tiles'] = data['tiles'] + sfftb_resource['tiles']



	# Find SFA without children and remove

	# for tile in data['tiles'][:]:
	# 	if tile['nodegroup_id'] == SFA:
	# 		num_children = 0
	# 		for child in data['tiles']:
	# 			if child['parenttile_id'] == tile['tileid']:
	# 				num_children += 1
	# 		if num_children == 0:
				
	# 			data['tiles'].remove(tile)

	# --------- End ----------


	# --- Start Manual Disturbances --- 
	if CONDITION_ASSIGNMENT_TILE:
		for res in disturbance_resources:
			res = json.loads(res)
			# Find the correct record
			if res['EAMENAID'] == EAMENAID:
				for dist_tile in res['tiles']:
					dist_tile['resourceinstance_id'] = RESOURCEID
					if dist_tile['nodegroup_id'] == DISTURBANCES:
						dist_tile['parenttile_id'] = CA_parent_tile
				data['tiles'] = data['tiles'] + res['tiles']
	# --------- End -----------

	# Clean up 

	for tile in data['tiles'][:]:
		kids = 0
		if tile['data'] == {}:
			for children_tile in data['tiles']:
				if children_tile['parenttile_id'] == tile['tileid']:
					kids += 1 
			if kids == 0:
				data['tiles'].remove(tile)

	for tile in data['tiles'][:]:
		num = 0
		if tile['nodegroup_id'] == SFA:

			for tile2 in data['tiles']:
				if tile2['parenttile_id'] == tile['tileid']:
					num +=1
			if num == 0:
				data['tiles'].remove(tile)

	# file writing
	#print(EAMENAID, len(data['tiles']))
	json_str = json.dumps(data)
	q.put(json_str)
	return json_str


def write_to_output(q): 

	with open(out_file, 'w') as f:
		while 1:
			m = q.get()
			if m == 'kill':
				break
			item = json.loads(m)
			json.dump(item, f)
			f.write('\n')
			f.flush()


def main():
	#must use Manager queue here, or will not work
	manager = mp.Manager()
	q = manager.Queue()    
	pool = mp.Pool()

	#put listener to work first
	watcher = pool.apply_async(write_to_output, (q,))

	#fire off workers
	jobs = []
	for i in range(records):

		job = pool.apply_async(migrate, (i, q))
		jobs.append(job)

	# collect results from the workers through the pool result queue
	for i,job in enumerate(jobs):
		if i % 100 == 0:
			print(i) 
		job.get()

	#now we are done, kill the listener
	q.put('kill')
	pool.close()
	pool.join()


if __name__ == '__main__':
	main()





			# if tile['nodegroup_id'] == CERTAINTY_OBSERVATION:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == SITE_MORPHOLOGY:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == ARCHAEOLOGICAL_TIMESPACE:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == MATERIAL:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == MEASUREMENTS:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == RELATED_GEOARCHAEOLOGY:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == BUILD_COMPONENT:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == SFIB:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == HERITAGE_PLACE_RESOURCE_INSTANCE:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == DESIGNATION:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == DESCRIPTION:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == NAME:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == PLACE_TYPE:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == ASSIGNMENT:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == TOPOGRAPHY:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == LAND_COVER:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == MARINE_ENV:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == DEPTH:
				
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == SURFICIAL_GEOGRAPHY:
			
			# 	data['tiles'].remove(tile)

			# if tile['nodegroup_id'] == BEDROCK_GEOGRAPHY:
			
			# 	data['tiles'].remove(tile)



