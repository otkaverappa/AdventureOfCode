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
from fractions import Fraction

def getTestFileList( tag ):
	return set( [ pathlib.Path( filename ).stem for filename in os.listdir( 'tests/usaco/{}'.format( tag ) ) ] )

def getTestFileSuffixList( tag ):
	return set( [ pathlib.Path( filename ).suffix for filename in os.listdir( 'tests/usaco/{}'.format( tag ) ) ] )

def readString( file ):
	return file.readline().strip()

def readStrings( file ):
	return file.readline().strip().split()

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

'''
USACO 2014 December Contest, Bronze

Problem 1: Marathon [Nick Wu, 2014]

Unhappy with the poor health of his cows, Farmer John enrolls them in
an assortment of different physical fitness activities.  His prize cow
Bessie is enrolled in a running class, where she is eventually
expected to run a marathon through the downtown area of the city near
Farmer John's farm!

The marathon course consists of N checkpoints (3 <= N <= 100,000) to
be visited in sequence, where checkpoint 1 is the starting location
and checkpoint N is the finish.  Bessie is supposed to visit all of
these checkpoints one by one, but being the lazy cow she is, she
decides that she will skip up to one checkpoint in order to shorten
her total journey.  She cannot skip checkpoints 1 or N, however, since
that would be too noticeable.

Please help Bessie find the minimum distance that she has to run if
she can skip up to one checkpoint.  

Note that since the course is set in a downtown area with a grid of
streets, the distance between two checkpoints at locations (x1, y1)
and (x2, y2) is given by |x1-x2| + |y1-y2|.  This way of measuring
distance -- by the difference in x plus the difference in y -- is
sometimes known as "Manhattan" distance because it reflects the fact
that in a downtown grid, you can travel parallel to the x or y axes,
but you cannot travel along a direct line "as the crow flies".

INPUT: (file marathon.in)

The first line gives the value of N.

The next N lines each contain two space-separated integers, x and y,
representing a checkpoint (-1000 <= x <= 1000, -1000 <= y <= 1000).
The checkpoints are given in the order that they must be visited.
Note that the course might cross over itself several times, with
several checkpoints occurring at the same physical location.  When
Bessie skips such a checkpoint, she only skips one instance of the
checkpoint -- she does not skip every checkpoint occurring at the same
location.

SAMPLE INPUT:

4
0 0
8 3
11 -1
10 0

OUTPUT: (file marathon.out)

Output the minimum distance that Bessie can run by skipping up to one
checkpoint.  Don't forget to end your output with a newline.  In the
sample case shown here, skipping the checkpoint at (8, 3) leads to the
minimum total distance of 14.

SAMPLE OUTPUT:

14
'''

class Marathon:
	def __init__( self, checkpointList ):
		self.checkpointList = checkpointList

	def totalMinimumDistance( self ):
		totalDistance = 0
		maximumSkipDistance = 0

		previousDistance = None
		for i in range( 1, len( self.checkpointList ) ):
			x, y = self.checkpointList[ i ]
			u, v = self.checkpointList[ i - 1 ]

			distance = abs( x - u ) + abs( y - v )
			totalDistance += distance

			if previousDistance is not None:
				m, n = self.checkpointList[ i - 2 ]
				skipDistance = abs( x - m ) + abs( y - n )
				skipDistance = previousDistance + distance - skipDistance
				maximumSkipDistance = max( maximumSkipDistance, skipDistance )
			previousDistance = distance

		return totalDistance - maximumSkipDistance

