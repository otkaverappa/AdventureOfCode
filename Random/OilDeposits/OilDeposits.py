import unittest
import itertools

class OilDeposit:
	def __init__( self, rows, cols, areaMap ):
		self.rows, self.cols = rows, cols
		self.areaMap = areaMap
		
		self.oilCellType = '@'

	def _searchOil( self, row, col, visited ):
		stack = list()

		stack.append( (row, col) )
		visited.add( (row, col) )

		while len( stack ) > 0:
			row, col = stack.pop()

			for du, dv in itertools.product( range( -1, 2 ), range( -1, 2 ) ):
				if du == 0 and dv == 0:
					continue
				u, v = row + du, col + dv
				if 0 <= u < self.rows and 0 <= v < self.cols and self.areaMap[ u ][ v ] == self.oilCellType and (u, v) not in visited:
					visited.add( (u, v) )
					stack.append( (u, v) )

	def deposit( self ):
		visited = set()

		areaCount = 0
		for (row, col) in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.areaMap[ row ][ col ] == self.oilCellType and (row, col) not in visited:
				self._searchOil( row, col, visited )
				areaCount += 1
		return areaCount

class OilDepositTest( unittest.TestCase ):
	def test_deposit( self ):
		for testcaseFile in ('oil1', 'oil2'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line.strip() ) )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			while True:
				rows, cols = map( int, inputFile.readline().strip().split() )
				if rows == 0 and cols == 0:
					break

				areaMap = list()
				for _ in range( rows ):
					areaMap.append( inputFile.readline().strip() )

				oilDeposit = OilDeposit( rows, cols, areaMap )
				expectedAreaCount = solutionList[ index ]
				index += 1

				print( 'Testcase {}#{} rows = {} cols = {} Expected area count = {}'.format( testcaseFile, index, rows, cols, expectedAreaCount ) )
				self.assertEqual( oilDeposit.deposit(), expectedAreaCount )

if __name__ == '__main__':
	unittest.main()