import unittest
import os
import pathlib

class Sunflowers:
	def __init__( self, measurementTable ):
		self.measurementTable = measurementTable
		self.size = len( self.measurementTable )

	def _rotate( self, rotateLeft=False ):
		table = self.measurementTable
		N = self.size

		rowOffset = colOffset = 0
		span = N
		
		while span > 1:
			r, c = rowOffset, colOffset
			for i in range( span - 1 ):
				y, x = r, c + i
				X = table[ y ][ x ]
				if rotateLeft:
					table[ y ][ x ] = table[ x ][ N - 1 - y ]
					table[ x ][ N - 1 - y ] = table[ N - 1 - y ][ N - 1 - x ]
					table[ N - 1 - y ][ N - 1 - x ] = table[ N - 1 - x ][ y ]
					table[ N - 1 - x ][ y ] = X
				else:
					table[ y ][ x ] = table[ N - 1 - x ][ y ]
					table[ N - 1 - x ][ y ] = table[ N - 1 - y ][ N - 1 - x ]
					table[ N - 1 - y ][ N - 1 - x ] = table[ x ][ N - 1 - y ]
					table[ x ][ N - 1 - y ] = X
			span = span - 2
			rowOffset, colOffset = rowOffset + 1, colOffset + 1

	def analyze( self ):
		rowSorted = columnSorted = None
		# What are the possible values for rowSorted and columnSorted ?
		# If (rowSorted, columnSorted) is equal to:
		# (True, True)   -> rotation angle = 0
		# (True, False)  -> rotation angle = 90, anti-clockwise
		# (False, False) -> rotation angle = 180
		# (False, True)  -> rotation angle = 90, clockwise

		rowSorted = True
		for col in range( 1, self.size ):
			if self.measurementTable[ 0 ][ col ] < self.measurementTable[ 0 ][ col - 1 ]:
				rowSorted = False
				break
		columnSorted = True
		for row in range( 1, self.size ):
			if self.measurementTable[ row ][ 0 ] < self.measurementTable[ row - 1 ][ 0 ]:
				columnSorted = False
				break

		if (rowSorted, columnSorted) == (True, True):
			pass
		elif (rowSorted, columnSorted) == (False, False):
			for row in range( self.size ):
				self.measurementTable[ row ].reverse()
			self.measurementTable.reverse()
		elif (rowSorted, columnSorted) == (True, False):
			self._rotate( rotateLeft=False )
		elif (rowSorted, columnSorted) == (False, True):
			self._rotate( rotateLeft=True )
		return self.measurementTable

class SunflowersTest( unittest.TestCase ):
	def test_Sunflowers_sample( self ):
		measurementTable = [ [ 1, 3 ], [ 2, 9 ] ]
		expectedMeasurementTable = [ [ 1, 3 ], [ 2, 9 ] ]
		self.assertEqual( Sunflowers( measurementTable ).analyze(), expectedMeasurementTable )

		measurementTable = [ [ 4, 3, 1 ], [ 6, 5, 2 ], [ 9, 7, 3 ] ]
		expectedMeasurementTable = [ [ 1, 2, 3 ], [ 3, 5, 7 ], [ 4, 6, 9 ] ]
		self.assertEqual( Sunflowers( measurementTable ).analyze(), expectedMeasurementTable )

		measurementTable = [ [ 3, 7, 9 ], [ 2, 5, 6 ], [ 1, 3, 4 ] ]
		expectedMeasurementTable = [ [ 1, 2, 3 ], [ 3, 5, 7 ], [ 4, 6, 9 ] ]
		self.assertEqual( Sunflowers( measurementTable ).analyze(), expectedMeasurementTable )

	def test_Sunflowers( self ):
		testFiles = set( [ pathlib.Path( filename ).stem for filename in os.listdir( 'tests/Sunflowers' ) ] )
		for testfile in testFiles:
			self._verify( testfile )

	def _verify( self, testfile ):
		measurementTable = list()
		with open( 'tests/Sunflowers/{}.in'.format( testfile ) ) as inputFile:
			size = int( inputFile.readline().strip() )
			for _ in range( size ):
				measurementTable.append( list( map( int, inputFile.readline().strip().split() ) ) )

		expectedMeasurementTable = list()
		with open( 'tests/Sunflowers/{}.out'.format( testfile ) ) as solutionFile:
			for _ in range( size ):
				expectedMeasurementTable.append( list( map( int, solutionFile.readline().strip().split() ) ) )

		print( 'Testcase {} Size of measurement table = {}'.format( testfile, size ) )
		self.assertEqual( Sunflowers( measurementTable ).analyze(), expectedMeasurementTable )

if __name__ == '__main__':
	unittest.main()