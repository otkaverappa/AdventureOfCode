import unittest

class Cookie:
	def __init__( self, C, F, X ):
		self.C, self.F, self.X = C, F, X
		self.delta = 1e-6

	def _equal( self, A, B ):
		return abs( A - B ) <= self.delta

	def minimumTime( self ):
		timeTaken, cookieCount, cookiePerSecond = 0, 0, 2

		if self._equal( cookieCount, self.X ):
			return timeTaken

		while True:
			cookiesRequired = self.X - cookieCount

			# Don't buy any cookie farm.
			A = ( cookiesRequired / cookiePerSecond )

			# Buy a cookie farm.
			B1 = ( self.C - cookieCount ) / cookiePerSecond
			# Then buy the required number of cookies.
			B2 = cookiesRequired / ( cookiePerSecond + self.F )

			if A < B1 + B2:
				timeTaken += A
				return timeTaken
			timeTaken += B1
			cookiePerSecond += self.F

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