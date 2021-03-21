import unittest
from collections import deque

class Maze:
	def __init__( self, rows, cols, layoutMap ):
		self.rows, self.cols = rows, cols
		self.layoutMap = layoutMap
		
		self.startCell, self.targetCell = (0, 0), (rows - 1, cols - 1)
		self.maximumHeight = 10

	def _getHeight( self, cell, numberOfSteps ):
		u, v = cell
		return ( self.layoutMap[ u ][ v ] + numberOfSteps ) % self.maximumHeight

	def play( self ):
		initialState = self.startCell, 0

		q = deque()
		q.append( initialState )

		visited = set()
		visited.add( initialState )

		while len( q ) > 0:
			currentCell, numberOfSteps = q.popleft()
			if currentCell == self.targetCell:
				return numberOfSteps

			u, v = currentCell
			height = self._getHeight( currentCell, numberOfSteps )

			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0), (0, 0) ]:
				x, y = newCell = u + du, v + dv
				if not 0 <= x < self.rows or not 0 <= y < self.cols:
					continue
				if self._getHeight( newCell, numberOfSteps ) - height > 1:
					continue
				newState = newCell, numberOfSteps + 1
				stepCountPhase = (numberOfSteps + 1) % self.maximumHeight
				if (newCell, stepCountPhase) not in visited:
					visited.add( (newCell, stepCountPhase) )
					q.append( newState )
		return None

class MazeTest( unittest.TestCase ):
	def test_play( self ):
		for testcaseFile in [ 'maze{}'.format( i ) for i in range( 1, 9 ) ]:
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			expectedSteps = int( solutionFile.readline().strip() )

		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			rows, cols = map( int, inputFile.readline().strip().split() )
			layoutMap = list()
			for _ in range( rows ):
				layoutMap.append( list( map( int, inputFile.readline().strip().split() ) ) )

			print( 'Testcase {} rows = {} cols = {} Expected number of steps = {}'.format( testcaseFile, rows, cols, expectedSteps ) )
			self.assertEqual( Maze( rows, cols, layoutMap ).play(), expectedSteps )

if __name__ == '__main__':
	unittest.main()