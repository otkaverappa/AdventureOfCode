import unittest
import heapq
import itertools

class TheCube:
	def __init__( self, rows, cols, labyrinth ):
		self.openMarker, self.wallMarker, self.targetMarker, self.boxMarker, self.startMarker = '.#TBS'
		
		self.targetLocation = self.boxLocation = self.startLocation = None
		self.rows, self.cols = rows, cols
		self.labyrinth = labyrinth

		for row, col in itertools.product( range( rows ), range( cols ) ):
			marker = self.labyrinth[ row ][ col ]
			if marker == self.targetMarker:
				self.targetLocation = (row, col)
			elif marker == self.boxMarker:
				self.boxLocation = (row, col)
			elif marker == self.startMarker:
				self.startLocation = (row, col)

		assert all( [ self.targetLocation, self.boxLocation, self.startLocation ] )

	def _isOutside( self, row, col ):
		return not 0 <= row < self.rows or not 0 <= col < self.cols

	def minimumPush( self ):
		startState = self.startLocation, self.boxLocation

		initialBoxPushCount = initialWalkCount = 0
		initialCost = (initialBoxPushCount, initialWalkCount)

		q = list()
		q.append( (initialCost, startState) )

		costDict = dict()
		costDict[ startState ] = initialCost

		while len( q ) > 0:
			currentCost, currentState = heapq.heappop( q )
			
			boxPushCount, walkCount = currentCost
			location, boxLocation = currentState

			if boxLocation == self.targetLocation:
				return (walkCount, boxPushCount)

			row, col = location
			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				newRow, newCol = row + du, col + dv
				if self._isOutside( newRow, newCol ) or self.labyrinth[ newRow ][ newCol ] == self.wallMarker:
					continue
				possibleState = None

				if (newRow, newCol) == boxLocation:
					# We are next to the box, and hence we should attempt to move the box.
					newBoxRow, newBoxCol = newRow + du, newCol + dv
					if self._isOutside( newBoxRow, newBoxCol ) or self.labyrinth[ newBoxRow ][ newBoxCol ] == self.wallMarker:
						continue
					possibleState = (newRow, newCol), (newBoxRow, newBoxCol)
					newCost = (boxPushCount + 1, walkCount + 1)
				else:
					possibleState = (newRow, newCol), boxLocation
					newCost = (boxPushCount, walkCount + 1)
				if possibleState not in costDict or newCost < costDict[ possibleState ]:
					costDict[ possibleState ] = newCost
					heapq.heappush( q, (newCost, possibleState) )

		return None

class TheCubeTest( unittest.TestCase ):
	def test_bestPath( self ):
		for testcaseFile in ('cube1', 'cube2', 'sample'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if len( line ) == 0 or 'Instancia' in line:
					continue
				if line == 'Impossivel':
					solutionList.append( None )
				else:
					walk, push = map( int, line.split() )
					solutionList.append( (walk, push) )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			while True:
				rows, cols = map( int, inputFile.readline().strip().split() )
				if rows == 0 and cols == 0:
					break

				labyrinth = list()
				for _ in range( rows ):
					labyrinth.append( inputFile.readline().strip() )

				expectedSolution = solutionList[ index ]
				index += 1

				formatString = 'Testcase {}#{} Rows = {} Cols = {} Expected solution = {}'
				print( formatString.format( testcaseFile, index, rows, cols, expectedSolution ) )

				self.assertEqual( TheCube( rows, cols, labyrinth ).minimumPush(), expectedSolution )

if __name__ == '__main__':
	unittest.main()