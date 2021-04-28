import unittest
import math
from collections import defaultdict

class DoubleSquares:
	def __init__( self, numberList ):
		self.numberList = numberList

	def _isSquare( self, x ):
		y = int( math.sqrt( x ) )
		return x == y * y

	def _numberOfPartitions( self, x ):
		numberSet = set()

		for i in range( 0, int( math.sqrt( x ) + 1 ) ):
			if self._isSquare( x - i * i ):
				j = int( math.sqrt( x - i * i ) )
				if j < i:
					i, j = j, i
				numberSet.add( (i, j) )
		return len( numberSet )

	def numberOfPartitions( self ):
		return [ self._numberOfPartitions( number ) for number in self.numberList ]

class DoubleSquaresTest( unittest.TestCase ):
	def test_DoubleSquares_sample( self ):
		numberList = [ 10, 25, 3, 0, 1 ]
		expectedCount = [ 1, 2, 0, 1, 1 ]
		self.assertEqual( DoubleSquares( numberList ).numberOfPartitions(), expectedCount )

	def test_DoubleSquares( self ):
		numberList = list()
		
		with open( 'tests/double_squares_input.txt' ) as inputFile:
			N = int( inputFile.readline().strip() )
			for _ in range( N ):
				numberList.append( int( inputFile.readline().strip() ) )

		expectedCount = list()
		with open( 'tests/double_squares_output.txt' ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, count = line.strip().split()
				expectedCount.append( int( count ) )

		for index in range( len( numberList ) ):
			print( 'Case #{}: {} -> {}'.format( index + 1, numberList[ index ], expectedCount[ index ] ) )

		self.assertEqual( DoubleSquares( numberList ).numberOfPartitions(), expectedCount )

class StringComparator:
	def __init__( self, string ):
		self.string = string

	def __lt__( self, other ):
		A, B = self.string, other.string
		
		return A + B < B + A

class StudiousStudent:
	@staticmethod
	def concat( stringList ):
		stringComparatorList = [ StringComparator( string ) for string in stringList ]
		stringComparatorList.sort()
		return ''.join( [ stringComparator.string for stringComparator in stringComparatorList ] )

class StudiousStudentTest( unittest.TestCase ):
	def test_StudiousStudent_sample( self ):
		testcases = [
		([ 'facebook', 'hacker', 'cup', 'for', 'studious', 'students' ], 'cupfacebookforhackerstudentsstudious'),
		([ 'k', 'duz', 'q', 'rc', 'lvraw' ], 'duzklvrawqrc'),
		([ 'mybea', 'zdr', 'yubx', 'xe', 'dyroiy' ], 'dyroiymybeaxeyubxzdr'),
		([ 'jibw', 'ji', 'jp', 'bw', 'jibw' ], 'bwjibwjibwjijp'),
		([ 'uiuy', 'hopji', 'li', 'j', 'dcyi' ], 'dcyihopjijliuiuy')
		]
		for stringList, expectedSolution in testcases:
			self.assertEqual( StudiousStudent.concat( stringList ), expectedSolution )

	def test_StudiousStudent( self ):
		solutionList = list()
		with open( 'tests/studious_student_output.txt' ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, expectedSolution = line.strip().split()
				solutionList.append( expectedSolution )

		with open( 'tests/studious_student_input.txt' ) as inputFile:
			N = int( inputFile.readline().strip() )
			for i in range( N ):
				_, * stringList = inputFile.readline().strip().split()

				print( 'Testcase #{} stringList = {}'.format( i + 1, stringList ) )
				self.assertEqual( StudiousStudent.concat( stringList ), solutionList[ i ] )

class PegGame:
	def __init__( self, rows, cols, targetColumn, missingPegLocationList ):
		self.rows, self.cols = rows, cols
		self.targetColumn = targetColumn
		self.missingPegLocationList = missingPegLocationList

	def bestLocation( self ):
		pegMap = self._getPegMap()
		
		bestColumn = bestProbability = None
		for col in range( self.cols - 1 ):
			probability = self._traceFromTop( col, pegMap )
			if bestProbability is None or probability > bestProbability:
				bestProbability = probability
				bestColumn = col
		return bestColumn, bestProbability

	def _traceFromTop( self, col, pegMap ):
		rows, cols = len( pegMap ), len( pegMap[ 0 ] )
		targetColumn, col = self.targetColumn * 2 + 1, col * 2 + 1

		cells = defaultdict( lambda : 0.0 )
		cells[ col ] = 1.0

		for row in range( rows - 1 ):
			newCells = defaultdict( lambda : 0.0 )
			for col, probability in cells.items():
				assert pegMap[ row ][ col ] == '.'
				if pegMap[ row + 1 ][ col ] == '.':
					newCells[ col ] += probability
				else:
					leftCellIsEmpty, rightCellIsEmpty = pegMap[ row + 1 ][ col - 1 ] == '.', pegMap[ row + 1 ][ col + 1 ] == '.'
					if leftCellIsEmpty and rightCellIsEmpty:
						newCells[ col - 1 ] += 0.5 * probability
						newCells[ col + 1 ] += 0.5 * probability
					elif leftCellIsEmpty:
						newCells[ col - 1 ] += probability
					else:
						newCells[ col + 1 ] += probability
			cells = newCells
		return cells[ targetColumn ]

	def _getPegMap( self ):
		pegMap = list()
		for row in range( self.rows ):
			pegMapRow = list()
			pegCount = self.cols - 1 if row % 2 == 0 else self.cols - 2
			
			if row % 2 != 0:
				pegMapRow.append( 'x' )
			for _ in range( pegCount ):
				pegMapRow.append( 'x' )
				pegMapRow.append( '.' )
			pegMapRow.append( 'x' )
			if row % 2 != 0:
				pegMapRow.append( 'x' )	

			pegMap.append( pegMapRow )

		for row, col in self.missingPegLocationList:
			if row % 2 == 0:
				r, c = row, 2 * col
			else:
				r, c = row, 2 * col + 1
			pegMap[ r ][ c ] = '.'

		return pegMap

	def bestLocationAsString( self ):
		col, probability = self.bestLocation()
		return '{} {:.6f}'.format( col, probability )

class PegGameTest( unittest.TestCase ):
	def test_PegGame_sample( self ):
		rows, cols, targetColumn, missingPegLocationList = 5, 4, 0, [ (2, 2) ]
		self.assertEqual( PegGame( rows, cols, targetColumn, missingPegLocationList ).bestLocationAsString(), '0 0.375000' )

		rows, cols, targetColumn, missingPegLocationList = 3, 4, 1, [ (1, 1) ]
		self.assertEqual( PegGame( rows, cols, targetColumn, missingPegLocationList ).bestLocationAsString(), '1 1.000000' )

		rows, cols, targetColumn, missingPegLocationList = 3, 3, 1, [ (1, 1), (1, 0) ]
		self.assertEqual( PegGame( rows, cols, targetColumn, missingPegLocationList ).bestLocationAsString(), '1 1.000000' )

		rows, cols, targetColumn, missingPegLocationList = 3, 4, 0, [ (1, 0), (1, 1) ]
		self.assertEqual( PegGame( rows, cols, targetColumn, missingPegLocationList ).bestLocationAsString(), '0 1.000000' )

		rows, cols, targetColumn, missingPegLocationList = 3, 4, 0, [ (1, 1) ]
		self.assertEqual( PegGame( rows, cols, targetColumn, missingPegLocationList ).bestLocationAsString(), '0 0.500000' )

	def test_PegGame( self ):
		expectedSolutionList = list()
		with open( 'tests/peg_game_output.txt' ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, * rest = line.strip().split()
				expectedSolutionList.append( ' '.join( rest ) )

		with open( 'tests/peg_game_input.txt' ) as inputFile:
			N = int( inputFile.readline().strip() )
			for i in range( N ):
				rows, cols, targetColumn, M, * missingPegLocations = map( int, inputFile.readline().strip().split() )
				assert len( missingPegLocations ) == 2 * M
				missingPegLocationList = list()
				for j in range( 0, len( missingPegLocations ), 2 ):
					row, col = missingPegLocations[ j ], missingPegLocations[ j + 1 ]
					missingPegLocationList.append( (row, col) )

				status = PegGame( rows, cols, targetColumn, missingPegLocationList ).bestLocationAsString()
				print( 'Testcase #{} rows = {} cols = {} targetColumn = {} status = {}'
					   .format( i + 1, rows, cols, targetColumn, status ) )
				expectedStatus = expectedSolutionList[ i ]
				self.assertEqual( status, expectedStatus )

if __name__ == '__main__':
	unittest.main()