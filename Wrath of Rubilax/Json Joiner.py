#!/usr/bin/python
from PIL import Image
import os, sys, json
import itertools
from collections import OrderedDict

listMerge = lambda *args: list(itertools.chain(*args))
uniqueify = lambda l: list(set(l))


path = ".\\Components"
Outputpath = ".\\Uploadable\\"
def generatepathlist(BasePath):
    filenames = []
    for (path, dir, files) in os.walk(BasePath):
        print(files)
        filenames.extend([path[len(BasePath):] + '\\' + f for f in files if f.endswith(".json")])# [] if no file
    return filenames
dirs = generatepathlist( path )
print(dirs)
indexVers = True
# indexVers = False

meta = {
        "sources": [{
            "json": "WOR",
            "abbreviation": "WOR",
            "full": "Wrath of Rubilax - Online",
            "authors": [
                "The prettiest girl at the party AKA Connor"
            ],
            "version": "1.0.0",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
            "color": "c2b280"
        }],
        "dateAdded": 1620498967,
        "dateLastModified": 1620498967
    }

def joinToolsData(dirs, path):
    keys = ['class', 'classFeature', 'subclass', 'subclassFeature']
    files = []
    outputData = OrderedDict()
    outputData['_meta'] = {}
    for key in keys:
        outputData[key] = []
    for item in dirs:
        # print(path+'\\'+item)

        if os.path.isfile(path+'\\'+item):
            with open(path+'\\'+item) as toolsFiles:
                print(1)
                print(toolsFiles)
                test = json.load(toolsFiles)
                print(2)
                if "tested" in test["_meta"]:
                    files.append(test)
                    keys.extend(test.keys())
        #     # im = Image.open(path+item)
        #     # f, e = os.path.splitext(path+item)
        #     # d = f.split('\\')
        #     # g = d[:-1]
        #     # g.extend(['Resized', d[-1]])
        #     # # print(g)
        #     # f = '\\'.join(g)
        #     # # print(f)
        #     # imResize = im.resize((400,400), Image.ANTIALIAS)
        #     # imResize.save(f + '.png', 'PNG', quality=90)

        else:
            # print(path+item)
            print(path+'\\'+item)
    keys = list(set(keys))
    print(keys)
    for key in keys:
        outputData[key] = []
        for file in files:
            if key in file:
                outputData[key].extend(file[key])
    return outputData



print(dirs)

data = joinToolsData(dirs, path)
data['_meta'] = meta
print(data)
print(data.keys())


def IndexVersionNumber(data):
    global d, f
    if os.path.isfile(Outputpath + 'WrathOfRubilax.json'):
        with open(Outputpath + 'WrathOfRubilax.json', 'r', encoding='utf-8') as json_file:
            # print(Outputpath+'WrathOfRubilax.json')
            # print(json_file)
            d = json.load(json_file)
    f = d["_meta"]["sources"][0]["version"].split(".")
    f[2] = str(1 + int(f[2]))
    # "Json Joiner.py"
    # ""
    print(".".join(f))
    data["_meta"]["sources"][0]["version"] = ".".join(f)
    return data


if indexVers:
    data = IndexVersionNumber(data)
# print(data)
with open(Outputpath+'WrathOfRubilax.json', 'w', encoding='utf-8') as f:
# with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
