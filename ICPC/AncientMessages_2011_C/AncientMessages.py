import unittest
from collections import deque
import itertools

class AncientMessage:
	def __init__( self, compressedImage, rows, cols ):
		self.image = [ [ '0' for _ in range( cols * 4 ) ] for _ in range( rows ) ]
		for rowIndex, compressedRow in enumerate( compressedImage ):
			for colIndex, hexDigit in enumerate( compressedRow ):
				# hexDigit is a single character from '0' to 'f'. We have to convert it
				# into four binary digits. 
				for offset, color in enumerate( format( int( hexDigit, 16 ), '04b' ) ):
					self.image[ rowIndex ][ colIndex * 4 + offset ] = color
		self.rows, self.cols = rows, cols * 4

		self.symbolCode = {
		0 : ('Was', 'W'),
		1 : ('Ankh', 'A'),
		2 : ('Akeht', 'K'),
		3 : ('Wedjat', 'J'),
		4 : ('Scarab', 'S'),
		5 : ('Djed', 'D')
		}

	def _floodfill( self, fillFrom, fillColor, visited ):
		row, col = fillFrom
		color = self.image[ row ][ col ]

		q = deque()
		q.append( fillFrom )

		distinctAdjacentCells = set()

		while len( q ) > 0:
			x, y = q.popleft()
			if (x, y) in visited:
				continue
			visited.add( (x, y) )

			self.image[ x ][ y ] = fillColor

			for dx, dy in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				u, v = x + dx, y + dy
				if not 0 <= u < self.rows or not 0 <= v < self.cols:
					distinctAdjacentCells.add( 'border' ) 
					continue
				if (u, v) in visited:
					continue
				if self.image[ u ][ v ] != color:
					distinctAdjacentCells.add( self.image[ u ][ v ] )
					continue
				q.append( (u, v) )
		return distinctAdjacentCells

	def decode( self ):
		currentSymbol = 0
		visited = set()
		symbolDict = dict()

		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if (row, col) not in visited and self.image[ row ][ col ] == '1':
				self._floodfill( (row, col), currentSymbol, visited )
				symbolDict[ currentSymbol ] = 0
				currentSymbol = currentSymbol + 1

		visited.clear()
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if (row, col) not in visited and self.image[ row ][ col ] == '0':
				distinctAdjacentCells = self._floodfill( (row, col), '1', visited )
				if len( distinctAdjacentCells ) == 1:
					boundaryColor = max( distinctAdjacentCells )
					symbolDict[ boundaryColor ] += 1

		decodedMessage = list()
		for _, enclosedCount in symbolDict.items():
			_, symbol = self.symbolCode[ enclosedCount ]
			decodedMessage.append( symbol )
		decodedMessage.sort()
		return ''.join( decodedMessage )

class AncientMessagesTest( unittest.TestCase ):
	def test_decode( self ):
		for datafile in ('sample', 'ancient'):
			self._verify( datafile )

	def _verify( self, datafile ):
		expectedResults = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			for inputLine in solutionFile.readlines():
				_, _, expectedResult = tuple( inputLine.strip().split() )
				expectedResults.append( expectedResult )
		index = 0
		with open( 'tests/{}.in'.format( datafile ) ) as testcaseFile:
			while True:
				rows, cols = map( int, testcaseFile.readline().strip().split() )
				if rows == 0 and cols == 0:
					break
				compressedImage = list()
				for _ in range( rows ):
					compressedRow = testcaseFile.readline().strip()
					assert len( compressedRow ) == cols
					compressedImage.append( compressedRow )
				decodedMessage = AncientMessage( compressedImage, rows, cols ).decode()
				print( 'Image Rows = {} Columns = {} Decoded Message = {}'.format( rows, cols, decodedMessage ) )
				self.assertEqual( decodedMessage, expectedResults[ index ] )
				index += 1

if __name__ == '__main__':
	unittest.main()