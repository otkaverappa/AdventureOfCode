import unittest
import itertools

class Gold:
	def __init__( self, rows, cols, layoutMap ):
		self.rows, self.cols = rows, cols
		self.layoutMap = layoutMap
		self.emptyCell, self.wallCell, self.startCell, self.goldCell, self.trapCell = '.', '#', 'P', 'G', 'T'

		self.startLocation = None
		self.goldLocationCount = 0
		for (row, col) in itertools.product( range( self.rows ), range( self.cols ) ):
			cellType = self.layoutMap[ row ][ col ]
			if cellType == self.startCell:
				self.startLocation = (row, col)
			elif cellType == self.goldCell:
				self.goldLocationCount += 1 
		assert self.startLocation is not None

	def maximumGold( self ):
		stack = list()
		stack.append( self.startLocation )

		visited = set()
		visited.add( self.startLocation )

		goldCollected = 0

		while len( stack ) > 0:
			u, v = stack.pop()
			if self.layoutMap[ u ][ v ] == self.goldCell:
				goldCollected += 1

			possibleCellsToMove = list()
			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				x, y = u + du, v + dv
				if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
					continue
				if self.layoutMap[ x ][ y ] == self.trapCell:
					possibleCellsToMove.clear()
					break
				if self.layoutMap[ x ][ y ] != self.wallCell:
					possibleCellsToMove.append( (x, y) )

			for cell in possibleCellsToMove:
				if cell not in visited:
					visited.add( cell )
					stack.append( cell )

		return goldCollected

class GoldTest( unittest.TestCase ):
	def test_sample( self ):
		rows, cols = 4, 7
		layoutMap = [
		'#######',
		'#P.GTG#',
		'#..TGG#',
		'#######'
		]
		self.assertEqual( Gold( rows, cols, layoutMap ).maximumGold(), 1 )

		rows, cols = 6, 8
		layoutMap = [
		'########',
		'#...GTG#',
		'#..PG.G#',
		'#...G#G#',
		'#..TG.G#',
		'########'
		]
		self.assertEqual( Gold( rows, cols, layoutMap ).maximumGold(), 4 )

	def test_maximumGold( self ):
		solutionList = list()
		with open( 'tests/gold.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line ) )

		index = 0
		with open( 'tests/gold.in' ) as inputFile:
			while True:
				header = inputFile.readline().strip()
				if len( header ) == 0:
					break

				cols, rows = map( int, header.split() )
				layoutMap = list()
				for _ in range( rows ):
					layoutMap.append( inputFile.readline().strip() )

				gold = Gold( rows, cols, layoutMap )
				maximumGold = solutionList[ index ]
				index += 1

				print( 'Testcase #{} rows = {} cols = {} Maximum gold that can be collected = {}'.format( index, rows, cols, maximumGold ) )
				self.assertEqual( gold.maximumGold(), maximumGold )

if __name__ == '__main__':
	unittest.main()