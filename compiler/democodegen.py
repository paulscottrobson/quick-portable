# **********************************************************************************************************
#
#		Name:		assignment.py
#		Purpose:	Assignment code class
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Date:		3rd February 2018
#
# **********************************************************************************************************

from exception import *
from term import *

# **********************************************************************************************************
#
#										Demonstration Code Generator
#
# **********************************************************************************************************

class DemoCodeGenerator(object):
	def __init__(self):
		self.address = 4096
	#
	#		Set operating size (byte or word, 1 or 2)
	#
	def setGenerationSize(self,size):
		self.sizeMode = size
		self.regName = "w" if size == 2 else "b"
	#
	#		Load a constant into the selected register
	#
	def loadConstant(self,const):
		print("{0:04x}\tld{1}  #${2:04x}".format(self.address,self.regName,const))
		self.address += 1
	#
	#		Load a variable into the selected register. May need byte<->word extension/chopping
	#
	def loadVariable(self,srcTerm):
		srcv = "byte" if isinstance(srcTerm,ByteVariableTerm) else "word"
		print("{0:04x}\tld{1}  [{3}:${2:04x}]".format(self.address,self.regName,srcTerm.getAddress(),srcv))		
		self.address += 1		
	#
	#		Store to a variable from the selected register. Note: because the variable size
	#		defines the size when this is used, there is no byte<->word conversion.
	#
	def storeVariable(self,tgtTerm):
		print("{0:04x}\tst{1}  [${2:04x}]".format(self.address,self.regName,tgtTerm.getAddress()))		
		self.address += 1
	#
	#		Load the address of an array element into the index register. The array element
	#	 	can be a numeric constant or a variable
	#
	def loadArrayElementAddress(self,array,index):
		if isinstance(index,NumericConstantTerm):
			eAddr = array.getAddress()+index.getValue()
			print("{0:04x}\tldx  #${1:04x}".format(self.address,eAddr))
			self.address += 1
		elif isinstance(index,VariableTerm):
			print("{0:04x}\tldx  #${1:04x}".format(self.address,array.getAddress()))
			typeName = "word" if isinstance(index,WordVariableTerm) else "byte"
			print("{0:04x}\tadx  [{1}:{2:04x}]".format(self.address+1,typeName,index.getAddress()))
			self.address += 2
		else:
			assert false			
	#
	#		Load byte value pointed to by index register into selected register.
	#
	def loadViaIndex(self):
		print("{0:04x}\tld{1}  [byte:x]".format(self.address,self.regName))		
		self.address += 1		
	#
	#		Store to given array element. This is done here incase you want to use the 
	#		same register for the value as you do for the result address - for example
	#		HL on a Z80. As with store variable, there is no byte<->word conversion.
	#
	def storeArrayElement(self,tgtTerm):
		# but here, we load the address into the index register
		self.loadArrayElementAddress(tgtTerm.getArray(),tgtTerm.getElement())
		# and store indirect via that.
		print("{0:04x}\tst{1}  [{2}:x]".format(self.address,self.regName,"byte" if self.sizeMode == 1 else "word"))		
		self.address += 1		

	#
	#		Code to copy memory from a given address, target address is in the index register
	#
	def copyMemory(self,srcAddress,copySize):
		print("{0:04x}\tcopy ${1:04x},${2:04x}".format(self.address,srcAddress,copySize))
		self.address += 1
	#
	#		Copy a string and terminating zero to the given address in memory.
	#
	def copyStringToArray(self,stringValue,address):
		print("{0:04x}\tlstr [${1:04x}],'{2}'".format(self.address,address,stringValue))
		self.address += 1
