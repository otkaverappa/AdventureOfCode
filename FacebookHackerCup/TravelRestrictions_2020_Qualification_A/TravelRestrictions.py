import unittest
import itertools

class TravelRestrictions:
	def __init__( self, N, airlineData ):
		self.N = N
		self.airlineData = airlineData

	def analyze( self ):
		incomingIndex, outgoingIndex = 0, 1
		connectionMartix = [ [ False for _ in range( self.N ) ] for _ in range( self.N )
		]

		for i in range( self.N ):
			j1 = j2 = i
			while j1 - 1 >= 0 and self.airlineData[ outgoingIndex ][ j1 ] == 'Y' and self.airlineData[ incomingIndex ][ j1 - 1 ] == 'Y':
				j1 = j1 - 1
			while j2 + 1 < self.N and self.airlineData[ outgoingIndex ][ j2 ] == 'Y' and self.airlineData[ incomingIndex ][ j2 + 1 ] == 'Y':
				j2 = j2 + 1
			# From i we can go to all cities within [j1, j2]
			j = j1
			while j1 <= j <= j2:
				connectionMartix[ i ][ j ] = True
				j = j + 1

		connectionMartixString = list()
		for rowData in connectionMartix:
			connectionMartixString.append( ''.join( [ 'Y' if element else 'N' for element in rowData ] ) )
		return connectionMartixString

class TravelRestrictionsTest( unittest.TestCase ):
	def test_TravelRestrictions( self ):
		testfileName = 'travel_restrictions'

		allAirlineData = list()

		with open( 'tests/{}.in'.format( testfileName ) ) as inputFile:
			T = int( inputFile.readline().strip() )
			for _ in range( T ):
				columnCount = int( inputFile.readline().strip() )
				airlineData = list()
				airlineData.append( inputFile.readline().strip() )
				airlineData.append( inputFile.readline().strip() )
				allAirlineData.append( (columnCount, airlineData) )

		index = 0
		with open( 'tests/{}.out'.format( testfileName ) ) as solutionFile:
			while index < len( allAirlineData ):
				N, airlineData = allAirlineData[ index ]
				index += 1

				solutionFile.readline()
				expectedSolution = list()
				for _ in range( N ):
					expectedSolution.append( solutionFile.readline().strip() )

				print( 'Testcase #{} N = {}'.format( index, N ) )
				for airlineDataRow in airlineData:
					print( airlineDataRow )

				connectionMartix = TravelRestrictions( N, airlineData ).analyze()
				print( 'Connection Matrix:' )
				for connectionMartixRow in connectionMartix:
					print( connectionMartixRow )

				self.assertEqual( connectionMartix, expectedSolution )

	def test_TravelRestrictions_sample( self ):
		N = 2
		airlineData = [ 'YY', 'YY' ]
		connectionMartix = [
		'YY',
		'YY'
		]
		self.assertEqual( TravelRestrictions( N, airlineData ).analyze(), connectionMartix )

		N = 2
		airlineData = [ 'NY', 'YY' ]
		connectionMartix = [
		'YY',
		'NY'
		]
		self.assertEqual( TravelRestrictions( N, airlineData ).analyze(), connectionMartix )

		N = 2
		airlineData = [ 'NN', 'YY' ]
		connectionMartix = [
		'YN',
		'NY'
		]
		self.assertEqual( TravelRestrictions( N, airlineData ).analyze(), connectionMartix )

		N = 5
		airlineData = [ 'YNNYY', 'YYYNY' ]
		connectionMartix = [
		'YNNNN',
		'YYNNN',
		'NNYYN',
		'NNNYN',
		'NNNYY'
		]
		self.assertEqual( TravelRestrictions( N, airlineData ).analyze(), connectionMartix )

		N = 10
		airlineData = [ 'NYYYNNYYYY', 'YYNYYNYYNY' ]
		connectionMartix = [
		'YYYNNNNNNN',
		'NYYNNNNNNN',
		'NNYNNNNNNN',
		'NNYYNNNNNN',
		'NNYYYNNNNN',
		'NNNNNYNNNN',
		'NNNNNNYYYN',
		'NNNNNNYYYN',
		'NNNNNNNNYN',
		'NNNNNNNNYY'
		]
		self.assertEqual( TravelRestrictions( N, airlineData ).analyze(), connectionMartix )

if __name__ == '__main__':
	unittest.main()