import unittest

class LetterPuzzle:
	def __init__( self, startState ):
		self.letterPuzzle = list()
		self.blankPosition = None

		for letterCombination in startState:
			letterPuzzleRow = list()
			for col, letter in enumerate( letterCombination ):
				letterPuzzleRow.append( letter )
				if letter == ' ':
					self.blankPosition = len( self.letterPuzzle ), col
			self.letterPuzzle.append( letterPuzzleRow )
		assert self.blankPosition is not None

	def applyMoves( self, moveString ):
		rows, cols = len( self.letterPuzzle ), len( self.letterPuzzle[ 0 ] )
		currentBlankPosition = self.blankPosition
		movementDeltaDict = {
		'L' : (0, -1), 'R' : (0, 1), 'A' : (-1, 0), 'B' : (1, 0)
		}

		def isOutsideGrid( row, col ):
			return not 0 <= row < rows or not 0 <= col < cols

		for movementCode in moveString:
			x, y = currentBlankPosition
			if movementCode not in movementDeltaDict:
				return None
			dx, dy = movementDeltaDict[ movementCode ]
			u, v = x + dx, y + dy
			if isOutsideGrid( u, v ):
				return None
			self.letterPuzzle[ x ][ y ], self.letterPuzzle[ u ][ v ] = self.letterPuzzle[ u ][ v ], self.letterPuzzle[ x ][ y ]
			currentBlankPosition = u, v
		finalConfiguration = list()
		for letterPuzzleRow in self.letterPuzzle:
			finalConfiguration.append( ''.join( letterPuzzleRow ) )
		return finalConfiguration

class LetterPuzzleTest( unittest.TestCase ):
	def _verifyMoves( self, datafile ):
		startStateMoveList = list()
		noConfig = 'This puzzle has no final configuration.'
		newline = '\n'

		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			while True:
				line = inputFile.readline().strip( newline )
				if line == 'Z':
					break
				startState = list()
				startState.append( line )
				for _ in range( 4 ):
					startState.append( inputFile.readline().strip( newline ) )
				moveString = str()
				readDone = False
				while True:
					moveStringFragment = inputFile.readline().strip( newline )
					if moveStringFragment[ -1 ] == '0':
						moveStringFragment = moveStringFragment[ : -1 ]
						readDone = True
					moveString += moveStringFragment
					if readDone:
						break
				startStateMoveList.append( (startState, moveString) )

		expectedResultList = list()
		solution, rowNumber = list(), 0
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip( newline )
				if len( line ) == 0:
					continue
				if line == noConfig:
					expectedResultList.append( None )
				elif 'Puzzle' in line:
					continue
				else:
					row = list()
					for i in range( 0, len( line ), 2 ):
						row.append( line[ i ] )
					solution.append( ''.join( row ) )
					rowNumber += 1
					if rowNumber == 5:
						expectedResultList.append( solution )
						solution, rowNumber = list(), 0

		assert len( startStateMoveList ) == len( expectedResultList )
		
		for i, (startState, moveString) in enumerate( startStateMoveList ):
			print( 'Testcase = {} datafile = {}'.format( i + 1, datafile ) )
			self.assertEqual( LetterPuzzle( startState ).applyMoves( moveString ), expectedResultList[ i ] )

	def test_moves( self ):
		for datafile in ('sample', 'puzzle'):
			self._verifyMoves( datafile )

if __name__ == '__main__':
	unittest.main()