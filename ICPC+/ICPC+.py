import unittest
import os
import pathlib
import itertools
from collections import deque
import heapq
from collections import defaultdict
import math
import operator
import string
import bisect

def getTestFileList( tag ):
	return set( [ pathlib.Path( filename ).stem for filename in os.listdir( 'tests/{}'.format( tag ) ) ] )

def getTestFileSuffixList( tag ):
	return set( [ pathlib.Path( filename ).suffix for filename in os.listdir( 'tests/{}'.format( tag ) ) ] )

def readString( file ):
	return file.readline().strip()

def readRawString( file ):
	newline = '\n'
	return file.readline().strip( newline )

def readAllStrings( file ):
	return [ line.strip() for line in file.readlines() ]

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
# Mid-CentralUSARegional2017.pdf - "Problem G : Faulty Robot"
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

			if distanceDict[ vertex ] < distance:
				continue

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

	def __iter__( self ):
		# Return an iterator which can traverse each element and its representative.
		return iter( [ (element, self._representative( element)) for element in self.uf ] )

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

			if costDict[ (city, flightTaken ) ] < cost:
				continue

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

				print( 'Testcase {} size = {} Maximum stones = {}'.format( index + 1, size, count ) )
				self.assertEqual( Ga( gameBoard ).ga(), count )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2009.pdf - "Problem E : The Pharaoh's Curse"
################################################################################

class Curse:
	def __init__( self, cavernMap ):
		self.rows, self.cols = len( cavernMap ), len( cavernMap[ 0 ] )
		self.cavernMap = cavernMap

		self.emptyCell, self.wallCell, self.stoneCell, self.startCell, self.buttonCell = '.', '#', 'X', 'S', 'B'
		self.exitCell = 'E'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (-1, 0), (1, 0) ]
		self.startLocation = None
		self.escapeImpossible = False
		
		stoneALocation = stoneBLocation = None
		buttonALocation = buttonBLocation = None
		
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			cellType = self.cavernMap[ row ][ col ]
			if cellType == self.startCell:
				self.startLocation = row, col
			elif cellType == self.stoneCell and stoneALocation is None:
				stoneALocation = row, col
			elif cellType == self.stoneCell:
				stoneBLocation = row, col
			elif cellType == self.buttonCell and buttonALocation is None:
				buttonALocation = row, col
			elif cellType == self.buttonCell and buttonBLocation is None:
				buttonBLocation = row, col
			elif cellType == self.buttonCell:
				# If there are more than two buttons, then escape is impossible.
				self.escapeImpossible = True

		self.stoneLocationTuple = stoneALocation, stoneBLocation
		self.buttonLocationTuple = buttonALocation, buttonBLocation

	def _stonesPlacedCorrectly( self, stoneLocationTuple ):
		S1, S2 = stoneLocationTuple
		buttonALocation, buttonBLocation = self.buttonLocationTuple
		
		if buttonALocation is None and buttonBLocation is None:
			return True
		elif buttonBLocation is None:
			return S1 == buttonALocation or S2 == buttonALocation
		else:
			return (S1, S2) == self.buttonLocationTuple or (S2, S1) == self.buttonLocationTuple

	def _isOutside( self, location ):
		r, c = location
		return not 0 <= r < self.rows or not 0 <= c < self.cols

	def escape( self ):
		startState = self.stoneLocationTuple, self.startLocation

		q = deque()
		if not self.escapeImpossible:
			q.append( startState )

		visited = set()
		visited.add( startState )

		stepCount = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				stoneLocationTuple, location = q.popleft()

				stoneALocation, stoneBLocation = stoneLocationTuple
				u, v = location

				if self.cavernMap[ u ][ v ] == self.exitCell and self._stonesPlacedCorrectly( stoneLocationTuple ):
					return stepCount

				for du, dv in self.adjacentCellDelta:
					newStoneALocation, newStoneBLocation = stoneALocation, stoneBLocation
					r, c = newLocation = u + du, v + dv
					
					if self._isOutside( newLocation ) or self.cavernMap[ r ][ c ] == self.wallCell:
						continue
					
					if newLocation == stoneALocation or newLocation == stoneBLocation:
						# Check whether we can move the sarcophagus.
						newStoneLocation = row, col = r + du, c + dv
						if self._isOutside( newStoneLocation ) or self.cavernMap[ row ][ col ] == self.wallCell:
							continue
						if newLocation == stoneALocation and newStoneLocation != stoneBLocation:
							newStoneALocation = newStoneLocation
						elif newLocation == stoneBLocation and newStoneLocation != stoneALocation:
							newStoneBLocation = newStoneLocation
						else:
							continue

					adjacentState = (newStoneALocation, newStoneBLocation), newLocation
					equivalentState = (newStoneBLocation, newStoneALocation), newLocation
					if adjacentState in visited or equivalentState in visited:
						continue
					visited.add( adjacentState )
					q.append( adjacentState )

			stepCount += 1
		return 'impossible'

class CurseTest( unittest.TestCase ):
	def test_Curse_Sample( self ):
		cavernMap = [
		'########',
		'#..S...#',
		'#.####.#',
		'#.#.XB.#',
		'#.####.#',
		'#......E',
		'########'
		]
		self.assertEqual( Curse( cavernMap ).escape(), 'impossible' )

		cavernMap = [
		'########',
		'#..S...#',
		'#.####.#',
		'#.#.BX.#',
		'#.####.#',
		'#......E',
		'########'
		]
		self.assertEqual( Curse( cavernMap ).escape(), 10 )

		cavernMap = [
		'##E#####',
		'#...####',
		'#SX.XBB#',
		'########'
		]
		self.assertEqual( Curse( cavernMap ).escape(), 19 )

	def test_Curse( self ):
		with open( 'tests/curse/testdata.in' ) as inputFile, \
		     open( 'tests/curse/testdata.out' ) as solutionFile:

			testcaseCount = readInteger( inputFile )
			for index in range( testcaseCount ):
				rows, cols = readIntegers( inputFile )
				cavernMap = [ readString( inputFile ) for _ in range( rows ) ]

				state = readString( solutionFile )
				if state != 'impossible':
					state = int( state )

				print( 'Testcase {} rows = {} cols = {} state= {}'.format( index + 1, rows, cols, state ) )
				self.assertEqual( Curse( cavernMap ).escape(), state )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2013_Preliminaries.pdf - "Problem K : Keys"
################################################################################

class Key:
	def __init__( self, buildingMap, keyString ):
		rows, cols = len( buildingMap ), len( buildingMap[ 0 ] )
		
		self.emptyCell, self.blockedCell, self.documentCell = '.', '*', '$'
		
		self.buildingMap = list()
		# Add a layer of empty cells around the building.
		emptyRow = self.emptyCell * ( cols + 2 )
		self.buildingMap.append( emptyRow )
		for buildingMapRow in buildingMap:
			self.buildingMap.append( self.emptyCell + buildingMapRow + self.emptyCell )
		self.buildingMap.append( emptyRow )

		self.rows, self.cols = rows + 2, cols + 2
		
		self.keyString = str() if keyString == '0' else keyString

		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def _key( self, keyString ):
		# We don't want repeated characters in the keyString.
		return ''.join( sorted( set( keyString ) ) )

	def _withinBuilding( self, location ):
		u, v = location
		return 0 <= u < self.rows and 0 <= v < self.cols

	def go( self ):
		startCell = 0, 0
		globalKeyString = self._key( self.keyString )

		documentLocations = set()

		stack = list()
		stack.append( startCell )

		visited = dict()

		while len( stack ) > 0:
			u, v = location = stack.pop()

			if location in visited and visited[ location ] == globalKeyString:
				continue

			if self.buildingMap[ u ][ v ] == self.documentCell:
				documentLocations.add( location )

			for du, dv in self.adjacentCellDelta:
				r, c = newLocation = u + du, v + dv
				if not self._withinBuilding( newLocation ):
					continue
				cellType = self.buildingMap[ r ][ c ]
				if cellType == self.blockedCell:
					continue

				if cellType.isalpha() and cellType.isupper() and cellType.lower() not in globalKeyString:
					continue

				if cellType.isalpha() and cellType.islower():
					globalKeyString = self._key( globalKeyString + cellType )

				stack.append( newLocation )

			visited[ location ] = globalKeyString

		return len( documentLocations )

class KeyTest( unittest.TestCase ):
	def test_Key_Sample( self ):
		buildingMap = [
		'*****************',
		'.............**$*',
		'*B*A*P*C**X*Y*.X.',
		'*y*x*a*p**$*$**$*',
		'*****************'
		]
		keyString = 'cz'
		self.assertEqual( Key( buildingMap, keyString ).go(), 3 )

		buildingMap = [
		'*.*********',
		'*...*...*x*',
		'*X*.*.*.*.*',
		'*$*...*...*',
		'***********'
		]
		keyString = '0'
		self.assertEqual( Key( buildingMap, keyString ).go(), 1 )

		buildingMap = [
		'*ABCDE*',
		'X.....F',
		'W.$$$.G',
		'V.$$$.H',
		'U.$$$.J',
		'T.....K',
		'*SQPML*'
		]
		keyString = 'irony'
		self.assertEqual( Key( buildingMap, keyString ).go(), 0 )

	def test_Key( self ):
		with open( 'tests/keys/K.in' ) as inputFile, \
		     open( 'tests/keys/K.out' ) as solutionFile:

			testcaseCount = readInteger( inputFile )
			for index in range( testcaseCount ):
				rows, cols = readIntegers( inputFile )
				buildingMap = [ readString( inputFile ) for _ in range( rows ) ]
				keyString = readString( inputFile )

				documentCount = readInteger( solutionFile )

				print( 'Testcase {} rows = {} cols = {} documentCount = {}'.format( index + 1, rows, cols, documentCount ) )
				self.assertEqual( Key( buildingMap, keyString ).go(), documentCount )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# BAPC2016.pdf - "Problem C: Brexit"
################################################################################

