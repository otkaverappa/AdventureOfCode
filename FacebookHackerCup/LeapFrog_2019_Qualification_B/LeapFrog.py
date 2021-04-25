import unittest

class LeapFrog:
	@staticmethod
	def jump( initialState ):
		N = len( initialState )
		betaFrogCount = initialState.count( 'B' )

		minimumBetaFrogsRequired = N // 2
		maximumBetaFrogs = N - 2

		jumpPossible = minimumBetaFrogsRequired <= betaFrogCount <= maximumBetaFrogs
		# Additional condition if the alpha frog can move in either direction.
		if not jumpPossible:
			jumpPossible = 2 <= betaFrogCount < minimumBetaFrogsRequired
		return 'Y' if jumpPossible else 'N'

class LeapFrogTest( unittest.TestCase ):
	def test_LeapFrogSample( self ):
		testcases = [
		('A.', 'N'), ('AB.', 'Y'), ('ABB', 'N'), ('A.BB', 'Y'),
		('A..BB..B', 'Y'), ('A.B..BBB.', 'Y'), ('AB.........', 'N'), ('A.B..BBBB.BB', 'Y')
		]
		for initialState, expectedResult in testcases:
			self.assertEqual( LeapFrog.jump( initialState ), expectedResult )

	def test_LeapFrog( self ):
		testFile = 'leapfrog2'

		initialStateList = list()
		with open( 'tests/{}.in'.format( testFile ) ) as inputFile:
			N = int( inputFile.readline().strip() )
			for _ in range( N ):
				initialStateList.append( inputFile.readline().strip() )

		expectedResultList = list()
		with open( 'tests/{}.out'.format( testFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, jumpPossible = line.strip().split()
				expectedResultList.append( jumpPossible )

		self.assertEqual( len( initialStateList ), len( expectedResultList ) )

		for i, initialState in enumerate( initialStateList ):
			expectedResult = expectedResultList[ i ]
			print( 'Testcase #{} length = {} jumpPossible ? {}'.format( i + 1, len( initialState ), expectedResult ) )
			self.assertEqual( LeapFrog.jump( initialState ), expectedResult )

if __name__ == '__main__':
	unittest.main()