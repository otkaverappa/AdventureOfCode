import unittest
import heapq

class Routing:
	def __init__( self, N, edgeList ):
		self.sourceVertex, self.targetVertex = 1, 2
		self.adjacencyList = [ list() for _ in range( N + 1 ) ]
		for u, v in edgeList:
			self.adjacencyList[ u ].append( v )

	def _getPriority( self, state ):
		pathA, pathB, _ = state
		verticesInPathA = set( pathA.split( '#' ) )
		verticesInPathB = set( pathB.split( '#' ) )

		if str() in verticesInPathB:
			verticesInPathB.remove( str() )
		return len( set.union( verticesInPathA, verticesInPathB ) )

	def minimumNodes( self ):
		# State is a tuple with three elements - (A, B, t)
		# A is the forward path from vertex 1 to vertex 2
		# B is the reverse path from vertex 2 to vertex 1. We start computing B only after path A has been found.
		# t is a boolean - True indicates path A has been found.

		initialState = str( self.sourceVertex ), str(), False
		q = list()
		q.append( (self._getPriority( initialState ), initialState) )

		visited = set()
		visited.add( initialState )

		def _getPreviousVertex( path ):
			return int( path.split( '#' )[ -1 ] )

		def _isVertexAlreadyVisited( path, vertex ):
			return str( vertex ) in path.split( '#' )

		while len( q ) > 0:
			priority, currentState = heapq.heappop( q )

			pathA, pathB, pathAFound = currentState
			currentPath = pathB if pathAFound else pathA
			previousVertex = _getPreviousVertex( currentPath )

			if pathAFound and previousVertex == self.sourceVertex:
				return priority

			if not pathAFound and previousVertex == self.targetVertex:
				newState = pathA, str( self.targetVertex ), True
				heapq.heappush( q, (priority, newState) )
				continue

			for adjacentVertex in self.adjacencyList[ previousVertex ]:
				if _isVertexAlreadyVisited( currentPath, adjacentVertex ):
					continue
				if pathAFound:
					newState = pathA, pathB + '#' + str( adjacentVertex ), True
				else:
					newState = pathA + '#' + str( adjacentVertex ), pathB, False
				if newState in visited:
					continue
				visited.add( newState )
				heapq.heappush( q, (self._getPriority( newState), newState) )
		return None

class RoutingTest( unittest.TestCase ):
	def test_routing( self ):
		for datafile in ('sample', 'routing'):
			self._verify( datafile )

	def _verify( self, datafile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if 'Impossible' in line:
					solutionList.append( None )
				elif 'Minimum' in line:
					_, _, _, _, _, minimumNodes = line.split()
					solutionList.append( int( minimumNodes ) )

		index = 0
		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			while True:
				N, numberOfEdges = map( int, inputFile.readline().strip().split() )
				if N == 0 and numberOfEdges == 0:
					break
				edgeList = list()
				for _ in range( numberOfEdges ):
					u, v = map( int, inputFile.readline().strip().split() )
					edgeList.append( (u, v) )

				expectedSolution = solutionList[ index ]

				formatString = 'Testcase file {} # {} Vertices = {} Edges = {} expectedSolution = {}'
				print( formatString.format( datafile, index + 1, N, numberOfEdges, expectedSolution ) )

				self.assertEqual( Routing( N, edgeList ).minimumNodes(), expectedSolution )

				index += 1

if __name__ == '__main__':
	unittest.main()