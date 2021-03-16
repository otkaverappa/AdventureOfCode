import unittest
import itertools
from collections import deque

class Robot:
	def __init__( self, rows, cols, layoutMap, numberOfParticles, maximumMoves ):
		self.rows, self.cols = rows, cols
		self.layoutMap = layoutMap
		self.numberOfDustParticles, self.maximumMoves = numberOfParticles, maximumMoves

		self.robotStartPositionTag, self.rechargeStationPositionTag = 'R', 'S'
		self.dustCell, self.emptyCell, self.blockedCell = '*', '.', '#'

		self.robotStartLocation = self.rechargeLocation = None
		dustLocationList = list()

		for row, col in itertools.product( range( rows ), range( cols ) ):
			if layoutMap[ row ][ col ] == self.robotStartPositionTag:
				self.robotStartLocation = (row, col)
			elif layoutMap[ row ][ col ] == self.rechargeStationPositionTag:
				self.rechargeLocation = (row, col)
			elif layoutMap[ row ][ col ] == self.dustCell:
				dustLocationList.append( (row, col) )

		# Assign a unique index to each location where a dust particle is present. This index corresponds
		# to the bit number for the dust particle in 'dustBitmap'.
		self.dustLocationMap = dict()
		for i, dustLocation in enumerate( dustLocationList ):
			self.dustLocationMap[ dustLocation ] = i

	def _setDustParticleLocation( self, bitmap, dustLocation ):
		bitmap = bitmap | ( 1 << self.dustLocationMap[ dustLocation ] )
		return bitmap

	def _numberOfDustParticleLocations( self, bitmap ):
		return bin( bitmap ).count( '1' )

	def _isOutsideLayout( self, cell ):
		row, col = cell
		return row < 0 or row >= self.rows or col < 0 or col >= self.cols

	def _calculateDistanceFromRechargeStation( self, distanceMap ):
		q = deque()
		q.append( self.rechargeLocation )

		visited = set()
		visited.add( self.rechargeLocation )

		distance = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1
				u, v = cell = q.popleft()

				distanceMap[ u ][ v ] = distance

				for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
					newCell = x, y = u + du, v + dv
					if self._isOutsideLayout( newCell ) or self.layoutMap[ x ][ y ] == self.blockedCell:
						continue
					if newCell not in visited:
						visited.add( newCell )
						q.append( newCell )
			distance += 1

	def move( self ):
		distanceMap = [ [ self.maximumMoves + 1 for _ in range( self.cols ) ] for _ in range( self.rows ) ]
		self._calculateDistanceFromRechargeStation( distanceMap )

		location, dustBitmap, numberOfMoves = self.robotStartLocation, 0, 0
		q = deque()
		q.append( (location, dustBitmap, numberOfMoves) )

		visited = set()
		visited.add( (location, dustBitmap) )

		bestDustCollection = None
		while len( q ) > 0:
			robotLocation, dustBitmap, numberOfMoves = q.popleft()

			u, v = robotLocation
			if numberOfMoves + distanceMap[ u ][ v ] > self.maximumMoves:
				continue
 
			dustCollectedSoFar = self._numberOfDustParticleLocations( dustBitmap )
			if bestDustCollection is None or dustCollectedSoFar > bestDustCollection:
				bestDustCollection = dustCollectedSoFar

			if dustCollectedSoFar == self.numberOfDustParticles:
				break

			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				newLocation = x, y = u + du, v + dv
				if self._isOutsideLayout( newLocation ) or self.layoutMap[ x ][ y ] == self.blockedCell:
					continue
				newMoveCount = numberOfMoves + 1
				newDustBitmap = dustBitmap
				if self.layoutMap[ x ][ y ] == self.dustCell:
					newDustBitmap = self._setDustParticleLocation( newDustBitmap, (x, y) )
				if (newLocation, newDustBitmap) not in visited:
					visited.add( (newLocation, newDustBitmap) )
					q.append( (newLocation, newDustBitmap, newMoveCount) )
		return bestDustCollection

class RobotTest( unittest.TestCase ):
	def test_vaccum( self ):
		solutionList = list()
		with open( 'tests/robot.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				steps = int( line.strip() )
				solutionList.append( None if steps == -1 else steps )

		index = 0
		with open( 'tests/robot.in' ) as inputFile:
			while True:
				header = inputFile.readline().strip()
				if len( header ) == 0:
					break
				numberOfParticles, maximumMoves = map( int, header.split() )
				cols, rows = map( int, inputFile.readline().strip().split() )

				layoutMap = list()
				for _ in range( rows ):
					layoutMap.append( inputFile.readline().strip() )

				expectedSolution = solutionList[ index ]
				index += 1

				formatString = 'Testcase {} rows = {} cols {} Dust particles that can be collected = {}'
				print( formatString.format( index, rows, cols, expectedSolution ) )

				self.assertEqual( Robot( rows, cols, layoutMap, numberOfParticles, maximumMoves ).move(), expectedSolution ) 

if __name__ == '__main__':
	unittest.main()