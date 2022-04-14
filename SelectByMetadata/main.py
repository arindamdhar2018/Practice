import nuke 
import os 
import re 

from rawImageTools.helpers import deselectAllNodes 

def selectByMetadata(searchString):
	"""
	Defines dictionaries of metadata for all BackdropNodes in Nuke then scans the metadata for matching criteria to the specified search string. 

	Args: 
		searchString (str): String to use as search criteria 
	"""

	# Define list of backdrop nodes 
	backdrops = {} 
	for bdNode in nuke.selectedNodes('BackdropNode') or nuke.allNodes('BackdropNode'): 

		# Define Node 
		name = bdNode.name() 
		label = bdNode.knob('label').value() 
		backdrops[name] = {'node': bdNode} 

		# Define nodes in backdrop 
		deselectAllNodes() 
		bdNode.selectNodes()
		backdrops[name]['kids'] = nuke.selectedNodes() 

		# Define primary Read Node 
		primeReadNode = None
		for readNode in nuke.selectedNodes('Read'): 
			fileInput = readNode.knob('file').value()
			fileName = os.path.splitext(os.path.basename(fileInput))[0]
			if fileName == label: 
				primeReadNode = readNode
				
		# Flatten metadata 
		backdrops[name]['metadata'] = []
		if primeReadNode is None: 
			continue 

		# Define primary Read Node 
		primeReadNode = None 
		for readNode in nuke.selectedNodes('Read'): 
			fileInput = readNode.knob('file').value()
			fileName = os.path.splitext(os.path.basename(fileInput))[0]
			if fileName == label: 		
				primeReadNode = readNode 

		# Flatten metadata 
		backdrops[name]['metadata'] = []
		if primeReadNode is None: 
			continue 
		else: 
			for field in primeReadNode.metadata().items():
				backdrops[name]['metadata'].append('{0} {1}'.format(*field))
				
	# Define list of backdrop nodes that match the search criteria 
	matchingBackdrops = []		
	for name in backdrops.keys():
		for metaField in backdrops[name]['metadata']:
			if re.findall(searchString, metaField, re.IGNORECASE): 
				matchingBackdrops.append(name) 
				continue 

	# Select Matching backdrops 
	deselectAllNodes()
	for name in matchingBackdrops:
		for node in backdrops[name]['kids']: 
			node.knob('selected').setValue(True) 
		backdrops[name]['node'].knob('selected').setValue(True) 

def main(): 
""" Launch a Nuke panel, then cal l selectByMetadata wi th using the user defined search string. 
""" 
	panel = nuke.Panel('Select by Metadata') 
	panel.addSingleLineInput('Search:', ") 
	search = panel.show()
	if search:	
		searchString = panel.value('Search:') 
		selectByMetadata(searchString.replace('*','.+')) 


