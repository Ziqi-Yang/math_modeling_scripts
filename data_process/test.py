import json
import yaml

a = {"a":[{"a":123},[3,4,5],{"a":1}],"b":[4,5,6],"c":9}

# with open("aaa.yaml","w") as f:
#     # json.dump(a,f,indent=4,ensure_ascii=False,sort_keys=False)
#     yaml.dump(a,f,indent=2)
with open("tmpConfig.yaml") as f:
    print(yaml.load(f,Loader=yaml.FullLoader))
