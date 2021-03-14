import unittest
import math
import heapq

class BumpyRobot:
	def __init__( self, rows, cols, grid, startLocation, targetLocation, parameterList ):
		self.rows, self.cols = rows, cols
		self.grid = grid
		self.alpha1, self.alpha2, self.gamma, self.beta1, self.beta2, self.delta, self.energy = parameterList
		self.startLocation = startLocation
		self.targetLocation = targetLocation

	def move( self ):
		q = list()
		q.append( ((0, 0), self.startLocation) )

		energyTimeDict = dict()
		energyTimeDict[ self.startLocation ] = (0, 0)

		while len( q ) > 0:
			(timeTaken, energyUtilized), location = heapq.heappop( q )
			if location == self.targetLocation:
				return timeTaken

			u, v = location
			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				newLocation = x, y = u + du, v + dv
				if not 0 <= x < self.rows or not 0 <= y < self.cols:
					continue
				h1, h2 = self.grid[ u ][ v ], self.grid[ x ][ y ]
				timeNeeded, energyNeeded = self._timeAndEnergy( h1, h2 )
				if energyUtilized + energyNeeded > self.energy:
					continue
				
				timeAndEnergy = totalTime, totalEnergy = timeTaken + timeNeeded, energyUtilized + energyNeeded
				if newLocation not in energyTimeDict or timeAndEnergy < energyTimeDict[ newLocation ]:
					energyTimeDict[ newLocation ] = timeAndEnergy
					heapq.heappush( q, (timeAndEnergy, newLocation) )
				else:
					# We have examine the current state when the energy requirement is better than the known
					# energy requirement, even when the time taken is higher than the known time taken.
					knownTime, knownEnergy = energyTimeDict[ newLocation ]
					if totalTime > knownTime and totalEnergy < knownEnergy:
						heapq.heappush( q, (timeAndEnergy, newLocation ) )
		return None

	def _timeAndEnergy( self, h1, h2 ):
		if h1 == h2:
			return self.delta, self.gamma
		elif h1 > h2:
			return math.ceil( self.beta1 * (h1 - h2) ) + self.delta, math.ceil( self.alpha1 * (h1 - h2) ) + self.gamma
		else:
			return math.ceil( self.beta2 * (h2 - h1) ) + self.delta, math.ceil( self.alpha2 * (h2 - h1) ) + self.gamma

class BumpyRobotTest( unittest.TestCase ):
	def test_bumpyRobot( self ):
		solutionList = list()
		with open( 'tests/bumpy.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				solutionList.append( int( line ) if line != 'failed' else None )

		index = 0
		with open( 'tests/bumpy.in' ) as inputFile:
			while True:
				M, N = map( int, inputFile.readline().strip().split() )
				if M == 0 and N == 0:
					break
				alpha1, alpha2, gamma = inputFile.readline().strip().split()
				beta1, beta2, delta = inputFile.readline().strip().split()
				
				alpha1, alpha2, beta1, beta2 = float( alpha1 ), float( alpha2 ), float( beta1 ), float( beta2 )
				gamma, delta = int( gamma ), int( delta )

				grid = list()
				for _ in range( M ):
					grid.append( list( map( int, inputFile.readline().strip().split() ) ) )

				sourceRow, sourceCol, targetRow, targetCol, energy = map( int, inputFile.readline().strip().split() )

				parameterList = (alpha1, alpha2, gamma, beta1, beta2, delta, energy)
				bumpyRobot = BumpyRobot( M, N, grid, (sourceRow - 1, sourceCol - 1), (targetRow - 1, targetCol - 1), parameterList )

				expectedTimeTaken = solutionList[ index ]
				index += 1

				formatString = 'Testcase #{} Rows = {} Cols = {} Energy = {} Expected time = {}'
				print( formatString.format( index, M, N, energy, expectedTimeTaken ) )
				
				self.assertEqual( bumpyRobot.move(), expectedTimeTaken )

if __name__ == '__main__':
	unittest.main()