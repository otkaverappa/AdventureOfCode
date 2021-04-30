from collections import deque
import unittest

class City:
	def __init__( self, cityMap ):
		self.cityMap = cityMap
		self.rows, self.cols = len( cityMap ), len( cityMap[ 0 ] )

		self.directionDelta = {
		'+' : [ (0, 1), (0, -1), (1, 0), (-1, 0) ],
		'|' : [ (-1, 0), (1, 0) ],
		'-' : [ (0, -1), (0, 1) ]
		}
		self.wallCell = '*'

	def intersectionCount( self ):
		startPosition = 0, 0
		targetPosition = self.rows - 1, self.cols - 1

		q = deque()
		q.append( startPosition )

		visited = set()
		visited.add( startPosition )

		stepCount = 1

		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				u, v = currentPosition = q.popleft()
				if currentPosition == targetPosition:
					return stepCount

				for du, dv in self.directionDelta[ self.cityMap[ u ][ v ] ]:
					newPosition = row, col = u + du, v + dv
					if not 0 <= row < self.rows or not 0 <= col < self.cols:
						continue
					if self.cityMap[ row ][ col ] == self.wallCell:
						continue
					if newPosition not in visited:
						visited.add( newPosition )
						q.append( newPosition )
			stepCount += 1
		return -1

class CityTest( unittest.TestCase ):
	def _verify( self, filename ):
		solutionList = list()
		with open( 'tests/{}.out'.format( filename ) ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line.strip() ) )

		index = 0
		with open( 'tests/{}.in'.format( filename ) ) as inputFile:
			T = int( inputFile.readline().strip() )

			for _ in range( T ):
				rows = int( inputFile.readline().strip() )
				cols = int( inputFile.readline().strip() )

				cityMap = list()
				for _ in range( rows ):
					cityMap.append( inputFile.readline().strip() )

				expectedSolution = solutionList[ index ]
				index += 1

				print( 'Testcase {}#{} rows = {} cols = {} stepCount = {}'.format( filename, index, rows, cols, expectedSolution ) )
				self.assertEqual( City( cityMap ).intersectionCount(), expectedSolution )

	def test_City( self ):
		for i in range( 5 ):
			filename = 's3.{}'.format( i + 1 )
			self._verify( filename )

	def test_City_sample( self ):
		cityMap = [
		'-|',
		'*+'
		]
		self.assertEqual( City( cityMap ).intersectionCount(), 3 )

		cityMap = [
		'+||*+',
		'+++|+',
		'**--+'
		]
		self.assertEqual( City( cityMap ).intersectionCount(), 7 )

		cityMap = [
		'+*+',
		'+*+'
		]
		self.assertEqual( City( cityMap ).intersectionCount(), -1 )

if __name__ == '__main__':
	unittest.main()