class MarathonTest( unittest.TestCase ):
	def test_Marathon_Sample( self ):
		checkpointList = [ (0, 0), (8, 3), (11, -1), (10, 0) ]
		self.assertEqual( Marathon( checkpointList ).totalMinimumDistance(), 14 )

	def test_Marathon( self ):
		for testfile in getTestFileList( tag='marathon' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/marathon/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/marathon/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			checkpointList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			totalMinimumDistance = readInteger( solutionFile )

			print( 'Testcase {} N = {} totalMinimumDistance = {}'.format( testfile, N, totalMinimumDistance ) )
			self.assertEqual( Marathon( checkpointList ).totalMinimumDistance(), totalMinimumDistance )

'''
USACO 2014 December Contest, Bronze

Problem 2: Crosswords [Mark Gordon, 2014]

Like all cows, Bessie the cow likes to solve crossword puzzles.
Unfortunately, her sister Elsie has spilled milk all over her book of
crosswords, smearing the text and making it difficult for her to see
where each clue begins.  It's your job to help Bessie out and recover
the clue numbering!

An unlabeled crossword is given to you as an N by M grid (3 <= N <=
50, 3 <= M <= 50).  Some cells will be clear (typically colored white)
and some cells will be blocked (typically colored black). Given this
layout, clue numbering is a simple process which follows two logical
steps:

Step 1: We determine if a each cell begins a horizontal or vertical
clue.  If a cell begins a horizontal clue, it must be clear, its
neighboring cell to the left must be blocked or outside the crossword
grid, and the two cells on its right must be clear (that is, a
horizontal clue can only represent a word of 3 or more characters).
The rules for a cell beginning a vertical clue are analogous: the cell
above must be blocked or outside the grid, and the two cells below
must be clear.

Step 2: We assign a number to each cell that begins a clue.  Cells are
assigned numbers sequentially starting with 1 in the same order that
you would read a book; cells in the top row are assigned numbers from
left to right, then the second row, etc.  Only cells beginning a clue
are assigned numbers.

For example, consider the grid, where '.' indicates a clear cell and
'#' a blocked cell.

...
#..
...
..#
.##

Cells that can begin a horizontal or vertical clue are marked with !
below:

!!!
#..
!..
..#
.##

If we assign numbers to these cells, we get the following;

123
#..
4..
..#
.##

Note that crossword described in the input data may not satisfy
constraints typically seen in published crosswords.  For example, some
clear cells may not be part of any clue.

INPUT: (file crosswords.in)

The first line of input contains N and M separated by a space.

The next N lines of input each describe a row of the grid.  Each
contains M characters, which are either '.' (a clear cell) or '#' (a
blocked cell).

SAMPLE INPUT:

5 3
...
#..
...
..#
.##

OUTPUT: (file crosswords.out)

On the first line of output, print the number of clues.

On the each remaining line, print the row and column giving the
position of a single clue (ordered as described above).  The top left
cell has position (1, 1).  The bottom right cell has position (N, M).

SAMPLE OUTPUT: 

4
1 1
1 2
1 3
3 1
'''

class Crosswords:
	def __init__( self, rows, cols, layout ):
		self.rows, self.cols = rows, cols
		self.layout = layout

		self.openCell, self.blockedCell = '.#'

	def clues( self ):
		clueList = list()

		for u in range( self.rows ):
			for v in range( self.cols ):
				if self.layout[ u ][ v ] == self.blockedCell:
					continue
				addCell = False
				if v == 0 or self.layout[ u ][ v - 1 ] == self.blockedCell:
					if v + 2 < self.cols and self.layout[ u ][ v + 1 ] == self.layout[ u ][ v + 2 ] == self.openCell:
						addCell = True
				if u == 0 or self.layout[ u - 1 ][ v ] == self.blockedCell:
					if u + 2 < self.rows and self.layout[ u + 1 ][ v ] == self.layout[ u + 2 ][ v ] == self.openCell:
						addCell = True
				if addCell:
					clueList.append( (u + 1, v + 1) )

		return clueList

class CrosswordsTest( unittest.TestCase ):
	def test_Crosswords_Sample( self ):
		rows, cols = 5, 3
		layout = [
		'...',
		'#..',
		'...',
		'..#',
		'.##'
		]
		self.assertEqual( Crosswords( rows, cols, layout ).clues(), [ (1, 1), (1, 2), (1, 3), (3, 1) ] )

	def test_Crosswords( self ):
		for testfile in getTestFileList( tag='crosswords' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/crosswords/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/crosswords/{}.out'.format( testfile ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			layout = [ readString( inputFile ) for _ in range( rows ) ]

			count = readInteger( solutionFile )
			clueList = [ tuple( readIntegers( solutionFile ) ) for _ in range( count ) ]

			print( 'Testcase {} rows = {} cols = {} clues = {}'.format( testfile, rows, cols, len( clueList ) ) )
			self.assertEqual( Crosswords( rows, cols, layout ).clues(), clueList )

'''
USACO 2014 December Contest, Bronze

Problem 3: Cow Jog [Mark Gordon, 2014]

The cows are out exercising their hooves again!  There are N cows
jogging on an infinitely-long single-lane track (1 <= N <= 100,000).
Each cow starts at a distinct position on the track, and some cows jog
at different speeds.

With only one lane in the track, cows cannot pass each other.  When a
faster cow catches up to another cow, she has to slow down to avoid
running into the other cow, becoming part of the same running group.

Eventually, no more cows will run into each other.  Farmer John
wonders how many groups will be left when this happens.  Please help
him compute this number.

INPUT: (file cowjog.in)

The first line of input contains the integer N.

The following N lines each contain the initial position and speed of a
single cow.  Position is a nonnegative integer and speed is a positive
integer; both numbers are at most 1 billion.  All cows start at 
distinct positions, and these will be given in increasing order in
the input.

SAMPLE INPUT:

5
0 1
1 2
2 3
3 2
6 1

OUTPUT: (file cowjog.out)

A single integer indicating how many groups remain.

SAMPLE OUTPUT:

2
'''

class CowJog:
	def __init__( self, positionSpeedList ):
		self.positionSpeedList = positionSpeedList

	def groups( self ):
		groupCount = 0
		keySpeed = float( 'inf' )

		for position, speed in reversed( self.positionSpeedList ):
			if speed <= keySpeed:
				groupCount += 1
				keySpeed = speed
		return groupCount

class CowJogTest( unittest.TestCase ):
	def test_CowJog_Sample( self ):
		positionSpeedList = [ (0, 1), (1, 2), (2, 3), (3, 2), (6, 1) ]
		self.assertEqual( CowJog( positionSpeedList ).groups(), 2 )

	def test_CowJog( self ):
		for testfile in getTestFileList( tag='cowjog' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowjog/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowjog/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			positionSpeedList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]

			groupCount = readInteger( solutionFile )

			print( 'Testcase {} N = {} groupCount = {}'.format( testfile, N, groupCount ) )
			self.assertEqual( CowJog( positionSpeedList ).groups(), groupCount )

if __name__ == '__main__':
	unittest.main()