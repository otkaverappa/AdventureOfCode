import unittest
import itertools

class Labyrinth:
	def __init__( self, labyrinthMap ):
		self.labyrinthMap = labyrinthMap
		self.rows, self.cols = len( labyrinthMap ), len( labyrinthMap[ 0 ] )
		self.wall, self.emptySpace = '#', '.'
		self.dotCount = 0

	def longestPath( self ):
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.labyrinthMap[ row ][ col ] == self.emptySpace:
				root = (row, col)
				break

		self._depth( root, None )
		return self.dotCount - 1

	def _getAdjacentCellList( self, currentLocation, parentLocation ):
		adjacentCellList = list()

		row, col = currentLocation
		for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
			u, v = location = row + du, col + dv
			if not 0 <= u < self.rows or not 0 <= v < self.cols:
				continue
			if self.labyrinthMap[ u ][ v ] == self.wall:
				continue
			if location == parentLocation:
				continue
			adjacentCellList.append( location )
		return adjacentCellList

	def _depth( self, currentLocation, parentLocation ):
		stack = list()
		stack.append( (currentLocation, parentLocation, None, 'new') )
		
		depth = None
		while len( stack ) > 0:
			currentLocation, parentLocation, depthList, tag = stack.pop()
			if tag == 'new':
				adjacentCellList = self._getAdjacentCellList( currentLocation, parentLocation )

				# If there are no adjacent cells, then we are at a leaf node. Otherwise,
				# we need to recursively get the depth of each adjacent cell.
				if len( adjacentCellList ) == 0:
					depth = 1
				else:
					newDepthList = list()
					stack.append( (currentLocation, parentLocation, newDepthList, 'return') )

				for adjacentCell in adjacentCellList:
					stack.append( (currentLocation, parentLocation, newDepthList, 'return-intermediate') )
					stack.append( (adjacentCell, currentLocation, None, 'new') )
			elif tag == 'return-intermediate':
				depthList.append( depth )
			elif tag == 'return':
				# depthList contains the depth returned by recursive calls.
				depth, dotCount = 1, 0
				if len( depthList ) > 0:
					depth = max( depthList ) + 1
				if len( depthList ) > 1:
					depthList.sort( reverse=True )
					D1, D2, * _ = depthList
					dotCount = D1 + D2 + 1
				self.dotCount = max( self.dotCount, dotCount, depth )

class LabyrinthTest( unittest.TestCase ):
	def test_Labyrinth_sample( self ):
		labyrinthMap = [
		'.#...',
		'...##',
		'.#..#',
		'.##..',
		'#####'
		]
		self.assertEqual( Labyrinth( labyrinthMap ).longestPath(), 8 )

		labyrinthMap = [
		'.....',
		'####.',
		'.....',
		'.####',
		'.....'
		]
		self.assertEqual( Labyrinth( labyrinthMap ).longestPath(), 16 )

	def _render( self, labyrinthMap ):
		print( 'Labyrinth Map:' )
		for labyrinthMapString in labyrinthMap:
			print( labyrinthMapString )
		print()

	def test_Labyrinth( self ):
		solutionList = list()
		with open( 'tests/labyrinth.out' ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line.strip() ) )

		index = 0
		with open( 'tests/labyrinth.in' ) as inputFile:
			while True:
				rows, cols = map( int, inputFile.readline().strip().split() )
				if rows == 0 and cols == 0:
					break
				labyrinthMap = list()
				for _ in range( rows ):
					labyrinthMap.append( inputFile.readline().strip() )

				expectedPathLength = solutionList[ index ]
				index += 1

				print( 'Testcase #{} rows = {} cols = {} expectedPathLength = {}'.format( index, rows, cols, expectedPathLength ) )
				pathLength = Labyrinth( labyrinthMap ).longestPath()
				self._render( labyrinthMap )

				self.assertEqual( pathLength, expectedPathLength )

if __name__ == '__main__':
	unittest.main()