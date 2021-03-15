import unittest
import heapq

class Cookie:
	def __init__( self, C, F, X ):
		self.C, self.F, self.X = C, F, X
		self.delta = 1e-6

	def _equal( self, A, B ):
		return abs( A - B ) <= self.delta

	def minimumTime( self ):
		timeTaken, cookieCount, cookiePerSecond = 0, 0, 2

		q = list()
		q.append( (timeTaken, cookieCount, cookiePerSecond ) )

		while len( q ) > 0:
			currentTimeTaken, currentCookieCount, currentCookiePerSecond = heapq.heappop( q )
			if self._equal( currentCookieCount, self.X ):
				return currentTimeTaken

			possibleStates = list()
			
			# Don't buy any cookie farm.
			cookiesRequired = self.X - currentCookieCount
			time = currentTimeTaken + ( cookiesRequired / currentCookiePerSecond )
			possibleStates.append( (time, self.X, currentCookiePerSecond) )

			# Buy a cookie farm if currentCookieCount >= self.C
			if currentCookieCount >= self.C:
				possibleStates.append( (currentTimeTaken, currentCookieCount - self.C, currentCookiePerSecond + self.F ) )
			# Wait until we have enough cookies to buy a cookie farm
			else:
				cookiesRequired = self.C - currentCookieCount
				time = currentTimeTaken + ( cookiesRequired / currentCookiePerSecond )
				possibleStates.append( (time, self.C, currentCookiePerSecond) )

			for (newTimeTaken, newCookieCount, newCookiePerSecond) in possibleStates:
				heapq.heappush( q, (newTimeTaken, newCookieCount, newCookiePerSecond) )

class CookieTest( unittest.TestCase ):
	def test_cookie( self ):
		for testcaseFile in ('cookie1', 'cookie2'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( line.strip() )

		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			testcaseCount = int( inputFile.readline().strip() )
			assert len( solutionList ) == testcaseCount

			for i in range( testcaseCount ):
				C, F, X = map( float, inputFile.readline().strip().split() )

				_, _, expectedTime = solutionList[ i ].split()
				expectedTime = float( expectedTime )

				print( 'Testcase {}#{} ({}, {}, {}) minimumTime = {}'.format( testcaseFile, i + 1, C, F, X, expectedTime ) )

				self._compare( Cookie( C, F, X ).minimumTime(), expectedTime )

	def _compare( self, A, B ):
		assert abs( A - B ) <= 1e-6

if __name__ == '__main__':
	unittest.main()