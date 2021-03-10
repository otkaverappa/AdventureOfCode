import unittest
import itertools
from collections import deque

class MultistoryLabyrinth:
	def __init__( self, labyrinth, rows, cols, levels ):
		self.startPosition = None
		self.rows, self.cols, self.levels = rows, cols, levels

		self.labyrinth = labyrinth
		for level, row, col in itertools.product( range( levels ), range( rows ), range( cols ) ):
			if self.labyrinth[ level ][ row ][ col ] == 'S':
				self.startPosition = (level, row, col)
				break
		assert self.startPosition is not None

		self.openSpace, self.elevator, self.targetSpace = '.', '-', 'E'
		self.openSpaces = set( [ self.openSpace, self.elevator, self.targetSpace ] )

	def minimumSteps( self ):
		q = deque()
		q.append( self.startPosition )

		visited = set()
		visited.add( self.startPosition )

		stepCount = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				level, row, col = currentPosition = q.popleft()
				if self.labyrinth[ level ][ row ][ col ] == 'E':
					return stepCount

				for (dl, du, dv) in [ (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0) ]:
					newLevel, newRow, newCol = level + dl, row + du, col + dv
					if not 0 <= newLevel < self.levels or not 0 <= newRow < self.rows or not 0 <= newCol < self.cols:
						continue
					possiblePosition = None

					if dl == 0 and self.labyrinth[ level ][ newRow ][ newCol ] in self.openSpaces:
						possiblePosition = (newLevel, newRow, newCol)
					elif dl != 0 and self.labyrinth[ level ][ row ][ col ] == self.labyrinth[ newLevel ][ row ][ col ] == self.elevator:
						possiblePosition = (newLevel, newRow, newCol)
					
					if possiblePosition is None or possiblePosition in visited:
						continue
					visited.add( possiblePosition )
					q.append( possiblePosition )

			stepCount = stepCount + 1

		return None

class MultistoryLabyrinthTest( unittest.TestCase ):
	def test_minimumSteps( self ):
		solutionList = list()
		with open( 'tests/labyrinth.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line.strip() ) )

		index = 0
		with open( 'tests/labyrinth.in' ) as inputFile:
			while True:
				rows, cols, levels = map( int, inputFile.readline().strip().split() )
				if rows == 0 and cols == 0 and levels == 0:
					break

				labyrinth = list()
				for _ in range( levels ):
					levelMap = list()
					for _ in range( rows ):
						levelMap.append( inputFile.readline().strip() )
					labyrinth.append( levelMap )
					inputFile.readline()

				expectedSolution = solutionList[ index ]
				# If there is no path across the labyrinth, the solution is encoded as -1. Translate it to "None".
				if expectedSolution < 0:
					expectedSolution = None
				index += 1

				formatString = 'Testcase {} Labyrinth size = {} x {} Levels = {} Expected minimum steps = {}'
				print( formatString.format( index, rows, cols, levels, expectedSolution ) )

				self.assertEqual( MultistoryLabyrinth( labyrinth, rows, cols, levels ).minimumSteps(), expectedSolution )

if __name__ == '__main__':
	unittest.main()