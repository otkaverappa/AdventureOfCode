import unittest

class ShiftingPaths:
	def __init__( self, numberOfClearings, edgeList ):
		self.numberOfClearings = numberOfClearings
		self.edgeList = edgeList

	def pathLength( self ):
		currentClearing = 1
		_pathLength = 0

		visited = set()
		turnStateBitmap = 0 # bit 0 at position i represents that the next turn to be taken at clearing i is "left". 

		while True:
			if currentClearing == self.numberOfClearings:
				return _pathLength
			index = currentClearing - 1

			leftClearing, rightClearing = self.edgeList[ index ]
			nextClearingToVisit = leftClearing if ( turnStateBitmap & ( 1 << index ) ) == 0 else rightClearing
			turnStateBitmap ^= ( 1 << index )

			_pathLength += 1

			state = (currentClearing, turnStateBitmap)
			if state in visited:
				return None
			visited.add( state )
			currentClearing = nextClearingToVisit

class ShiftingPathsTest( unittest.TestCase ):
	def test_pathLength( self ):
		solutionList = list()
		with open( 'tests/small.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( line.strip() )

		i = 0
		with open( 'tests/small.in' ) as inputFile:
			T = int( inputFile.readline().strip() )
			for _ in range( T ):
				numberOfClearings = int( inputFile.readline().strip() )

				edgeList = list()
				for _ in range( numberOfClearings - 1 ):
					left, right = map( int, inputFile.readline().strip().split() )
					edgeList.append( (left, right) )

				pathLength = ShiftingPaths( numberOfClearings, edgeList ).pathLength()
				print( 'Testcase {} Expected solution = {}'.format( i + 1, solutionList[ i ] ) )

				solutionString = 'Case #{}: {}'.format( i + 1, int( pathLength ) if pathLength is not None else 'Infinity' )
				self.assertEqual( solutionString, solutionList[ i ]  )
				i += 1

if __name__ == '__main__':
	unittest.main()