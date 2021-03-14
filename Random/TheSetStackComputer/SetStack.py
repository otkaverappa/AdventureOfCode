import unittest
import copy

class SetStack:
	def __init__( self ):
		self.stack = list()
		self.setRepresentationToIdDict = dict()
		self.nextIdToAllocate = 0

	@staticmethod
	def setRepresentation( inputSet ):
		return '#'.join( map( str, sorted( inputSet ) ) )

	def _getSetFromCache( self, inputSet ):
		setRepresentation = SetStack.setRepresentation( inputSet )
		if setRepresentation not in self.setRepresentationToIdDict:
			self.setRepresentationToIdDict[ setRepresentation ] = self.nextIdToAllocate
			self.nextIdToAllocate += 1
		return self.setRepresentationToIdDict[ setRepresentation ]

	def _applyCommand( self, command ):
		if command == 'PUSH':
			self.stack.append( set() )
		elif command == 'DUP':
			topSet = self.stack[ -1 ]
			self.stack.append( copy.deepcopy( topSet ) )
		elif command == 'UNION':
			A, B = self.stack.pop(), self.stack.pop()
			self.stack.append( set.union( A, B ) )
		elif command == 'INTERSECT':
			A, B = self.stack.pop(), self.stack.pop()
			self.stack.append( set.intersection( A, B ) )
		elif command == 'ADD':
			topSet = self.stack.pop()
			id_ = self._getSetFromCache( topSet )
			self.stack[ -1 ].add( id_ )
		return len( self.stack[ -1 ] )

	def apply( self, commandList ):
		return list( map( self._applyCommand, commandList ) )

class SetStackTest( unittest.TestCase ):
	def r( self ):
		commandList = [ 'PUSH', 'DUP', 'ADD', 'PUSH', 'ADD', 'DUP', 'ADD', 'DUP', 'UNION' ]
		expectedResult = [ 0, 0, 1, 0, 1, 1, 2, 2, 2 ]
		self.assertEqual( SetStack().apply( commandList ), expectedResult )

		commandList = [ 'PUSH', 'PUSH', 'ADD', 'PUSH', 'INTERSECT' ]
		expectedResult = [ 0, 0, 1, 0, 0 ]
		self.assertEqual( SetStack().apply( commandList ), expectedResult )

	def test_setStack( self ):
		for testcaseFile in ('stack1', 'stack2'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			currentSolutionList = list()
			for line in solutionFile.readlines():
				line = line.strip()
				if line == '***':
					solutionList.append( currentSolutionList )
					currentSolutionList = list()
				else:
					currentSolutionList.append( int( line ) )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			N = int( inputFile.readline().strip() )
			assert N == len( solutionList )
			for _ in range( N ):
				commandList = list()
				numberOfCommands = int( inputFile.readline().strip() )
				for _ in range( numberOfCommands ):
					commandList.append( inputFile.readline().strip() )

				expectedSolution = solutionList[ index ]
				index += 1

				formatString = 'Testcase {}#{} Number of commands = {}'
				print( formatString.format( testcaseFile, index, numberOfCommands ) )

				self.assertEqual( SetStack().apply( commandList ), expectedSolution )

if __name__ == '__main__':
	unittest.main()