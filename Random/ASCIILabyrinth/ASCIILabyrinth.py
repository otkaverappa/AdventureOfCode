import unittest

class Direction:
	NORTH, SOUTH, EAST, WEST = 'north', 'south', 'east', 'west'

	@staticmethod
	def matchDirection( direction ):
		matchDirectionDict = {
		Direction.NORTH : Direction.SOUTH, Direction.SOUTH : Direction.NORTH,
		Direction.EAST  : Direction.WEST,  Direction.WEST  : Direction.EAST,
		}
		return matchDirectionDict[ direction ]

class ASCIITile:
	def __init__( self, A=None, B=None ):
		self.rotationDict = {
		Direction.NORTH : Direction.EAST,
		Direction.EAST  : Direction.SOUTH,
		Direction.SOUTH : Direction.WEST,
		Direction.WEST  : Direction.NORTH,
		None : None
		}
		self._validate( A, B )
		self.A, self.B = A, B

	def _validate( self, A, B ):
		#For an empty tile, A and B are None.
		#For a non-empty tile, A and B should not be equal.
		assert A in self.rotationDict and B in self.rotationDict
		if A is None or B is None:
			assert A is None and B is None
		else:
			assert A != B

	def orientation( self ):
		return self.A, self.B

	def rotate( self ):
		self.A = self.rotationDict[ self.A ]
		self.B = self.rotationDict[ self.B ]

	def __repr__( self ):
		A, B = self.A, self.B
		if A is None and B is None:
			return 'Empty Tile'
		return '{}-{}'.format( A, B ) if A < B else '{}-{}'.format( B, A )

class ASCIITilePattern:
	linesPerRow, linesPerCol = 3, 3
	horizontalTilePattern = [
	'   '
	'***'
	'   '
	].pop()
	emptyTilePattern = [
	'   '
	'   '
	'   '
	].pop()
	southWestTilePattern = [
	'   '
	'** '
	' * '
	].pop()
	patternToParameterDict = {
	horizontalTilePattern : (Direction.EAST, Direction.WEST),
	emptyTilePattern: (None, None),
	southWestTilePattern : (Direction.SOUTH, Direction.WEST)
	}

	@staticmethod
	def patternToASCIITile( pattern ):
		A, B = ASCIITilePattern.patternToParameterDict[ pattern ]
		return ASCIITile( A, B )

class ASCIILabyrinth:
	def __init__( self, rows, cols, asciiLabyrinth ):
		self.asciiLabyrinth = asciiLabyrinth
		self.rows, self.cols = rows, cols
		self.totalPathCount = 0

	@staticmethod
	def readFromFile( rows, cols, inputFile ):
		asciiLabyrinth = list()

		for _ in range( rows ):
			tileRow = [ str() for _ in range( cols ) ]
			#Read the header and ignore it.
			inputFile.readline()

			for _ in range( ASCIITilePattern.linesPerRow ):
				patternList = inputFile.readline().strip().split( '|' )
				#The line read from the inputFile is of the form:
				#|***|***|***|** |***|** |** |
				#Ignore the first and last element in patternList.
				patternList = patternList[ 1 : -1 ]
				assert len( patternList ) == cols

				for i in range( cols ):
					tileRow[ i ] = tileRow[ i ] + patternList[ i ]

			asciiLabyrinth.append( [ ASCIITilePattern.patternToASCIITile( tilePattern ) for tilePattern in tileRow ] )
		#Fence post - we need to read one more line from the file to complete processing the current ASCIILabyrinth.
		inputFile.readline()

		return asciiLabyrinth

	def _bottomRightOfLabyrinth( self, cell ):
		return cell == (self.rows - 1, self.cols) or cell == (self.rows, self.cols - 1)

	def _cellInDirection( self, cell, direction ):
		directionDelta = {
		Direction.NORTH : (-1, 0), Direction.SOUTH : (1, 0), Direction.EAST : (0, 1), Direction.WEST : (0, -1)
		}
		row, col = cell
		du, dv = directionDelta[ direction ]
		return row + du, col + dv

	def _backtrack( self, cell, visited, orientationToMatch ):
		if self._bottomRightOfLabyrinth( cell ):
			self.totalPathCount += 1
			return
		row, col = cell
		if not 0 <= row < self.rows or not 0 <= col < self.cols:
			return
		if cell in visited:
			return

		currentAsciiTile = self.asciiLabyrinth[ row ][ col ]
		representation = repr( currentAsciiTile )

		visited.add( cell )
		
		while True:
			currentAsciiTile.rotate()
			A, B = currentAsciiTile.orientation()
			matchDirection = Direction.matchDirection( orientationToMatch )

			if matchDirection in (A, B):
				newOrientationToMatch = B if matchDirection == A else A
				newCell = self._cellInDirection( cell, newOrientationToMatch )
				self._backtrack( newCell, visited, orientationToMatch=newOrientationToMatch )
			if repr( currentAsciiTile ) == representation:
				break
		visited.remove( cell )

	def count( self ):
		visited = set()
		self._backtrack( (0, 0), visited, Direction.SOUTH )
		self._backtrack( (0, 0), visited, Direction.EAST )
		return self.totalPathCount

class ASCIILabyrinthTest( unittest.TestCase ):
	def test_count( self ):
		solutionList = list()
		with open( 'tests/labyrinth.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				# line is the form:
				# Number of solutions: 2
				solutionList.append( int( line.strip().split() [ -1 ] ) )
		
		index = 0
		with open( 'tests/labyrinth.in' ) as inputFile:
			testcaseCount = int( inputFile.readline().strip() )

			for _ in range( testcaseCount ):
				rows, cols = map( int, inputFile.readline().strip().split() )
				asciiLabyrinth = ASCIILabyrinth.readFromFile( rows, cols, inputFile )

				expectedCount = solutionList[ index ]
				index += 1

				count = ASCIILabyrinth( rows, cols, asciiLabyrinth ).count()
				print( 'Testcase {} rows = {} cols = {} Expected count = {}'.format( index, rows, cols, expectedCount ) )
				self.assertEqual( count, expectedCount )

if __name__ == '__main__':
	unittest.main()