import unittest

class Separation:
	def __init__( self, tagCount, relationshipList ):
		self.distanceMatrix = [ [ None for _ in range( tagCount ) ] for _ in range( tagCount ) ]
		nameToId = dict()
		nextId = 0

		for A, B in relationshipList:
			id1 = id2 = None
			if A not in nameToId:
				nameToId[ A ] = nextId
				nextId += 1
			if B not in nameToId:
				nameToId[ B ] = nextId
				nextId += 1
			id1, id2 = nameToId[ A ], nameToId[ B ]
			self.distanceMatrix[ id1 ][ id2 ] = self.distanceMatrix[ id2 ][ id1 ] = 1
		assert nextId <= tagCount

		for i in range( tagCount ):
			self.distanceMatrix[ i ][ i ] = 0

	def separation( self ):
		tagCount = len( self.distanceMatrix )
		for k in range( tagCount ):
			for i in range( tagCount ):
				for j in range( i + 1, tagCount ):
					A, B = self.distanceMatrix[ i ][ k ], self.distanceMatrix[ k ][ j ]
					if A is None or B is None:
						continue
					d = A + B
					currentDistance = self.distanceMatrix[ i ][ j ]
					if currentDistance is None or d < currentDistance:
						self.distanceMatrix[ i ][ j ] = self.distanceMatrix[ j ][ i ] = d

		maximumSeparation = None
		for i in range( tagCount ):
			for j in range( i, tagCount ):
				d = self.distanceMatrix[ i ][ j ]
				if d is None:
					return None
				if maximumSeparation is None or d > maximumSeparation:
					maximumSeparation = d
		return maximumSeparation

class SeparationTest( unittest.TestCase ):
	def test_separation( self ):
		for datafile in ('separation1', 'separation2', 'separation3'):
			self._verify( datafile )

	def _verify( self, datafile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if len( line ) == 0:
					continue
				_, _, solution = line.split()
				solutionList.append( None if 'DISCONNECTED' in solution else int( solution ) )

		index = 0
		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			while True:
				tagCount, relationshipCount = map( int, inputFile.readline().strip().split() )
				if relationshipCount == 0:
					break
				relationshipList = list()
				for _ in range( relationshipCount ):
					relationshipList.append( tuple( inputFile.readline().strip().split() ) )

				expectedSolution = solutionList[ index ]
				formatString = 'Testcase {} #{} Number of relationships = {} Degrees of separation = {}'
				print( formatString.format( datafile, index + 1, len( relationshipList ), expectedSolution) )
				
				self.assertEqual( Separation( tagCount, relationshipList ).separation(), expectedSolution )
				
				index += 1

if __name__ == '__main__':
	unittest.main()