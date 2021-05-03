import unittest
import os
import pathlib
import itertools
from collections import deque

class Robo:
	def __init__( self, factoryMap ):
		self.rows, self.cols = len( factoryMap ), len( factoryMap[ 0 ] )
		self.factoryMap = factoryMap
		self.emptyCell, self.wallCell, self.startPositionCell = '.', 'W', 'S'
		self.cameraCell = 'C'
		self.conveyorCells = {
		'L' : (0, -1), 'R' : (0, 1), 'U' : (-1, 0), 'D' : (1, 0)
		}

		self.startPosition = None
		self.cameraFieldPositions = set()
		for r, c in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.factoryMap[ r ][ c ] == self.startPositionCell:
				self.startPosition = r, c
			elif self.factoryMap[ r ][ c ] == self.cameraCell:
				self._populateCameraFieldPositions( r, c )

	def _populateCameraFieldPositions( self, r, c ):
		self.cameraFieldPositions.add( (r, c) )
		for du, dv in self.conveyorCells.values():
			cellRow, cellCol = r, c
			while True:
				cellRow, cellCol = cellRow + du, cellCol + dv
				currentCell = self.factoryMap[ cellRow ][ cellCol ]
				if currentCell == self.wallCell or currentCell == self.cameraCell:
					break
				if currentCell not in self.conveyorCells:
					self.cameraFieldPositions.add( (cellRow, cellCol) )

	def analyze( self ):
		q = deque()
		visited = set()

		if self.startPosition not in self.cameraFieldPositions:
			q.append( (self.startPosition, 0) )

		bestDistanceDict = dict()

		while len( q ) > 0:
			currentPosition, distance = q.popleft()
			row, col = currentPosition

			if currentPosition in visited:
				continue
			visited.add( currentPosition )

			currentCell = self.factoryMap[ row ][ col ]
			if currentCell == self.emptyCell:
				bestDistanceDict[ (currentPosition) ] = distance
			elif currentCell in self.conveyorCells:
				du, dv = self.conveyorCells[ currentCell ]
				newPosition = r, c = row + du, col + dv
				if newPosition in self.cameraFieldPositions:
					continue
				newCell = self.factoryMap[ r ][ c ]
				if newCell == self.wallCell:
					continue
				q.appendleft( (newPosition, distance) )
				continue

			for du, dv in self.conveyorCells.values():
				newPosition = r, c = row + du, col + dv
				if newPosition in self.cameraFieldPositions:
					continue
				newCell = self.factoryMap[ r ][ c ]
				if newCell == self.wallCell:
					continue
				q.append( (newPosition, distance + 1) )

		distanceList = list()
		for r, c in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.factoryMap[ r ][ c ] == self.emptyCell:
				distanceList.append( bestDistanceDict.get( (r, c), -1 ) )
		return distanceList

class RoboTest( unittest.TestCase ):
	def test_Robo_sample( self ):
		factoryMap = [
		'WWWWW',
		'W.W.W',
		'WWS.W',
		'WWWWW'
		]
		self.assertEqual( Robo( factoryMap ).analyze(), [ -1, 2, 1 ] )

		factoryMap = [
		'WWWWWWW',
		'WD.L.RW',
		'W.WCU.W',
		'WWW.S.W',
		'WWWWWWW'
		]
		self.assertEqual( Robo( factoryMap ).analyze(), [ 2, 1, 3, -1, -1, 1 ] )

	def test_Robo( self ):
		testFiles = set( [ pathlib.Path( filename ).stem for filename in os.listdir( 'tests/RoboThieves' ) ] )
		for testfile in testFiles:
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/RoboThieves/{}.in'.format( testfile ) ) as inputFile:
			rows, cols = map( int, inputFile.readline().strip().split() )
			factoryMap = list()
			for _ in range( rows ):
				factoryMap.append( inputFile.readline().strip() )

		solutionList = list()
		with open( 'tests/RoboThieves/{}.out'.format( testfile ) ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line ) )

		print( 'Testcase {} rows = {} cols = {}'.format( testfile, rows, cols ) )
		self.assertEqual( Robo( factoryMap ).analyze(), solutionList )

if __name__ == '__main__':
	unittest.main()