import unittest
from collections import deque
import heapq

class Rose:
	def __init__( self, roseGarden ):
		self.size = len( roseGarden )
		self.roseGarden = roseGarden
		self._verify()

	def _verify( self ):
		assert self.size % 2 == 1
		for roseGardenRow in self.roseGarden:
			assert len( roseGardenRow ) == self.size
		assert self.roseGarden[ self.size // 2 ][ self.size // 2 ] == 'P'

	def _atEdge( self, x, y ):
		return x in (0, self.size - 1) or y in (0, self.size - 1)

	def minimumRosesTrampled( self ):
		M = self.size // 2
		rosesTrampled = (0, 0, 0, 0)
		startPosition = (M, M)

		q = list()
		q.append( (max( rosesTrampled ), rosesTrampled, startPosition) )

		rosesTrampledCount = dict()

		while len( q ) > 0:
			maximumRosesTrampled, rosesTrampled, currentPosition = heapq.heappop( q )

			x, y = currentPosition
			if self._atEdge( x, y ):
				return maximumRosesTrampled

			if currentPosition in rosesTrampledCount and rosesTrampledCount[ currentPosition ] < maximumRosesTrampled:
				continue
			key = currentPosition, rosesTrampled
			rosesTrampledCount[ key ] = maximumRosesTrampled

			r1, r2, r3, r4 = rosesTrampled
			for dx, dy, direction in [ (-1, 0, 'up'), (0, 1, 'right'), (0, -1, 'left'), (1, 0, 'down') ]:
				if self.roseGarden[ x ][ y ] == 'P' and direction != 'up':
					continue

				newPosition = u, v = x + dx, y + dy
				delta_x, delta_y = u - M, v - M
				
				A = M - delta_x, M - delta_y
				B = M - delta_y, M + delta_x
				C = M + delta_y, M - delta_x

				rosePresentList = list()
				for m, n in [ newPosition, A, B, C ]:
					rosePresentList.append( 1 if self.roseGarden[ m ][ n ] == 'R' else 0 )
				x1, x2, x3, x4 = tuple( rosePresentList )

				newRosesTrampledTuple = r1 + x1, r2 + x2, r3 + x3, r4 + x4
				key = newPosition, newRosesTrampledTuple
				if key in rosesTrampledCount and rosesTrampledCount[ key ] <= max( newRosesTrampledTuple ):
					continue
				heapq.heappush( q, (max( newRosesTrampledTuple ), newRosesTrampledTuple, newPosition) )

class RoseTest( unittest.TestCase ):
	def _render( self, roseGarden ):
		for roseGardenRow in roseGarden:
			print( roseGardenRow )
		print()

	def test_minimumRosesTrampled( self ):
		roseGarden = [
		'.RRR.',
		'R.R.R',
		'R.P.R',
		'R.R.R',
		'.RRR.'
		]
		self.assertEqual( Rose( roseGarden ).minimumRosesTrampled(), 2 )

		expectedResultList = list()
		with open( 'tests/rose.ans' ) as solutionFile:
			for inputLine in solutionFile.readlines():
				expectedResultList.append( int( inputLine.strip() ) )

		index = 0
		with open( 'tests/rose.in' ) as inputFile:
			while True:
				size = int( inputFile.readline().strip() )
				if size == 0:
					break

				roseGarden = list()
				for _ in range( size ):
					roseGarden.append( inputFile.readline().strip() )

				expectedResult = expectedResultList[ index ]
				print( 'Processing Rose Garden : {} minimumRosesTrampled = {}'.format( index + 1, expectedResult ) )
				self._render( roseGarden )
				self.assertEqual( Rose( roseGarden ).minimumRosesTrampled(), expectedResultList[ index ] )
				index += 1

if __name__ == '__main__':
	unittest.main() 