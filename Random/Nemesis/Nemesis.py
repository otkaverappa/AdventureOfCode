import unittest
import heapq
import itertools

class Nemesis:
	def __init__( self, rows, cols, layoutMap ):
		self.rows, self.cols = rows, cols
		self.layoutMap = layoutMap

		self.startLocationToken, self.targetLocationToken = 'H', 'E'
		self.emptySpaceToken, self.blockedToken = '.', '#'

		self.zeroEnergyCellToken = set( [ self.emptySpaceToken, self.startLocationToken, self.targetLocationToken ] )

		self.startCell = self.targetCell = None
		for (row, col) in itertools.product( range( rows ), range( cols ) ):
			token = self.layoutMap[ row ][ col ]
			if token == self.startLocationToken:
				self.startCell = (row, col)
			elif token == self.targetLocationToken:
				self.targetCell = (row, col)
		assert self.startCell is not None and self.targetCell is not None

	def _getEnergyRequired( self, cell ):
		row, col = cell
		token = self.layoutMap[ row ][ col ]
		return 0 if token in self.zeroEnergyCellToken else int( token )

	def _minimumEnergy( self ):
		bestCostDict = dict()
		bestCostDict[ self.startCell ] = 0

		priorityQueue = list()
		priorityQueue.append( (0, self.startCell) )

		while len( priorityQueue ) > 0:
			energyConsumed, currentCell = heapq.heappop( priorityQueue )
			if currentCell == self.targetCell:
				return energyConsumed

			u, v = currentCell
			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				adjacentCell = x, y = u + du, v + dv
				if not 0 <= x < self.rows or not 0 <= y < self.cols:
					continue
				token = self.layoutMap[ x ][ y ]
				if token == self.blockedToken:
					continue
				energyNeeded = self._getEnergyRequired( adjacentCell )
				totalEnergyConsumed = energyConsumed + energyNeeded
				if adjacentCell not in bestCostDict or totalEnergyConsumed < bestCostDict[ adjacentCell ]:
					bestCostDict[ adjacentCell ] = totalEnergyConsumed
					heapq.heappush( priorityQueue, (totalEnergyConsumed, adjacentCell) )
		return None

	def minimumEnergy( self ):
		_minimumEnergy = self._minimumEnergy()
		return _minimumEnergy if _minimumEnergy is not None else 'ARTSKJID'

class NemesisTest( unittest.TestCase ):
	def test_Nemesis( self ):
		rows, cols = 3, 10
		layoutMap = [
		'.138764..2',
		'7H###19##2',
		'.23#61.E#2'
		]
		self.assertEqual( Nemesis( rows, cols, layoutMap ).minimumEnergy(), 27 )

		rows, cols = 2, 2
		layoutMap = [
		'E#',
		'#H'
		]
		self.assertEqual( Nemesis( rows, cols, layoutMap ).minimumEnergy(), 'ARTSKJID' )

		rows, cols = 2, 2
		layoutMap = [
		'H2',
		'2E'
		]
		self.assertEqual( Nemesis( rows, cols, layoutMap ).minimumEnergy(), 2 )

		for testcaseFile in ('map1', 'map2', 'map3'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		expectedMinimumEnergy = None
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			expectedMinimumEnergy = int( solutionFile.readline().strip() )

		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			rows, cols = map( int, inputFile.readline().strip().split() )
			layoutMap = list()
			for _ in range( rows ):
				layoutMap.append( inputFile.readline().strip() )

			minimumEnergy = Nemesis( rows, cols, layoutMap ).minimumEnergy()

			self.assertEqual( minimumEnergy, expectedMinimumEnergy )

if __name__ == '__main__':
	unittest.main()