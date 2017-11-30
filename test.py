required = ['key3','key4','key5']
d = {'key1':'asd','key2':'asd'}
error = {"invalid_fields":[]}

for key in d.keys():
    if key not in required:
        error["invalid_fields"].append({"field": key,"reason": key+" is a required property"})

print (error)
