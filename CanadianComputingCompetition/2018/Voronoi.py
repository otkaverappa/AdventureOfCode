import unittest
import os
import pathlib

class Voronoi:
	@staticmethod
	def smallest( positionList ):
		positionList.sort()

		smallestSize = None
		L = R = None

		for i in range( 1, len( positionList ) - 1 ):
			if L is None:
				L = positionList[ i ] - positionList[ i - 1 ]
			R = positionList[ i + 1 ] - positionList[ i ]
			
			size = ( R + L ) / 2
			smallestSize = min( smallestSize, size ) if smallestSize is not None else size
			L = R
		return '{:.1f}'.format( smallestSize )

class VoronoiTest( unittest.TestCase ):
	def test_Voronoi_sample( self ):
		positionList = [ 16, 0, 10, 4, 15 ]
		self.assertEqual( Voronoi.smallest( positionList ), '3.0' )

	def test_Voronoi( self ):
		testFiles = set( [ pathlib.Path( filename ).stem for filename in os.listdir( 'tests/Voronoi' ) ] )
		for testfile in testFiles:
			self._verify( testfile )

	def _verify( self, testfile ):
		positionList = list()
		with open( 'tests/Voronoi/{}.in'.format( testfile ) ) as inputFile:
			N = int( inputFile.readline().strip() )
			for _ in range( N ):
				positionList.append( int( inputFile.readline().strip() ) )

		with open( 'tests/Voronoi/{}.out'.format( testfile ) ) as solutionFile:
			smallestSize = solutionFile.readline().strip()

		print( 'Testcase {} Size of position list = {} smallestSize = {}'.format( testfile, len( positionList ), smallestSize ) )
		self.assertEqual( Voronoi.smallest( positionList ), smallestSize )

if __name__ == '__main__':
	unittest.main()