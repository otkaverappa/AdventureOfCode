import unittest
import itertools

class StickerCollectorRobot:
	def __init__( self, rows, cols, arena, instructionString ):
		self.blockedCell, self.openCell, self.stickerCell = '#', '.', '*'
		self.rightTurnDict = {
		'N' : 'E', 'E' : 'S', 'S' : 'W', 'W' : 'N'
		}
		self.leftTurnDict = {
		'N' : 'W', 'W' : 'S', 'S' : 'E', 'E' : 'N'
		}
		self.tokenMap = {
		'N' : 'N', 'S' : 'S', 'L' : 'E', 'O' : 'W'
		}
		self.directionDelta = {
		'N' : (-1, 0), 'S' : (1, 0), 'E' : (0, 1), 'W' : (0, -1)
		}

		self.rows, self.cols = rows, cols
		self.arena = arena
		self.instructionString = instructionString
		self.currentLocation = self.currentDirection = None
		for row, col in itertools.product( range( rows ), range( cols ) ):
			token = self.arena[ row ][ col ]
			if token in self.tokenMap:
				self.currentLocation = row, col
				self.currentDirection = self.tokenMap[ token ]
				break

	def _canRobotMoveTo( self, location ):
		row, col = location
		if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
			return False
		if self.arena[ row ][ col ] == self.blockedCell:
			return False
		return True

	def _stickerPresent( self, location ):
		row, col = location
		return self.arena[ row ][ col ] == self.stickerCell

	def collect( self ):
		collectedStickers = set()

		for instructionCode in self.instructionString:
			if instructionCode == 'D':
				self.currentDirection = self.rightTurnDict[ self.currentDirection ]
			elif instructionCode == 'E':
				self.currentDirection = self.leftTurnDict[ self.currentDirection ]
			elif instructionCode == 'F':
				du, dv = self.directionDelta[ self.currentDirection ]
				row, col = self.currentLocation
				newLocation = newRow, newCol = row + du, col + dv
				if self._canRobotMoveTo( newLocation ):
					self.currentLocation = newLocation
					if self._stickerPresent( newLocation ):
						collectedStickers.add( newLocation )
		return len( collectedStickers )

class StickerCollectorRobotTest( unittest.TestCase ):
	def test_collect( self ):
		for testcaseFile in ('arena1', 'arena2'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line.strip() ) )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			while True:
				rows, cols, instructionCount = map( int, inputFile.readline().strip().split() )
				if rows == cols == instructionCount == 0:
					break

				arena = list()
				for _ in range( rows ):
					arena.append( inputFile.readline().strip() )
				instructionString = inputFile.readline().strip()
				assert len( instructionString ) == instructionCount

				expectedSolution = solutionList[ index ]
				index += 1

				print( 'Testcase {}#{} rows = {} cols = {} instructionCount = {}'.format( testcaseFile, index, rows, cols, instructionCount ) )
				self.assertEqual( StickerCollectorRobot( rows, cols, arena, instructionString ).collect(),  expectedSolution )

if __name__ == '__main__':
	unittest.main()