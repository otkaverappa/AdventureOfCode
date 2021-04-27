import unittest

class Tourist:
	def __init__( self, attractionList, K, V ):
		self.attractionList = attractionList
		self.K, self.V = K, V

	def visit( self ):
		N = len( self.attractionList )
		i = ( self.K * ( self.V - 1 ) ) % N

		offset = 0
		if i + self.K >= N:
			offset = ( i + self.K ) % N
		return self.attractionList[ : offset ] + self.attractionList[ i : i + self.K ]

class TouristTest( unittest.TestCase ):
	def test_Tourist_sample( self ):
		attractionList = [ 'LikeSign', 'Arcade', 'SweetStop', 'SwagStore' ]
		K, V = 1, 3
		expectedSolution = [ 'SweetStop' ]
		self.assertEqual( Tourist( attractionList, K, V ).visit(), expectedSolution )

		attractionList = [ 'FoxGazebo', 'MPK20Roof', 'WoodenSculpture', 'Biryani' ]
		K, V = 4, 100
		expectedSolution = [ 'FoxGazebo', 'MPK20Roof', 'WoodenSculpture', 'Biryani' ]
		self.assertEqual( Tourist( attractionList, K, V ).visit(), expectedSolution )

		attractionList = [ 'LikeSign', 'Arcade', 'SweetStop', 'SwagStore' ]
		K, V = 3, 1
		expectedSolution = [ 'LikeSign', 'Arcade', 'SweetStop' ]
		self.assertEqual( Tourist( attractionList, K, V ).visit(), expectedSolution )

		K, V = 3, 3
		expectedSolution = [ 'LikeSign', 'SweetStop', 'SwagStore' ]
		self.assertEqual( Tourist( attractionList, K, V ).visit(), expectedSolution )

		K, V = 3, 10
		expectedSolution = [ 'LikeSign', 'Arcade', 'SwagStore' ]
		self.assertEqual( Tourist( attractionList, K, V ).visit(), expectedSolution )

		attractionList = [ 'RainbowStairs' ,'WallOfPhones' ]
		K, V = 1, 1000000000000
		expectedSolution = [ 'WallOfPhones' ]
		self.assertEqual( Tourist( attractionList, K, V ).visit(), expectedSolution )

	def test_Tourist( self ):
		testcaseFile = 'tourist'

		solutionList = list()
		with open( 'tests/{}.out'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, * attractionList = line.strip().split()
				solutionList.append( attractionList )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			T = int( inputFile.readline().strip() )
			for _ in range( T ):
				N, K, V = map( int, inputFile.readline().strip().split() )
				attractionList = list()
				for _ in range( N ):
					attractionList.append( inputFile.readline().strip() )

				expectedSolution = solutionList[ index ]
				index += 1

				print( 'Testcase #{} Total attractions = {} K = {} Visit #{}'.format( index, N, K, V ) )
				self.assertEqual( Tourist( attractionList, K, V ).visit(), expectedSolution )

if __name__ == '__main__':
	unittest.main()