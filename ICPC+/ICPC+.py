import unittest
import os
import pathlib
import itertools
from collections import deque
import heapq
from collections import defaultdict
import math

def getTestFileList( tag ):
	return set( [ pathlib.Path( filename ).stem for filename in os.listdir( 'tests/{}'.format( tag ) ) ] )

def readString( file ):
	return file.readline().strip()

def readTokens( file ):
	return readString( file ).split()

def readInteger( file ):
	return int( readString( file ) )

def readIntegers( file ):
	return map( int, file.readline().strip().split() )

################################################################################
################################################################################
################################################################################
# amoeba.pdf
################################################################################

class Amoeba:
	def __init__( self, imageData ):
		self.rows, self.cols = len( imageData ), len( imageData[ 0 ] )
		self.imageData = imageData
		self.whitePixel, self.blackPixel = '.', '#'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1) ]

	def _dfs( self, cell, visited ):
		stack = list()
		stack.append( cell )
		
		visited.add( cell )
		
		while len( stack ) > 0:
			row, col = stack.pop()
			for du, dv in self.adjacentCellDelta:
				u, v = newCell = row + du, col + dv
				if 0 <= u < self.rows and 0 <= v < self.cols and self.imageData[ u ][ v ] == self.blackPixel and newCell not in visited:
					visited.add( newCell )
					stack.append( newCell )

	def loopCount( self ):
		count = 0

		visited = set()
		for cell in itertools.product( range( self.rows ), range( self.cols ) ):
			row, col = cell
			if self.imageData[ row ][ col ] == self.blackPixel and cell not in visited:
				self._dfs( cell, visited )
				count += 1
		return count

class AmoebaTest( unittest.TestCase ):
	def test_Amoeba_Sample( self ):
		imageData = [
		'.##########.',
		'#..........#',
		'#..#...##..#',
		'#.##..#..#.#',
		'#......#.#.#',
		'#....#..#..#',
		'#...#.#....#',
		'#..#...#...#',
		'.#..#.#....#',
		'#....#.....#',
		'#.........#.',
		'.#########..'
		]
		self.assertEqual( Amoeba( imageData ).loopCount(), 4 )

		imageData = [
		'.#####....',
		'#.....#...',
		'#..#..#...',
		'#.#.#.#...',
		'#..#..#...',
		'.#...#....',
		'..###.....',
		'......#...',
		'.##..#.#..',
		'#..#..#...',
		'.##.......',
		'..........'
		]
		self.assertEqual( Amoeba( imageData ).loopCount(), 4 )

	def test_Amoeba( self ):
		for testfile in getTestFileList( tag='amoeba' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/amoeba/{}.ans'.format( testfile ) ) as solutionFile:
			loopCount = readInteger( solutionFile )

		with open( 'tests/amoeba/{}.in'.format( testfile ) ) as inputFile:
			rows, cols = readIntegers( inputFile )
			imageData = list()
			for _ in range( rows ):
				imageData.append( readString( inputFile ) )

			print( 'Testfile {} rows = {} cols = {} Loop count = {}'.format( testfile, rows, cols, loopCount ) )
			self.assertEqual( Amoeba( imageData ).loopCount(), loopCount )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# mcpc2017.pdf - Problem G
################################################################################

class FaultyRobot:
	def __init__( self, vertexCount, edgeCount, edgeList ):
		self.vertexList = [ list() for _ in range( vertexCount + 1 ) ]
		for (u, v) in edgeList:
			fromVertex, toVertex = abs( u ), v
			self.vertexList[ fromVertex ].append( v if u > 0 else -v )

	def restVertexCount( self ):
		startState = 1, False # Start vertex is 1, False indicates that the bug in the Robot hasn't triggered yet.
		restVertices = set()

		q = deque()
		q.append( startState )

		visited = set()
		visited.add( startState )

		while len( q ) > 0:
			currentVertex, bugTriggeredAlready = q.popleft()
			canRest = True

			for toVertex in self.vertexList[ currentVertex ]:
				newState = None
				
				isForcedEdge = toVertex < 0
				toVertex = abs( toVertex )

				if isForcedEdge:
					newState = toVertex, bugTriggeredAlready
					canRest = False
				elif not isForcedEdge and not bugTriggeredAlready:
					newState = toVertex, True
				
				if newState is not None and newState not in visited:
					visited.add( newState )
					q.append( newState )
			if canRest:
				restVertices.add( currentVertex )
		return len( restVertices )

class FaultyRobotTest( unittest.TestCase ):
	def test_FaultyRobot_Sample( self ):
		vertexCount, edgeCount = 7, 9
		edgeList = [ (1, 2), (2, 3), (-1, 5), (2, 6), (5, 1), (-4, 1), (5, 6), (-6, 7), (-5, 4) ]
		self.assertEqual( FaultyRobot( vertexCount, edgeCount, edgeList ).restVertexCount(), 2 )

		vertexCount, edgeCount = 3, 2
		edgeList = [ (1, 2), (1, 3) ]
		self.assertEqual( FaultyRobot( vertexCount, edgeCount, edgeList ).restVertexCount(), 3 )

	def test_FaultyRobot( self ):
		for testfile in getTestFileList( tag='faultyrobot' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/faultyrobot/{}.ans'.format( testfile ) ) as solutionFile:
			count = readInteger( solutionFile )

		with open( 'tests/faultyrobot/{}.in'.format( testfile ) ) as inputFile:
			vertexCount, edgeCount = readIntegers( inputFile )
			edgeList = list()
			for _ in range( edgeCount ):
				u, v = readIntegers( inputFile )
				edgeList.append( (u, v) )

			formatString = 'Testcase {} vertexCount = {} edgeCount = {} Possible rest vertex count = {}'
			print( formatString.format( testfile, vertexCount, edgeCount, count ) )
			self.assertEqual( FaultyRobot( vertexCount, edgeCount, edgeList ).restVertexCount(), count )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# minesweeper.pdf
################################################################################

class Minesweeper:
	def __init__( self, minesweeperGrid ):
		self.rows, self.cols = len( minesweeperGrid ), len( minesweeperGrid[ 0 ] )
		self.minesweeperGrid = minesweeperGrid

		self.emptyCell, self.mineCell = '.', '*'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1) ]

	def expand( self ):
		expandedList = [ [ 0 for _ in range( self.cols ) ] for _ in range( self.rows ) ]

		for u, v in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.minesweeperGrid[ u ][ v ] == self.mineCell:
				for du, dv in self.adjacentCellDelta:
					r, c = u + du, v + dv
					if 0 <= r < self.rows and 0 <= c < self.cols and self.minesweeperGrid[ r ][ c ] == self.emptyCell:
						expandedList[ r ][ c ] += 1
				expandedList[ u ][ v ] = self.mineCell

		return [ ''.join( map( str, expandedListRow ) ) for expandedListRow in expandedList ]

class MinesweeperTest( unittest.TestCase ):
	def test_Minesweeper_Sample( self ):
		minesweeperGrid = [
		'..',
		'.*',
		'..'
		]
		expandedGrid = [
		'11',
		'1*',
		'11'
		]
		self.assertEqual( Minesweeper( minesweeperGrid ).expand(), expandedGrid )

		minesweeperGrid = [
		'*.*.*',
		'..*..',
		'*****',
		'.....',
		'..**.'
		]
		expandedGrid = [
		'*3*3*',
		'36*63',
		'*****',
		'24553',
		'01**1'
		]
		self.assertEqual( Minesweeper( minesweeperGrid ).expand(), expandedGrid )

	def test_Minesweeper( self ):
		testcaseCount = 0
		with open( 'tests/minesweeper/mine.in' ) as inputFile, open( 'tests/minesweeper/mine.out' ) as solutionFile:
			while True:
				rows, cols = readIntegers( inputFile )
				if rows == 0 and cols == 0:
					break
				minesweeperGrid = list()
				for _ in range( rows ):
					minesweeperGrid.append( readString( inputFile ) )

				expandedGrid = list()
				for _ in range( rows ):
					expandedGrid.append( readString( solutionFile ) )

				testcaseCount += 1
				print( 'Testcase {}#{} rows = {} cols = {}'.format( 'mine', testcaseCount, rows, cols ) )
				self.assertEqual( Minesweeper( minesweeperGrid ).expand(), expandedGrid )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# SER-2015-Problems-D1.pdf
################################################################################

class Grid:
	def __init__( self, numberGrid ):
		self.rows, self.cols = len( numberGrid ), len( numberGrid[ 0 ] )
		self.numberGrid = numberGrid
		self.startCell = (0, 0)
		self.targetCell = (self.rows - 1, self.cols - 1)
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def move( self ):
		q = deque()
		q.append( self.startCell )

		visited = set()
		visited.add( self.startCell )

		count = 0

		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				currentCell = u, v = q.popleft()
				if currentCell == self.targetCell:
					return count

				step = self.numberGrid[ u ][ v ]
				for du, dv in self.adjacentCellDelta:
					newCell = r, c = u + du * step, v + dv * step
					if 0 <= r < self.rows and 0 <= c < self.cols and newCell not in visited:
						visited.add( newCell )
						q.append( newCell )
			count += 1
		return -1

