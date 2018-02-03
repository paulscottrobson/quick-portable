# **********************************************************************************************************
#
#		Name:		term.py
#		Purpose:	Term classes
#		Author:		Paul Robson (paul@robsons.org.uk)
#		Date:		3rd February 2018
#
# **********************************************************************************************************

from exception import *

class Term(object):
	pass

# **********************************************************************************************************
#											Constant classes
# **********************************************************************************************************

class ConstantTerm(Term):
	def __init__(self,value):
		self.value = value 
	def getValue(self):
		return self.value

class NumericConstantTerm(ConstantTerm):
	def toString(self):
		return "NumConst:{0}".format(self.value)

class StringConstantTerm(ConstantTerm):
	def toString(self):
		return "StrConst:'{0}'".format(self.value)

# **********************************************************************************************************
#											Variable Classes
# **********************************************************************************************************

class VariableTerm(Term):
	def __init__(self,name,address):
		self.name = name.lower().strip()
		self.address = address
	def getName(self):
		return self.name
	def getAddress(self):
		return self.address

class ByteVariableTerm(VariableTerm):
	def toString(self):
		return "ByteVar:{0} at ${1:04x}".format(self.name,self.address)

class WordVariableTerm(VariableTerm):
	def toString(self):
		return "WordVar:{0} at ${1:04x}".format(self.name,self.address)

# **********************************************************************************************************
#											Array Classes
# **********************************************************************************************************

class ArrayTerm(Term):
	def __init__(self,name,address,size):
		self.name = name.lower().strip()
		self.address = address
		self.size = size
	def getName(self):
		return self.name 
	def getAddress(self):
		return self.address
	def getSize(self):
		return self.size 
	def toString(self):
		return "Array:{2} (${0:04x} length {1})".format(self.address,self.size,self.name)

class ArrayElementTerm(Term):
	def __init__(self,array,element):
		assert isinstance(array,ArrayTerm)
		assert isinstance(element,NumericConstantTerm) or isinstance(element,VariableTerm)		
		self.array = array
		self.element = element 
	def getArray(self):
		return self.array
	def getElement(self):
		return self.element 
	def toString(self):
		return "ArrayElem:{0}[{1}]".format(self.array.getName(),self.element.toString())

if __name__ == '__main__':
	nc = NumericConstantTerm(42)
	print(nc.getValue())
	print(nc.toString())
	print()

	sc = StringConstantTerm("hello, world!")
	print(sc.getValue())
	print(sc.toString())
	print()

	bv = ByteVariableTerm("bv",257)
	print(bv.getName(),bv.getAddress())
	print(bv.toString())
	print()

	wv = WordVariableTerm("wv",258)
	print(wv.getName(),wv.getAddress())
	print(wv.toString())	
	print()

	ar = ArrayTerm("ar",4097,128)
	print(ar.getAddress(),ar.getSize())
	print(ar.toString())
	print()

	bat = ArrayElementTerm(ar,bv)
	print(bat.toString())
	print()

	wat = ArrayElementTerm(ar,wv)
	print(wat.toString())
	print()

	cat = ArrayElementTerm(ar,nc)
	print(cat.toString())
	print()
