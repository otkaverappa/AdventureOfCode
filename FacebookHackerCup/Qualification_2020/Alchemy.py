import unittest

class Alchemy:
	@staticmethod
	def analyze( inputString ):
		return 'Y' if abs( inputString.count( 'A' ) - inputString.count( 'B' ) ) == 1 else 'N'

class AlchemyTest( unittest.TestCase ):
	def test_Alchemy_sample( self ):
		testcases = [
		('BAB', 'Y'), ('BBB', 'N'),
		('AABBA', 'Y'), ('BAAABAA', 'N'),
		('BBBAABAAAAB', 'Y'), ('BABBBABBABB', 'N')
		]

		for inputString, expectedSolution in testcases:
			self.assertEqual( Alchemy.analyze( inputString ), expectedSolution )

	def test_Alchemy( self ):
		testcaseFile = 'Alchemy'

		inputStringList = list()
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			T = int( inputFile.readline().strip() )
			for _ in range( T ):
				inputFile.readline()
				inputStringList.append( inputFile.readline().strip() )

		solutionList = list()
		with open( 'tests/{}.out'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				_, _, status = line.strip().split()
				solutionList.append( status )

		self.assertEqual( len( inputStringList ), len( solutionList ) )
		for i in range( len( inputStringList ) ):
			inputString, expectedSolution = inputStringList[ i ], solutionList[ i ]

			print( 'Testcase #{} inputString = {} possible ? {}'.format( i + 1, inputString, expectedSolution ) )
			self.assertEqual( Alchemy.analyze( inputString ), expectedSolution )

if __name__ == '__main__':
	unittest.main()