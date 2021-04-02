import unittest
import bisect

class Price:
	def __init__( self, numberList, price ):
		self.numberList = numberList
		self.price = price

	def sequenceCount( self ):
		prefixSumList = self.numberList
		for i in range( 1, len( prefixSumList ) ):
			prefixSumList[ i ] = prefixSumList[ i ] + prefixSumList[ i - 1 ]

		count = 0
		for i in range( len( prefixSumList ) ):
			prefixSum = 0 if i == 0 else prefixSumList[ i - 1 ]
			
			key = self.price + prefixSum
			j = bisect.bisect( prefixSumList, key )
			count += j - i
		return count

class PriceTest( unittest.TestCase ):
	def test_Price( self ):
		solutionList = list()
		with open( 'tests/Price.ans' ) as solutionFile:
			for solutionLine in solutionFile.readlines():
				_, _, count = solutionLine.strip().split()
				solutionList.append( int( count ) )

		with open( 'tests/Price' ) as inputFile:
			testcaseCount = int( inputFile.readline().strip() )
			for i in range( testcaseCount ):
				N, price = map( int, inputFile.readline().strip().split() )
				numberList = list( map( int, inputFile.readline().strip().split() ) )
				assert len( numberList ) == N

				expectedSequenceCount = solutionList[ i ]
				
				print( 'Testcase #{} N = {} Price = {} Number of sequences = {}'.format( i + 1, N, price, expectedSequenceCount ) )
				self.assertEqual( Price( numberList, price ).sequenceCount(), expectedSequenceCount )

if __name__ == '__main__':
	unittest.main()