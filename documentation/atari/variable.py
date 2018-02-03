# ********************************************************************************
# ********************************************************************************
#
#		File : 		variables.py
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Date:		22nd Dec 2017
#		Purpose:	Variable objects and variable management
#
# ********************************************************************************
# ********************************************************************************

# ********************************************************************************
#
#								Base Variable Class
#
# ********************************************************************************

class Variable:
	def __init__(self,name,address,isLocal):
		self.name = name.strip().lower()
		self.address = address
		self.isLocal = isLocal
	#
	#	Accessors/Mutators
	#
	def getName(self):
		return self.name
	def getAddress(self):
		return self.address
	def isLocal:
		return self.isLocal

# ********************************************************************************
#
#									Subclasses
#
# ********************************************************************************

class ByteVariable(Variable):
	#
	#	Accessors/Mutators
	#
	def getElementSize(self):
		return 1

class WordVariable(Variable):
	#
	#	Accessors/Mutators
	#
	def getElementSize(self):
		return 2

class ByteArray(ByteVariable):
	#
	#	Accessors/Mutators
	#
	def __init__(self,name,address,isLocal,length):
		Variable.__init__(self,name,address,isLocal)
		self.length = length
	def getLength(self):
		return self.length
		