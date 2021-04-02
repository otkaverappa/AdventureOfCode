import unittest
import itertools

class SquareDetector:
	def __init__( self, size, layoutMap ):
		self.size = size
		self.layoutMap = layoutMap
		self.whiteCellToken, self.blackCellToken = '.', '#'

	def _dfs( self, cell ):
		stack = list()
		stack.append( cell )

		visited = set()
		visited.add( cell )

		while len( stack ) > 0:
			u, v = cell = stack.pop()
			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				newCell = x, y = u + du, v + dv
				if not 0 <= x < self.size or not 0 <= y < self.size:
					continue
				if self.layoutMap[ x ][ y ] == self.blackCellToken and newCell not in visited:
					visited.add( newCell )
					stack.append( newCell )
		return visited

	def isSquare( self ):
		visited = None
		for row, col in itertools.product( range( self.size ), range( self.size ) ):
			if self.layoutMap[ row ][ col ] == self.blackCellToken:
				cell = row, col
				if visited is not None and cell not in visited:
					return False
				visited = self._dfs( cell )
				r1, c1 = min( visited )
				r2, c2 = max( visited )

				width, height = c2 - c1 + 1, r2 - r1 + 1
				cellCount = width * height
				if width != height or cellCount != len( visited ):
					return False
		return True

class SquareDetectorTest( unittest.TestCase ):
	def test_SquareDetector( self ):
		solutionList = list()
		with open( 'tests/square.ans' ) as solutionFile:
			for solutionLine in solutionFile.readlines():
				_, _, isSquareToken = solutionLine.strip().split()
				isSquare = isSquareToken == 'YES'
				solutionList.append( isSquare )

		with open( 'tests/square' ) as inputFile:
			testcaseCount = int( inputFile.readline().strip() )
			for i in range( testcaseCount ):
				N = int( inputFile.readline().strip() )
				layoutMap = list()
				for _ in range( N ):
					layoutMap.append( inputFile.readline().strip() )

				isSquare = solutionList[ i ]
				
				print( 'Testcase #{} Size = {} isSquare {}'.format( i + 1, N, isSquare ) )
				self.assertEqual( SquareDetector( N, layoutMap ).isSquare(), isSquare )

if __name__ == '__main__':
	unittest.main()