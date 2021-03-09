import unittest
import math

class EndOfProgram( Exception ):
	pass

class InfiniteLoop( Exception ):
	pass

class RegisterBank:
	def __init__( self, numberOfRegisters=10, int_max=1000 ):
		self.registerBank = [ 0 for _ in range( numberOfRegisters ) ]
		self.numberOfRegisters = numberOfRegisters
		self.int_max = int_max

	def _registerNameToIndex( self, registerName ):
		prefix, * rest = registerName
		index = int( ''.join( rest ) )
		assert prefix == 'R' and 0 <= index < self.numberOfRegisters
		return index

	def readRegister( self, registerName ):	
		return self.registerBank[ self._registerNameToIndex( registerName ) ]

	def writeRegister( self, registerName, value ):
		value = value % self.int_max
		self.registerBank[ self._registerNameToIndex( registerName ) ] = value

	def __repr__( self ):
		return '#'.join( map( str, self.registerBank ) )

class BabelVM:
	def __init__( self, program, N ):
		self.stack = list()
		self.pc = 0
		
		self.currentRegisterBank = None

		self.program = program
		self.argument = N

		self.basicCommands = set( [ 'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD' ] )
		self.decisionFlowCommands = set( [ 'IFEQ', 'IFNEQ', 'IFG', 'IFL', 'IFGE', 'IFLE' ] )
		self.callCommand = 'CALL'
		self.returnCommand = 'RET'
		self.endIfCommand = 'ENDIF'

		self.jumpTable = dict()
		self._populateJumpTable()

		self.stateCache = set()
		self.functionCallCache = dict()

	def _populateJumpTable( self ):
		stack = list()

		for i in range( len( self.program ) ):
			instruction = self.program[ i ]
			command, * _ = instruction.split()

			if command in self.decisionFlowCommands:
				stack.append( i )
			elif command == self.endIfCommand:
				assert len( stack ) > 0
				self.jumpTable[ stack.pop() ] = i
		assert len( stack ) == 0

	def _readRegister( self, registerName ):
		return self.currentRegisterBank.readRegister( registerName )

	def _readRegisterOrLiteral( self, token ):
		prefix, * rest = token
		return self._readRegister( token ) if prefix == 'R' else int( token )

	def _writeRegister( self, registerName, value ):
		self.currentRegisterBank.writeRegister( registerName, value )

	def execute( self ):
		self._executeCall( self.argument )
		
		while True:
			try:
				self._executeInstruction()
			except InfiniteLoop:
				result = '*'
				break
			except EndOfProgram:
				result = self.currentRegisterBank.readRegister( 'R9' )
				break
		return result

	def _executeCall( self, N ):
		if N in self.functionCallCache:
			self.currentRegisterBank.writeRegister( 'R9', self.functionCallCache[ N ] )
			self.pc += 1
			return

		if self.currentRegisterBank is not None:
			state = repr( self.currentRegisterBank )
			if state in self.stateCache:
				raise InfiniteLoop()
			self.stateCache.add( state )

			self.stack.append( (self.pc, N, self.currentRegisterBank ) )
		self.currentRegisterBank = RegisterBank()

		self.currentRegisterBank.writeRegister( 'R0', N )
		self.pc = 0

	def _executeReturn( self, N ):
		stackSize = len( self.stack )

		if stackSize > 0:
			self.pc, argument, self.currentRegisterBank = self.stack.pop()
			self.stateCache.remove( repr( self.currentRegisterBank ) )

			self.functionCallCache[ argument ] = N

		self.currentRegisterBank.writeRegister( 'R9', N )
		
		if stackSize == 0:
			raise EndOfProgram()

	def _executeInstruction( self ):
		instruction = self.program[ self.pc ]
		tokenList = instruction.split()
		
		if len( tokenList ) == 2:
			command, operand = tokenList
		else:
			assert len( tokenList ) == 1
			command, operand = tokenList.pop(), None

		if command in self.basicCommands:
			registerName, token = operand.split( ',' )
			A, B = self._readRegister( registerName ), self._readRegisterOrLiteral( token )
			
			if command == 'MOV':
				A = B
			elif command == 'ADD':
				A += B
			elif command == 'SUB':
				A -= B
			elif command == 'MUL':
				A *= B
			elif command == 'DIV':
				A = ( A // B ) if B != 0 else 0
			elif command == 'MOD':
				A = ( A % B ) if B != 0 else 0
			self._writeRegister( registerName, A )
		elif command in self.decisionFlowCommands:
			token1, token2 = operand.split( ',' )
			A, B = self._readRegisterOrLiteral( token1 ), self._readRegisterOrLiteral( token2 )

			conditionSatisfied = None
			if command == 'IFEQ':
				conditionSatisfied = ( A == B )
			elif command == 'IFNEQ':
				conditionSatisfied = ( A != B )
			elif command == 'IFG':
				conditionSatisfied = ( A > B )
			elif command == 'IFL':
				conditionSatisfied = ( A < B )
			elif command == 'IFGE':
				conditionSatisfied = ( A >= B )
			elif command == 'IFLE':
				conditionSatisfied = ( A <= B )

			if not conditionSatisfied:
				self.pc = self.jumpTable[ self.pc ]
		elif command == self.endIfCommand:
			pass
		elif command == self.callCommand:
			self._executeCall( self._readRegisterOrLiteral( operand ) )
			return
		elif command == self.returnCommand:
			self._executeReturn( self._readRegisterOrLiteral( operand ) )
		self.pc += 1

class HaltTest( unittest.TestCase ):
	def test_factorial( self ):
		programStringList = [
		'IFEQ R0,0',
		'RET 1',
		'ENDIF',
		'MOV R1,R0',
		'SUB R1,1',
		'CALL R1',
		'MOV R2,R9',
		'MUL R2,R0',
		'RET R2'
		]
		for N in range( 6 ):
			result = BabelVM( programStringList, N ).execute()
			expectedResult = math.factorial( N )
			print( 'Calculating factorial of {}. Expected result = {}'.format( N, expectedResult ) )
			self.assertEqual( result, expectedResult )

	def test_halt( self ):
		for testcaseFile in ('sample', 'halt'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				solution = line.strip()
				solutionList.append( int( solution ) if solution != '*' else solution )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			while True:
				L, N = map( int, inputFile.readline().strip().split() )
				if L == 0 and N == 0:
					break
				programStringList = list()
				for _ in range( L ):
					programStringList.append( inputFile.readline().strip() )

				formatString = 'Testcase {}#{} Program size = {} N = {} Expected result = {}'
				print( formatString.format( testcaseFile, index	+ 1, L, N, solutionList[ index ] ) )

				result = BabelVM( programStringList, N ).execute()
				self.assertEqual( result, solutionList[ index ] )
				index += 1

if __name__ == '__main__':
	unittest.main()