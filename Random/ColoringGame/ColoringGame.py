import unittest
import itertools

class ColoringGame:
	def __init__( self, rows, cols, imageData ):
		self.rows, self.cols = rows, cols
		self.imageData = imageData

		self.whitePixel, self.blackPixel = '.', 'o'

	def _isOutsideImage( self, row, col ):
		return not 0 <= row < self.rows or not 0 <= col < self.cols

	def _floodFill( self, row, col ):
		stack = list()
		stack.append( (row, col) )

		while len( stack ) > 0:
			currentRow, currentCol = stack.pop()
			self.imageData[ currentRow ][ currentCol ] = self.blackPixel

			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				u, v = currentRow + du, currentCol + dv
				if self._isOutsideImage( u, v ):
					continue
				if self.imageData[ u ][ v ] == self.whitePixel:
					stack.append( (u, v) )

	def numberOfClicks( self ):
		islandCount = 0
		stack = list()

		for i, j in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.imageData[ i ][ j ] == self.whitePixel:
				self._floodFill( i, j )
				islandCount += 1
		return islandCount

class ColoringGameTest( unittest.TestCase ):
	def test_numberOfClicks( self ):
		for testcaseFile in ('sample', 'color1', 'color2'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		expectedClicks = None
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			expectedClicks = int( solutionFile.readline().strip() )

		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			rows, cols = map( int, inputFile.readline().strip().split() )
			imageData = list()
			for _ in range( rows ):
				imageData.append( list( inputFile.readline().strip() ) )

			print( 'Image: rows = {} cols = {} Number of clicks = {}'.format( rows, cols, expectedClicks ) )
			self.assertEqual( ColoringGame( rows, cols, imageData ).numberOfClicks(), expectedClicks )

if __name__ == '__main__':
	unittest.main()