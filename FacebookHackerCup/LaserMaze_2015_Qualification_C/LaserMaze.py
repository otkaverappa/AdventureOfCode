import unittest
import itertools
from collections import deque

class LaserMaze:
	def __init__( self, rows, cols, laserMaze ):
		self.rows, self.cols = rows, cols
		self.laserMaze = laserMaze

		laserTurretCell = set( '^v<>' )
		self.directionDeltaDict = {
		'^' : (-1, 0), 'v' : (1, 0), '<' : (0, -1), '>' : (0, 1)
		}

		self.rotationDict = {
		'^' : '>', '>' : 'v', 'v' : '<', '<' : '^'
		}

		self.startPosition = self.targetPosition = None
		self.laserTurretDict = dict()

		self.blockedCell, self.startCell, self.targetCell, self.emptyCell = '#', 'S', 'G', '.'
		self.passableCells = set( [ self.startCell, self.targetCell, self.emptyCell ] )

		for row, col in itertools.product( range( rows ), range( cols ) ):
			cellType = self.laserMaze[ row ][ col ]
			if cellType == self.startCell:
				self.startPosition = (row, col)
			elif cellType == self.targetCell:
				self.targetPosition = (row, col)
			elif cellType in laserTurretCell:
				self.laserTurretDict[ (row, col) ] = dict()

		assert self.startPosition is not None and self.targetPosition is not None
		self._populateLaserTurretTrajectory()

		self.dangerCells = dict()
		self._populateDangerCells()

	def _populateDangerCells( self ):
		for stepCount in range( 4 ):
			self.dangerCells[ stepCount ] = set()
			for (row, col) in self.laserTurretDict.keys():
				directionAfterRotation = self._rotate( self.laserMaze[ row ][ col ], stepCount )
				A = self.dangerCells[ stepCount ]
				B = self.laserTurretDict[ (row, col) ][ directionAfterRotation ]
				self.dangerCells[ stepCount ] = set.union( A, B )

	def _rotate( self, direction, count ):
		assert direction in self.rotationDict
		for _ in range( count % 4 ):
			direction = self.rotationDict[ direction ]
		return direction

	def _populateLaserTurretTrajectory( self ):
		for (row, col) in self.laserTurretDict.keys():
			for direction, (du, dv) in self.directionDeltaDict.items():
				self.laserTurretDict[ (row, col) ][ direction ] = set()
				u, v = row + du, col + dv
				while not self._isOutsideMaze( u, v ) and self.laserMaze[ u ][ v ] in self.passableCells:
					self.laserTurretDict[ (row, col) ][ direction ].add( (u, v) )
					u, v = u + du, v + dv

	def _isOutsideMaze( self, row, col ):
		return row < 0 or row >= self.rows or col < 0 or col >= self.cols

	def move( self ):
		initialPosition, numberOfSteps = self.startPosition, 0
		
		q = deque()
		q.append( (initialPosition, numberOfSteps) )

		visited = set()
		visited.add( (initialPosition, numberOfSteps) )

		while len( q ) > 0:
			currentPosition, stepCount = q.popleft()
			if currentPosition == self.targetPosition:
				return stepCount

			u, v = currentPosition
			stepCountPhase = (stepCount + 1) % 4
			for (du, dv) in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				x, y = u + du, v + dv
				if self._isOutsideMaze( x, y ) or self.laserMaze[ u ][ v ] == self.blockedCell or (u, v) in self.laserTurretDict:
					continue
				if (x, y) in self.dangerCells[ stepCountPhase ]:
					continue
				newPosition = (x, y)
				possibleState = newPosition, stepCount + 1
				if (newPosition, stepCountPhase) not in visited:
					visited.add( (newPosition, stepCountPhase) )
					q.append( possibleState )
		return None

class LaserMazeTest( unittest.TestCase ):
	def _render( self, laserMaze ):
		for laserMazeRow in laserMaze:
			print( laserMazeRow )
		print()

	def test_move( self ):
		for testcaseFile in ('sample', 'maze', 'bigmaze'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, solutionString = line.strip().split()
				solutionList.append( None if solutionString == 'impossible' else int( solutionString ) )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			N = int( inputFile.readline().strip() )
			assert N == len( solutionList )

			for _ in range( N ):
				rows, cols = map( int, inputFile.readline().strip().split() )
				laserMaze = list()
				for _ in range( rows ):
					laserMaze.append( inputFile.readline().strip() )

				maze = LaserMaze( rows, cols, laserMaze )
				expectedSolution = solutionList[ index ]
				index += 1

				formatString = 'Testcase {}#{} rows = {} cols = {} Expected solution = {}'
				print( formatString.format( testcaseFile, index, rows, cols, expectedSolution ) )
				
				#self._render( laserMaze )
				self.assertEqual( maze.move(), expectedSolution )

if __name__ == '__main__':
	unittest.main()