# Pre Migration Processing
import json
file = "/home/rosborne/Projects/archesprojects/eamena-arches-5-project/eamena/pkg/business_data/HERITAGE_PLACES.jsonl"
outputfile = "/home/rosborne/Projects/archesprojects/eamena-arches-5-project/eamena/pkg/business_data/HERITAGE_PLACES_PRE.jsonl"

with open (file) as jsonl:
        json_list = list(jsonl)
 
new_json_list=[]      
for i,json_str in enumerate(json_list):
    print(i)
    # run through 1,2,3,4,5 and replace effect type and cert
    for i in range(1,6):
        json_str = json_str.replace(f"EFFECT_TYPE_{i}", "EFFECT_TYPE")
        json_str = json_str.replace(f"EFFECT_CERTAINTY_{i}", "EFFECT_CERTAINTY")
    new_json_list.append(json_str)

with open(outputfile, 'w') as outfile:
    for i,item in enumerate(new_json_list):
        print(i)
        item= json.loads(item)
        json.dump(item, outfile)
        outfile.write('\n')