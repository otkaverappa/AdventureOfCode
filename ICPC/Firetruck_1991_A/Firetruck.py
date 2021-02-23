import unittest
import copy

class FireTruck:
	def __init__( self, adjacentLocations, destination ):
		self.pathDict = dict()
		for (u, v) in adjacentLocations:
			if u not in self.pathDict:
				self.pathDict[ u ] = list()
			if v not in self.pathDict:
				self.pathDict[ v ] = list()
			self.pathDict[ u ].append( v )
			self.pathDict[ v ].append( u )

		self.destination = destination
		self.source = 1

	def pathList( self ):
		fireTruckPathList = list()

		stack = list()
		stack.append( ( [ self.source ] ) )

		while len( stack ) > 0:
			currentPath = stack.pop()

			previousVertex = currentPath[ -1 ]
			if previousVertex == self.destination:
				fireTruckPathList.append( currentPath )
				continue

			for nextVertex in self.pathDict.get( previousVertex, list() ):
				if nextVertex in currentPath:
					continue
				newPath = copy.deepcopy( currentPath )
				newPath.append( nextVertex )
				stack.append( newPath )

		return fireTruckPathList

class FireTruckTest( unittest.TestCase ):
	def test_pathListSample( self ):
		adjacentLocations = [ (1, 2), (1, 3), (3, 4), (3, 5), (4, 6), (5, 6), (2, 3), (2, 4) ]
		destination = 6
		expectedPathList = [
		[ 1, 2, 3, 4, 6 ],
		[ 1, 2, 3, 5, 6 ],
		[ 1, 2, 4, 3, 5, 6 ],
		[ 1, 2, 4, 6 ],
		[ 1, 3, 2, 4, 6 ],
		[ 1, 3, 4, 6 ],
		[ 1, 3, 5, 6 ]
		]
		self._compare( FireTruck( adjacentLocations, destination ).pathList(), expectedPathList )

		adjacentLocations = [ (2, 3), (3, 4), (5, 1), (1, 6), (7, 8), (8, 9), (2, 5), (5, 7), (3, 1), (1, 8), (4, 6), (6, 9) ]
		destination = 4
		expectedPathList = [
		[ 1, 3, 2, 5, 7, 8, 9, 6, 4 ],
		[ 1, 3, 4 ],
		[ 1, 5, 2, 3, 4 ],
		[ 1, 5, 7, 8, 9, 6, 4 ],
		[ 1, 6, 4 ],
		[ 1, 6, 9, 8, 7, 5, 2, 3, 4 ],
		[ 1, 8, 7, 5, 2, 3, 4 ],
		[ 1, 8, 9, 6, 4 ]
		]
		self._compare( FireTruck( adjacentLocations, destination ).pathList(), expectedPathList )

		adjacentLocations = [ (1, 8), (2, 11), (3, 4), (3, 6), (4, 14), (5, 6), (5, 8), (6, 11), (6, 12), (8, 14), (9, 14), (10, 14), (11, 14) ]
		destination = 14
		expectedPathList = [
		[ 1, 8, 5, 6, 3, 4, 14 ],
		[ 1, 8, 5, 6, 11, 14 ],
		[ 1, 8, 14 ]
		]
		self._compare( FireTruck( adjacentLocations, destination ).pathList(), expectedPathList )

	def test_pathList( self ):
		fireTruckList = list()
		with open( 'tests/firetruck.in' ) as inputFile:
			while True:
				header = inputFile.readline().strip()
				if len( header ) == 0:
					break
				destination = int( header )
				adjacentLocations = list()
				while True:
					x, y = map( int, inputFile.readline().strip().split() )
					if x == 0 and y == 0:
						break
					adjacentLocations.append( (x, y) )
				fireTruckList.append( FireTruck( adjacentLocations, destination ) )

		index = 0
		with open( 'tests/firetruck.ans' ) as solutionFile:
			currentPathList = list()
			for line in solutionFile.readlines():
				line = line.strip()
				if 'CASE' in line:
					currentPathList.clear()
				elif 'routes' in line:
					print( 'Testcase {} Expected path list length = {}'.format( index + 1, len( currentPathList ) ) )
					self._compare( fireTruckList[ index ].pathList(), currentPathList )
					index += 1
				else:
					currentPathList.append( list( map( int, line.split() ) ) )

	def _compare( self, calculatedPathList, expectedPathList ):
		self.assertEqual( len( calculatedPathList ), len( expectedPathList ) )
		calculatedPathSet = set( [ '#'.join( map( str, path ) ) for path in calculatedPathList ] )
		expectedPathSet = set( [ '#'.join( map( str, path ) ) for path in expectedPathList ] )
		self.assertEqual( calculatedPathSet, expectedPathSet )

if __name__ == '__main__':
	unittest.main()