class Brexit:
	def __init__( self, numberOfCountries, homeCountry, leavingCountry, tradeList ):
		self.emptySet = set()
		self.tradingPartnersList = [ set() for _ in range( numberOfCountries + 1 ) ]
		self.homeCountry, self.leavingCountry = homeCountry, leavingCountry

		for (c1, c2) in tradeList:
			self.tradingPartnersList[ c1 ].add( c2 )
			self.tradingPartnersList[ c2 ].add( c1 )
		self.tradingPartnersCountList = [ len( tradingPartners ) for tradingPartners in self.tradingPartnersList ]

	def _isLeaving( self, country, leavingCountry ):
		self.tradingPartnersList[ country ].remove( leavingCountry )
		return self.tradingPartnersCountList[ country ] >= 2 * len( self.tradingPartnersList[ country ] )

	def eval( self ):
		evaluationSet = set()
		evaluationSet.add( self.leavingCountry )

		while len( evaluationSet ) > 0:
			leavingCountry = evaluationSet.pop()

			if leavingCountry == self.homeCountry:
				return 'leave'

			for tradingPartner in self.tradingPartnersList[ leavingCountry ]:
				if self._isLeaving( tradingPartner, leavingCountry ):
					evaluationSet.add( tradingPartner )
			self.tradingPartnersList[ leavingCountry ] = self.emptySet
		return 'stay'

