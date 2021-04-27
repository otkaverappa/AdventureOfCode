import unittest
import itertools

class Timber:
	def __init__( self, N, treePositionList ):
		self.N = N
		self.treePositionList = treePositionList

	def maximumTimberInterval( self ):
		self.treePositionList.sort()

		bestTimberInterval = 0
		cache = dict()

		for (x, height) in self.treePositionList:
			intervalLeft = cache.get( x - height, 0 ) + height

			knownBestInterval = cache.get( x, 0 )
			intervalRight = knownBestInterval + height

			if knownBestInterval < intervalLeft:
				cache[ x ] = intervalLeft
			if cache.get( x + height, 0 ) < ( knownBestInterval + height ):
				cache[ x + height ] = knownBestInterval + height

			bestTimberInterval = max( bestTimberInterval, intervalLeft, intervalRight )

		return bestTimberInterval

class TimberTest( unittest.TestCase ):
	def test_Timber( self ):
		for testcaseFile in ('sample', 'timber'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.out'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, maximumTimberInterval = line.strip().split()
				solutionList.append( int( maximumTimberInterval ) )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			T = int( inputFile.readline().strip() )
			for _ in range( T ):
				N = int( inputFile.readline().strip() )
				treePositionList = list()
				for _ in range( N ):
					x, height = map( int, inputFile.readline().strip().split() )
					treePositionList.append( (x, height) )

				maximumTimberInterval = solutionList[ index ]
				index += 1

				print( 'Testcase: {}#{} Number of trees = {}'.format( testcaseFile, index, N ) )
				self.assertEqual( Timber( N, treePositionList ).maximumTimberInterval(), maximumTimberInterval )

if __name__ == '__main__':
	unittest.main()