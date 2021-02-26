import unittest
from collections import deque
import copy

class MarbleGame:
	def __init__( self, size, marbleLocationList, holeLocationList, wallLocationList ):
		self.size = size
		self.initialMarbleLocationList = marbleLocationList
		
		assert len( marbleLocationList ) == len( holeLocationList )
		self.locationCount = len( marbleLocationList )

		self.holeLocationList = holeLocationList
		
		self.wallLocation = set()
		for A, B, C, D in wallLocationList:
			cellA, cellB = (A, B), (C, D)
			self.wallLocation.add( (cellA, cellB) )
			self.wallLocation.add( (cellB, cellA) )

	def _boardState( self, marbleLocationList ):
		return '#'.join( [ '{},{}'.format( row, col ) for row, col in marbleLocationList ] )

	def _generateMoves( self, currentMarbleLocationList ):
		possibleLocationList = list()

		for movementDelta in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
			newLocationList = self._applyMovement( currentMarbleLocationList, movementDelta )
			if newLocationList is not None:
				possibleLocationList .append( newLocationList )
		return possibleLocationList

	def _isOutsideGrid( self, location ):
		row, col = location
		return not 0 <= row < self.size or not 0 <= col < self.size

	def _applyMovement( self, currentMarbleLocationList, movementDelta ):
		dx, dy = movementDelta
		newLocationList = copy.deepcopy( currentMarbleLocationList )

		noMoreMoves = False
		while not noMoreMoves:
			noMoreMoves = True

			filledIndices = set()
			for i in range( self.locationCount ):
				if newLocationList[ i ] == self.holeLocationList[ i ]:
					filledIndices.add( i )

			for i in range( self.locationCount ):
				row, col = currentLocation = newLocationList[ i ]
				if i in filledIndices:
					continue
				newLocation = row + dx, col + dy
				if self._isOutsideGrid( newLocation ):
					continue
				if (currentLocation, newLocation) in self.wallLocation:
					continue
				if newLocation in self.holeLocationList:
					index = self.holeLocationList.index( newLocation )
					if index != i and index not in filledIndices:
						return None
				elif newLocation in newLocationList:
					continue
				newLocationList[ i ] = newLocation
				noMoreMoves = False
				break
		return newLocationList 

	def play( self ):
		q = deque()
		q.append( self.initialMarbleLocationList )

		visited = set()
		visited.add( self._boardState( self.initialMarbleLocationList ) )

		numberOfTurns = 0

		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1
				currentMarbleLocationList = q.popleft()
				if currentMarbleLocationList == self.holeLocationList:
					return numberOfTurns

				for possibleLocationList in self._generateMoves( currentMarbleLocationList ):
					boardState = self._boardState( possibleLocationList )
					if boardState in visited:
						continue
					visited.add( boardState )
					q.append( possibleLocationList )

			numberOfTurns += 1
		return None

class MarbleGameTest( unittest.TestCase ):
	def _verify( self, datafile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if len( line ) == 0:
					continue
				_, _, state, * rest = line.split()
				if 'impossible' in state:
					solutionList.append( None )
				else:
					solutionList.append( int( state ) )

		marbleGameParameterList = list()
		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			while True:
				size, marbleCount, wallCount = map( int, inputFile.readline().strip().split() )
				if size == 0 and marbleCount == 0 and wallCount == 0:
					break
				marbleLocationList = list()
				for _ in range( marbleCount ):
					row, col = map( int, inputFile.readline().strip().split() )
					marbleLocationList.append( (row, col) )
				holeLocationList = list()
				for _ in range( marbleCount ):
					row, col = map( int, inputFile.readline().strip().split() )
					holeLocationList.append( (row, col) )
				wallLocationList = list()
				for _ in range( wallCount ):
					A, B, C, D = map( int, inputFile.readline().strip().split() )
					wallLocationList.append( (A, B, C, D) )
				marbleGameParameterList.append( (size, marbleLocationList, holeLocationList, wallLocationList) )

		assert len( solutionList ) == len( marbleGameParameterList )
		for i in range( len( solutionList ) ):
			size, marbleLocationList, holeLocationList, wallLocationList = marbleGameParameterList[ i ]
			print( 'Game = {} size = {} marbleLocationList = {}'.format( i + 1, size, marbleLocationList ) )
			game = MarbleGame( size, marbleLocationList, holeLocationList, wallLocationList )
			self.assertEqual( game.play(), solutionList[ i ] )

	def test_play( self ):
		for datafile in ('sample', 'marble'):
			self._verify( datafile )

if __name__ == '__main__':
	unittest.main()