class BrexitTest( unittest.TestCase ):
	def test_Brexit_Sample( self ):
		numberOfCountries = 4
		homeCountry, leavingCountry = 4, 1
		tradeList = [ (2, 3), (2, 4), (1, 2) ]
		self.assertEqual( Brexit( numberOfCountries, homeCountry, leavingCountry, tradeList ).eval(), 'stay' )

		numberOfCountries = 5
		homeCountry, leavingCountry = 1, 1
		tradeList = [ (3, 4), (1, 2), (2, 3), (1, 3), (2, 5) ]
		self.assertEqual( Brexit( numberOfCountries, homeCountry, leavingCountry, tradeList ).eval(), 'leave' )

		numberOfCountries = 4
		homeCountry, leavingCountry = 3, 1
		tradeList = [ (1, 2), (1, 3), (2, 3), (2, 4), (3, 4) ]
		self.assertEqual( Brexit( numberOfCountries, homeCountry, leavingCountry, tradeList ).eval(), 'stay' )

		numberOfCountries = 10
		homeCountry, leavingCountry = 1, 10
		tradeList = [ (1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5), (5, 6), (5, 7), (5, 8), (5, 9), (6, 10),
		(7, 10), (8, 10), (9, 10) ]
		self.assertEqual( Brexit( numberOfCountries, homeCountry, leavingCountry, tradeList ).eval(), 'leave' )

	def test_Brexit( self ):
		for testfile in getTestFileList( tag='brexit' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/brexit/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/brexit/{}.ans'.format( testfile ) ) as solutionFile:

			numberOfCountries, tradeListLength, homeCountry, leavingCountry = readIntegers( inputFile )
			tradeList = list()
			for _ in range( tradeListLength ):
				c1, c2 = readIntegers( inputFile )
				tradeList.append( (c1, c2) )

			leaveOrStay = readString( solutionFile )

			formatString = 'Testcase {} numberOfCountries = {} homeCountry = {} leavingCountry = {} leaveOrStay = {}'
			print( formatString.format( testfile, numberOfCountries, homeCountry, leavingCountry, leaveOrStay ) )
			self.assertEqual( Brexit( numberOfCountries, homeCountry, leavingCountry, tradeList ).eval(), leaveOrStay )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# BAPC2016.pdf - "Problem B: Battle Simulation"
################################################################################

class Battle:
	def __init__( self, battleString ):
		self.battleString = battleString
		self.counterMoveDict = {
		'R' : 'S', 'B' : 'K', 'L' : 'H',
		}
		self.comboMoveSet = set( [ 'RBL', 'RLB', 'BRL', 'BLR', 'LRB', 'LBR' ] )
		self.comboCounterMove = 'C'

	def fight( self ):
		counterMoveList = list()
		i = 0
		j = i + 3

		while i < len( self.battleString ):
			if j <= len( self.battleString ) and self.battleString[ i : j ] in self.comboMoveSet:
				counterMoveList.append( self.comboCounterMove )
				i = j
				j = i + 3
			else:
				counterMoveList.append( self.counterMoveDict[ self.battleString[ i ] ] )
				i, j = i + 1, j + 1
		return ''.join( counterMoveList )

class BattleTest( unittest.TestCase ):
	def test_Battle_Sample( self ):
		self.assertEqual( Battle( 'RRBBBLLR' ).fight(), 'SSKKKHHS' )
		self.assertEqual( Battle( 'RBLLLBRR' ).fight(), 'CHCS' )
		self.assertEqual( Battle( 'RBLBR' ).fight(), 'CKS' )

	def test_Battle( self ):
		for testfile in getTestFileList( tag='battle' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/battle/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/battle/{}.ans'.format( testfile ) ) as solutionFile:

			battleString = readString( inputFile )
			counterMoveString = readString( solutionFile )

			formatString = 'Testcase {} Battle string length = {} Counter move string length = {}'
			print( formatString.format( testfile, len( battleString ), len( counterMoveString ) ) )
			self.assertEqual( Battle( battleString ).fight(), counterMoveString )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Mid-CentralUSARegional2017.pdf - "Problem A : Nine Knights"
################################################################################

class NineKnights:
	def __init__( self, layout ):
		self.expectedKnightCount = 9
		self.knight = 'k'
		self.knightLocations = set()
		self.adjacentCellDelta = [ (1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1) ]

		rows, cols = len( layout ), len( layout[ 0 ] )
		for row, col in itertools.product( range( rows ), range( cols ) ):
			if layout[ row ][ col ] == self.knight:
				self.knightLocations.add( (row, col) )

	def analyze( self ):
		if len( self.knightLocations ) != self.expectedKnightCount:
			return 'invalid'
		for u, v in self.knightLocations:
			for du, dv in self.adjacentCellDelta:
				attackedLocation = u + du, v + dv
				if attackedLocation in self.knightLocations:
					return 'invalid'
		return 'valid'

class NineKnightsTest( unittest.TestCase ):
	def test_NineKnights( self ):
		for testfile in getTestFileList( tag='nineknights' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/nineknights/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/nineknights/{}.ans'.format( testfile ) ) as solutionFile:

			layout = [ readString( inputFile ) for _ in range( 5 ) ]
			state = readString( solutionFile )

			print( 'Testcase {} [{}]'.format( testfile, state ) )
			for layoutRow in layout:
				print( layoutRow )
			self.assertEqual( NineKnights( layout ).analyze(), state )

	def test_NineKnights_Sample( self ):
		layout = [
		'...k.',
		'...k.',
		'k.k..',
		'.k.k.',
		'k.k.k'
		]
		self.assertEqual( NineKnights( layout ).analyze(), 'invalid' )

		layout = [
		'.....',
		'...k.',
		'k.k.k',
		'.k.k.',
		'k.k.k'
		]
		self.assertEqual( NineKnights( layout ).analyze(), 'valid' )

		layout = [
		'.....',
		'...k.',
		'k.k.k',
		'.k.k.',
		'k...k'
		]
		self.assertEqual( NineKnights( layout ).analyze(), 'invalid' )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Mid-CentralUSARegional2016.pdf - "Problem D : Buggy Robot"
################################################################################

class BuggyRobot:
	def __init__( self, areaMap ):
		self.rows, self.cols = len( areaMap ), len( areaMap[ 0 ] )
		self.areaMap = areaMap

		self.commandTokenToDelta = {
		'U' : (-1, 0), 'D' : (1, 0), 'L' : (0, -1), 'R' : (0, 1)
		}
		self.emptyCell, self.blockedCell, self.startCell, self.goalCell = '.', '#', 'S', 'G'
		self.startLocation = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.areaMap[ row ][ col ] == self.startCell:
				self.startLocation = row, col

	def _applyCommand( self, location, commandToken ):
		u, v = location
		du, dv = self.commandTokenToDelta[ commandToken ]
		r, c = newLocation = u + du, v + dv
		if 0 <= r < self.rows and 0 <= c < self.cols and self.areaMap[ r ][ c ] != self.blockedCell:
			return newLocation
		else:
			return location

	def correct( self, commandString ):
		startIndex, endIndex = 0, len( commandString )

		q = deque()
		q.append( (self.startLocation, startIndex, 0) )

		visited = set()

		while len( q ) > 0:
			location, currentIndex, correctionCount = q.popleft()
			u, v = location

			if (location, currentIndex) in visited:
				continue
			visited.add( (location, currentIndex) )

			if self.areaMap[ u ][ v ] == self.goalCell:
				return correctionCount

			stateList = list()
			# Generate all possible state transitions from the current state.
			# 1. Apply the command at the currentIndex if currentIndex < endIndex.
			if currentIndex < endIndex:
				newLocation = self._applyCommand( location, commandString[ currentIndex ] )
				stateList.append( (newLocation, currentIndex + 1, False) )
			# 2. Insert a new command token.
			for commandToken in self.commandTokenToDelta.keys():
				newLocation = self._applyCommand( location, commandToken )
				stateList.append( (newLocation, currentIndex, True) )
			# 3. Delete the current command token (equivalent to ignoring the current command token, and
			#    incrementing the currentIndex).
			if currentIndex < endIndex:
				stateList.append( (location, currentIndex + 1, True) )

			for location, index, correctionMade in stateList:
				if (location, index) in visited:
					continue
				if correctionMade:
					q.append( (location, index, correctionCount + 1) )
				else:
					q.appendleft( (location, index, correctionCount) )

class BuggyRobotTest( unittest.TestCase ):
	def test_BuggyRobot( self ):
		for testfile in getTestFileList( tag='buggyrobot' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/buggyrobot/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/buggyrobot/{}.ans'.format( testfile ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			areaMap = [ readString( inputFile ) for _ in range( rows ) ]
			commandString = readString( inputFile )

			corrections = readInteger( solutionFile )

			formatString = 'Testcase {} rows = {} cols = {} commandString = [{}] corrections = {}'
			print( formatString.format( testfile, rows, cols, commandString, corrections ) )
			self.assertEqual( BuggyRobot( areaMap ).correct( commandString ), corrections )

	def test_BuggyRobot_Sample( self ):
		areaMap = [
		'S..',
		'.#.',
		'..G'
		]
		self.assertEqual( BuggyRobot( areaMap ).correct( 'DRRDD'), 1 )

		areaMap = [
		'.......',
		'.G.#.S.',
		'.......'
		]
		self.assertEqual( BuggyRobot( areaMap ).correct( 'LDLDLLDR'), 1 )

		areaMap = [
		'.#.....',
		'.G.##S.',
		'.......'
		]
		self.assertEqual( BuggyRobot( areaMap ).correct( 'LDLDLLDR'), 2 )

		areaMap = [
		'S.#.',
		'#..G'
		]
		self.assertEqual( BuggyRobot( areaMap ).correct( 'RRUUDDRRUUUU'), 0 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Mid-CentralUSARegional2014_Fun.pdf - "Problem B : Fun House"
################################################################################

class FunHouse:
	def __init__( self, carnivalRoom ):
		self.rows, self.cols = len( carnivalRoom ), len( carnivalRoom[ 0 ] )
		self.carnivalRoom = carnivalRoom

		self.startCell, self.emptyCell, self.wallCell, self.exitCell = '*', '.', 'x', '&'
		self.forwardMirrorCell, self.backwardMirrorCell = '/', '\\'

		# When a ray of light is traveling in direction d1, and hits the mirror type m, then
		# it gets reflected onto direction d2.
		# (d1, m) is mapped to d2 using the following dictionary.
		self.reflectionDirectionDict = {
		('E', '/') : 'N', ('E', '\\') : 'S',
		('W', '/') : 'S', ('W', '\\') : 'N',
		('N', '/') : 'E', ('N', '\\') : 'W',
		('S', '/') : 'W', ('S', '\\') : 'E'
		}
		self.directionDelta = {
		'N' : (-1, 0), 'S' : (1, 0), 'E' : (0, 1), 'W' : (0, -1)
		}

	def mark( self ):
		startLocation = None
		direction = None

		# We have to set up the startLocation and direction. Scan the horizontal edge.
		# If the startLocation is on row 0, direction is South; else direction is North.
		for row, col in itertools.product( [ 0, self.rows - 1 ], range( self.cols ) ):
			if self.carnivalRoom[ row ][ col ] == self.startCell:
				startLocation = row, col
				direction = 'S' if row == 0 else 'N'
				break
		for row, col in itertools.product( range( self.rows ), [ 0, self.cols - 1 ] ):
			if self.carnivalRoom[ row ][ col ] == self.startCell:
				startLocation = row, col
				direction = 'E' if col == 0 else 'W'

		location = startLocation
		exitLocation = None
		
		while True:
			u, v = location
			cellType = self.carnivalRoom[ u ][ v ]

			if cellType == self.wallCell:
				exitLocation = location
				break
			elif cellType == self.forwardMirrorCell or cellType == self.backwardMirrorCell:
				direction = self.reflectionDirectionDict[ (direction, cellType) ]
			du, dv = self.directionDelta[ direction ]
			location = u + du, v + dv

		# Fix the carnivalRoom so that exitLocation is marked by "self.exitCell".
		row, col = exitLocation
		replaceRow = list( self.carnivalRoom[ row ] )
		replaceRow[ col ] = self.exitCell
		self.carnivalRoom[ row ] = ''.join( replaceRow )
		return self.carnivalRoom

class FunHouseTest( unittest.TestCase ):
	def test_FunHouse_Sample( self ):
		carnivalRoom = [
		'xxxxxxxxxxx',
		'x../..\\...x', # We have to use \\ because \ is a an escape character.
		'x..../....x',
		'*../......x',
		'x.........x',
		'xxxxxxxxxxx'
		]
		carnivalRoomWithExit = [
		'xxxxxxxxxxx',
		'x../..\\...x',
		'x..../....x',
		'*../......x',
		'x.........x',
		'xxxxxx&xxxx'
		]
		self.assertEqual( FunHouse( carnivalRoom ).mark(), carnivalRoomWithExit )

	def test_FunHouse( self ):
		with open( 'tests/fun/fun.in' ) as inputFile, \
		     open( 'tests/fun/fun.out' ) as solutionFile:

			testcaseCount = 0
			while True:
				cols, rows = readIntegers( inputFile )
				if rows == 0 and cols == 0:
					break
				carnivalRoom = [ readString( inputFile ) for _ in range( rows ) ]

				readString( solutionFile )
				carnivalRoomWithExit = [ readString( solutionFile ) for _ in range( rows ) ]

				testcaseCount += 1
				print( 'Testcase #{} rows = {} cols = {}'.format( testcaseCount, rows, cols ) )

				for carnivalRoomRow, carnivalRoomWithExitRow in zip( carnivalRoom, carnivalRoomWithExit ):
					print( carnivalRoomRow, ' ' * 24, carnivalRoomWithExitRow )
				self.assertEqual( FunHouse( carnivalRoom ).mark(), carnivalRoomWithExit )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Croatian_Open_Competition_In_Informatics_2020_Round1.pdf - "Task Patkice"
################################################################################

class Patkice:
	def __init__( self, seaMap ):
		self.rows, self.cols = len( seaMap ), len( seaMap[ 0 ] )
		self.seaMap = seaMap

		self.calmSea, self.startIsland, self.targetIsland = '.', 'o', 'x'
		self.oceanCurrents = {
		'^' : (-1, 0), 'v' : (1, 0), '<' : (0, -1), '>' : (0, 1)
		}
		self.directions = {
		'N' : (-1, 0), 'S' : (1, 0), 'W' : (0, -1), 'E' : (0, 1)
		}

		self.startLocation = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.seaMap[ row ][ col ] == self.startIsland:
				self.startLocation = row, col

	def go( self ):
		bestDirection = bestDistance = None

		for direction in sorted( self.directions.keys() ):
			u, v = self.startLocation
			du, dv = self.directions[ direction ]
			u, v = u + du, v + dv
			stepCount = 1

			while True:
				currentCellType = self.seaMap[ u ][ v ]
				if currentCellType == self.targetIsland:
					if bestDistance is None or stepCount < bestDistance:
						bestDistance = stepCount
						bestDirection = direction
					break
				if currentCellType in (self.calmSea, self.startIsland):
					break
				du, dv = self.oceanCurrents[ currentCellType ]
				u, v = u + du, v + dv
				stepCount += 1
		return ':(' if bestDirection is None else ':) {}'.format( bestDirection )

class PatkiceTest( unittest.TestCase ):
	def test_Patkice( self ):
		for suffix in getTestFileSuffixList( tag='patkice' ):
			self._verify( suffix )

	def _verify( self, suffix ):
		with open( 'tests/patkice/patkice.in{}'.format( suffix ) ) as inputFile, \
		     open( 'tests/patkice/patkice.out{}'.format( suffix ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			seaMap = [ readString( inputFile ) for _ in range( rows ) ]

			state = readString( solutionFile )
			if state == ':)':
				direction = readString( solutionFile )
				state = '{} {}'.format( state, direction )

			print( 'Testcase {} rows = {} cols = {} state = {}'.format( suffix, rows, cols, state ) )
			self.assertEqual( Patkice( seaMap ).go(), state )

	def test_Patkice_Sample( self ):
		seaMap = [
		'..>>>v',
		'.o^..v',
		'.v.<.v',
		'.>>^.v',
		'.x<<<<',
		'......'
		]
		self.assertEqual( Patkice( seaMap ).go(), ":) E" )

		seaMap = [
		'v<<<<',
		'>v.>^',
		'v<.o.',
		'>>v>v',
		'..>>x'
		]
		self.assertEqual( Patkice( seaMap ).go(), ":) S" )

		seaMap = [
		'x>.',
		'.o^',
		'^<.'
		]
		self.assertEqual( Patkice( seaMap ).go(), ":(" )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Croatian_Open_Competition_In_Informatics_2020_Round4.pdf - "Task Patkice II"
################################################################################

class PatkiceV2( Patkice ):
	def __init__( self, seaMap ):
		Patkice.__init__( self, seaMap )

	def _isWithInSeaMap( self, location ):
		r, c = location
		return 0 <= r < self.rows and 0 <= c < self.cols

	def isValidCorrection( self, correctedSeaMap, count ):
		diffCount = 0
		for r, c in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.seaMap[ r ][ c ] == self.startIsland and correctedSeaMap[ r ][ c ] != self.startIsland:
				return False
			if self.seaMap[ r ][ c ] == self.targetIsland and correctedSeaMap[ r ][ c ] != self.targetIsland:
				return False
			if self.seaMap[ r ][ c ] != correctedSeaMap[ r ][ c ]:
				diffCount += 1
		return diffCount == count 

	def go( self ):
		# Can we go from the startLocation to targetIsland ? Return True or False !
		# A visited set is required because vortexes may exist.
		for direction in self.directions.keys():
			u, v = self.startLocation
			du, dv = self.directions[ direction ]
			u, v = u + du, v + dv

			visited = set()
			while True:
				location = u, v
				if not self._isWithInSeaMap( location ) or location in visited:
					break
				visited.add( location )
				currentCellType = self.seaMap[ u ][ v ]
				if currentCellType == self.targetIsland:
					return True
				if currentCellType in (self.calmSea, self.startIsland):
					break
				du, dv = self.oceanCurrents[ currentCellType ]
				u, v = u + du, v + dv
		return False

	def correct( self ):
		q = deque()
		visited = [ [ None for _ in range( self.cols ) ] for _ in range( self.rows ) ]

		u, v = self.startLocation
		for direction, (du, dv) in self.directions.items():
			r, c = location = u + du, v + dv
			if self._isWithInSeaMap( location ):
				q.append( (location, 0, None, None) )

		while len( q ) > 0:
			location, correctionCount, fromLocation, oceanCurrentType = q.popleft()
			u, v = location

			if self.seaMap[ u ][ v ] == self.targetIsland:
				break

			# If we have visited this state, then continue
			if visited[ u ][ v ] is not None:
				continue
			visited[ u ][ v ] = (fromLocation, oceanCurrentType)

			# We cannot modify the cell in the start location; hence do not explore this state.
			if location == self.startLocation:
				continue

			stateList = list()
			for oceanCurrentType, (du, dv) in self.oceanCurrents.items():
				r, c = newLocation = u + du, v + dv
				if not self._isWithInSeaMap( newLocation ):
					continue

				if self.seaMap[ u ][ v ] == oceanCurrentType:
					stateList.append( (newLocation, False, None) )
				else:
					stateList.append( (newLocation, True, oceanCurrentType) )

			for newLocation, correctionDone, oceanCurrentType in stateList:
				r, c = newLocation
				if visited[ r ][ c ] is not None:
					continue
				if correctionDone:
					q.append( (newLocation, correctionCount + 1, location, oceanCurrentType) )
				else:
					q.appendleft( (newLocation, correctionCount, location, oceanCurrentType) )

		# (location, correctionCount) contains target location and the minimum correction count.
		# fromLocation and oceanCurrentType are set for the target location. Traverse the path
		# in reverse, to gather the corrections that need to be applied.
		correctedSeaMap = [ list( seaMapRow ) for seaMapRow in self.seaMap ]
		while fromLocation is not None:
			if oceanCurrentType is not None:
				r, c = fromLocation
				correctedSeaMap[ r ][ c ] = oceanCurrentType
			location = u, v = fromLocation
			fromLocation, oceanCurrentType = visited[ u ][ v ]
		return correctionCount, [ ''.join( correctedSeaMapRow ) for correctedSeaMapRow in correctedSeaMap ]

class PatkiceV2Test( unittest.TestCase ):
	def test_PatkiceV2_Sample( self ):
		seaMap = [
		'>vo',
		'vv>',
		'x>>'
		]
		correctedSeaMap = [
		'>vo',
		'vv>',
		'x<>'
		]
		self._applyVerification( seaMap, correctedSeaMap, 1 )

		seaMap = [
		'>>vv<<',
		'^ovvx^',
		'^<<>>^'
		]
		correctedSeaMap = [
		'>>vv<<',
		'^o>>x^',
		'^<<>>^'
		]
		self._applyVerification( seaMap, correctedSeaMap, 2 )

		seaMap = [
		'x.v.',
		'.>.<',
		'>.<.',
		'.^.o'
		]
		correctedSeaMap = [
		'x<<.',
		'.>^<',
		'>.<^',
		'.^.o'
		]
		self._applyVerification( seaMap, correctedSeaMap, 4 )

	def test_PatkiceV2( self ):
		for suffix in getTestFileSuffixList( tag='patkiceV2' ):
			self._verify( suffix )

	def _verify( self, suffix ):
		with open( 'tests/patkiceV2/patkice2.in{}'.format( suffix ) ) as inputFile, \
		     open( 'tests/patkiceV2/patkice2.out{}'.format( suffix ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			seaMap = [ list( readString( inputFile ) ) for _ in range( rows ) ]

			minimumCorrections = readInteger( solutionFile )
			correctedSeaMap = [ readString( solutionFile ) for _ in range( rows ) ]

			print( 'Testcase patkice2{} rows = {} cols = {} minimumCorrections = {}'.format( suffix, rows, cols, minimumCorrections ) )
			self._applyVerification( seaMap, correctedSeaMap, minimumCorrections )

	def _applyVerification( self, seaMap, correctedSeaMap, minimumCorrections ):
		patkice = PatkiceV2( seaMap )
		corrections, modifiedSeaMap = patkice.correct()
		self.assertEqual( corrections, minimumCorrections )
		if correctedSeaMap != modifiedSeaMap:
			self.assertTrue( patkice.isValidCorrection( modifiedSeaMap, minimumCorrections ) )
			self.assertTrue( PatkiceV2( modifiedSeaMap ).go() )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Croatian_Open_Competition_In_Informatics_2007_Round1.pdf - "Peg"
################################################################################

class Peg:
	def __init__( self, boardLayout ):
		rows, cols = len( boardLayout ), len( boardLayout[ 0 ] )
		assert rows == cols == 7
		self.rows, self.cols = rows, cols
		self.boardLayout = boardLayout
		self.emptySlot, self.piece = '.', 'o'

		self.movementDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def _isInsideBoard( self, r, c ):
		return 0 <= r < self.rows and 0 <= c < self.cols

	def moveCount( self ):
		count = 0
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.boardLayout[ row ][ col ] == self.piece:
				# If there is a piece at (row, col) then check whether there is a piece and an empty slot at
				# (row + du, col + dv) and (row + 2 * du, col + 2 * dv) respectively, for all valid values of
				# (du, dv).
				for du, dv in self.movementDelta:
					r1, c1 = row + du, col + dv
					r2, c2 = r1 + du, c1 + dv
					if self._isInsideBoard( r1, c1 ) and self._isInsideBoard( r2, c2 ) and self.boardLayout[ r1 ][ c1 ] == self.piece \
					   and self.boardLayout[ r2 ][ c2 ] == self.emptySlot:
						count += 1
		return count

class PegTest( unittest.TestCase ):
	def test_Peg( self ):
		for suffix in getTestFileSuffixList( tag='peg' ):
			self._verify( suffix )

	def _verify( self, suffix ):
		with open( 'tests/peg/peg.in{}'.format( suffix ) ) as inputFile, \
		     open( 'tests/peg/peg.out{}'.format( suffix ) ) as solutionFile:

		     boardLayout = [ readRawString( inputFile ) for _ in range( 7 ) ]
		     count = readInteger( solutionFile )

		     print( 'Testcase peg{} Valid moves = {}'.format( suffix, count ) )
		     for boardLayoutRow in boardLayout:
		     	print( boardLayoutRow )
		     self.assertEqual( Peg( boardLayout ).moveCount(), count )

	def test_Peg_Sample( self ):
		boardLayout = [
		'  ooo  ',
		'  ooo  ',
		'ooooooo',
		'ooo.ooo',
		'ooooooo',
		'  ooo  ',
		'  ooo  '
		]
		self.assertEqual( Peg( boardLayout ).moveCount(), 4 )

		boardLayout = [
		'  ooo  ',
		'  ooo  ',
		'..ooo..',
		'oo...oo',
		'..ooo..',
		'  ooo  ',
		'  ooo  '
		]
		self.assertEqual( Peg( boardLayout ).moveCount(), 12 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Central Europe Regional Contest 2007
# KeyTask.pdf - "Key Task"
################################################################################

class KeyTask:
	def __init__( self, areaMap ):
		self.rows, self.cols = len( areaMap ), len( areaMap[ 0 ] )
		self.wallCell, self.emptyCell, self.startCell = '#', '.', '*'
		self.exitCell = 'X'
		self.doors = 'BYRG'
		self.keys = 'byrg'
		self.doorBitmapMask = {
		'B' : 0x1, 'Y' : 0x2, 'R' : 0x4, 'G' : 0x8
		}
		self.keyBitmapMask = {
		'b' : 0x1, 'y' : 0x2, 'r' : 0x4, 'g' : 0x8
		}

		self.areaMap = areaMap
		self.startLocation = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.areaMap[ row ][ col ] == self.startCell:
				self.startLocation = row, col
				break

		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]
		self.searchSuccess = 'Escape possible in {} steps.'
		self.searchFail = 'The poor student is trapped!'

	def _go( self ):
		state = self.startLocation, 0
		
		q = deque()
		q.append( state )

		visited = set()
		visited.add( state )

		stepCount = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				location, keyBitmap = q.popleft()
				u, v = location

				if self.areaMap[ u ][ v ] == self.exitCell:
					return stepCount

				for du, dv in self.adjacentCellDelta:
					r, c = newLocation = u + du, v + dv
					if not 0 <= r < self.rows or not 0 <= c < self.cols:
						continue
					cellType = self.areaMap[ r ][ c ]
					if cellType == self.wallCell:
						continue

					if cellType in self.doorBitmapMask and ( keyBitmap & self.doorBitmapMask[ cellType ] == 0 ):
						continue
					newKeyBitmap = keyBitmap
					if cellType in self.keyBitmapMask:
						newKeyBitmap = newKeyBitmap | ( self.keyBitmapMask[ cellType ] )

					newState = newLocation, newKeyBitmap
					if newState not in visited:
						visited.add( newState )
						q.append( newState )
			stepCount += 1
		return None

	def analyze( self ):
		steps = self._go()
		if steps is None:
			return self.searchFail
		else:
			return self.searchSuccess.format( steps )

class KeyTaskTest( unittest.TestCase ):
	def test_KeyTask( self ):
		with open( 'tests/keytask/k.in' ) as inputFile, \
		     open( 'tests/keytask/k.out' ) as solutionFile:

			testcaseCount = 0
			while True:
				rows, cols = readIntegers( inputFile )
				if rows == 0 and cols == 0:
					break

				testcaseCount += 1
				areaMap = [ readString( inputFile ) for _ in range( rows ) ]
				state = readString( solutionFile )

				# Discard the blank line between testcases.
				readString( inputFile )

				print( 'Testcase #{} rows = {} cols = {} [{}]'.format( testcaseCount, rows, cols, state ) )
				self.assertEqual( KeyTask( areaMap ).analyze(), state )

	def test_KeyTask_Sample( self ):
		areaMap = [
		'*........X'
		]
		self.assertEqual( KeyTask( areaMap ).analyze(), 'Escape possible in 9 steps.' )

		areaMap = [
		'*#X'
		]
		self.assertEqual( KeyTask( areaMap ).analyze(), 'The poor student is trapped!' )

		areaMap = [
		'####################',
		'#XY.gBr.*.Rb.G.GG.y#',
		'####################'
		]
		self.assertEqual( KeyTask( areaMap ).analyze(), 'Escape possible in 45 steps.' )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# Central Europe Regional Contest 2011
# StackMachineExecutor.pdf - "Stack Machine Executor"
################################################################################

class StackMachineError( Exception ):
	pass

class StackMachine:
	def __init__( self, program ):
		self.stack = list()
		self.program = program

		self.INT_MAX = 1_000_000_000

		self.instructionToMinimumStackSize = {
		'POP' : 1, 'INV' : 1, 'DUP' : 1,
		'SWP' : 2, 'ADD' : 2, 'SUB' : 2, 'MUL' : 2, 'DIV' : 2, 'MOD' : 2
		}

	def execute( self, initialValueList ):
		resultList = list()

		for initialValue in initialValueList:
			try:
				self.stack.append( initialValue )
				for instructionString in self.program:
					self._execute( instructionString )
				if len( self.stack ) != 1:
					resultList.append( 'ERROR' )
				else:
					resultList.append( self.stack.pop() )
			except StackMachineError as e:
				resultList.append( 'ERROR' )
			self.stack.clear()

		return resultList

	def _ensureStackSize( self, size ):
		if len( self.stack ) < size:
			raise StackMachineError( 'STACK UNDERFLOW' )

	def _ensureNoOverflow( self, result ):
		if abs( result ) > self.INT_MAX:
			raise StackMachineError( 'INTEGER OVERFLOW' )

	def _getOperands( self ):
		B = self.stack.pop()
		A = self.stack.pop()
		return A, B

	def _execute( self, instructionString ):
		self._ensureStackSize( self.instructionToMinimumStackSize.get( instructionString, 0 ) )

		if instructionString == 'POP':
			self.stack.pop()
		elif instructionString == 'INV':
			self.stack[ -1 ] = - self.stack[ -1 ]
		elif instructionString == 'DUP':
			self.stack.append( self.stack[ -1 ] )
		elif instructionString == 'SWP':
			A, B = self._getOperands()
			self.stack.append( B )
			self.stack.append( A )
		elif instructionString == 'ADD':
			A, B = self._getOperands()
			result = A + B
			self._ensureNoOverflow( result )
			self.stack.append( result )
		elif instructionString == 'SUB':
			A, B = self._getOperands()
			result = A - B
			self._ensureNoOverflow( result )
			self.stack.append( result )
		elif instructionString == 'MUL':
			A, B = self._getOperands()
			result = A * B
			self._ensureNoOverflow( result )
			self.stack.append( result )
		elif instructionString == 'DIV':
			A, B = self._getOperands()
			if B == 0:
				raise StackMachineError( 'DIVISION BY ZERO' )
			result = abs( A ) // abs( B )
			if A * B < 0:
				result = - result
			self.stack.append( result )
		elif instructionString == 'MOD':
			A, B = self._getOperands()
			if B == 0:
				raise StackMachineError( 'DIVISION BY ZERO' )
			result = abs( A ) % abs( B )
			if A < 0:
				result = - result
			self.stack.append( result )
		else:
			instruction, operand = instructionString.split()
			assert instruction == 'NUM'
			self.stack.append( int( operand ) )

class StackMachineTest( unittest.TestCase ):
	def test_StackMachine( self ):
		with open( 'tests/stackmachine/execute.in' ) as inputFile, \
		     open( 'tests/stackmachine/execute.out' ) as solutionFile:

			testcaseCount = 0
			while True:
				instructionString = readString( inputFile )
				if instructionString == 'QUIT':
					break

				testcaseCount += 1
				program = list()
				while True:
					if instructionString == 'END':
						break
					program.append( instructionString )
					instructionString = readString( inputFile )
				N = readInteger( inputFile )
				initialValueList = [ readInteger( inputFile ) for _ in range( N ) ]

				print( 'Testcase #{} Program size = {} Program runs = {}'.format( testcaseCount, len( program ), len( initialValueList ) ) )

				expectedSolution = list()
				for _ in range( N ):
					result = readString( solutionFile )
					expectedSolution.append( result if result == 'ERROR' else int( result ) )

				# Discard the blank line between testcases.
				readString( inputFile )
				readString( solutionFile )

				self.assertEqual( StackMachine( program ).execute( initialValueList ), expectedSolution )

	def test_StackMachine_Sample( self ):
		program = [ 'DUP', 'MUL', 'NUM 2', 'ADD' ]
		initialValueList = [ 1, 10, 50 ]
		
		self.assertEqual( StackMachine( program ).execute( initialValueList ), [ 3, 102, 2502 ] )

		program = [ 'NUM 1', 'NUM 1', 'ADD' ]
		initialValueList = [ 42, 43 ]
		
		self.assertEqual( StackMachine( program ).execute( initialValueList ), [ 'ERROR', 'ERROR' ] )

		program = [ 'NUM 600000000', 'ADD' ]
		initialValueList = [ 0, 600000000, 1 ]
		
		self.assertEqual( StackMachine( program ).execute( initialValueList ), [ 600000000, 'ERROR', 600000001 ] )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# VirginiaTechHighSchoolProgrammingContest_2019.pdf - "Problem C : Spelling Bee"
################################################################################

class SpellingBee:
	def __init__( self, letters, dictionary ):
		self.hexLetter, * _ = letters
		self.letters = set( letters )
		self.dictionary = dictionary

	def go( self ):
		def isValidWord( word ):
			return len( word ) >= 4 and self.hexLetter in word and set.issubset( set( word ), self.letters )
		return list( filter( isValidWord, self.dictionary ) )

class SpellingBeeTest( unittest.TestCase ):
	def test_SpellingBee( self ):
		for testfile in getTestFileList( tag='spellingbee' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/spellingbee/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/spellingbee/{}.ans'.format( testfile ) ) as solutionFile:

		     letters = readString( inputFile )
		     wordCount = readInteger( inputFile )
		     dictionary = [ readString( inputFile ) for _ in range( wordCount ) ]

		     validWordList = readAllStrings( solutionFile )

		     print( 'Testcase {} wordCount = {} valid words = {}'.format( testfile, wordCount, len( validWordList ) ) )
		     self.assertEqual( SpellingBee( letters, dictionary ).go(), validWordList )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# VirginiaTechHighSchoolProgrammingContest_2019.pdf - "Problem B : Escape Wall Maria"
################################################################################

class EscapeWallMaria:
	def __init__( self, areaMap, maximumTime ):
		self.rows, self.cols = len( areaMap ), len( areaMap[ 0 ] )
		self.areaMap = areaMap
		self.maximumTime = maximumTime

		self.startCell, self.safeCell, self.unsafeCell = 'S', '0', '1'
		self.adjacentCellDelta = {
		(0, 1) : 'L', (0, -1) : 'R', (1, 0) : 'U', (-1, 0) : 'D'
		}

		self.startLocation = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.areaMap[ row ][ col ] == self.startCell:
				self.startLocation = row, col
				break

	def _isOnBoundary( self, location ):
		u, v = location
		return u == 0 or u == self.rows - 1 or v == 0 or v == self.cols - 1

	def escape( self ):
		timeTaken = 0

		q = deque()
		q.append( self.startLocation )

		visited = set()
		visited.add( self.startLocation )

		while len( q ) > 0 and timeTaken <= self.maximumTime:
			N = len( q )
			while N > 0:
				N = N - 1

				currentLocation = q.popleft()
				if self._isOnBoundary( currentLocation ):
					return timeTaken

				u, v = currentLocation
				for (du, dv), allowedCellType in self.adjacentCellDelta.items():
					r, c = newLocation = u + du, v + dv
					cellType = self.areaMap[ r ][ c ]

					if cellType == self.unsafeCell:
						continue
					if ( cellType == self.safeCell or cellType == allowedCellType ) and newLocation not in visited:
						visited.add( newLocation )
						q.append( newLocation )
			timeTaken += 1
		return 'NOT POSSIBLE'

class EscapeWallMariaTest( unittest.TestCase ):
	def test_EscapeWallMaria_Sample( self ):
		maximumTime = 2
		areaMap = [
		'1111',
		'1S01',
		'1011',
		'0U11'
		]
		self.assertEqual( EscapeWallMaria( areaMap, maximumTime ).escape(), 2 )

	def test_EscapeWallMaria( self ):
		for testfile in getTestFileList( tag='escapewallmaria' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/escapewallmaria/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/escapewallmaria/{}.ans'.format( testfile ) ) as solutionFile:

			maximumTime, rows, cols = readIntegers( inputFile )
			areaMap = [ readString( inputFile ) for _ in range( rows ) ]

			escapeState = readString( solutionFile )
			if escapeState != 'NOT POSSIBLE':
				escapeState = int( escapeState )

			print( 'Testcase {} maximumTime = {} rows = {} cols = {}'.format( testfile, maximumTime, rows, cols ) )
			self.assertEqual( EscapeWallMaria( areaMap, maximumTime ).escape(), escapeState )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# UCF_2014.pdf - "Jumping Frog"
################################################################################

class JumpingFrog:
	def __init__( self, pathString, jumpDistance ):
		self.pathString = pathString
		self.jumpDistance = jumpDistance

		self.emptySlot, self.blockedSlot = '.', 'X'
		self.targetIndex = len( self.pathString ) - 1

	def jump( self ):
		currentIndex = 0
		stepCount = 0

		while True:
			if currentIndex == self.targetIndex:
				return stepCount
			newIndex = currentIndex
			# Jump as far as possible !
			# stepSize decreases from self.jumpDistance to 0.
			for stepSize in range( self.jumpDistance, -1, -1 ):
				j = min( currentIndex + stepSize + 1, self.targetIndex )
				if self.pathString[ j ] == self.emptySlot:
					newIndex = j
					stepCount += 1
					break
			if newIndex == currentIndex:
				return 0
			currentIndex = newIndex

class JumpingFrogTest( unittest.TestCase ):
	def test_JumpingFrog_Sample( self ):
		self.assertEqual( JumpingFrog( '.XX.X.X.', 3 ).jump(), 2 )
		self.assertEqual( JumpingFrog( '...', 1 ).jump(), 1 )
		self.assertEqual( JumpingFrog( '...XX...', 1 ).jump(), 0 )
		self.assertEqual( JumpingFrog( '..XXXX.XX.', 4 ).jump(), 3 )

	def test_JumpingFrog( self ):
		with open( 'tests/frog/frog.in' ) as inputFile, open( 'tests/frog/frog.out' ) as solutionFile:
			testcaseCount = readInteger( inputFile )

			for index in range( testcaseCount ):
				_, jumpDistance = readIntegers( inputFile )
				pathString = readString( inputFile )

				# Each section of output is of the form:
				# Day #1
				# 8 3
				# .XX.X.X.
				# 2
				# (blank line)
				_ = readString( solutionFile )
				_ = readString( solutionFile )
				_ = readString( solutionFile )
				expectedSteps = readInteger( solutionFile )
				_ = readString( solutionFile ) # blank line

				formatString = 'Testcase #{} pathString = {} d = {} steps = {}'
				print( formatString.format( index + 1, pathString, jumpDistance, expectedSteps ) )
				self.assertEqual( JumpingFrog( pathString, jumpDistance ).jump(), expectedSteps )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# DoraTrip.pdf - "Dora Trip"
################################################################################

class DoraTrip:
	def __init__( self, areaMap ):
		self.rows, self.cols = len( areaMap ), len( areaMap[ 0 ] )
		self.areaMap = areaMap

		self.startCell, self.emptyCell, self.blockedCell, self.wallCell, self.activityCell = 'S', ' ', 'X', '#', '*'
		
		self.startLocation = None
		self.activityBitNumberDict = dict()
		
		bitNumber = 0
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.areaMap[ row ][ col ] == self.startCell:
				self.startLocation = row, col
			elif self.areaMap[ row ][ col ] == self.activityCell:
				self.activityBitNumberDict[ (row, col) ] = bitNumber
				bitNumber += 1

		self.directionDelta = {
		'N' : (-1, 0), 'S' : (1, 0), 'E' : (0, 1), 'W' : (0, -1)
		}
		self.directionAttemptOrder = sorted( self.directionDelta.keys() )
		self.searchFailStatus = 'Stay home!'

	def path( self ):
		# Search state : current location, bitmap of activities, pathString, boolean which is True if Dora is heading back !
		q = deque()
		q.append( (self.startLocation, 0, str(), False) )

		visited = set()
		visited.add( (self.startLocation, 0, False) )

		bestActivityCount, bestPath = 0, str()
		
		while len( q ) > 0:
			location, bitmap, pathString, headingBack = q.popleft()
			activityCount = Bitmap.builtin_popcount( bitmap )
			
			if location == self.startLocation and headingBack:
				# We are back at the start location. Check the number of activities accumulated so that we can update
				# bestActivityCount and bestPath.
				if activityCount > bestActivityCount:
					bestActivityCount = activityCount
					bestPath = pathString
				continue

			u, v = location
			for direction in self.directionAttemptOrder:
				du, dv = self.directionDelta[ direction ]
				r, c = newLocation = u + du, v + dv
				# The areaMap is surrounded by wall cells. Hence, the newLocation is always within the areaMap.
				if self.areaMap[ r ][ c ] in (self.blockedCell, self.wallCell):
					continue
				newBitmap = bitmap
				if self.areaMap[ r ][ c ] == self.activityCell:
					bitNumber = self.activityBitNumberDict[ newLocation ]
					newBitmap = Bitmap.setBitnumber( bitmap, bitNumber )
				if (newLocation, newBitmap, headingBack) not in visited:
					visited.add( (newLocation, newBitmap, headingBack) )
					q.append( (newLocation, newBitmap, pathString + direction, headingBack) )
				# How about heading back from the current location ?
				if not headingBack and (newLocation, newBitmap, True) not in visited:
					visited.add( (newLocation, newBitmap, True) )
					q.append( (newLocation, newBitmap, pathString + direction, True) )

		return self.searchFailStatus if bestActivityCount == 0 else bestPath

class DoraTripTest( unittest.TestCase ):
	def test_DoraTrip( self ):
		with open( 'tests/doratrip/doratrip.in' ) as inputFile, open( 'tests/doratrip/doratrip.out' ) as solutionFile:
			testcaseCount = 0
			while True:
				rows, cols = readIntegers( inputFile )
				if rows == 0 and cols == 0:
					break
				testcaseCount += 1
				
				areaMap = [ readString( inputFile ) for _ in range( rows ) ]
				bestPath = readString( solutionFile )

				print( 'Testcase {} rows = {} cols = {} bestPath = {}'.format( testcaseCount, rows, cols, bestPath ) )
				for areaMapRow in areaMap:
					print( areaMapRow )
				self.assertEqual( DoraTrip( areaMap ).path(), bestPath )

	def test_DoraTrip_Sample( self ):
		areaMap = [
		'#####',
		'#  S#',
		'# XX#',
		'#  *#',
		'#####'
		]
		self.assertEqual( DoraTrip( areaMap ).path(), 'WWSSEEWWNNEE' )

		areaMap = [
		'#####',
		'#* X#',
		'###X#',
		'#S *#',
		'#####'
		]
		self.assertEqual( DoraTrip( areaMap ).path(), 'EEWW' )

		areaMap = [
		'#####',
		'#S X#',
		'#  X#',
		'# #*#',
		'#####'
		]
		self.assertEqual( DoraTrip( areaMap ).path(), 'Stay home!' )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
################################################################################
# BlackbeardThePirate.pdf - "Blackbeard The Pirate"
################################################################################

class Pirate:
	def __init__( self, areaMap ):
		self.rows, self.cols = len( areaMap ), len( areaMap[ 0 ] )
		self.areaMap = areaMap

		self.landingCell, self.waterCell, self.treeCell, self.sandCell, self.nativeCell, self.treasureCell = '@~#.*!'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]
		self.adjacentDiagonalDelta = [ (1, 1), (1, -1), (-1, 1), (-1, -1) ]

		bitNumber = 0
		self.treasureToBitNumberDict = dict()
		self.locationsToAvoid = set()
		self.startLocation = None
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			location, cellType = (row, col), self.areaMap[ row ][ col ]
			if cellType == self.landingCell:
				self.startLocation = location
			elif cellType == self.treasureCell:
				self.treasureToBitNumberDict[ location ] = bitNumber
				bitNumber += 1
			elif cellType == self.nativeCell:
				self.locationsToAvoid.add( location )
				for du, dv in self.adjacentCellDelta + self.adjacentDiagonalDelta:
					self.locationsToAvoid.add( (row + du, col + dv) )

		self.totalTreasures = bitNumber

	def go( self ):
		startState = self.startLocation, 0

		q = deque()
		q.append( startState )

		visited = set()
		visited.add( startState )

		stepCount = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				location, bitmap = q.popleft()

				u, v = location
				if location == self.startLocation and Bitmap.builtin_popcount( bitmap ) == self.totalTreasures:
					return stepCount

				for du, dv in self.adjacentCellDelta:
					r, c = newLocation = u + du, v + dv
					if not 0 <= r < self.rows or not 0 <= c < self.cols:
						continue
					# Avoid locations where natives are active.
					if newLocation in self.locationsToAvoid:
						continue
					cellType = self.areaMap[ r ][ c ]
					if cellType in (self.waterCell, self.treeCell):
						continue
					newBitmap = bitmap
					if cellType == self.treasureCell:
						newBitmap = Bitmap.setBitnumber( bitmap, self.treasureToBitNumberDict[ newLocation ] )
					newState = newLocation, newBitmap
					if newState not in visited:
						visited.add( newState )
						q.append( newState )
			stepCount += 1
		# It is not possible to obtain all treasures !
		return -1

class PirateTest( unittest.TestCase ):
	def test_Pirate( self ):
		with open( 'tests/pirate/pirate.in' ) as inputFile, open( 'tests/pirate/pirate.out' ) as solutionFile:
			testcaseCount = 0
			while True:
				rows, cols = readIntegers( inputFile )
				if rows == 0 and cols == 0:
					break
				testcaseCount += 1
				
				areaMap = [ readString( inputFile ) for _ in range( rows ) ]
				stepCount = readInteger( solutionFile )

				print( 'Testcase {} rows = {} cols = {} stepCount = {}'.format( testcaseCount, rows, cols, stepCount ) )
				for areaMapRow in areaMap:
					print( areaMapRow )
				self.assertEqual( Pirate( areaMap ).go(), stepCount )

	def test_Pirate_Sample( self ):
		areaMap = [
		'~~~~~~~',
		'~#!###~',
		'~...#.~',
		'~~....~',
		'~~~.@~~',
		'.~~~~~~',
		'...~~~.'
		]
		self.assertEqual( Pirate( areaMap ).go(), 10 )

		areaMap = [
		'~~~~~~~~~~',
		'~~!!!###~~',
		'~##...###~',
		'~#....*##~',
		'~#!..**~~~',
		'~~....~~~~',
		'~~~....~~~',
		'~~..~..@~~',
		'~#!.~~~~~~',
		'~~~~~~~~~~'
		]
		self.assertEqual( Pirate( areaMap ).go(), 32 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2016_Preliminaries.pdf - "Problem H : Presidential Elections"
################################################################################

class PresidentialElection:
	def __init__( self, stateInfoList ):
		self.stateInfoList = stateInfoList
		self.numberOfDelegates = 0
		for delegatesInState, _, _, _ in self.stateInfoList:
			self.numberOfDelegates += delegatesInState

	def analyze( self ):
		numberOfStates = len( self.stateInfoList )
		# delegateVoteList[ i ][ d ] - Minimum number of voters we need
		# to get exactly "d" delegates considering states upto index "i".
		# 0 <= i < numberOfStates
		# 0 <= d <= self.numberOfDelegates
		delegateVoteList = [ [ float( 'inf' ) for _ in range( self.numberOfDelegates + 1 ) ] for _ in range( numberOfStates ) ]
		for i in range( numberOfStates ):
			delegateVoteList[ i ][ 0 ] = 0

		for i in range( numberOfStates ):
			delegatesInState, voterCount_C, voterCount_F, undecidedVoters = self.stateInfoList[ i ]

			delegatesWeCanGet, votersToConvince = 0, 0
			votesNeededToWin = ( voterCount_C + voterCount_F + undecidedVoters ) // 2 + 1
			extraVotesNeeded = votesNeededToWin - voterCount_C
			if extraVotesNeeded > 0 and undecidedVoters >= extraVotesNeeded:
				votersToConvince = extraVotesNeeded
				delegatesWeCanGet = delegatesInState
			elif extraVotesNeeded <= 0:
				delegatesWeCanGet = delegatesInState

			if i == 0:
				delegateVoteList[ i ][ delegatesWeCanGet ] = votersToConvince
				continue

			for d in range( self.numberOfDelegates + 1 ):
				v1 = float( 'inf' ) if d - delegatesWeCanGet < 0 else \
				     delegateVoteList[ i - 1 ][ d - delegatesWeCanGet ] + votersToConvince
				v2 = delegateVoteList[ i - 1 ][ d ]
				delegateVoteList[ i ][ d ] = min( v1, v2 )

		minimumVotersToConvince = float( 'inf' )
		for d in range( self.numberOfDelegates // 2 + 1, self.numberOfDelegates + 1 ):
			votersToConvince = delegateVoteList[ numberOfStates - 1 ][ d ]
			minimumVotersToConvince = min( minimumVotersToConvince, votersToConvince )
		return 'impossible' if minimumVotersToConvince == float( 'inf' ) else minimumVotersToConvince

class PresidentialElectionTest( unittest.TestCase ):
	def test_PresidentialElection( self ):
		for testfile in getTestFileList( tag='presidential_elections' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/presidential_elections/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/presidential_elections/{}.ans'.format( testfile ) ) as solutionFile:

			numberOfStates = readInteger( inputFile )
			stateInfoList = [ list( readIntegers( inputFile ) ) for _ in range( numberOfStates ) ]

			votersToConvince = readString( solutionFile )
			if votersToConvince != 'impossible':
				votersToConvince = int( votersToConvince )

			print( 'Testcase {} numberOfStates = {} minimumVotersToConvince = {}'.format( testfile, numberOfStates, votersToConvince ) )
			self.assertEqual( PresidentialElection( stateInfoList ).analyze(), votersToConvince )

	def test_PresidentialElection_Sample( self ):
		stateInfoList = [
		(7, 2401, 3299, 0), (6, 2401, 2399, 0), (2, 750, 750, 99)
		]
		self.assertEqual( PresidentialElection( stateInfoList ).analyze(), 50 )

		stateInfoList = [
		(7, 100, 200, 200), (8, 100, 300, 200), (9, 100, 400, 200)
		]
		self.assertEqual( PresidentialElection( stateInfoList ).analyze(), 'impossible' )

		stateInfoList = [
		(32, 0, 0, 20), (32, 0, 0, 20), (64, 0, 0, 41)
		]
		self.assertEqual( PresidentialElection( stateInfoList ).analyze(), 32 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# BAPC2016_Preliminaries.pdf - "Problem G : Millionaire Madness"
################################################################################

class Millionaire:
	def __init__( self, vaultMap ):
		self.rows, self.cols = len( vaultMap ), len( vaultMap[ 0 ] )
		self.vaultMap = vaultMap

		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def go( self ):
		startLocation = 0, 0
		targetLocation = self.rows - 1, self.cols - 1

		q = list()
		q.append( (0, startLocation) )

		distanceDict = dict()
		distanceDict[ startLocation ] = 0

		while len( q ) > 0:
			ladderLength, location = heapq.heappop( q )
			if location == targetLocation:
				return ladderLength

			if distanceDict[ location ] < ladderLength:
				continue

			u, v = location
			for du, dv in self.adjacentCellDelta:
				r, c = newLocation = u + du, v + dv
				if not 0 <= r < self.rows or not 0 <= c < self.cols:
					continue
				newLadderLength = max( ladderLength, self.vaultMap[ r ][ c ] - self.vaultMap[ u ][ v ] )
				if newLocation not in distanceDict or distanceDict[ newLocation ] > newLadderLength:
					distanceDict[ newLocation ] = newLadderLength
					heapq.heappush( q, (newLadderLength, newLocation) )

class MillionaireTest( unittest.TestCase ):
	def test_Millionaire( self ):
		for testfile in getTestFileList( tag='millionaire' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/millionaire/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/millionaire/{}.ans'.format( testfile ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			vaultMap = [ list( readIntegers( inputFile ) ) for _ in range( rows ) ]

			ladderLength = readInteger( solutionFile )

			print( 'Testcase {} rows = {} cols = {} ladderLength = {}'.format( testfile, rows, cols, ladderLength ) )
			self.assertEqual( Millionaire( vaultMap ).go(), ladderLength )

	def test_Millionaire_Sample( self ):
		vaultMapStringList = [
		'1 2 3',
		'6 5 4',
		'7 8 9'
		]
		vaultMap = [ list( map( int, vaultMapString.split() ) ) for vaultMapString in vaultMapStringList ]
		self.assertEqual( Millionaire( vaultMap ).go(), 1 )

		vaultMapStringList = [
		'4 3 2 1'
		]
		vaultMap = [ list( map( int, vaultMapString.split() ) ) for vaultMapString in vaultMapStringList ]
		self.assertEqual( Millionaire( vaultMap ).go(), 0 )

		vaultMapStringList = [
		'10 11 12 13 14',
		'11 20 16 17 16',
		'12 10 18 21 24',
		'14 10 14 14 22',
		'16 18 20 20 25',
		'25 24 22 10 25',
		'26 27 28 21 25'
		]
		vaultMap = [ list( map( int, vaultMapString.split() ) ) for vaultMapString in vaultMapStringList ]
		self.assertEqual( Millionaire( vaultMap ).go(), 3 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# NorthAmericanInvitationalProgrammingContest_2014.pdf - " Problem J: Two Knight’s Poem"
################################################################################

class TwoKnights:
	def __init__( self ):
		self.upperKeys = [
		'QWERTYUIOP',
		'ASDFGHJKL:',
		'ZXCVBNM<>?',
		'$$      $$'
		]
		self.lowerKeys = [
		'qwertyuiop',
		'asdfghjkl;',
		'zxcvbnm,./',
		'$$      $$'
		]

		self.rows, self.cols = len( self.upperKeys ), len( self.upperKeys[ 0 ] )
		self.knight1Location = self.rows - 1, 0
		self.knight2Location = self.rows - 1, self.cols - 1

		self.movementDelta = [ (1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1) ]
		self.SHIFT_KEY = '$'

	def _isWithInKeyboard( self, location ):
		r, c = location
		return 0 <= r < self.rows and 0 <= c < self.cols

	def type_01( self, stringToType ):
		return 1 if self.type( stringToType ) else 0

	def type( self, stringToType ):
		startState = self.knight1Location, self.knight2Location, 0
		
		q = deque()
		q.append( startState )

		visited = set()
		visited.add( startState )

		while len( q ) > 0:
			knight1Location, knight2Location, index = q.popleft()
			if index == len( stringToType ):
				return True

			u1, v1 = knight1Location
			u2, v2 = knight2Location

			adjacentStateList = list()
			
			# Try to move knight1.
			for du, dv in self.movementDelta:
				r, c = newKnight1Location = u1 + du, v1 + dv
				if not self._isWithInKeyboard( newKnight1Location ):
					continue
				if newKnight1Location == knight2Location:
					continue
				typedCharacter = self.upperKeys[ r ][ c ] if self.lowerKeys[ u2 ][ v2 ] == self.SHIFT_KEY else self.lowerKeys[ r ][ c ]
				if typedCharacter == stringToType[ index ]:
					adjacentStateList.append( (newKnight1Location, knight2Location, index + 1) )
				elif typedCharacter == self.SHIFT_KEY:
					adjacentStateList.append( (newKnight1Location, knight2Location, index) )

			# Try to move knight2.
			for du, dv in self.movementDelta:
				r, c = newKnight2Location = u2 + du, v2 + dv
				if not self._isWithInKeyboard( newKnight2Location ):
					continue
				if newKnight2Location == knight1Location:
					continue
				typedCharacter = self.upperKeys[ r ][ c ] if self.lowerKeys[ u1 ][ v1 ] == self.SHIFT_KEY else self.lowerKeys[ r ][ c ]
				if typedCharacter == stringToType[ index ]:
					adjacentStateList.append( (knight1Location, newKnight2Location, index + 1) )
				elif typedCharacter == self.SHIFT_KEY:
					adjacentStateList.append( (knight1Location, newKnight2Location, index) )

			for newState in adjacentStateList:
				if newState not in visited:
					visited.add( newState )
					q.append( newState )
		return False

class TwoKnightsTest( unittest.TestCase ):
	def test_TwoKnights( self ):
		with open( 'tests/twoknights/twoKnights.in' ) as inputFile, \
		     open( 'tests/twoknights/twoKnights.out' ) as solutionFile:

			testcaseCount = 0
			while True:
				stringToType = readString( inputFile )
				if stringToType == '*':
					break
				testcaseCount += 1

				possibility = readInteger( solutionFile )

				print( 'Testcase #{} stringToType = [{}] state = {}'.format( testcaseCount, stringToType, possibility ) )
				self.assertEqual( TwoKnights().type_01( stringToType ), possibility )

	def test_TwoKnights_Sample( self ):
		twoKnights = TwoKnights()

		stringToType = 'S,veA,eVE,aU'
		self.assertEqual( twoKnights.type_01( stringToType ), 1 )

		stringToType = 'S,veA,eVE,aUc'
		self.assertEqual( twoKnights.type_01( stringToType ), 0 )

		stringToType = 'CAlmimg eventa'
		self.assertEqual( twoKnights.type_01( stringToType ), 1 )

		stringToType = 'CAL'
		self.assertEqual( twoKnights.type_01( stringToType ), 1 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# ObstacleCourse.pdf
################################################################################

class ObstacleCourse:
	def __init__( self, locationMap ):
		self.size = len( locationMap )
		self.locationMap = locationMap

		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def minimumEnergy( self ):
		startLocation, targetLocation = (0, 0), (self.size - 1, self.size - 1)
		initialCost = self.locationMap[ 0 ][ 0 ]
		
		q = list()
		q.append( (initialCost, startLocation) )

		costDict = dict()
		costDict[ startLocation ] = initialCost

		while len( q ) > 0:
			cost, location = heapq.heappop( q )
			if location == targetLocation:
				return cost

			if costDict[ location ] > cost:
				continue

			u, v = location
			for du, dv in self.adjacentCellDelta:
				r, c = newLocation = u + du, v + dv
				if not 0 <= r < self.size or not 0 <= c < self.size:
					continue
				newCost = cost + self.locationMap[ r ][ c ]
				if newLocation not in costDict or costDict[ newLocation ] > newCost:
					costDict[ newLocation ] = newCost
					heapq.heappush( q, (newCost, newLocation) )

class ObstacleCourseTest( unittest.TestCase ):
	def test_ObstacleCourse( self ):
		with open( 'tests/obstacle/d.in' ) as inputFile, \
		     open( 'tests/obstacle/d.out' ) as solutionFile:

			testcaseCount = 0
			while True:
				size = readInteger( inputFile )
				if size == 0:
					break

				testcaseCount += 1

				locationMapStringList = [ readString( inputFile ) for _ in range( size ) ]
				locationMap = [ list( map( int, locationMapStringRow.split() ) ) for locationMapStringRow in locationMapStringList ]

				_, _, minimumEnergy = readString( solutionFile ).split()
				minimumEnergy = int( minimumEnergy )

				print( 'Testcase #{} size = {} minimumEnergy = {}'.format( testcaseCount, size, minimumEnergy ) )
				self.assertEqual( ObstacleCourse( locationMap ).minimumEnergy(), minimumEnergy )

	def test_ObstacleCourse_Sample( self ):
		locationMapStringList = [
		'5 5 4',
		'3 9 1',
		'3 2 7'
		]
		locationMap = [ list( map( int, locationMapStringRow.split() ) ) for locationMapStringRow in locationMapStringList ]
		self.assertEqual( ObstacleCourse( locationMap ).minimumEnergy(), 20 )

		locationMapStringList = [
		'3 7 2 0 1',
		'2 8 0 9 1',
		'1 2 1 8 1',
		'9 8 9 2 0',
		'3 6 5 1 5'
		]
		locationMap = [ list( map( int, locationMapStringRow.split() ) ) for locationMapStringRow in locationMapStringList ]
		self.assertEqual( ObstacleCourse( locationMap ).minimumEnergy(), 19 )

		locationMapStringList = [
		'9 0 5 1 1 5 3',
		'4 1 2 1 6 5 3',
		'0 7 6 1 6 8 5',
		'1 1 7 8 3 2 3',
		'9 4 0 7 6 4 1',
		'5 8 3 2 4 8 3',
		'7 4 8 4 8 3 4'
		]
		locationMap = [ list( map( int, locationMapStringRow.split() ) ) for locationMapStringRow in locationMapStringList ]
		self.assertEqual( ObstacleCourse( locationMap ).minimumEnergy(), 36 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# HSPT2005.pdf - He Got the Box!
################################################################################

class Box:
	def __init__( self, areaMap ):
		self.rows, self.cols = len( areaMap ), len( areaMap[ 0 ] )
		self.areaMap = areaMap
		self.startCell, self.emptyCell, self.wallCell, self.boxCell = 'B', '.', 'W', 'X'

		self.startLocation = None
		self.teleportLocationDict = dict()

		teleportDevices = dict()
		for row, col in itertools.product( range( self.rows ), range( self.cols ) ):
			cellType = self.areaMap[ row ][ col ]
			if cellType == self.startCell:
				self.startLocation = row, col
			elif cellType in string.digits:
				if cellType in teleportDevices:
					cell1, cell2 = teleportDevices[ cellType ], (row, col)
					self.teleportLocationDict[ cell1 ] = cell2
					self.teleportLocationDict[ cell2 ] = cell1
				else:
					teleportDevices[ cellType ] = (row, col)

		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]
		self.message = 'He got the Box in {} steps!'

	def go( self ):
		q = deque()
		q.append( self.startLocation )

		visited = set()
		visited.add( self.startLocation )

		stepCount = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				u, v = currentLocation = q.popleft()
				if self.areaMap[ u ][ v ] == self.boxCell:
					return self.message.format( stepCount )

				possibleLocations = list()
				for du, dv in self.adjacentCellDelta:
					r, c = newLocation = u + du, v + dv
					if not 0 <= r < self.rows or not 0 <= c < self.cols:
						continue
					if self.areaMap[ r ][ c ] == self.wallCell:
						continue
					possibleLocations.append( newLocation )
					if newLocation in self.teleportLocationDict:
						possibleLocations.append( self.teleportLocationDict[ newLocation ] )

				for newLocation in possibleLocations:
					if newLocation not in visited:
						visited.add( newLocation )
						q.append( newLocation )
			stepCount += 1
		return None

class BoxTest( unittest.TestCase ):
	def test_Box( self ):
		with open( 'tests/box/box.in' ) as inputFile, \
		     open( 'tests/box/box.out' ) as solutionFile:

			testcaseCount = 0
			while True:
				rows, cols = readIntegers( inputFile )
				if rows == cols == 0:
					break
				testcaseCount += 1

				areaMap = [ readString( inputFile ) for _ in range( rows ) ]
				message = readString( solutionFile )

				print( 'Testcase #{} rows = {} cols = {} [{}]'.format( testcaseCount, rows, cols, message ) )
				for areaMapRow in areaMap:
					print( areaMapRow )

				self.assertEqual( Box( areaMap ).go(), message )

	def test_Box_Sample( self ):
		areaMap = [
		'B....',
		'....1',
		'WWWWW',
		'1....',
		'....X'
		]
		self.assertEqual( Box( areaMap ).go(), 'He got the Box in 10 steps!' )

		areaMap = [
		'...B',
		'WWW.',
		'5XW.',
		'WWW.',
		'.5..'
		]
		self.assertEqual( Box( areaMap ).go(), 'He got the Box in 7 steps!' )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# HSPT2021.pdf - Alphabetic Road Trip
################################################################################

class AlphabeticRoadTrip:
	def __init__( self, cityList, roadList ):
		self.startCityIndices = set()
		self.targetCityIndices = set()
		self.startLetter, self.endLetter = 'A', 'J'
		
		self.cityList = cityList
		self.cityToIndexDict = dict()
		for index, city in enumerate( cityList ):
			self.cityToIndexDict[ city ] = index
			startLetter, * _ = city
			if startLetter == self.startLetter:
				self.startCityIndices.add( index )
			elif startLetter == self.endLetter:
				self.targetCityIndices.add( index )

		self.roadNetwork = [ list() for _ in range( len( cityList ) ) ]
		for city1, city2, cost in roadList:
			city1Index = self.cityToIndexDict[ city1 ]
			city2Index = self.cityToIndexDict[ city2 ]
			self.roadNetwork[ city1Index ].append( (city2Index, cost) )
			self.roadNetwork[ city2Index ].append( (city1Index, cost) )

	def _nextLetter( self, letter ):
		return chr( ord( letter ) + 1 )

	def go( self  ):
		q = list()
		costDict = dict()

		for startCityIndex in sorted( self.startCityIndices ):
			q.append( (0, startCityIndex, self._nextLetter( self.startLetter) ) )
			costDict[ (startCityIndex, self._nextLetter( self.startLetter ) ) ] = 0

		while len( q ) > 0:
			cost, currentCityIndex, letterToMatch = heapq.heappop( q )
			if currentCityIndex in self.targetCityIndices and letterToMatch > self.endLetter:
				return cost

			if costDict[ (currentCityIndex, letterToMatch) ] < cost:
				continue

			for (toCityIndex, additionalCost) in self.roadNetwork[ currentCityIndex ]:
				city = self.cityList[ toCityIndex ]
				startLetter, * _ = city
				
				totalCost = cost + additionalCost
				
				nextLetterToMatch = letterToMatch
				if startLetter == letterToMatch:
					nextLetterToMatch = self._nextLetter( letterToMatch )

				costDictKey = (toCityIndex, nextLetterToMatch)
				if costDictKey not in costDict or costDict[ costDictKey ] > totalCost:
					costDict[ costDictKey ] = totalCost
					heapq.heappush( q,  (totalCost, toCityIndex, nextLetterToMatch) )

class AlphabeticRoadTripTest( unittest.TestCase ):
	def test_AlphabeticRoadTrip( self ):
		with open( 'tests/roadtrip/roadtrip.in' ) as inputFile, \
		     open( 'tests/roadtrip/roadtrip.out' ) as solutionFile:

			testcaseCount = readInteger( inputFile )
			for index in range( testcaseCount ):
				cityCount, roadCount = readIntegers( inputFile )

				cityList = [ readString( inputFile ) for _ in range( cityCount ) ]
				roadList = list()
				for _ in range( roadCount ):
					city1, city2, cost = readString( inputFile ).split()
					roadList.append( (city1, city2, int( cost ) ) )

				bestCost = readInteger( solutionFile )

				formatString = 'Testcase #{} Number of cities = {}, roads = {} bestCost = {}'
				print( formatString.format( index + 1, cityCount, roadCount, bestCost ) )

				self.assertEqual( AlphabeticRoadTrip( cityList, roadList ).go(), bestCost )

	def test_AlphabeticRoadTrip_Sample( self ):
		cityList = [ 'Alabama', 'Alaska', 'Buffalo', 'Columbia', 'Delaware', 'Elfville', 'Florida', 'Georgia',
		             'Hawaii', 'Idaho', 'Jupiter' ]
		roadList = [
		('Alabama', 'Jupiter', 1), ('Jupiter', 'Alaska', 2), ('Idaho', 'Jupiter', 1),
        ('Georgia', 'Idaho', 1), ('Hawaii', 'Georgia', 1), ('Florida', 'Hawaii', 1), ('Elfville', 'Florida', 1),
        ('Elfville', 'Delaware', 1), ('Delaware', 'Columbia', 1), ('Buffalo', 'Columbia', 1)
		]
		self.assertEqual( AlphabeticRoadTrip( cityList, roadList ).go(), 19 )

		cityList = [ 'Avalon', 'Harrison', 'Dover', 'Bermuda', 'Gillian', 'Camelot',
		             'Jackson', 'Elliot', 'Florida', 'Iguana' ]
		roadList = [
		('Dover', 'Avalon', 3), ('Avalon', 'Gillian', 10), ('Florida', 'Avalon', 71), 
		('Avalon', 'Bermuda', 5), ('Jackson', 'Avalon', 5), ('Avalon', 'Harrison', 52), ('Elliot', 'Avalon', 6), 
		('Iguana', 'Avalon', 4), ('Camelot', 'Avalon', 5)
		]
		self.assertEqual( AlphabeticRoadTrip( cityList, roadList ).go(), 317 )

################################################################################
################################################################################
################################################################################

################################################################################
################################################################################
# HSPT2006.pdf - Su-Do-Kode
################################################################################

class SudokuChecker:
	GRID_SIZE = 9

	@staticmethod
	def check( numberGrid ):
		rows, cols = len( numberGrid ), len( numberGrid[ 0 ] )
		if not rows == cols == SudokuChecker.GRID_SIZE:
			return False
		requisiteDigits = set( '123456789' )

		# Check whether each row contains numbers from 1 to 9.
		for numberGridRow in numberGrid:
			if set( numberGridRow ) != requisiteDigits:
				return False

		# Check whether each column contains numbers from 1 to 9.
		for col in range( cols ):
			numbersInColumn = set()
			for row in range( rows ):
				numbersInColumn.add( numberGrid[ row ][ col ] )
			if numbersInColumn != requisiteDigits:
				return False

		# Check whether each 3*3 grid contains numbers from 1 to 9.
		for startRow, startCol in itertools.product( range( 0, SudokuChecker.GRID_SIZE, 3 ), range( 0, SudokuChecker.GRID_SIZE, 3 ) ):
			numbersInGrid = set()
			for row, col in itertools.product( range( 3 ), range( 3 ) ):
				numbersInGrid.add( numberGrid[ startRow + row ][ startCol + col ] )
			if numbersInGrid != requisiteDigits:
				return False
		return True

class SuDoKode:
	def __init__( self, numberGrid ):
		self.numberGrid = numberGrid
		self.messageForValidGrid = 'Dave\'s the man!'
		self.messageForInvalidGrid = 'Try again, Dave!'

	def go( self ):
		return self.messageForValidGrid if SudokuChecker.check( self.numberGrid ) else self.messageForInvalidGrid

class SuDoKodeTest( unittest.TestCase ):
	def test_SuDoKode( self ):
		with open( 'tests/sudokode/sudokode.in' ) as inputFile, \
		     open( 'tests/sudokode/sudokode.out' ) as solutionFile:

			testcaseCount = readInteger( inputFile )
			for index in range( testcaseCount ):
				numberGrid = [ readString( inputFile ) for _ in range( 9 ) ]
				message = readString( solutionFile )
				readString( solutionFile ) # A blank line is present after each message.

				prefix = 'Sudoku #{}:  '.format( index + 1 )
				print( 'Testcase #{} {}'.format( index + 1, message ) )
				self.assertEqual( prefix + SuDoKode( numberGrid ).go(), message )

	def test_SuDoKode_Sample( self ):
		numberGrid = [
		'357648912',
		'216539748',
		'948712536',
		'521486397',
		'463197285',
		'789325164',
		'632974851',
		'174853629',
		'895261473'
		]
		self.assertEqual( SuDoKode( numberGrid ).go(), 'Dave\'s the man!' )

		numberGrid = [
		'263847159',
		'514936278',
		'987125364',
		'645382917',
		'139574826',
		'872619543',
		'658791632',
		'791263485',
		'326458791'
		]
		self.assertEqual( SuDoKode( numberGrid ).go(), 'Try again, Dave!' )

################################################################################
################################################################################
################################################################################

if __name__ == '__main__':
	unittest.main()