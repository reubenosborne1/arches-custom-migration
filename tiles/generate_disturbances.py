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
    v4tiles = []

    for entity in (data['child_entities']):
        if "EAMENA-" in entity['label'] :
            EAMENAID = entity['label']
        
        for child1 in entity['child_entities']:
             if child1['entitytypeid'] ==  "CONDITION_STATE.E3":
                for child2 in child1['child_entities']:
                    v4tile = {}
                    if child2['entitytypeid'] ==  "DAMAGE_STATE.E3":
                        for child3 in child2['child_entities']:
                            for child4 in child3['child_entities']:
                                if child4['entitytypeid'] =="DISTURBANCE_CAUSE_CATEGORY_TYPE.E55":
                                    v4tile[child4['entitytypeid']]  = child4['value']
                                for child5 in child4['child_entities']:
              
                                    if child5['child_entities']:
                                        for child6 in child5['child_entities']:
                                            v4tile[child6['entitytypeid']]  = child6['value']
                      
                                    else:
                                        v4tile[child5['entitytypeid']]  = child5['value'] 
                        v4tiles.append(v4tile)  





    v4_data_nodes =  {
    "EFFECT_TYPE": "34cfea90-c2c0-11ea-9026-02e7594ce0a0",
    "EFFECT_CERTAINTY":"34cfea5c-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_DATE_OCCURRED_BEFORE":"34cfea92-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_DATE_OCCURRED_ON": "34cfea7f-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_DATE_FROM": "34cfea65-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_DATE_TO":"34cfea7a-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_CAUSE_CATEGORY_TYPE":"34cfea68-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_CAUSE_TYPE":"34cfea79-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_CAUSE_CERTAINTY":"34cfea3d-c2c0-11ea-9026-02e7594ce0a0",
    "DISTURBANCE_CAUSE_ASSIGNMENT_ASSESSOR_NAME":"34cfea36-c2c0-11ea-9026-02e7594ce0a0"}

    v4_nodegroups ={
        "DISTURBANCES": "34cfe9aa-c2c0-11ea-9026-02e7594ce0a0",
        "DISTURBANCE":"34cfe9c2-c2c0-11ea-9026-02e7594ce0a0",
        "CAUSE":"34cfe99e-c2c0-11ea-9026-02e7594ce0a0",
        "EFFECT": "34cfe9ce-c2c0-11ea-9026-02e7594ce0a0",
    }    
    

    tiles = []
    grandparent_id = str(uuid.uuid4())
    grandparent_tile = {
            'data': {},
            'nodegroup_id': v4_nodegroups["DISTURBANCES"],
            'parenttile_id': "",# Correct parent tile id
            'provisionaledits': None,
            'resourceinstance_id': '',# Check this? Guess it is the id of this resource
            'sortorder': 0,
            'tileid': grandparent_id,
    }
    tiles.append(grandparent_tile)


    for data_dict in v4tiles:
        
        try: 
            disturbance_category = data_dict['DISTURBANCE_CAUSE_CATEGORY_TYPE.E55']
        except:
            disturbance_category = None
       
        parent_id = str(uuid.uuid4())
        parent_tile = {
                'data': {
                    v4_data_nodes['DISTURBANCE_CAUSE_CATEGORY_TYPE']: disturbance_category
                 },
                'nodegroup_id': v4_nodegroups["DISTURBANCE"],
                'parenttile_id': grandparent_id,
                'provisionaledits': None,
                'resourceinstance_id': '',
                'sortorder': 0,
                'tileid': parent_id,
        }
        tiles.append(parent_tile)

        
        try:
            disturbance_cause = data_dict["DISTURBANCE_CAUSE_TYPE.I4"]
        except:
            disturbance_cause = None
        try: 
            disturbance_certainty = data_dict["DISTURBANCE_CAUSE_CERTAINTY.I6"]
        except:
            disturbance_certainty = None
        try:
            date_from = data_dict['DISTURBANCE_DATE_FROM.E61']
        except: 
            date_from = None
        try:
            date_to = data_dict['DISTURBANCE_DATE_TO.E61']
        except: 
            date_to = None
        try:
            date_on = data_dict['DISTURBANCE_DATE_OCCURRED_ON.E61']
        except: 
            date_on = None
        try:
            date_before = data_dict['DISTURBANCE_DATE_OCCURRED_BEFORE.E61']
        except: 
            date_before = None
        try: 
            assessor = data_dict['DISTURBANCE_CAUSE_ASSIGNMENT_ASSESSOR_NAME.E41']
        except:
            assessor = None

        if date_from:
            date_from = date_from.split('T')[0]
        if date_to:
            date_to = date_to.split('T')[0]
        if date_on:
            date_on = date_on.split('T')[0]
        if date_before:
            date_before = date_before.split('T')[0]
        
            
        child_id = str(uuid.uuid4())
        child_tile = {
                'data': {
                    v4_data_nodes["DISTURBANCE_CAUSE_TYPE"]: disturbance_cause,
                    v4_data_nodes["DISTURBANCE_CAUSE_CERTAINTY"]: disturbance_certainty,
                    v4_data_nodes["DISTURBANCE_DATE_FROM"]: date_from,
                    v4_data_nodes["DISTURBANCE_DATE_TO"]: date_to,
                    v4_data_nodes["DISTURBANCE_DATE_OCCURRED_ON"]: date_on,
                    v4_data_nodes["DISTURBANCE_DATE_OCCURRED_BEFORE"]:date_before,
                    v4_data_nodes['DISTURBANCE_CAUSE_ASSIGNMENT_ASSESSOR_NAME']:assessor,
                },
                'nodegroup_id': v4_nodegroups["CAUSE"],
                'parenttile_id': parent_id,
                'provisionaledits': None,
                'resourceinstance_id': '',# Check this? Guess it is the id of this resource
                'sortorder': 0,
                'tileid': child_id,
        }
        tiles.append(child_tile)
        
        for i in range(1,6):
            
            if f'EFFECT_TYPE_{i}.I4' in data_dict:
               
                effect_type = data_dict[f'EFFECT_TYPE_{i}.I4']
       
                try:
                    effect_certainty = data_dict[f'EFFECT_CERTAINTY_{i}.I6']
                except:
                    effect_certainty = None

                grandchild_id = str(uuid.uuid4())
                grandchild_tile = {
                        'data': {
                            v4_data_nodes["EFFECT_TYPE"]: effect_type,
                            v4_data_nodes["EFFECT_CERTAINTY"]: effect_certainty,
                        },
                        'nodegroup_id': v4_nodegroups["EFFECT"],
                        'parenttile_id': child_id,
                        'provisionaledits': None,
                        'resourceinstance_id': '',# Check this? Guess it is the id of this resource
                        'sortorder': 0,
                        'tileid': grandchild_id,
                }
                tiles.append(grandchild_tile)
                
    finished_tiles = {'EAMENAID': EAMENAID,'tiles': tiles}
    finished_tiles = json.dumps(finished_tiles)
    period_json_list.append(finished_tiles)
    print(resnum)

with open((os.path.join(APP_ROOT, 'tiles/')) + 'disturbances_tiles.jsonl', 'w') as outfile:
    for item in period_json_list:
        item= json.loads(item)
        json.dump(item, outfile)
        outfile.write('\n')
