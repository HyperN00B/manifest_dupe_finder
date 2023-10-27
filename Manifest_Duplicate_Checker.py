import os
import sys
import time

vCurrentPath=os.getcwd()
vManifestsFound=[]
vHasSubfolder=False
vCurrentPathList=vCurrentPath.split("/")

def mReadFolderContent(miPath): # Reads the xml files in the main and subfolder and appends them into a list which gets returned
	if not vCurrentPathList[len(vCurrentPathList)-1]=="manifests" and ".git" in os.listdir(miPath):
		os.system("clear")
		print("This script must be run inside a freshly inited \".repo/manifests/\" folder!")
		time.sleep(3)
		sys.exit()
	for index,content in enumerate(os.listdir(miPath)):
		if os.path.isdir(content) and content != ".git":
			vHasSubfolder=True
			vSubfolderName=content
		elif content.endswith(".xml"):
			vManifestsFound.append(miPath+"/"+content)
		else:
			continue
		pass
	pass
	if vHasSubfolder:
		for index,content in enumerate(os.listdir(miPath+"/"+vSubfolderName)):
			vManifestsFound.append(miPath+"/"+vSubfolderName+"/"+content)
		pass
	pass
	return vManifestsFound
pass

def mRemovePaths(miXmlList): # Since the reading method returns a full path and we'll need only the xml filenames for later proccessing, remove the paths
	mvXmlFiles=[]
	for index,content in enumerate(miXmlList):
		content=content.split("/")
		content=content[len(content)-1][:-4]
		mvXmlFiles.append(content)
	pass
	return mvXmlFiles
pass

def mReadProjectsFromManifest(miXmlFiles):
	mvAllProjectLines=[]
	mvProjectPaths=[]
	for index,content in enumerate(miXmlFiles):
		mvFileContent=open(content,"r").readlines()
		for index,content in enumerate(mvFileContent):
			if "project" in content:
				mvAllProjectLines.append(content)
			pass
		pass
	pass
	for index,content in enumerate(mvAllProjectLines):
		if not "<!--" in content:
			content=content.split(" ")
			for index,content in enumerate(content):
				if "path" in content:
					mvProjectPaths.append(content[6:-1])
				pass
			pass
		pass
	pass
	mvProjectPaths.sort()
	return mvProjectPaths
pass

def mFindDupes(miProjectsList):
	mvDupesList=[]
	for index,content in enumerate(miProjectsList):
		if miProjectsList.count(content) > 1:
			mvDupesList.append(content)
		pass
	pass
	del mvDupesList[::2]
	return mvDupesList
pass

vAbsoluteXMLs=mReadFolderContent(vCurrentPath) # List
vRelativeXMLs=mRemovePaths(vAbsoluteXMLs) # List
vProjectsFound=mReadProjectsFromManifest(vAbsoluteXMLs) # List
for index,content in enumerate(mFindDupes(vProjectsFound)):
	print(content)
pass