class GridTest( unittest.TestCase ):
	def test_Grid_Sample( self ):
		numberGridStringList = [
		'11',
		'11'
		]
		numberGrid = [ list( map( int, numberGridRowString ) ) for numberGridRowString in numberGridStringList ]
		self.assertEqual( Grid( numberGrid ).move(), 2 )

		numberGridStringList = [
		'22',
		'22'
		]
		numberGrid = [ list( map( int, numberGridRowString ) ) for numberGridRowString in numberGridStringList ]
		self.assertEqual( Grid( numberGrid ).move(), -1 )

		numberGridStringList = [
		'2120',
		'1203',
		'3113',
		'1120',
		'1110'
		]
		numberGrid = [ list( map( int, numberGridRowString ) ) for numberGridRowString in numberGridStringList ]
		self.assertEqual( Grid( numberGrid ).move(), 6 )

	def test_Grid( self ):
		for testfile in getTestFileList( tag='grid' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/grid/{}.ans'.format( testfile ) ) as solutionFile:
			count = readInteger( solutionFile )

		with open( 'tests/grid/{}.in'.format( testfile ) ) as inputFile:
			rows, cols = readIntegers( inputFile )
			numberGrid = list()
			for _ in range( rows ):
				numberGrid.append( [ int( digit ) for digit in readString( inputFile ) ] )

			print( 'Testcase {} rows = {} cols = {} count = {}'.format( testfile, rows, cols, count ) )
			self.assertEqual( Grid( numberGrid ).move(), count )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# BAPC2012.pdf
################################################################################

class Fire:
	def __init__( self, buildingMap ):
		self.rows, self.cols = len( buildingMap ), len( buildingMap[ 0 ] )
		self.buildingMap = buildingMap
		self.emptyCell, self.wallCell, self.fireCell, self.startCell = '.', '#', '*', '@'

		self.startLocation = None
		self.fireLocations = list()

		for r, c in itertools.product( range( self.rows ), range( self.cols ) ):
			cell = self.buildingMap[ r ][ c ]
			if cell == self.startCell:
				self.startLocation =  r, c
			elif cell == self.fireCell:
				self.fireLocations.append( (r, c) )
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def _updateDistanceMap( self, fireLocations, distanceMap ):
		q = deque()
		visited = set()

		for fireLocation in fireLocations:
			q.append( fireLocation)
			visited.add( fireLocation )

		distance = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				currentCell = r, c = q.popleft()
				distanceMap[ r ][ c ] = distance

				for du, dv in self.adjacentCellDelta:
					newCell = u, v = r + du, c + dv
					if 0 <= u < self.rows and 0 <= v < self.cols and self.buildingMap[ u ][ v ] != self.wallCell and newCell not in visited:
						visited.add( newCell )
						q.append( newCell )
			distance += 1

	def time( self ):
		distanceMap = [ [ None for _ in range( self.cols ) ] for _ in range( self.rows ) ]
		self._updateDistanceMap( self.fireLocations, distanceMap )
		
		q = deque()
		q.append( self.startLocation )

		visited = set()
		visited.add( self.startLocation )

		timeTaken = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				currentCell = r, c = q.popleft()

				for du, dv in self.adjacentCellDelta:
					newCell = u, v = r + du, c + dv
					
					if not 0 <= u < self.rows or not 0 <= v < self.cols:
						return timeTaken + 1
					if self.buildingMap[ u ][ v ] == self.wallCell or newCell in visited:
						continue	
					timeTakenForFire = distanceMap[ u ][ v ]
					if timeTakenForFire is not None and timeTakenForFire <= timeTaken + 1:
						continue
					visited.add( newCell )
					q.append( newCell )
			timeTaken += 1
		return None

class FireTest( unittest.TestCase ):
	def test_Fire_Sample( self ):
		buildingMap = [
		'####',
		'#*@.',
		'####'
		]
		self.assertEqual( Fire( buildingMap ).time(), 2 )

		buildingMap = [
		'###.###',
		'#*#.#*#',
		'#.....#',
		'#.....#',
		'#..@..#',
		'#######'
		]
		self.assertEqual( Fire( buildingMap ).time(), 5 )

		buildingMap = [
		'###.###',
		'#....*#',
		'#@....#',
		'.######'
		]
		self.assertEqual( Fire( buildingMap ).time(), None )

		buildingMap = [
		'.....',
		'.***.',
		'.*@*.',
		'.***.',
		'.....'
		]
		self.assertEqual( Fire( buildingMap ).time(), None )

		buildingMap = [
		'###',
		'#@#',
		'###'
		]
		self.assertEqual( Fire( buildingMap ).time(), None )

	def test_Fire( self ):
		with open( 'tests/fire/F.in' ) as inputFile, open( 'tests/fire/F.out' ) as solutionFile:
			T = readInteger( inputFile )
			for index in range( T ):
				cols, rows = readIntegers( inputFile )
				buildingMap = list()
				for _ in range( rows ):
					buildingMap.append( readString( inputFile ) )

				time = readString( solutionFile )
				time = None if time == 'IMPOSSIBLE' else int( time )

				print( 'Testcase {}#{} rows = {} cols = {} time = {}'.format( 'Fire', index + 1, rows, cols, time ) )
				self.assertEqual( Fire( buildingMap ).time(), time )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# SWERC2014.pdf
################################################################################

class FloweryTrails:
	def __init__( self, pointsOfInterest, trailList ):
		self.pointsOfInterest = pointsOfInterest
		self.vertexList = [ list() for _ in range( pointsOfInterest ) ]
		for (p1, p2, distance) in trailList:
			if p1 == p2:
				continue
			self.vertexList[ p1 ].append( (p2, distance) )
			self.vertexList[ p2 ].append( (p1, distance) )

	def length( self ):
		startVertex, targetVertex = 0, self.pointsOfInterest - 1

		q = list()
		q.append( (0, startVertex) )

		distanceDict = dict()
		distanceDict[ startVertex ] = 0

		stateDict = defaultdict( lambda : list() )

		while len( q ) > 0:
			distance, vertex = heapq.heappop( q )

			if vertex == targetVertex:
				break

			for vertexIndex, (toVertex, pathLength) in enumerate( self.vertexList[ vertex ] ):
				totalDistance = distance + pathLength
				
				if toVertex not in distanceDict or totalDistance < distanceDict[ toVertex ]:
					distanceDict[ toVertex ] = totalDistance
					stateDict[ toVertex ] = [ (vertex, vertexIndex) ]
					heapq.heappush( q, (totalDistance, toVertex) )
				elif totalDistance == distanceDict[ toVertex ]:
					stateDict[ toVertex ].append( (vertex, vertexIndex) )

		q = deque()
		q.append( targetVertex )

		visited = set()

		totalLength = 0
		while len( q ) > 0:
			currentVertex = q.pop()
			for vertex, vertexIndex in stateDict[ currentVertex ]:
				_, distance = self.vertexList[ vertex ][ vertexIndex ]
				totalLength += distance
				if vertex not in visited:
					visited.add( vertex )
					q.append( vertex )
		return totalLength * 2

class FloweryTrailsTest( unittest.TestCase ):
	def test_FloweryTrails( self ):
		for testfile in getTestFileList( tag='flowerytrails' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/flowerytrails/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/flowerytrails/{}.out'.format( testfile ) ) as solutionFile:

			length = readInteger( solutionFile )
			pointsOfInterest, trails = readIntegers( inputFile )
			trailList = list()
			for _ in range( trails ):
				fromVertex, toVertex, distance = readIntegers( inputFile )
				trailList.append( (fromVertex, toVertex, distance) )

			formatString = 'Testfile {} pointsOfInterest = {} trails = {} length = {}'
			print( formatString.format( testfile, pointsOfInterest, trails, length ) )
			self.assertEqual( FloweryTrails( pointsOfInterest, trailList ).length(), length )

	def test_FloweryTrails_Sample( self ):
		pointsOfInterest = 10
		trailList = [ (0, 1, 580), (1, 4, 90), (1, 4, 90), (4, 9, 250), (4, 2, 510), (2, 7, 600), (7, 3, 200),
		(3, 3, 380), (3, 0, 150), (0, 3, 100), (7, 8, 500), (7, 9, 620), (9, 6, 510), (6, 5, 145), (5, 9, 160) ]

		self.assertEqual( FloweryTrails( pointsOfInterest, trailList ).length(), 3860 )

		pointsOfInterest = 4
		trailList = [ (0, 1, 1), (0, 2, 2), (0, 3, 10), (0, 3, 3), (1, 3, 2), (2, 3, 1), (1, 1, 1) ]

		self.assertEqual( FloweryTrails( pointsOfInterest, trailList ).length(), 18 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Croatian_Regional_Competition_in_Informatics_2008.pdf
################################################################################

class Nikola:
	def __init__( self, tollList ):
		self.tollList = tollList

	def toll( self ):
		targetIndex = len( self.tollList ) - 1
		startState = 0, None

		q = list()
		q.append( (0, startState) )

		costDict = dict()
		costDict[ startState ] = 0

		while len( q ) > 0:
			cost, (index, previousStep) = heapq.heappop( q )
			if index == targetIndex:
				return cost
			
			adjacentStates = list()
			# Can Nikola move forward ?
			step = 1 if previousStep is None else previousStep + 1
			adjacentStates.append( (index + step, step) )
			# Can Nikola move backward ?
			if previousStep is not None:
				adjacentStates.append( (index - previousStep, previousStep) )

			for newIndex, step in adjacentStates:
				if 0 <= newIndex <= targetIndex:
					newCost = cost + self.tollList[ newIndex ]
					newState = newIndex, step
					if newState not in costDict or newCost < costDict[ newState ]:
						costDict[ newState ] = newCost
						heapq.heappush( q, (newCost, newState) )
		return None

class NikolaTest( unittest.TestCase ):
	def test_Nikola_Sample( self ):
		self.assertEqual( Nikola( [ 1, 2, 3, 4, 5, 6 ] ).toll(), 12 )
		self.assertEqual( Nikola( [ 2, 3, 4, 3, 1, 6, 1, 4 ] ).toll(), 14 )

	def test_Nikola( self ):
		for i in range( 10 ):
			with open( 'tests/nikola/nikola.in.{}'.format( i + 1 ) ) as inputFile, \
			     open( 'tests/nikola/nikola.out.{}'.format( i + 1 ) ) as solutionFile:

				toll = readInteger( solutionFile )
				N = readInteger( inputFile )
				tollList = [ readInteger( inputFile ) for _ in range( N ) ]

				print( 'Testcase {} N = {} toll = {}'.format( i + 1, N, toll ) )
				self.assertEqual( Nikola( tollList ).toll(), toll )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# ICPC_2013_NorthAmerican_Qualification.pdf
################################################################################

class EvenUpSolitaire:
	def __init__( self, cardList ):
		self.cardList = cardList

	def play( self ):
		stack = list()
		for number in self.cardList:
			if len( stack ) > 0 and ( stack[ -1 ] + number ) % 2 == 0:
				stack.pop()
			else:
				stack.append( number )
		return len( stack )

class EvenUpSolitaireTest( unittest.TestCase ):
	def test_EvenUpSolitaire_Sample( self ):
		self.assertEqual( EvenUpSolitaire( [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ] ).play(), 10 )
		self.assertEqual( EvenUpSolitaire( [ 1, 3, 3, 4, 2, 4, 1, 3, 7,  1 ] ).play(),  2 )

	def test_EvenUpSolitaire( self ):
		for testfile in getTestFileList( tag='evenup' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/evenup/{}.in'.format( testfile) ) as inputFile, \
		     open( 'tests/evenup/{}.ans'.format( testfile ) ) as solutionFile:
			count = readInteger( solutionFile )
			N = readInteger( inputFile )
			cardList = list( readIntegers( inputFile ) )

			print( 'Testcase {} N = {} count = {}'.format( testfile, N, count ) )
			self.assertEqual( EvenUpSolitaire( cardList ).play(), count )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# ICPC_2013_NorthAmerican_Qualification.pdf
################################################################################

class UnionFind:
	def __init__( self ):
		self.uf = dict()
		self.disjointSetCount = 0

	def _representative( self, elementId ):
		if elementId not in self.uf:
			return None
		if elementId == self.uf[ elementId ]:
			return elementId
		return self._representative( self.uf[ elementId ] )

	def _merge( self, elementIdA, elementIdB ):
		representativeA = self._representative( elementIdA )
		representativeB = self._representative( elementIdB )
		if representativeA != representativeB:
			self.uf[ representativeB ] = representativeA
			return True
		return False

	def add( self, elementId ):
		if elementId not in self.uf:
			self.uf[ elementId ] = elementId
			self.disjointSetCount += 1

	def merge( self, elementIdA, elementIdB ):
		if elementIdA not in self.uf:
			self.add( elementIdA )
		if elementIdB not in self.uf:
			self.add( elementIdB )
		if self._merge( elementIdA, elementIdB ):
			# Decrement the number of disjoint sets only if the merge step succeeds.
			self.disjointSetCount -= 1

	def __len__( self ):
		# Return the number of disjoint sets.
		return self.disjointSetCount

class IslandBuses:
	def __init__( self, islandMap, tag ):
		self.rows, self.cols = len( islandMap ), len( islandMap[ 0 ] )
		self.islandMap = islandMap
		self.tag = tag
		self.emptyCell, self.landCell, self.bridgeCell, self.bridgeEndCell = '.', '#', 'B', 'X'

		self.landIdDict = dict()
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

		self.connectedIslands = UnionFind()

	def _isLandArea( self, location ):
		r, c = location
		return self.islandMap[ r ][ c ] in (self.landCell, self.bridgeEndCell)

	def _exploreLand( self, location, landId ):
		q = deque()
		q.append( location )

		self.landIdDict[ location ] = landId

		while len( q ) > 0:
			u, v = currentLocation = q.popleft()
			for du, dv in self.adjacentCellDelta:
				newLocation = r, c = u + du, v + dv
				if 0 <= r < self.rows and 0 <= c < self.cols and self._isLandArea( newLocation ) and newLocation not in self.landIdDict:
					self.landIdDict[ newLocation ] = landId
					q.append( newLocation )

	def _exploreBridge( self, location, visitedBridges ):
		horizontalBridge = False
		r, c = location
		# Check if the bridge is horizontal.
		if c + 1 < self.cols and self.islandMap[ r ][ c + 1 ] in (self.bridgeCell, self.bridgeEndCell):
			horizontalBridge = True

		landIdA = landIdB = None
		if horizontalBridge:
			c1 = c2 = c
			while self.islandMap[ r ][ c1 ] == self.bridgeCell:
				visitedBridges.add( (r, c1) )
				c1 = c1 - 1
			while self.islandMap[ r ][ c2 ] == self.bridgeCell:
				visitedBridges.add( (r, c2) )
				c2 = c2 + 1
			landIdA, landIdB = self.landIdDict[ (r, c1) ], self.landIdDict[ (r, c2) ]
		else:
			r1 = r2 = r
			while self.islandMap[ r1 ][ c ] == self.bridgeCell:
				visitedBridges.add( (r1, c) )
				r1 = r1 - 1
			while self.islandMap[ r2 ][ c ] == self.bridgeCell:
				visitedBridges.add( (r2, c) )
				r2 = r2 + 1
			landIdA, landIdB = self.landIdDict[ (r1, c) ], self.landIdDict[ (r2, c) ]
		self.connectedIslands.merge( landIdA, landIdB )

	def analyze( self ):
		islands = bridges = busesNeeded = 0

		landId = 0
		for location in itertools.product( range( self.rows ), range( self.cols ) ):
			if self._isLandArea( location ) and location not in self.landIdDict:
				self._exploreLand( location, landId )
				self.connectedIslands.add( landId )
				landId += 1

		visitedBridges = set()
		for location in itertools.product( range( self.rows ), range( self.cols ) ):
			r, c = location
			if self.islandMap[ r ][ c ] == self.bridgeCell and location not in visitedBridges:
				self._exploreBridge( location, visitedBridges )
				bridges += 1

		islands = landId
		# Number of bridges are already updated in bridges.
		busesNeeded = len( self.connectedIslands )

		return [
		'Map {}'.format( self.tag ),
		'islands: {}'.format( islands ),
		'bridges: {}'.format( bridges ),
		'buses needed: {}'.format( busesNeeded )
		]

class IslandBusesTest( unittest.TestCase ):
	def test_IslandBuses( self ):
		for testfile in getTestFileList( tag='islandbuses' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/islandbuses/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/islandbuses/{}.ans'.format( testfile ) ) as solutionFile:

		    mapNumber = 0
		    while True:
		    	islandMap = list()
		    	while True:
		    		mapRow = readString( inputFile )
		    		if len( mapRow ) == 0:
		    			break
		    		islandMap.append( mapRow )
		    	if len( islandMap ) == 0:
		    		break
		    	# The summary contains four lines followed by a blank line.
		    	summaryText = [ readString( solutionFile ) for _ in range( 4 ) ]
		    	_ = readString( solutionFile )

		    	mapNumber += 1
		    	rows, cols = len( islandMap ), len( islandMap[ 0 ] )
		    	print( 'Testcase {}#{} Map size = {} x {}'.format( testfile, mapNumber, rows, cols ) )
		    	for islandMapRow in islandMap:
		    		print( islandMapRow )
		    	for summaryLine in summaryText:
		    		print( summaryLine )

		    	self.assertEqual( IslandBuses( islandMap, tag=mapNumber ).analyze(), summaryText )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# ICPC_2013_NorthAmerican_Qualification.pdf
################################################################################

class ErraticAnts:
	def __init__( self, pathCode ):
		self.pathCode = pathCode
		self.pathDict = defaultdict( lambda : set() )
		self.directionDelta = {
		'N' : (-1, 0), 'S' : (1, 0), 'E' : (0, 1), 'W' : (0, -1)
		}

	def pathLength( self ):
		currentLocation = r, c = origin = 0, 0
		for pathToken in self.pathCode:
			du, dv = self.directionDelta[ pathToken ]
			newLocation = u, v = r + du, c + dv

			self.pathDict[ currentLocation ].add( newLocation )
			self.pathDict[ newLocation ].add( currentLocation )
			currentLocation = r, c = newLocation

		targetLocation = currentLocation

		q = deque()
		q.append( origin )

		visited = set()
		visited.add( origin )

		optimalPathLength = 0

		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				currentLocation = q.popleft()

				if currentLocation == targetLocation:
					return optimalPathLength
				
				for newLocation in self.pathDict[ currentLocation ]:
					if newLocation not in visited:
						visited.add( newLocation )
						q.append( newLocation )
			optimalPathLength += 1
		return None

class ErraticAntsTest( unittest.TestCase ):
	def test_ErraticAnts( self ):
		for testfile in getTestFileList( tag='erraticants' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/erraticants/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/erraticants/{}.ans'.format( testfile ) ) as solutionFile:

			T = readInteger( inputFile )
			for index in range( T ):
				readString( inputFile )
				N = readInteger( inputFile )
				pathCode = [ readString( inputFile ) for _ in range( N ) ]

				pathLength = readInteger( solutionFile )

				print( 'Testcase {}#{} pathCode = {} pathLength = {}'.format( testfile, index + 1, ''.join( pathCode ), pathLength ) )
				self.assertEqual( ErraticAnts( pathCode ).pathLength(), pathLength )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# ICPC_2019_NorthAmerican_Qualification.pdf
################################################################################

class CircuitMath:
	def __init__( self, valueList, expression ):
		self.valueList = [ True if valueString == 'T' else False for valueString in valueList ]
		self.expression = expression

	def _read( self, token ):
		# Index of A is 0 and 'Z' is 25.
		return self.valueList[ ord( token ) - ord( 'A' ) ]

	def _popOperands( self, stack ):
		operand1 = stack.pop()
		operand2 = stack.pop()
		return operand1, operand2

	def eval( self ):
		stack = list()
		
		for token in self.expression.split():
			if token.isupper():
				stack.append( self._read( token ) )
			elif token == '*':
				operand1, operand2 = self._popOperands( stack )
				stack.append( operand1 and operand2 )
			elif token == '+':
				operand1, operand2 = self._popOperands( stack )
				stack.append( operand1 or operand2 )
			elif token == '-':
				stack[ -1 ] = not stack[ -1 ]
		assert len( stack ) == 1
		booleanResult = stack.pop()
		return 'T' if booleanResult else 'F'

class CircuitMathTest( unittest.TestCase ):
	def test_CircuitMath_Sample( self ):
		self.assertEqual( CircuitMath( 'TFTF', 'A B * C D + - +' ).eval(), 'F' )

	def test_CircuitMath( self ):
		for testfile in getTestFileList( tag='circuitmath' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/circuitmath/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/circuitmath/{}.ans'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			valueList = readTokens( inputFile )
			expression = readString( inputFile )

			result = readString( solutionFile )

			formatString = 'Testcase {} Expression = [{}] [{}] Result = {}'
			print( formatString.format( testfile, expression, ''.join( valueList ), result ) )

			self.assertEqual( CircuitMath( valueList, expression ).eval(), result )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# ICPC_2017_NorthAmerican_Qualification.pdf
################################################################################

class GlitchBot:
	def __init__( self, targetLocation, commandList ):
		self.targetLocation = targetLocation
		self.commandList = commandList

		self.directionDelta = {
		'N' : (0, 1), 'S' : (0, -1), 'E' : (1, 0), 'W' : (-1, 0)
		}
		self.leftTurn = {
		'N' : 'W', 'W' : 'S', 'S' : 'E', 'E' : 'N'
		}
		self.rightTurn = {
		'N' : 'E', 'E' : 'S', 'S' : 'W', 'W' : 'N'
		}
		self.commands = set( [ 'Left', 'Right', 'Forward' ] )

	def _applyCommand( self, command, location, direction ):
		if command == 'Left':
			return location, self.leftTurn[ direction ]
		elif command == 'Right':
			return location, self.rightTurn[ direction ]
		else:
			x, y = location
			dx, dy = self.directionDelta[ direction ]
			newLocation = x + dx, y + dy
			return newLocation, direction

	def _possibleFixes( self, command ):
		return set.difference( self.commands, set( [ command ] ) )

	def fix( self ):
		startLocation, startDirection = (0, 0), 'N'
		# State is composed of (location, direction, Whether we have attempted a fix, Fix applied (None if no fix has been applied yet !))
		state = startLocation, startDirection, False, None

		q = deque()
		q.append( state )

		for index, command in enumerate( self.commandList ):
			N = len( q )
			while N > 0:
				N = N - 1

				currentLocation, currentDirection, fixApplied, fix = q.popleft()
				# Attempt a fix, if and only if fixApplied is False
				if not fixApplied:
					for fixedCommand in self._possibleFixes( command ):
						newLocation, newDirection = self._applyCommand( fixedCommand, currentLocation, currentDirection )
						newState = newLocation, newDirection, True, '{} {}'.format( index + 1, fixedCommand )
						q.append( newState )
				# Apply command as-is.
				newLocation, newDirection = self._applyCommand( command, currentLocation, currentDirection )
				newState = newLocation, newDirection, fixApplied, fix
				q.append( newState )

		for location, _, _, fix in q:
			if location == self.targetLocation:
				return fix
		return None

class GlitchBotTest( unittest.TestCase ):
	def test_GlitchBot( self ):
		for testfile in getTestFileList( tag='glitchbot' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/glitchbot/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/glitchbot/{}.ans'.format( testfile ) ) as solutionFile:

			x, y = readIntegers( inputFile )
			numberOfCommands = readInteger( inputFile )
			commandList = [ readString( inputFile ) for _ in range( numberOfCommands ) ]

			fixString = readString( solutionFile )

			print( 'Testcase {} numberOfCommands = {} fixString = [{}]'.format( testfile, numberOfCommands, fixString ) )
			self.assertEqual( GlitchBot( (x, y), commandList ).fix(), fixString )

	def test_GlitchBot_Sample( self ):
		targetLocation = 3, 2
		commandList = [
		'Forward',
		'Right',
		'Forward',
		'Forward',
		'Left',
		'Forward',
		'Forward',
		'Left',
		'Forward',
		'Right',
		'Forward'
		]
		self.assertEqual( GlitchBot( targetLocation, commandList ).fix(), '8 Right' )

		targetLocation = -1, 1
		commandList = [
		'Right',
		'Left',
		'Forward'
		]
		self.assertEqual( GlitchBot( targetLocation, commandList ).fix(), '1 Forward' )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# KTH_Challenge_2011.pdf
################################################################################

class CoastLength:
	def __init__( self, areaMap ):
		self.areaMap = [ list( areaMapRow ) for areaMapRow in areaMap ]
		self.rows, self.cols = len( areaMap ), len( areaMap[ 0 ] )

		self.waterCell, self.landCell, self.seaCell = '0', '1', '~'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def _floodFill( self, location ):
		q = deque()
		q.append( location )

		while len( q ) > 0:
			currentLocation = u, v = q.popleft()

			if self.areaMap[ u ][ v ] == self.seaCell:
				continue

			self.areaMap[ u ][ v ] = self.seaCell

			for du, dv in self.adjacentCellDelta:
				newLocation = r, c = u + du, v + dv
				if 0 <= r < self.rows and 0 <= c < self.cols and self.areaMap[ r ][ c ] == self.waterCell:
					q.append( newLocation )

	def coast( self ):
		# For any water cell present on the boundary, use floodfill to replace with '~' (sea cells).
		# Horizontal boundary:
		for row, col in itertools.product( [ 0, self.rows - 1 ], range( self.cols ) ):
			location = row, col
			if self.areaMap[ row ][ col ] == self.waterCell:
				self._floodFill( location )
		# Vertical boundary:
		for row, col in itertools.product( range( self.rows ), [ 0, self.cols - 1 ] ):
			location = row, col
			if self.areaMap[ row ][ col ] == self.waterCell:
				self._floodFill( location )

		# Compute the total coastal length.
		length = 0
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.areaMap[ row ][ col ] != self.landCell:
				continue
			# For a land cell, examine the adjacent cells. If an adjacent cell is outside the grid, or a sea cell,
			# then we have to increment the coastal length.
			for du, dv in self.adjacentCellDelta:
				r, c = row + du, col + dv
				if not 0 <= r < self.rows or not 0 <= c < self.cols:
					length += 1
				elif self.areaMap[ r ][ c ] == self.seaCell:
					length += 1
		return length

class CoastLengthTest( unittest.TestCase ):
	def test_CoastLength_Sample( self ):
		areaMap = [
		'011110',
		'010110',
		'111000',
		'000010',
		'000000'
		]
		self.assertEqual( CoastLength( areaMap ).coast(), 20 )

	def test_CoastLength( self ):
		for testfile in getTestFileList( tag='coast' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/coast/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/coast/{}.ans'.format( testfile ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			areaMap = [ readString( inputFile ) for _ in range( rows ) ]

			coastLength = readInteger( solutionFile )

			print( 'Testcase {} rows = {} cols = {} coastLength = {}'.format( testfile, rows, cols, coastLength ) )
			self.assertEqual( CoastLength( areaMap ).coast(), coastLength )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2013.pdf
################################################################################

class Jailbreak:
	def __init__( self, locationMap ):
		self.rows, self.cols = len( locationMap ), len( locationMap[ 0 ] )
		self.locationMap = locationMap

		self.emptyCell, self.doorCell, self.wallCell, self.startCell = '.', '#', '*', '$'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]
		self.startLocation1 = self.startLocation2 = None

		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.locationMap[ row ][ col ] == self.startCell:
				if self.startLocation1 is None:
					self.startLocation1 = row, col
				else:
					self.startLocation2 = row, col
					break

	def _outsideJail( self, location ):
		r, c = location
		return not 0 <= r < self.rows or not 0 <= c < self.cols

	def _shortestPath( self, locations ):
		distanceList = [ [ None for _ in range( self.cols ) ] for _ in range( self.rows ) ]

		q = deque()
		visited = set()
		for location in locations:
			u, v = location
			if self.locationMap[ u ][ v ] == self.doorCell:
				q.append( (location, 1) )
				distanceList[ u ][ v ] = 1
			else:
				q.appendleft( (location, 0) )
				distanceList[ u ][ v ] = 0
			visited.add( location )

		while len( q ) > 0:
			currentLocation, doorCount = q.popleft()

			u, v = currentLocation
			for du, dv in self.adjacentCellDelta:
				r, c = newLocation = u + du, v + dv
				if self._outsideJail( newLocation ) or newLocation in visited:
					continue
				if self.locationMap[ r ][ c ] == self.wallCell:
					continue
				if self.locationMap[ r ][ c ] == self.doorCell:
					q.append( (newLocation, doorCount + 1) )
					distanceList[ r ][ c ] = doorCount + 1
				else:
					q.appendleft( (newLocation, doorCount) )
					distanceList[ r ][ c ] = doorCount
				visited.add( newLocation )
		return distanceList

	def minimumDoors( self ):
		distanceFromPrisoner1 = self._shortestPath( [ self.startLocation1 ] )
		distanceFromPrisoner2 = self._shortestPath( [ self.startLocation2 ] )

		outsideAccessLocations = list()
		for row, col in itertools.product( [ 0, self.rows - 1 ], range( self.cols ) ):
			if self.locationMap[ row ][ col ] != self.wallCell:
				outsideAccessLocations.append( (row, col) )
		for row, col in itertools.product( range( self.rows ), [ 0, self.cols - 1 ] ):
			if self.locationMap[ row ][ col ] != self.wallCell:
				outsideAccessLocations.append( (row, col) )

		distanceFromOutside = self._shortestPath( outsideAccessLocations )

		doorCount = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.locationMap[ row ][ col ] == self.wallCell:
				continue
			O = distanceFromOutside[ row ][ col ]
			D1, D2 = distanceFromPrisoner1[ row ][ col ], distanceFromPrisoner2[ row ][ col ]

			if O is None or D1 is None or D2 is None:
				continue

			if self.locationMap[ row ][ col ] == self.doorCell:
				count = D1 + D2 + O - 2
			else:
				count = D1 + D2 + O
			if doorCount is None or count < doorCount:
				doorCount = count
		return doorCount

class JailbreakTest( unittest.TestCase ):
	def test_Jailbreak( self ):
		with open( 'tests/jailbreak/J.in' ) as inputFile, \
		     open( 'tests/jailbreak/J.out' ) as solutionFile:

			T = readInteger( inputFile )
			for index in range( T ):
				rows, cols = readIntegers( inputFile )
				locationMap = [ readString( inputFile ) for _ in range( rows ) ]

				minimumDoors = readInteger( solutionFile )

				print( 'Testcase {} rows = {} cols = {} minimumDoors = {}'.format( index + 1, rows, cols, minimumDoors ) )
				self.assertEqual( Jailbreak( locationMap ).minimumDoors(), minimumDoors )

	def test_Jailbreak_Sample( self ):
		locationMap = [
		'****#****',
		'*..#.#..*',
		'****.****',
		'*$#.#.#$*',
		'*********'
		]
		self.assertEqual( Jailbreak( locationMap ).minimumDoors(), 4 )

		locationMap = [
		'*#*********',
		'*$*...*...*',
		'*$*.*.*.*.*',
		'*...*...*.*',
		'*********.*'
		]
		self.assertEqual( Jailbreak( locationMap ).minimumDoors(), 0 )

		locationMap = [
		'*#**#**#*',
		'*#**#**#*',
		'*#**#**#*',
		'*#**.**#*',
		'*#*#.#*#*',
		'*$##*##$*',
		'*#*****#*',
		'*.#.#.#.*',
		'*********'
		]
		self.assertEqual( Jailbreak( locationMap ).minimumDoors(), 9 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2020_Preliminaries.pdf - "Problem K Kangaroo Commotion"
################################################################################

class Kangaroo:
	def __init__( self, forestMap, K ):
		self.rows, self.cols = len( forestMap ), len( forestMap[ 0 ] )
		self.forestMap = forestMap
		self.K = K

		safeLocation = str( K + 1 )
		self.startLocation = self.targetLocation = None

		self.emptyCell, self.bushCell = '.', '#'

		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.forestMap[ row ][ col ] == '0':
				self.startLocation = row, col
			elif self.forestMap[ row ][ col ] == safeLocation:
				self.targetLocation = row, col

		self.possibleJumpDiff = list( itertools.product( [ -1, 0, 1 ], [ -1, 0, 1 ] ) )

	def jump( self ):
		startState = startLocation, startSpeed, nextKangaroo = self.startLocation, (0, 0), 1
		
		q = deque()
		q.append( startState )

		visited = set()
		visited.add( startState )

		numberOfJumps = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				currentLocation, currentSpeed, nextKangaroo = q.popleft()
				if currentLocation == self.targetLocation and currentSpeed == (0, 0) and nextKangaroo == self.K + 1:
					return numberOfJumps

				u, v = currentLocation
				speed_row, speed_col = currentSpeed
				for du, dv in self.possibleJumpDiff:
					newSpeed = newSpeed_row, newSpeed_col = speed_row + du, speed_col + dv

					r, c = newLocation = u + newSpeed_row, v + newSpeed_col
					if not 0 <= r < self.rows or not 0 <= c < self.cols:
						continue
					if self.forestMap[ r ][ c ] == self.bushCell:
						continue
					_nextKangaroo = nextKangaroo
					# If we have already informed all Kangaroos, then do not increment _nextKangaroo.
					# In such a case, _nextKangaroo equals self.K + 1.
					if _nextKangaroo != self.K + 1 and self.forestMap[ r ][ c ] == str( nextKangaroo ):
						_nextKangaroo = nextKangaroo + 1

					newState = newLocation, newSpeed, _nextKangaroo
					if newState not in visited:
						visited.add( newState )
						q.append( newState )
			numberOfJumps += 1
		return 'impossible'

class KangarooTest( unittest.TestCase ):
	def test_Kangaroo_Sample( self ):
		forestMap = [
		'0..2.',
		'.###.',
		'.....',
		'.....',
		'.#.#1'
		]
		self.assertEqual( Kangaroo( forestMap, 1 ).jump(), 9 )

		forestMap = [
		'03',
		'12'
		]
		self.assertEqual( Kangaroo( forestMap, 2 ).jump(), 4 )

		forestMap = [
		'.0#21'
		]
		self.assertEqual( Kangaroo( forestMap, 1 ).jump(), 8 )

		forestMap = [
		'#0##',
		'#.#2',
		'1###'
		]
		self.assertEqual( Kangaroo( forestMap, 1 ).jump(), 'impossible' )

	def test_Kangaroo( self ):
		for testfile in getTestFileList( tag='kangaroo' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/kangaroo/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/kangaroo/{}.ans'.format( testfile ) ) as solutionFile:

			rows, cols, K = readIntegers( inputFile )
			forestMap = [ readString( inputFile ) for _ in range( rows ) ]

			state = readString( solutionFile )
			if state != 'impossible':
				state = int( state )

			print( 'Testcase {} rows = {} cols = {} K = {} state = {}'.format( testfile, rows, cols, K, state ) )
			self.assertEqual( Kangaroo( forestMap, K ).jump(), state )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# ICPC_2017_NorthAmerican_Qualification.pdf - "Problem B Bumped!"
################################################################################

class Bumped:
	def __init__( self, cityCount, roadList, flightList ):
		self.cityCount = cityCount
		self.transportGrid = [ list() for _ in range( cityCount ) ]

		for cityA, cityB, cost in roadList:
			self.transportGrid[ cityA ].append( (cityB, cost, 'ROAD') )
			self.transportGrid[ cityB ].append( (cityA, cost, 'ROAD') )
		for fromCity, toCity in flightList:
			self.transportGrid[ fromCity ].append( (toCity, 0, 'FLIGHT') )

	def go( self, fromCity, destinationCity ):
		startState = fromCity, False # Boolean indicates whether we have already taken a flight.
		q = list()
		q.append( (0, startState) )

		costDict = dict()
		costDict[ startState ] = 0

		while len( q ) > 0:
			cost, (city, flightTaken) = heapq.heappop( q )
			if city == destinationCity:
				return cost

			for toCity, costForSegment, transportType in self.transportGrid[ city ]:
				if flightTaken and transportType == 'FLIGHT':
					continue
				totalCost = cost + costForSegment

				possibleState = toCity, flightTaken or transportType == 'FLIGHT'
				if possibleState not in costDict or costDict[ possibleState ] > totalCost:
					costDict[ possibleState ] = totalCost
					heapq.heappush( q, (totalCost, possibleState) )
		return None

class BumpedTest( unittest.TestCase ):
	def test_Bumped_Sample( self ):
		cityCount = 8
		roadList = [
		(0, 1, 10), (0, 2, 10), (1, 2, 10), (2, 6, 40), (6, 7, 10),
		(5, 6, 10), (3, 5, 15), (3, 6, 40), (3, 4, 20), (1, 4, 20),
		(1, 3, 20)
		]
		flightList = [ (4, 7) ]
		self.assertEqual( Bumped( cityCount, roadList, flightList ).go( 0, 5 ), 45 )

		cityCount = 8
		roadList = [
		(0, 1, 10), (0, 2, 10), (1, 2, 10), (2, 6, 40), (6, 7, 10),
		(5, 6, 10), (3, 5, 15), (3, 6, 40), (3, 4, 20), (1, 4, 20),
		(1, 3, 30)
		]
		flightList = [ (4, 7) ]
		self.assertEqual( Bumped( cityCount, roadList, flightList ).go( 0, 5 ), 50 )

	def test_Bumped( self ):
		for testfile in getTestFileList( tag='bumped' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/bumped/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/bumped/{}.ans'.format( testfile ) ) as solutionFile:

			cityCount, roadCount, flightCount, source, destination = readIntegers( inputFile )
			roadList = list()
			for _ in range( roadCount ):
				cityA, cityB, cost = readIntegers( inputFile )
				roadList.append( (cityA, cityB, cost) )
			flightList = list()
			for _ in range( flightCount ):
				fromCity, toCity = readIntegers( inputFile )
				flightList.append( (fromCity, toCity) )

			cost =  readInteger( solutionFile )

			formatString = 'Testcase {} Cities = {} Roads = {} Flights = {} Cost = {}'
			print( formatString.format( testfile, cityCount, roadCount, flightCount, cost ) )
			self.assertEqual( Bumped( cityCount, roadList, flightList ).go( source, destination ), cost )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2011.pdf - "Problem B Quick out of the Harbour"
################################################################################

class Harbour:
	def __init__( self, harbourMap, bridgeDelay ):
		self.rows, self.cols = len( harbourMap ), len( harbourMap[ 0 ] )
		self.harbourMap = harbourMap
		self.bridgeDelay = bridgeDelay

		self.startCell, self.waterCell, self.landCell, self.bridgeCell = 'S', '.', '#', '@'
		self.startLocation = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.harbourMap[ row ][ col ] == self.startCell:
				self.startLocation = row, col
				break
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def _inSea( self, location ):
		r, c = location
		return not 0 <= r < self.rows or not 0 <= c < self.cols

	def sea( self ):
		q = list()
		q.append( (0, self.startLocation) )

		timeDict = dict()
		timeDict[ self.startLocation ] = 0

		while len( q ) > 0:
			timeTaken, currentLocation = heapq.heappop( q )
			if self._inSea( currentLocation ):
				return timeTaken

			u, v = currentLocation
			for du, dv in self.adjacentCellDelta:
				newLocation = r, c = u + du, v + dv
				
				if not self._inSea( newLocation ) and self.harbourMap[ r ][ c ] == self.landCell:
					continue
				newTimeTaken = timeTaken + 1
				if self.harbourMap[ u ][ v ] == self.bridgeCell:
					newTimeTaken += self.bridgeDelay

				if newLocation not in timeDict or timeDict[ newLocation ] > newTimeTaken:
					timeDict[ newLocation ] = newTimeTaken
					heapq.heappush( q, (newTimeTaken, newLocation) )
		return None

class HarbourTest( unittest.TestCase ):
	def test_Harbour_Sample( self ):
		harbourMap = [
		'#####',
		'#S..#',
		'#@#.#',
		'#...#',
		'#@###',
		'#.###'
		]
		self.assertEqual( Harbour( harbourMap, 7 ).sea(), 16 )

		harbourMap = [
		'#####',
		'#S#.#',
		'#@..#',
		'###@#'
		]
		self.assertEqual( Harbour( harbourMap, 3 ).sea(), 11 )

	def test_Harbour( self ):
		for testfile in getTestFileList( tag='harbour' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/harbour/B.in' ) as inputFile, \
		     open( 'tests/harbour/B.out' ) as solutionFile:

			T = readInteger( inputFile )
			for index in range( T ):
				rows, cols, bridgeDelay = readIntegers( inputFile )
				harbourMap = [ readString( inputFile ) for _ in range( rows ) ]

				timeTaken = readInteger( solutionFile )

				print( 'Testcase #{} rows = {} cols = {} timeTaken = {}'.format( index + 1, rows, cols, timeTaken ) )
				self.assertEqual( Harbour( harbourMap, bridgeDelay ).sea(), timeTaken )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2013.pdf
################################################################################

class Administrative:
	def __init__( self, carInfoList, logList ):
		self.carInfoDict = dict()
		for carInfoString in carInfoList:
			carType, price, pickupCost, costPerKM = carInfoString.split()
			price, pickupCost, costPerKM = int( price ), int( pickupCost ), int( costPerKM )
			self.carInfoDict[ carType ] = (price, pickupCost, costPerKM)

		self.logList = logList

	def analyze( self ):
		costDict = defaultdict( lambda : 0 )
		inconsistentSpies = set()
		spyToBookedCar = dict()

		for statusString in self.logList:
			timeStamp, spyName, command, commandInfo = statusString.split()

			# Ensure that any referenced spy has an entry in costDict.
			costDict[ spyName ] += 0
			if spyName in inconsistentSpies:
				# Once an inconsistent event is detected, do not process subsequent events for the spy.
				continue

			if command == 'p':
				# Pick-up !
				# Ensure that the spy hasn't already booked a car.
				carType = commandInfo
				if spyName in spyToBookedCar:
					inconsistentSpies.add( spyName )
					continue
				_, pickupCost, _ = self.carInfoDict[ carType ]
				costDict[ spyName ] += pickupCost
				spyToBookedCar[ spyName ] = carType
			elif command == 'r':
				# Return !
				# Ensure that the spy is not attempting to return a car which hasn't been booked.
				if spyName not in spyToBookedCar:
					inconsistentSpies.add( spyName )
					continue
				distanceCovered = int( commandInfo )
				_, _, costPerKM = self.carInfoDict[ spyToBookedCar[ spyName ] ]
				costDict[ spyName ] += ( distanceCovered * costPerKM )
				del spyToBookedCar[ spyName ]
			elif command == 'a':
				# Accident !
				# Ensure that the spy is not claiming an accident on a car which hasn't been booked.
				if spyName not in spyToBookedCar:
					inconsistentSpies.add( spyName )
					continue
				accidentSeverity = int( commandInfo )
				price, _, _ = self.carInfoDict[ spyToBookedCar[ spyName ] ]
				costDict[ spyName ] += math.ceil( (price * accidentSeverity) / 100 )

		# If there are spies who haven't returned their cars, mark them as inconsistent.
		inconsistentSpies.update( spyToBookedCar.keys() )

		statusList = list()
		for spyName in sorted( costDict.keys() ):
			status = 'INCONSISTENT' if spyName in inconsistentSpies else costDict[ spyName ]
			statusList.append( '{} {}'.format( spyName, status) )
		return statusList

class AdministrativeTest( unittest.TestCase ):
	def test_Administrative( self ):
		with open( 'tests/administrative/A.in' ) as inputFile, \
		     open( 'tests/administrative/A.out' ) as solutionFile:

			T = readInteger( inputFile )
			for index in range( T ):
				carCount, logSize = readIntegers( inputFile )
				carInfoList = [ readString( inputFile ) for _ in range( carCount ) ]
				logList = [ readString( inputFile ) for _ in range( logSize ) ]

				print( 'Testcase #{} Number of cars = {} Log size = {}'.format( index + 1, len( carInfoList ), len( logList ) ) )

				statusList = Administrative( carInfoList, logList ).analyze()
				for status in statusList:
					self.assertEqual( status, readString( solutionFile ) )

	def test_Administrative_Sample( self ):
		carInfoList = [
		'bmw 5000 150 10',
		'jaguar 7000 200 25'
		]
		logList = [
		'10 mallory p bmw',
		'15 jb p jaguar',
		'20 jb r 500',
		'35 badluckbrian a 100',
		'50 mallory a 10',
		'55 silva p jaguar',
		'60 mallory r 100',
		'110 silva a 30'
		]
		statusList = [
		'badluckbrian INCONSISTENT',
		'jb 12700',
		'mallory 1650',
		'silva INCONSISTENT'
		]
		self.assertEqual( Administrative( carInfoList, logList ).analyze(), statusList )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# ICPC_2016_NorthAmerican_Qualification.pdf - Problem C : Big Truck
################################################################################

class BigTruck:
	def __init__( self, locationCount, itemList, roadInfo ):
		self.locationCount = locationCount
		self.itemList = [ None ] + itemList

		self.roadNetwork = [ list() for _ in range( self.locationCount + 1 ) ]
		for (fromLocation, toLocation, distance) in roadInfo:
			self.roadNetwork[ fromLocation ].append( (toLocation, distance) )
			self.roadNetwork[ toLocation ].append( (fromLocation, distance) )

	def go( self ):
		startLocation, targetLocation = 1, self.locationCount
		# The best weight has the lowest cost, and highest number of items. Hence multiply the number
		# of items collected by -1, so that we can use the default tuple comparator.
		weight = (0, - self.itemList[ startLocation ])

		q = list()
		q.append( (weight, startLocation) )

		bestWeightDict = dict()
		bestWeightDict[ startLocation ] = weight

		while len( q ) > 0:
			currentWeight, currentLocation = heapq.heappop( q )
			cost, itemCount = currentWeight

			if currentLocation == targetLocation:
				return cost, abs( itemCount )

			for toLocation, distance in self.roadNetwork[ currentLocation ]:
				newWeight = cost + distance, itemCount - self.itemList[ toLocation ]
				if toLocation not in bestWeightDict or bestWeightDict[ toLocation ] > newWeight:
					bestWeightDict[ toLocation ] = newWeight
					heapq.heappush( q, (newWeight, toLocation) )
		return 'impossible'

class BigTruckTest( unittest.TestCase ):
	def test_BigTruck( self ):
		for testfile in getTestFileList( tag='bigtruck' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/bigtruck/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/bigtruck/{}.ans'.format( testfile ) ) as solutionFile:

			locationCount = readInteger( inputFile )
			itemList = list( readIntegers( inputFile ) )
			
			roadCount = readInteger( inputFile )
			roadInfo = list()
			for _ in range( roadCount ):
				fromLocation, toLocation, distance = readIntegers( inputFile )
				roadInfo.append( (fromLocation, toLocation, distance) )

			state = readString( solutionFile )
			if state != 'impossible':
				state = tuple( map( int, state.split() ) )

			print( 'Testcase {} locations = {} roads = {} state = {}'.format( testfile, locationCount, roadCount, state ) )
			self.assertEqual( BigTruck( locationCount, itemList, roadInfo ).go(), state )

	def test_BigTruck_Sample( self ):
		locationCount = 6
		itemList = [ 1, 1, 2, 3, 1, 0 ]
		roadInfo = [
		(1, 2, 2), (2, 3, 3), (3, 6, 4), (1, 4, 4), (4, 3, 2), (4, 5, 3), (5, 6, 2)
		]
		self.assertEqual( BigTruck( locationCount, itemList, roadInfo ).go(), (9, 5) )

		locationCount = 9
		itemList = [ 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
		roadInfo = [
		(1, 2, 3), (2, 5, 3), (1, 6, 2), (6, 7, 2), (7, 5, 2), (5, 3, 1), (3, 4, 2), (4, 9, 3), (5, 8, 2), (8, 9, 4)
		]
		self.assertEqual( BigTruck( locationCount, itemList, roadInfo ).go(), (12, 7) )

		locationCount = 2
		itemList = [ 5, 5 ]
		roadInfo = [ ]
		self.assertEqual( BigTruck( locationCount, itemList, roadInfo ).go(), 'impossible' )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# VirginiaTechHighSchoolProgrammingContest_2016 - Problem H: RobotTurtles
################################################################################

class Bitmap:
	@staticmethod
	def builtin_popcount( x ):
		count = 0
		while x > 0:
			x = x & (x - 1)
			count += 1
		return count

	@staticmethod
	def setBitnumber( bitmap, bitNumber ):
			return bitmap | ( 1 << bitNumber )

	@staticmethod
	def isBitnumberSet( bitmap, bitNumber ):
			return ( bitmap & ( 1 << bitNumber ) ) > 0

class RobotTurtle:
	def __init__( self, boardData ):
		self.rows = self.cols = 8
		self.boardData = boardData

		self.emptyCell, self.rockCell, self.iceCell, self.diamondCell = '.', 'C', 'I', 'D'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

		self.startLocation = self.rows - 1, 0
		self.startDirection = 'E'
		self.leftTurn = {
		'N' : 'W', 'W' : 'S', 'S' : 'E', 'E' : 'N'
		}
		self.rightTurn = {
		'N' : 'E', 'E' : 'S', 'S' : 'W', 'W' : 'N'
		}
		self.directionDelta = {
		'N' : (-1, 0), 'S' : (1, 0), 'E' : (0, 1), 'W' : (0, -1)
		}

		self.iceCastleId = dict()
		index = 0
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.boardData[ row ][ col ] == self.iceCell:
				self.iceCastleId[ (row, col) ] = index
				index += 1

		self.noSolution = 'no solution'

	def _isOutside( self, location ):
		r, c = location
		return not 0 <= r < self.rows or not 0 <= c < self.cols

	def go( self ):
		startState = (self.startLocation, self.startDirection, 0)
		
		q = deque()
		q.append( (startState, str()) )

		visited = set()
		visited.add( startState )

		while len( q ) > 0:
			(currentLocation, currentDirection, iceCastleBitmap), program = q.popleft()

			u, v = currentLocation
			if self.boardData[ u ][ v ] == self.diamondCell:
				return program
			
			stateList = list()
			# We have to generate all possible state transitions.
			
			# Turn left, turn right !
			stateList.append( (currentLocation, self.leftTurn[ currentDirection ], iceCastleBitmap, program + 'L') )
			stateList.append( (currentLocation, self.rightTurn[ currentDirection ], iceCastleBitmap, program + 'R') )

			# Move forward !
			du, dv = self.directionDelta[ currentDirection ]
			newLocation = r, c = u + du, v + dv
			_isOutside = self._isOutside( newLocation ) 

			if not _isOutside and self.boardData[ r ][ c ] != self.rockCell:
				# If we are moving into an ice castle, then ensure that it is already destroyed.
				validState = True
				if self.boardData[ r ][ c ] == self.iceCell and not Bitmap.isBitnumberSet( iceCastleBitmap, self.iceCastleId[ newLocation ] ):
					validState = False
				if validState:
					stateList.append( (newLocation, currentDirection, iceCastleBitmap, program + 'F') )

			# Can we shoot an ice castle ?
			if not _isOutside and self.boardData[ r ][ c ] == self.iceCell and not Bitmap.isBitnumberSet( iceCastleBitmap, self.iceCastleId[ newLocation ] ):
				newIceCastleBitmap = Bitmap.setBitnumber( iceCastleBitmap, self.iceCastleId[ newLocation ] )
				stateList.append( (currentLocation, currentDirection, newIceCastleBitmap, program + 'X') )

			for (location, direction, iceCastleBitmap, program) in stateList:
				cacheKey = location, direction, iceCastleBitmap
				if cacheKey not in visited:
					visited.add( cacheKey )
					q.append( (cacheKey, program) )
		return self.noSolution

	def verifyProgram( self, programString ):
		location, direction = self.startLocation, self.startDirection
		destroyedIceCastles = set()

		for token in programString:
			if token == 'F':
				u, v = location
				du, dv = self.directionDelta[ direction ]
				location = r, c = u + du, v + dv
				if self._isOutside( location ) or self.boardData[ r ][ c ] == self.rockCell:
					return False
				if self.boardData[ r ][ c ] == self.iceCell and location not in destroyedIceCastles:
					return False
			elif token == 'R':
				direction = self.rightTurn[ direction ]
			elif token == 'L':
				direction = self.leftTurn[ direction ]
			elif token == 'X':
				u, v = location
				du, dv = self.directionDelta[ direction ]
				shotLocation = r, c = u + du, v + dv
				if self._isOutside( shotLocation ):
					return False
				if self.boardData[ r ][ c ] in (self.rockCell, self.emptyCell):
					return False
				if shotLocation in destroyedIceCastles:
					return False
				destroyedIceCastles.add( shotLocation )
			else:
				return False
		r, c = location
		return self.boardData[ r ][ c ] == self.diamondCell
				
class RobotTurtleTest( unittest.TestCase ):
	def test_RobotTurtle( self ):
		for testfile in getTestFileList( tag='roboturtle' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/roboturtle/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/roboturtle/{}.ans'.format( testfile ) ) as solutionFile:

			boardData = [ readString( inputFile ) for _ in range( 8 ) ]
			program = readString( solutionFile )
			robotTurtle = RobotTurtle( boardData )
			generatedProgram = robotTurtle.go()

			if program == generatedProgram:
				print( 'Testcase {} [{}]'.format( testfile, program ) )
			else:
				print( 'Testcase {} [{}] [{}]'.format( testfile, program, generatedProgram ) )
				self.assertEqual( len( program ), len( generatedProgram ) )
				self.assertTrue( robotTurtle.verifyProgram( generatedProgram ) )

	def test_RobotTurtle_Sample( self ):
		boardData = [
		'........',
		'........',
		'........',
		'...CC...',
		'..C.DC..',
		'.C..C...',
		'C.IC....',
		'T.C.....'
		]
		program = 'FLFRXFLFRFLFRF'
		robotTurtle = RobotTurtle( boardData )
		self.assertTrue( robotTurtle.verifyProgram( program ) )
		
		generatedProgram = robotTurtle.go()
		if program != generatedProgram:
			self.assertEqual( len( program ), len( generatedProgram ) )
			self.assertTrue( robotTurtle.verifyProgram( generatedProgram ) )

		boardData = [
		'........',
		'........',
		'........',
		'...CC...',
		'..CIDC..',
		'.CI.C...',
		'C.IC....',
		'T.C.....'
		]
		program = 'FLFRXFLXFRFLXFRF'
		robotTurtle = RobotTurtle( boardData )
		self.assertTrue( robotTurtle.verifyProgram( program ) )
		
		generatedProgram = robotTurtle.go()
		if program != generatedProgram:
			self.assertEqual( len( program ), len( generatedProgram ) )
			self.assertTrue( robotTurtle.verifyProgram( generatedProgram ) )

		boardData = [
		'........',
		'........',
		'........',
		'...CCD..',
		'..C..C..',
		'.C..I...',
		'C.IC....',
		'T.C.....'
		]
		program = 'FLFRXFLFRFXFFFLFFLF'
		robotTurtle = RobotTurtle( boardData )
		self.assertTrue( robotTurtle.verifyProgram( program ) )
		
		generatedProgram = robotTurtle.go()
		if program != generatedProgram:
			self.assertEqual( len( program ), len( generatedProgram ) )
			self.assertTrue( robotTurtle.verifyProgram( generatedProgram ) )

		boardData = [
		'........',
		'........',
		'........',
		'CCCCC...',
		'..C.DC..',
		'..C.C...',
		'C.IC....',
		'T.C.....'
		]
		self.assertEqual( RobotTurtle( boardData ).go(), 'no solution' )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# VirginiaTechHighSchoolProgrammingContest_2016 - Problem C: TurtleMaster
################################################################################

class TurtleMaster:
	@staticmethod
	def go( boardData, program ):
		return 'Diamond!' if RobotTurtle( boardData ).verifyProgram( program ) else 'Bug!'

class TurtleMasterTest( unittest.TestCase ):
	def test_TurtleMaster_Sample( self ):
		boardData = [
		'........',
		'........',
		'........',
		'...CC...',
		'..C.DC..',
		'.C..C...',
		'C.IC....',
		'T.C.....'
		]
		self.assertEqual( TurtleMaster.go( boardData, 'FLFRXFLFRFLFRF' ), 'Diamond!' )
		self.assertEqual( TurtleMaster.go( boardData, 'FLFRFLFRFLFRF' ), 'Bug!' )
		self.assertEqual( TurtleMaster.go( boardData, 'FLFRXFLFRFLFFR' ), 'Bug!' )

	def test_TurtleMaster( self ):
		for testfile in getTestFileList( tag='turtlemaster' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/turtlemaster/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/turtlemaster/{}.ans'.format( testfile ) ) as solutionFile:

			boardData = [ readString( inputFile ) for _ in range( 8 ) ]
			program = readString( inputFile )
			state = readString( solutionFile )

			print( 'Testcase {} program = {} state = {}'.format( testfile, program, state ) )
			for boardDataRow in boardData:
				print( boardDataRow )
			self.assertEqual( TurtleMaster.go( boardData, program ), state )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# SouthWesternEuropeanRegionalContest_2009.pdf - Problem F : Haunted Graveyard
################################################################################

class Haunted:
	def __init__( self, width, height, stoneList, hauntedList ):
		self.width, self.height = width, height
		self.blockedCells = set( stoneList )

		self.hauntedCells = dict()
		for (x1, y1, x2, y2, timeTaken) in hauntedList:
			self.hauntedCells[ (x1, y1) ] = (x2, y2, timeTaken)
		self.startCell = 0, 0
		self.targetCell = self.width - 1, self.height - 1

		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]
		self.adjacencyList = [ [ list() for _ in range( self.height ) ] for _ in range( self.width ) ]
		
		for (x, y) in itertools.product( range( self.width ), range( self.height ) ):
			self._populateAdjacencyList( x, y )

	def _populateAdjacencyList( self, x, y ):
		# What are the cells adjacent to x, y ?
		listToPopulate = self.adjacencyList[ x ][ y ]

		if (x, y) in self.hauntedCells:
			listToPopulate.append( self.hauntedCells[ (x, y) ] )
		elif (x, y) in self.blockedCells or (x, y) == self.targetCell:
			# No outgoing paths from blocked cells. Also, no outgoing paths from the target cell.
			pass
		else:
			for du, dv in self.adjacentCellDelta:
				u, v = x + du, y + dv
				if 0 <= u < self.width and 0 <= v < self.height and (u, v) not in self.blockedCells:
					listToPopulate.append( (u, v, 1) )

	def go( self ):
		# Index by x distance, and then by y distance.
		distanceList = [ [ float( 'inf' ) for _ in range( self.height ) ] for _ in range( self.width ) ]

		x, y = self.startCell
		distanceList[ x ][ y ] = 0

		for iterationCount in range( self.width * self.height ):
			nomoreRelaxations = True
			
			for (x1, y1) in itertools.product( range( self.width ), range( self.height ) ):
				for (x2, y2, timeTaken) in self.adjacencyList[ x1 ][ y1 ]:
					# There is a path from (x1, y1) to (x2, y2) taking "timeTaken" seconds.
					currentTimeTaken = distanceList[ x2 ][ y2 ]
					newTimeTaken = distanceList[ x1 ][ y1 ] + timeTaken
					if newTimeTaken < currentTimeTaken:
						distanceList[ x2 ][ y2 ] = newTimeTaken
						nomoreRelaxations = False
			# Optimization.
			# If there are no more relaxations, then we can terminate the loop.
			if nomoreRelaxations:
				break

		# If there is a negative loop, return 'Never'
		if not nomoreRelaxations:
			return 'Never'
		x, y = self.targetCell
		distanceToExit = distanceList[ x ][ y ]
		return 'Impossible' if distanceToExit == float( 'inf' ) else distanceToExit

class HauntedTest( unittest.TestCase ):
	def test_Haunted_Sample( self ):
		width, height = 3, 3
		stoneList = [ (2, 1), (1, 2) ]
		hauntedList = []
		self.assertEqual( Haunted( width, height, stoneList, hauntedList ).go(), 'Impossible' )

		width, height = 4, 3
		stoneList = [ (2, 1), (3, 1) ]
		hauntedList = [ (3, 0, 2, 2, 0) ]
		self.assertEqual( Haunted( width, height, stoneList, hauntedList ).go(), 4 )

		width, height = 4, 2
		stoneList = []
		hauntedList = [ (2, 0, 1, 0, -3) ]
		self.assertEqual( Haunted( width, height, stoneList, hauntedList ).go(), 'Never' )

	def test_Haunted( self ):
		with open( 'tests/haunted/labyrinth.in' ) as inputFile, \
		     open( 'tests/haunted/labyrinth.out' ) as solutionFile:

			testcaseCount = 0
			while True:
				width, height = readIntegers( inputFile )
				if width == 0 and height == 0:
					break

				stoneCount = readInteger( inputFile )
				stoneList = list()
				for _ in range( stoneCount ):
					x, y = readIntegers( inputFile )
					stoneList.append( (x, y) )

				hauntedCount = readInteger( inputFile )
				hauntedList = list()
				for _ in range( hauntedCount ):
					x1, y1, x2, y2, timeTaken = readIntegers( inputFile )
					hauntedList.append( (x1, y1, x2, y2, timeTaken) )

				state = readString( solutionFile )
				if state != 'Impossible' and state != 'Never':
					state = int( state )

				testcaseCount += 1
				print( 'Testcase #{} width = {} height = {} state = {}'.format( testcaseCount, width, height, state ) )
				self.assertEqual( Haunted( width, height, stoneList, hauntedList ).go(), state )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# VirginiaTechHighSchoolProgrammingContest_2018.pdf - Problem I : The Grand Adventure
################################################################################

class Adventure:
	def __init__( self, string ):
		self.string = string

		trader, jeweler, banker = 't', 'j', 'b'
		money, incense, gem = '$', '|', '*'
		
		self.collectorDict = {
		banker  : money,
		trader  : incense,
		jeweler : gem
		}
		self.emptyCell = '.'

	def go( self ):
		stack = list()
		for token in self.string:
			if token in self.collectorDict:
				item = self.collectorDict[ token ]
				if len( stack ) == 0 or stack.pop() != item:
					return 'NO'
			elif token == self.emptyCell:
				pass
			else:
				stack.append( token )
		return 'YES' if len( stack ) == 0 else 'NO'

class AdventureTest( unittest.TestCase ):
	def test_Adventure_Sample( self ):
		self.assertEqual( Adventure( '.......$....$......*....*.....|......t........j...j.....b..b........' ).go(), 'YES' )
		self.assertEqual( Adventure( '...$.$.$..*..*..*...*..|..*..b.....*******...' ).go(), 'NO' )

	def test_Adventure( self ):
		for testfile in getTestFileList( tag='adventure' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/adventure/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/adventure/{}.ans'.format( testfile ) ) as solutionFile:

			testcaseCount = readInteger( inputFile )
			for index in range( testcaseCount ):
				string = readString( inputFile )
				result = readString( solutionFile )

				print( 'Testcase {}#{} adventureString = {} Result = {}'.format( testfile, index + 1, string, result ) )
				self.assertEqual( Adventure( string ).go(), result )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2015_Preliminaries.pdf - "Problem G : Pac-Man"
################################################################################

class PacMan:
	def __init__( self, gameMap ):
		self.rows, self.cols = len( gameMap ), len( gameMap[ 0 ] )
		self.gameMap = gameMap
		self.directionDelta = {
		'N' : (-1, 0), 'S' : (1, 0), 'E' : (0, 1), 'W' : (0, -1)
		}
		self.directionAttemptOrder = 'WNES'

		self.pacmanCell, self.emptyCell, self.ghostCell, self.blockedCell = 'P', '.', 'G', 'X'
		
		self.pacman1Location = self.pacman2Location = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			cellType = self.gameMap[ row ][ col ]
			if cellType == self.pacmanCell and self.pacman1Location is None:
				self.pacman1Location = row, col
			elif cellType == self.pacmanCell and self.pacman2Location is None:
				self.pacman2Location = row, col
				break 

	def _tryMove( self, location, direction ):
		row, col = location
		du, dv = self.directionDelta[ direction ]
		return ( row + du ) % self.rows, ( col + dv ) % self.cols

	def play( self ):
		startState = self.pacman1Location, self.pacman2Location

		q = deque()
		q.append( (startState, str()) )

		visited = set()
		visited.add( startState )

		while len( q ) > 0:
			( pacman1Location, pacman2Location ), movementString = q.popleft()
			r1, c1 = pacman1Location
			r2, c2 = pacman2Location

			if r1 == r2 and c1 == c2:
				return movementString

			for directionToken in self.directionAttemptOrder:
				du, dv = self.directionDelta[ directionToken ]
				# Try to move pacman1 and pacman2.
				newPacman1Location = pacman1Location
				newPacman2Location = pacman2Location

				r, c = self._tryMove( pacman1Location, directionToken )
				if self.gameMap[ r ][ c ] == self.ghostCell:
					continue
				if self.gameMap[ r ][ c ] != self.blockedCell:
					newPacman1Location = r, c

				r, c = self._tryMove( pacman2Location, directionToken )
				if self.gameMap[ r ][ c ] == self.ghostCell:
					continue
				if self.gameMap[ r ][ c ] != self.blockedCell:
					newPacman2Location = r, c

				newState = newPacman1Location, newPacman2Location
				if newState not in visited:
					visited.add( newState )
					q.append( (newState, movementString + directionToken) )

		return None

	def playPrettyPrint( self ):
		movementString = self.play()
		if movementString is None:
			return 'IMPOSSIBLE'
		else:
			return '{} {}'.format( len( movementString ), movementString )

	def cheat( self, movementString ):
		r1, c1 = self.pacman1Location
		r2, c2 = self.pacman2Location
		
		for movementToken in movementString:
			# Try to move pacman1.
			r, c = self._tryMove( (r1, c1), movementToken )
			if self.gameMap[ r ][ c ] == self.ghostCell:
				return False
			if self.gameMap[ r ][ c ] != self.blockedCell:
				r1, c1 = r, c
			# Try to move pacman2.
			r, c = self._tryMove( (r2, c2), movementToken )
			if self.gameMap[ r ][ c ] == self.ghostCell:
				return False
			if self.gameMap[ r ][ c ] != self.blockedCell:
				r2, c2 = r, c
		return r1 == r2 and c1 == c2

class PacManTest( unittest.TestCase ):
	def test_PacMan( self ):
		with open( 'tests/pacman/test.in' ) as inputFile, \
		     open( 'tests/pacman/test.out' ) as solutionFile:

			testcaseCount = readInteger( inputFile )
			for index in range( testcaseCount ):
				rows, cols = readIntegers( inputFile )
				gameMap = [ readString( inputFile ) for _ in range( rows ) ]

				state = readString( solutionFile )

				print( 'Testcase {} rows = {} cols = {} state = {}'.format( index + 1, rows, cols, state ) )
				game = PacMan( gameMap )
				generatedState = game.playPrettyPrint()
				if generatedState != state:
					l1, generatedMoveString = generatedState.split()
					l2, moveString = state.split()
					print( 'Generated moves : [{}]'.format( generatedMoveString ) )
					self.assertEqual( l1, l2 )
					self.assertTrue( game.cheat( generatedMoveString ) )

	def test_PacMan_Sample( self ):
		gameMap = [
		'.P...',
		'XG.P.'
		]
		movementString = 'WSEESEE'
		game = PacMan( gameMap )
		string = game.play()
		if string != movementString:
			self.assertEqual( len( string ), len( movementString ) )
			self.assertTrue( game.cheat( string ) )

		gameMap = [
		'X...X.X.',
		'X.......',
		'.XXP...X',
		'..X..X..',
		'.PXXXX..',
		'.......X',
		'........',
		'XXXXXXX.'
		]
		movementString = 'EEESSWWWSS'
		game = PacMan( gameMap )
		string = game.play()
		if string != movementString:
			self.assertEqual( len( string ), len( movementString ) )
			self.assertTrue( game.cheat( string ) )

		gameMap = [
		'P.',
		'GP'
		]
		self.assertEqual( PacMan( gameMap ).play(), None )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2015_Preliminaries.pdf - "Problem D : Ga"
################################################################################

class Ga:
	def __init__( self, gameBoard ):
		self.size = len( gameBoard )
		self.gameBoard = [ list( gameBoardRow ) for gameBoardRow in gameBoard ]
		self.blackStone, self.whiteStone, self.emptyCell = 'b', 'w', '-'

		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1) ]

	def _whiteStoneIsAdjacent( self, location ):
		u, v = location
		for du, dv in self.adjacentCellDelta:
			r, c = u + du, v + dv
			if 0 <= r < self.size and 0 <= c < self.size and self.gameBoard[ r ][ c ] == self.whiteStone:
				return True
		return False

	def _floodFill( self, location ):
		q = deque()
		q.append( location )

		count = 0
		while len( q ) > 0:
			u, v = q.popleft()
			if self.gameBoard[ u ][ v ] != self.emptyCell:
				continue
			count += 1
			self.gameBoard[ u ][ v ] = self.whiteStone

			for du, dv in self.adjacentCellDelta:
				r, c = adjacentLocation = u + du, v + dv
				if 0 <= r < self.size and 0 <= c < self.size and self.gameBoard[ r ][ c ] == self.emptyCell:
					q.append( adjacentLocation )
		return count
 
	def ga( self ):
		count = 0

		for row, col in itertools.product( range( self.size ), range( self.size ) ):
			location = row, col
			if self.gameBoard[ row ][ col ] == self.emptyCell and self._whiteStoneIsAdjacent( location ):
				count += self._floodFill( location )

		return count

class GaTest( unittest.TestCase ):
	def test_Ga_Sample( self ):
		gameBoard = [
		'bbb',
		'bwb',
		'bbb'
		]
		self.assertEqual( Ga( gameBoard ).ga(), 0 )

		gameBoard = [
		'--b---',
		'bbww--',
		'-bbbw-',
		'---bbb',
		'---b--',
		'------'
		]
		self.assertEqual( Ga( gameBoard ).ga(), 8 )

	def test_Ga( self ):
		with open( 'tests/ga/test.in' ) as inputFile, \
		     open( 'tests/ga/test.out' ) as solutionFile:

			testcaseCount = readInteger( inputFile )
			for index in range( testcaseCount ):
				size = readInteger( inputFile )
				gameBoard = [ readString( inputFile ) for _ in range( size ) ]

				count = readInteger( solutionFile )

				print( 'Testcase {} size = {} Maximum stones = {}'.format( testcaseCount, size, count ) )
				self.assertEqual( Ga( gameBoard ).ga(), count )

################################################################################
################################################################################
################################################################################

if __name__ == '__main__':
	unittest.main()