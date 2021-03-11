from collections import deque
import itertools
import unittest

class NoOneLabyrinth:
	def __init__( self, labyrinth ):
		self.rows, self.cols = len( labyrinth ), len( labyrinth[ 0 ] )

		self.startCell = self.targetCell = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if labyrinth[ row ][ col ] == '@':
				self.startCell = row, col
			elif labyrinth[ row ][ col ] == '*':
				self.targetCell = row, col
		assert self.startCell is not None and self.targetCell is not None

		self.labyrinth = labyrinth

		self.blockedCell = '#'

	def _outsideMap( self, x, y ):
		return x < 0 or x >= self.rows or y < 0 or y >= self.cols

	def pathLength( self ):
		_pathLength = 0

		initialState = self.startCell, str()
		q = deque()
		q.append( initialState )

		visited = set()
		visited.add( initialState )

		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1
				
				currentCell, keysTaken = q.popleft()
				if currentCell == self.targetCell:
					return _pathLength
				
				u, v = currentCell
				for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
					newCell = x, y = u + du, v + dv
					if self._outsideMap( x, y ):
						continue
					cellType = self.labyrinth[ x ][ y ]
					if cellType == self.blockedCell:
						continue
					if cellType.isalpha() and cellType.isupper() and cellType.lower() not in keysTaken:
						continue
					
					currentKey = str()
					if cellType.isalpha() and cellType not in keysTaken:
						currentKey = cellType
					newKeysTaken = keysTaken + currentKey
					newKeysTaken = ''.join( sorted( list( newKeysTaken ) ) )
					
					newState = newCell, newKeysTaken
					if newState not in visited:
						visited.add( newState )
						q.append( newState )
			_pathLength += 1
		return None

class NoOneLabyrinthTest( unittest.TestCase ):
	def test_pathLength( self ):
		for testcaseFile in ('sample1', 'sample2', 'sample3'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		expectedSolution = None
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			solutionString = solutionFile.readline().strip()
			expectedSolution = None if solutionString == '--' else int( solutionString )

		labyrinth = list()
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			for labyrinthRow in inputFile.readlines():
				labyrinth.append( labyrinthRow.strip() )

		pathLength = NoOneLabyrinth( labyrinth ).pathLength()
		print( 'Testcase {} Expected solution = {}'.format( testcaseFile, expectedSolution ) )
		self.assertEqual( pathLength, expectedSolution )

if __name__ == '__main__':
	unittest.main()