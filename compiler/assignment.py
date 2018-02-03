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
from democodegen import *

# **********************************************************************************************************
#
#								   Generate Assignment Class Code
#
# **********************************************************************************************************

class AssignmentGenerator(object):
	def __init__(self,codeGenerator):
		self.codeGen = codeGenerator
		self.termZero = NumericConstantTerm(0)

	# ************************************************************************************************
	#									Main Generation Routine
	# ************************************************************************************************

	def generate(self,srcTerm,tgtTerm,forceWordArrayElement = False):
		print(srcTerm.toString() +" ==>> "+tgtTerm.toString())
		# check for special cases - arrays, strings and so on.
		if self.specialCases(srcTerm,tgtTerm):
			return
		# check the source which should be numeric constant,array element or variable.
		srcOk = isinstance(srcTerm,NumericConstantTerm) or \
						isinstance(srcTerm,ArrayElementTerm) or isinstance(srcTerm,VariableTerm)
		if not srcOk:
			raise CompilerException("Bad source term in assignment")
		# check the target which should be array element or variable.
		tgtOk = isinstance(tgtTerm,VariableTerm) or isinstance(tgtTerm,ArrayElementTerm)
		if not tgtOk:
			raise CompilerException("Bad target term in assignment")
		# work out the variable size from where it is going.
		if isinstance(tgtTerm,VariableTerm):
			varSize = 2 if isinstance(tgtTerm,WordVariableTerm) else 1
		else:
			varSize = 2 if forceWordArrayElement else 1
		# tell the code generator.
		self.codeGen.setGenerationSize(varSize)
		self.varSize = varSize
		# load the value in
		self.loadCode(srcTerm)
		# write the value out
		self.storeCode(tgtTerm)

	# ************************************************************************************************
	#									 Load in the value
	# ************************************************************************************************

	def loadCode(self,srcTerm):
		#
		#	Load in a numeric constant
		#
		if isinstance(srcTerm,NumericConstantTerm):
			# calculate the value, putting it in range.
			const = srcTerm.getValue() & (255 if self.varSize == 1 else 65535)
			self.codeGen.loadConstant(const)
		#
		#	Load in a variable, byte or word.
		#
		elif isinstance(srcTerm,VariableTerm):
			self.codeGen.loadVariable(srcTerm)
		#
		#	Load in an array element, always a byte.
		#
		elif isinstance(srcTerm,ArrayElementTerm):
			# Load index register with address of array element.
			self.codeGen.loadArrayElementAddress(srcTerm.getArray(),srcTerm.getElement())
			# Load into working register
			self.codeGen.loadViaIndex()
		else:
			assert False

	# ************************************************************************************************
	#									Store out the value
	# ************************************************************************************************

	def storeCode(self,tgtTerm):
		#
		#	Store to a variable, byte or word.
		#
		if isinstance(tgtTerm,VariableTerm):
			self.codeGen.storeVariable(tgtTerm)
		#
		#	Array element term
		#
		elif isinstance(tgtTerm,ArrayElementTerm):
			self.codeGen.storeArrayElement(tgtTerm)
		else:
			assert False

	# ************************************************************************************************
	#									Process special cases
	# ************************************************************************************************

	def specialCases(self,srcTerm,tgtTerm):
		processed = False
		#
		# 	copying a string constant to an array.
		#
		if isinstance(srcTerm,StringConstantTerm) and isinstance(tgtTerm,ArrayTerm):
			# get string truncate if required, i.e. it won't fit in the array.
			strCopy = srcTerm.getValue()
			if len(strCopy) > tgtTerm.getSize()-1:
				strCopy = strCopy[:tgtTerm.getSize()-1]
			# and copy it.
			self.codeGen.copyStringToArray(strCopy,tgtTerm.getAddress())
			processed = True
		#
		#	copying one array to another.
		#
		elif isinstance(srcTerm,ArrayTerm) and isinstance(tgtTerm,ArrayTerm):
			# this is the target - element zero.
			self.codeGen.loadArrayElementAddress(tgtTerm,self.termZero)
			# bytes to copy
			bCount = min(srcTerm.getSize(),tgtTerm.getSize())
			# copy bytes
			self.codeGen.copyMemory(srcTerm.getAddress(),bCount)
			processed = True
		#
		#	copy array to array element
		#
		elif isinstance(srcTerm,ArrayTerm) and isinstance(tgtTerm,ArrayElementTerm):
			# this is the target - the address of the element.
			self.codeGen.loadArrayElementAddress(tgtTerm.getArray(),tgtTerm.getElement())
			# copy bytes, but no check
			self.codeGen.copyMemory(srcTerm.getAddress(),srcTerm.getSize())
			processed = True

		return processed


if __name__ == '__main__':
	ag = AssignmentGenerator(DemoCodeGenerator())
	sc = StringConstantTerm("hello")
	nc = NumericConstantTerm(42)
	bv = ByteVariableTerm("bv",0x2000)
	wv = WordVariableTerm("wv",0x2001)
	ar = ArrayTerm("arr1",0x8000,32)
	ar2 = ArrayTerm("arr2",0x8100,16)
	ean1 = ArrayElementTerm(ar2,NumericConstantTerm(3))
	eab1 = ArrayElementTerm(ar2,bv)
	eaw1 = ArrayElementTerm(ar2,wv)
	print("===========================================================================")
	ag.generate(sc,ar)
	print("===========================================================================")
	ag.generate(ar,ar2)
	print("===========================================================================")
	ag.generate(ar,ean1)
	print("===========================================================================")
	ag.generate(ar,eab1)	
	print("===========================================================================")
	ag.generate(ar,eaw1)		
	print("===========================================================================")
	ag.generate(nc,bv)
	print("===========================================================================")
	ag.generate(nc,wv)	
	print("===========================================================================")
	ag.generate(bv,bv)
	print("===========================================================================")
	ag.generate(bv,wv)		
	print("===========================================================================")
	ag.generate(wv,bv)
	print("===========================================================================")
	ag.generate(wv,wv)			
	print("===========================================================================")
	ag.generate(ean1,bv)
	print("===========================================================================")
	ag.generate(eab1,wv)				
	print("===========================================================================")
	ag.generate(bv,ean1)
	print("===========================================================================")
	ag.generate(wv,eab1)					
	print("===========================================================================")
	ag.generate(bv,ean1,True)
	print("===========================================================================")
	ag.generate(ean1,eab1)

# Optimise for array[const] as both source and target

