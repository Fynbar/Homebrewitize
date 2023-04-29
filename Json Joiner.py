#!/usr/bin/python
# from PIL import Image
import os, sys, json
import itertools
from collections import OrderedDict
from os import listdir
from os.path import isfile, join
from datetime import timezone
import datetime

indexVers = True
# indexVers = False

listMerge = lambda *args: list(itertools.chain(*args))
uniqueify = lambda l: list(set(l))
getUTC = lambda: datetime.datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()//1

def generatepathlist(BasePath):
    filenames = []
    for (path, dir, files) in os.walk(BasePath):
        print(path, dir, files)
        filenames.extend([path[len(BasePath):] + '\\' + f for f in files if f.endswith(".json")])# [] if no file
    return filenames
# dirs = generatepathlist( path )
# print(dirs)

def IndexVersionNumber(data, outputFile):
    # global d, f
    print(".",end="") #1
    if os.path.isfile(outputFile):
        with open(outputFile, 'r', encoding='utf-8') as json_file:
            # print(Outputpath+'WrathOfRubilax.json')
            # print(json_file)
            print(".",end="") #2
            d = json.load(json_file)
    for i,t in enumerate(d["_meta"]["sources"]):
        f = t["version"].split(".")
        f[2] = str(1 + int(f[2]))

    # "Json Joiner.py"
    # ""
        data["_meta"]["sources"][i]["version"] = ".".join(f)
    print(".",end="")
    data["_meta"]["dateLastModified"] = getUTC()
    return data

# print(data)
def joinToolsData(dirs, path):
    # Set up order for properties in final file
    keys = ['class', 'classFeature', 'subclass', 'subclassFeature']
    files = []
    outputData = OrderedDict()
    outputData['_meta'] = {}
    
    # Inputting keys into output 
    for key in keys:
        outputData[key] = []
    
    # For each filename that was found...
    for item in dirs:
        print(path+item)

        # If there actually is a file...
        if os.path.isfile(path+item):
            # Open that file as a dictionary
            with open(path+item, 'r', encoding='utf-8') as toolsFiles:
                """# print(1)
                # print(toolsFiles)
                # print('a')
                # print(2)"""
                test = json.load(toolsFiles)

                # Add it to the final file if it's been tested
                if "_meta" in test:
                    if "tested" in test["_meta"]:
                        files.append(test)
                        keys.extend(test.keys())
                else:
                    # If the file doesn't have a meta field, then it adds one.
                    with open(path+item, 'w', encoding='utf-8') as f:
                        test["_meta"] = {}
                        json.dump(test, f, ensure_ascii=False, indent=4)
                    
        
        else:
            print(path+item)
            # print(path+'\\'+item)
    keys = list(set(keys))
    # print(keys)
    for key in keys:
        outputData[key] = []
        for file in files:
            if key in file:
                outputData[key].extend(file[key])
    # print(outputData)
    return outputData

def cleanData(data):
    # Remove the empty lists in the file
    listKeys = [key for key in data.keys() if isinstance(data[key], list)]
    [data.pop(key) for key in listKeys if len(data[key]) == 0]   

def rewriteJSON(data, outputFile, indexVers = False):
    if indexVers:
        print("Indexing",end="")
        data = IndexVersionNumber(data, outputFile)
    
    with open(outputFile, 'w', encoding='utf-8') as f:
    # with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def getPathFiles(i = -1):
    subfolders = [f for f in os.scandir() if f.is_dir() and os.path.isfile(f.path+'\\meta.json')]
    [print(n+1, subfolder.name) for (n, subfolder) in enumerate(subfolders)]
    print()
    # if True:
    k = []
    if i < 0:
        try:
            selectedNum = input("Select File Number: ")
            selectedSubfolder = subfolders[int(selectedNum)-1].path
            print()
        except:
            print("You blew it")
            selectedNum = 0
            selectedSubfolder = subfolders[selectedNum].path
    else:
        try:
            selectedNum = i
            selectedSubfolder = subfolders[int(selectedNum)-1].path
            print()
        except:
            print("You blew it")
            selectedNum = 0
            selectedSubfolder = subfolders[selectedNum].path
    
    with open(selectedSubfolder+'\\meta.json', 'r', encoding='utf-8') as toolsFiles:
        k.append({"meta":json.load(toolsFiles), "project":selectedSubfolder})
    return k
# print()
def updateOutputFile(meta, project):
    # Create Path and Output path
    outputPath = project+"\\Uploadable"
    path = project+"\\Components"
    # print(listdir(outputPath))
    outputFiles = [f for f in listdir(outputPath) if isfile(join(outputPath, f))]
    if len(outputFiles) > 0:
        outputFile = outputPath+'\\'+outputFiles[0]
    else:
        pass
        # print(outputFile)

    # Create File names from path
    dirs = generatepathlist( path )
    # print('Filenames',dirs)

    print(dirs)

    data = joinToolsData(dirs, path)
    data['_meta'] = meta
    cleanData(data)
    # print(data)
    # print(data.keys())

    rewriteJSON(data, outputFile, indexVers)

    # Figure out how to create
metaData = getPathFiles()
for mD in metaData:
    updateOutputFile(**mD)