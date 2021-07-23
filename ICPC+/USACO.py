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

'''
USACO 2014 December Contest, Bronze

Problem 4: Learning by Example [Brian Dean, 2014]

Farmer John has been reading all about the exciting field of machine
learning, where one can learn interesting and sometimes unexpected
patterns by analyzing large data (he has even started calling one of
the fields on his farm the "field of machine learning"!).  FJ decides
to use data about his existing cow herd to build an automatic
classifier that can guess whether a cow will have spots or not.

Unfortunately, FJ hasn't been very good at keeping track of data about
his cows.  For each of his N cows (1 <= N <= 50,000), all he knows is
the weight of the cow, and whether the cow has spots.  Each of his
cows has a distinct weight.  Given this data, he builds what is called
a "nearest neighbor classifier".  To guess whether a new cow C will
have spots or not, FJ first finds the cow C' in his herd with weight
closest to that of C.  If C' has spots, then FJ guesses that C will
also have spots; if C' has no spots, FJ guesses the same for C.  If
there is not one unique nearest neighbor C' but rather a tie between
two of FJ's cows, then FJ guesses that C will have spots if one or
both these nearest neighbors has spots.

FJ wants to test his new automatic spot predictor on a group of new
cows that are just arriving at his farm.  After weighing these cows,
he sees that the new shipment of cows contains a cow of every integer
weight between A and B (inclusive).  Please determine how many of
these cows will be classified as having spots, using FJ's new
classifier.  Note that the classifier only makes decisions using data
from FJ's N existing cows, not any of the new cows.  Also note that
since A and B can both be quite large, your program will not likely
run fast enough if it loops from A to B counting by ones.

INPUT: (file learning.in) 

The first line of the input contains three integers N, A, and B
(1 <= A <= B <= 1,000,000,000).

The next N lines each describe a single cow.  Each line contains
either S W, indicating a spotted cow of weight W, or NS W, indicating
a non-spotted cow of weight W.  Weights are all integers in the range
1 ... 1,000,000,000. 

SAMPLE INPUT:

3 1 10
S 10
NS 4
S 1

OUTPUT: (file learning.out)

A single integer giving the number of incoming cows that FJ's
algorithm will classify as having spots.  In the example shown
here, the incoming cows of weights 1, 2, 7, 8, 9, and 10 
will all be classified as having spots.

SAMPLE OUTPUT:

6
'''

class LearningByExample:
	def __init__( self, A, B, cowFeatureList ):
		self.A, self.B = A, B

		self.cowWeightList = list()
		self.cowFeatureList = list()
		for weight, feature in sorted( cowFeatureList ):
			self.cowWeightList.append( weight )
			self.cowFeatureList.append( feature )
		
		self.spot, self.noSpot = 'S', 'NS'

	def spots( self ):
		spottedCows = 0

		return spottedCows

class LearningByExampleTest( unittest.TestCase ):
	def test_LearningByExample_Sample( self ):
		A, B = 1, 10
		cowFeatureList = [ (10, 'S'), (4, 'NS'), (1, 'S') ]
		self.assertEqual( LearningByExample( A, B, cowFeatureList ).spots(), 6 )

	def test_LearningByExample( self ):
		for testfile in getTestFileList( tag='learning' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/learning/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/learning/{}.out'.format( testfile ) ) as solutionFile:

			N, A, B = readIntegers( inputFile )
			cowFeatureList = list()
			for _ in range( N ):
				feature, weight = readString( inputFile ).split()
				cowFeatureList.append( (int( weight ), feature) )

			spottedCows = readInteger( solutionFile )

			print( 'Testcase {} Cows = {} [{} : {}] spottedCows = {}'.format( testfile, N, A, B, spottedCows ) )
			self.assertEqual( LearningByExample( A, B, cowFeatureList ).spots(), spottedCows )

'''
USACO 2014 December Contest, Silver

Problem 1: Piggy Back [Brian Dean, 2014]

Bessie and her sister Elsie graze in different fields during the day,
and in the evening they both want to walk back to the barn to rest.
Being clever bovines, they come up with a plan to minimize the total
amount of energy they both spend while walking.

Bessie spends B units of energy when walking from a field to an
adjacent field, and Elsie spends E units of energy when she walks to
an adjacent field.  However, if Bessie and Elsie are together in the
same field, Bessie can carry Elsie on her shoulders and both can move
to an adjacent field while spending only P units of energy (where P
might be considerably less than B+E, the amount Bessie and Elsie would
have spent individually walking to the adjacent field).  If P is very
small, the most energy-efficient solution may involve Bessie and Elsie
traveling to a common meeting field, then traveling together piggyback
for the rest of the journey to the barn.  Of course, if P is large, it
may still make the most sense for Bessie and Elsie to travel
separately.  On a side note, Bessie and Elsie are both unhappy with
the term "piggyback", as they don't see why the pigs on the farm
should deserve all the credit for this remarkable form of
transportation.

Given B, E, and P, as well as the layout of the farm, please compute
the minimum amount of energy required for Bessie and Elsie to reach
the barn.

INPUT: (file piggyback.in)

The first line of input contains the positive integers B, E, P, N, and
M.  All of these are at most 40,000.  B, E, and P are described above.
N is the number of fields in the farm (numbered 1..N, where N >= 3),
and M is the number of connections between fields.  Bessie and Elsie
start in fields 1 and 2, respectively.  The barn resides in field N.

The next M lines in the input each describe a connection between a
pair of different fields, specified by the integer indices of the two
fields.  Connections are bi-directional.  It is always possible to
travel from field 1 to field N, and field 2 to field N, along a series
of such connections.  

SAMPLE INPUT:

4 4 5 8 8
1 4
2 3
3 4
4 7
2 5
5 6
6 8
7 8


OUTPUT: (file piggyback.out)

A single integer specifying the minimum amount of energy Bessie and
Elsie collectively need to spend to reach the barn.  In the example
shown here, Bessie travels from 1 to 4 and Elsie travels from 2 to 3
to 4.  Then, they travel together from 4 to 7 to 8.

SAMPLE OUTPUT:

22
'''

class Piggyback:
	def __init__( self, B, E, P, numberOfFields, connectionList ):
		self.B, self.E, self.P = B, E, P
		self.numberOfFields = numberOfFields
		self.graph = [ list() for _ in range( numberOfFields + 1 ) ]
		for u, v in connectionList:
			self.graph[ u ].append( v )
			self.graph[ v ].append( u )
		self.bessieField, self.elsieField, self.barnLocation = 1, 2, numberOfFields

	def _bfs( self, source, distanceList ):
		q = deque()
		q.append( source )

		distanceList[ source ] = 0

		while len( q ) > 0:
			currentLocation = q.popleft()
			for adjacentLocation in self.graph[ currentLocation ]:
				if distanceList[ adjacentLocation ] is None:
					distanceList[ adjacentLocation ] = distanceList[ currentLocation ] + 1
					q.append( adjacentLocation )

	def minimumEnergy( self ):
		distanceFromBessie = [ None for _ in range( self.numberOfFields + 1 ) ]
		distanceFromElsie  = [ None for _ in range( self.numberOfFields + 1 ) ]
		distanceFromBarn   = [ None for _ in range( self.numberOfFields + 1 ) ]

		self._bfs( self.bessieField, distanceFromBessie )
		self._bfs( self.elsieField, distanceFromElsie )
		self._bfs( self.barnLocation, distanceFromBarn )

		energyUsage = distanceFromBessie[ self.barnLocation ] * self.B + distanceFromElsie[ self.barnLocation ] * self.E
		for field in range( 1, self.numberOfFields + 1 ):
			if field == self.barnLocation:
				continue
			# Calculate energyUsage if field is the meeting point.
			energy = distanceFromBessie[ field ] * self.B + distanceFromElsie[ field ] * self.E + \
			         distanceFromBarn[ field ] * self.P
			energyUsage = min( energyUsage, energy )
		return energyUsage

class PiggybackTest( unittest.TestCase ):
	def test_Piggyback_Sample( self ):
		B, E, P, numberOfFields = 4, 4, 5, 8
		connectionList = [ (1, 4), (2, 3), (3, 4), (4, 7), (2, 5), (5, 6), (6, 8), (7, 8) ]
		self.assertEqual( Piggyback( B, E, P, numberOfFields, connectionList ).minimumEnergy(), 22 )

	def test_Piggyback( self ):
		for testfile in getTestFileList( tag='piggyback' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/piggyback/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/piggyback/{}.out'.format( testfile ) ) as solutionFile:

			B, E, P, numberOfFields, numberOfConnections = readIntegers( inputFile )
			connectionList = [ tuple( readIntegers( inputFile ) ) for _ in range( numberOfConnections ) ]

			minimumEnergy = readInteger( solutionFile )

			formatString = 'Testcase {} numberOfFields = {} numberOfConnections = {} minimumEnergy = {}'
			print( formatString.format( testfile, numberOfFields, numberOfConnections, minimumEnergy ) )
			self.assertEqual( Piggyback( B, E, P, numberOfFields, connectionList ).minimumEnergy(), minimumEnergy )

'''
USACO 2012 US Open, Bronze Division

Problem 1: Cows in a Row [Brian Dean, 2012]

Farmer John's N cows (1 <= N <= 1000) are lined up in a row.  Each cow is
identified by an integer "breed ID"; the breed ID of the ith cow in the
lineup is B(i).

FJ thinks that his line of cows will look much more impressive if there is
a large contiguous block of cows that all have the same breed ID.  In order
to create such a block, FJ decides remove from his lineup all the cows
having a particular breed ID of his choosing.  Please help FJ figure out
the length of the largest consecutive block of cows with the same breed ID
that he can create by removing all the cows having some breed ID of his
choosing.

PROBLEM NAME: cowrow

INPUT FORMAT:

* Line 1: The integer N.

* Lines 2..1+N: Line i+1 contains B(i), an integer in the range
        0...1,000,000.

SAMPLE INPUT (file cowrow.in):

9
2
7
3
7
7
3
7
5
7

INPUT DETAILS:

There are 9 cows in the lineup, with breed IDs 2, 7, 3, 7, 7, 3, 7, 5, 7.

OUTPUT FORMAT:

* Line 1: The largest size of a contiguous block of cows with
        identical breed IDs that FJ can create.

SAMPLE OUTPUT (file cowrow.out):

4

OUTPUT DETAILS:

By removing all cows with breed ID 3, the lineup reduces to 2, 7, 7, 7, 7,
5, 7.  In this new lineup, there is a contiguous block of 4 cows with the
same breed ID (7).
'''

class CowsInARow:
	def __init__( self, idList ):
		self.idList = idList

	def block( self ):
		frequencyDict = dict()
		i = j = 0

		blockSize = 0
		while j < len( self.idList ):
			id_ = self.idList[ j ]
			j += 1

			if id_ not in frequencyDict:
				frequencyDict[ id_ ] = 0
			frequencyDict[ id_ ] += 1

			while len( frequencyDict ) > 2:
				id_ = self.idList[ i ]
				i += 1
				frequencyDict[ id_ ] -= 1
				if frequencyDict[ id_ ] == 0:
					del frequencyDict[ id_ ]
			blockSize = max( blockSize, max( frequencyDict.values() ) )
		return blockSize

class CowsInARowTest( unittest.TestCase ):
	def test_CowsInARow( self ):
		for testfile in getTestFileList( tag='cowrow' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowrow/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowrow/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			idList = [ readInteger( inputFile ) for _ in range( N ) ]

			blockSize = readInteger( solutionFile )

			print( 'Testcase {} N = {} blockSize = {}'.format( testfile, N, blockSize ) )
			self.assertEqual( CowsInARow( idList ).block(), blockSize )

	def test_CowsInARow_Sample( self ):
		idList = [ 2, 7, 3, 7, 7, 3, 7, 5, 7 ]
		self.assertEqual( CowsInARow( idList ).block(), 4 )

'''
USACO 2012 March Contest, Silver Division

Problem 1: Tractor [Brian Dean, 2012]

After a long day of work, Farmer John completely forgot that he left his
tractor in the middle of the field.  His cows, always up to no good, decide
to play a prank of Farmer John: they deposit N bales of hay (1 <= N <=
50,000) at various locations in the field, so that Farmer John cannot
easily remove the tractor without first removing some of the bales of hay.  

The location of the tractor, as well as the locations of the N hay bales,
are all points in the 2D plane with integer coordinates in the range
1..1000.  There is no hay bale located at the initial position of the
tractor.  When Farmer John drives his tractor, he can only move it in
directions that are parallel to the coordinate axes (north, south, east,
and west), and it must move in a sequence of integer amounts.  For example,
he might move north by 2 units, then east by 3 units.  The tractor cannot
move onto a point occupied by a hay bale.

Please help Farmer John determine the minimum number of hay bales he needs
to remove so that he can free his tractor (that is, so he can drive his
tractor to the origin of the 2D plane).

PROBLEM NAME: tractor

INPUT FORMAT:

* Line 1: Three space-separated integers: N, and the (x,y) starting
        location of the tractor.

* Lines 2..1+N: Each line contains the (x,y) coordinates of a bale of
        hay.

SAMPLE INPUT (file tractor.in):

7 6 3
6 2
5 2
4 3
2 1
7 3
5 4
6 4

INPUT DETAILS:

The tractor starts at (6,3).  There are 7 bales of hay, at positions (6,2),
(5,2), (4,3), (2,1), (7,3), (5,4), and (6,4).

OUTPUT FORMAT:

* Line 1: The minimum number of bales of hay Farmer John must remove
        in order to open up a path for his tractor to move to the
        origin.

SAMPLE OUTPUT (file tractor.out):

1

OUTPUT DETAILS:

Farmer John only needs to remove one bale of hay to free his tractor.
'''

class Tractor:
	def __init__( self, tractorLocation, hayLocations ):
		self.tractorLocation = tractorLocation
		self.hayLocations = set( hayLocations )
		self.size = 1000

	def go( self ):
		q = deque()
		q.append( (0, self.tractorLocation) )

		visited = set()

		while len( q ) > 0:
			hay, currentLocation = q.popleft()

			u, v = currentLocation
			if u <= 0 or u > self.size or v <= 0 or v > self.size:
				return hay

			if currentLocation in visited:
				continue
			visited.add( currentLocation )

			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				adjacentLocation = x, y = u + du, v + dv
				if adjacentLocation in self.hayLocations:
					q.append( (hay + 1, adjacentLocation) )
				else:
					q.appendleft( (hay, adjacentLocation) )

class TractorTest( unittest.TestCase ):
	def test_Tractor_Sample( self ):
		tractorLocation = (6, 3)
		hayLocations = [ (6, 2), (5, 2), (4, 3), (2, 1), (7, 3), (5, 4), (6, 4) ]
		self.assertEqual( Tractor( tractorLocation, hayLocations ).go(), 1 )

	def test_Tractor( self ):
		for testfile in getTestFileList( tag='tractor' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/tractor/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/tractor/{}.out'.format( testfile ) ) as solutionFile:

			N, x, y = readIntegers( inputFile )
			tractorLocation = x, y
			hayLocations = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]

			removalCount = readInteger( solutionFile )

			print( 'Testcase {} hay locations count = {} removalCount = {}'.format( testfile, N, removalCount ) )
			self.assertEqual( Tractor( tractorLocation, hayLocations ).go(), removalCount )

'''
USACO 2011 December Contest, Bronze Division

Problem 1: Hay Bales [Brian Dean, 2011]

The cows are at it again!  Farmer John has carefully arranged N (1 <= N <=
10,000) piles of hay bales, each of the same height.  When he isn't
looking, however, the cows move some of the hay bales between piles, so
their heights are no longer necessarily the same.  Given the new heights of
all the piles, please help Farmer John determine the minimum number of hay
bales he needs to move in order to restore all the piles to their original,
equal heights.

PROBLEM NAME: haybales

INPUT FORMAT:

* Line 1: The number of piles, N (1 <= N <= 10,000).

* Lines 2..1+N: Each line contains the number of hay bales in a single
        pile (an integer in the range 1...10,000).

SAMPLE INPUT (file haybales.in):

4
2
10
7
1

INPUT DETAILS:

There are 4 piles, of heights 2, 10, 7, and 1.

OUTPUT FORMAT:

* Line 1: An integer giving the minimum number of hay bales that need
        to be moved to restore the piles to having equal heights.

SAMPLE OUTPUT (file haybales.out):

7

OUTPUT DETAILS:

By moving 7 hay bales (3 from pile 2 to pile 1, 2 from pile 2 to pile 4, 2
from pile 3 to pile 4), we can make all piles have height 5.
'''

class HayBales:
	def __init__( self, heightList ):
		self.heightList = heightList

	def go( self ):
		count = 0
		originalHeight = sum( self.heightList ) // len( self.heightList )

		for height in self.heightList:
			if height > originalHeight:
				count += height - originalHeight
		return count

class HayBalesTest( unittest.TestCase ):
	def test_HayBales( self ):
		for testfile in range( 1, 10 + 1 ):
			with open( 'tests/usaco/haybales/I.{}'.format( testfile ) ) as inputFile, \
			     open( 'tests/usaco/haybales/O.{}'.format( testfile ) ) as solutionFile:

				N = readInteger( inputFile )
				heightList = [ readInteger( inputFile ) for _ in range( N ) ]

				movesNeeded = readInteger( solutionFile )

				print( 'Testcase {} N = {} movesNeeded = {}'.format( testfile, N, movesNeeded ) )
				self.assertEqual( HayBales( heightList ).go(), movesNeeded )

	def test_HayBales_Sample( self ):
		heightList = [ 2, 10, 7, 1 ]
		self.assertEqual( HayBales( heightList ).go(), 7 ) 

'''
USACO 2011 December Contest, Bronze Division

Problem 2: Cow Photography (Bronze) [Brian Dean, 2011]

The cows are in a particularly mischievous mood today!  All Farmer John
wants to do is take a photograph of the cows standing in a line, but they
keep moving right before he has a chance to snap the picture.

Specifically, FJ's N (1 <= N <= 20,000) cows are tagged with ID numbers
1...N.  FJ wants to take a picture of the cows standing in a line in a
very specific ordering, represented by the contents of an array A[1...N],
where A[j] gives the ID number of the jth cow in the ordering.  He arranges
the cows in this order, but just before he can press the button on his
camera to snap the picture, up to one cow moves to a new position in the
lineup. More precisely, either no cows move, or one cow vacates her current
position in the lineup and then re-inserts herself at a new position in the
lineup.  Frustrated but not deterred, FJ again arranges his cows according
to the ordering in A, but again, right before he can snap a picture, up to
one cow (different from the first) moves to a new position in the lineup. 

The process above repeats for a total of five photographs before FJ gives
up.  Given the contents of each photograph, see if you can reconstruct the
original intended ordering A.  Each photograph shows an ordering of the
cows in which up to one cow has moved to a new location, starting from the
initial ordering in A.  Moreover, if a cow opts to move herself to a new
location in one of the photographs, then she does not actively move in any
of the other photographs (although she can end up at a different position
due to other cows moving, of course).

PROBLEM NAME: photo

INPUT FORMAT:

* Line 1: The number of cows, N (1 <= N <= 20,000).

* Lines 2..5N+1: The next 5N lines describe five orderings, each one a
        block of N contiguous lines.  Each line contains the ID of a
        cow, an integer in the range 1..N.

SAMPLE INPUT (file photo.in):

5
1 
2 
3 
4 
5
2
1
3
4
5
3
1
2
4
5
4
1
2
3
5
5
1
2
3
4

INPUT DETAILS:

There are 5 cows, with IDs 1, 2, 3, 4, and 5.  In each of the 5
photos, a different cow moves to the front of the line (although the cows
could have moved anywhere else, if they wanted).

OUTPUT FORMAT:

* Lines 1..N: The intended ordering A, one ID per line.

SAMPLE OUTPUT (file photo.out):

1
2
3
4
5

OUTPUT DETAILS:

The correct original ordering A[1..5] is 1,2,3,4,5.
'''

class CowPhotography:
	def __init__( self ):
		pass

class CowPhotographyTest( unittest.TestCase ):
	def test_CowPhotography_Sample( self ):
		pass

'''
USACO 2012 November Contest, Bronze

Problem 1: Find the Cow! [Brian Dean, 2012]

Bessie the cow has escaped and is hiding on a ridge covered with tall
grass.  Farmer John, in an attempt to recapture Bessie, has decided to
crawl through the grass on his hands and knees so he can approach
undetected.  Unfortunately, he is having trouble spotting Bessie from this
vantage point. The grass in front of Farmer John looks like a string of N
(1 <= N <= 50,000) parentheses; for example:

)((()())())

Farmer John knows that Bessie's hind legs look just like an adjacent pair
of left parentheses ((, and that her front legs look exactly like a pair of
adjacent right parentheses )).  Bessie's location can therefore be
described by a pair of indices x < y such that (( is found at position x, and
)) is found at position y.  Please compute the number of different such
possible locations at which Bessie might be standing.

PROBLEM NAME: cowfind

INPUT FORMAT:

* Line 1: A string of parentheses of length N (1 <= N <= 50,000).

SAMPLE INPUT (file cowfind.in):

)((()())())

OUTPUT FORMAT:

* Line 1: The number of possible positions at which Bessie can be
        standing -- that is, the number of distinct pairs of indices
        x < y at which there is the pattern (( at index x and the
        pattern )) at index y.

SAMPLE OUTPUT (file cowfind.out):

4

OUTPUT DETAILS:

There are 4 possible locations for Bessie, indicated below:

1. )((()())())
    ^^   ^^

2. )((()())())
     ^^  ^^

3. )((()())())
     ^^     ^^

4. )((()())())
    ^^      ^^
'''

class FindTheCow:
	def __init__( self, inputString ):
		self.inputString = inputString
		self.openBracket, self.closeBracket = '()'

	def go( self ):
		count = 0
		startLocations = 0
		for i in range( 1, len( self.inputString ) ):
			if self.inputString[ i ] == self.inputString[ i - 1 ] == self.openBracket:
				startLocations += 1
			elif self.inputString[ i ] == self.inputString[ i - 1 ] == self.closeBracket:
				count += startLocations
		return count

class FindTheCowTest( unittest.TestCase ):
	def test_FindTheCow_Sample( self ):
		self.assertEqual( FindTheCow( ')((()())())' ).go(), 4 )

	def test_FindTheCow( self ):
		for testfile in getTestFileList( tag='cowfind' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowfind/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowfind/{}.out'.format( testfile ) ) as solutionFile:

			inputString = readString( inputFile )
			count = readInteger( solutionFile )

			print( 'Testcase {} N = {} count = {}'.format( testfile, len( inputString ), count ) )
			self.assertEqual( FindTheCow( inputString ).go(), count )

'''
USACO 2012 November Contest, Bronze

Problem 3: Horseshoes [Brian Dean, 2012]

Although Bessie the cow finds every string of balanced parentheses to be
aesthetically pleasing, she particularly enjoys strings that she calls
"perfectly" balanced -- consisting of a string of ('s followed by a string
of )'s having the same length.  For example:

(((())))

While walking through the barn one day, Bessie discovers an N x N grid of
horseshoes on the ground, where each horseshoe is oriented so that it looks
like either ( or ).  Starting from the upper-left corner of this grid,
Bessie wants to walk around picking up horseshoes so that the string she
picks up is perfectly balanced.  Please help her compute the length of the
longest perfectly-balanced string she can obtain.

In each step, Bessie can move up, down, left, or right. She can only move
onto a grid location containing a horseshoe, and when she does this, she
picks up the horseshoe so that she can no longer move back to the same
location (since it now lacks a horseshoe).  She starts by picking up the
horseshoe in the upper-left corner of the grid.  Bessie only picks up a
series of horseshoes that forms a perfectly balanced string, and she may
therefore not be able to pick up all the horseshoes in the grid.

PROBLEM NAME: hshoe

INPUT FORMAT:

* Line 1: An integer N (2 <= N <= 5).

* Lines 2..N+1: Each line contains a string of parentheses of length
        N.  Collectively, these N lines describe an N x N grid of
        parentheses.

SAMPLE INPUT (file hshoe.in):

4
(())
()((
(()(
))))

OUTPUT FORMAT:

* Line 1: The length of the longest perfectly balanced string of
        horseshoes Bessie can collect.  If Bessie cannot collect any
        balanced string of horseshoes (e.g., if the upper-left square
        is a right parenthesis), output 0.

SAMPLE OUTPUT (file hshoe.out):

8

OUTPUT DETAILS:

The sequence of steps Bessie takes to obtain a balanced string of length 8
is as follows:

1())
2)((
345(
876)
'''

class HorseShoes:
	def __init__( self, layout ):
		self.size = len( layout )
		self.layout = layout

		self.leftShoe, self.rightShoe = '()'
		self.maximumHorseShoes = 0

	def _dfs( self, currentLocation, leftShoe, rightShoe, visited ):
		visited.add( currentLocation )
		
		u, v = currentLocation
		isLeftShoe = self.layout[ u ][ v ] == self.leftShoe

		if isLeftShoe:
			leftShoe += 1
		else:
			rightShoe += 1

		if leftShoe == rightShoe:
			self.maximumHorseShoes = max( self.maximumHorseShoes, leftShoe + rightShoe )
		# We cannot pick up a leftShoe if we have started picking up rightShoes.
		elif leftShoe < rightShoe or isLeftShoe and rightShoe > 0:
			pass
		else:
			for du, dv in [ (0, 1), (0, -1), (1, 0), (-1, 0) ]:
				m, n = adjacentLocation = u + du, v + dv
				if not 0 <= m < self.size or not 0 <= n < self.size:
					continue
				if adjacentLocation in visited:
					continue
				self._dfs( adjacentLocation, leftShoe, rightShoe, visited )
		visited.remove( currentLocation )

	def go( self ):
		startLocation = 0, 0
		visited = set()
		self._dfs( startLocation, 0, 0, visited )
		return self.maximumHorseShoes

class HorseShoesTest( unittest.TestCase ):
	def test_HorseShoes( self ):
		for testfile in getTestFileList( tag='horseshoe' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/horseshoe/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/horseshoe/{}.out'.format( testfile ) ) as solutionFile:

			size = readInteger( inputFile )
			layout = [ readString( inputFile ) for _ in range( size ) ]

			count = readInteger( solutionFile )

			layoutString = '_'.join( layout )
			print( 'Testcase {} Layout = {} count = {}'.format( testfile, layoutString, count ) )

			self.assertEqual( HorseShoes( layout ).go(), count )

	def test_HorseShoes_Sample( self ):
		layout = [
		'(())',
		'()((',
		'(()(',
		'))))'
		]
		self.assertEqual( HorseShoes( layout ).go(), 8 )

'''
USACO 2012 December Contest, Bronze

Problem 1: Meet and Greet [Brian Dean, 2012]

As is commonly known, cows are very socially polite creatures: any time two
cows meet after being apart, they greet each-other with a friendly "moo".

Bessie the cow and her friend, Elsie, are walking around on a long
path on Farmer John's farm.  For all practical purposes, we can think
of this path as a one-dimensional number line.  Bessie and Elsie both
start at the origin, and they both then begin walking around at
identical speeds for some amount of time.  Given a description of the
movements taken by each cow, please determine the number of "moos"
exchanged.  

Bessie and Elsie can stop moving at different points in time, and
neither cow will travel for more than 1,000,000 units of time.

PROBLEM NAME: greetings

INPUT FORMAT:

* Line 1: Two space-separated integers, B (1 <= B <= 50,000) and E 
        (1 <= E <= 50,000).

* Lines 2..1+B: These B lines describe Bessie's movements.  Each line
        contains a positive integer followed by either "L" or "R",
        indicating the distance Bessie moves in a direction that is
        either left or right.  

* Lines 2+B..1+B+E: These E lines describe Elsie's movements.  Each
        line contains a positive integer followed by either "L" or
        "R", indicating the distance Elsie moves in a direction that
        is either left or right.

SAMPLE INPUT (file greetings.in):

4 5
3 L
5 R
1 L
2 R
4 R
1 L
3 L
4 R
2 L

INPUT DETAILS:

Bessie moves left for 3 units of time, then right for 5 units of time, then
left for 1 unit of time, and finally right for 2 units of time; she then
stands still.  Elsie moves right for 4 units of time, then left for 4 units
of time, then right for 4 units of time, then left for 2 units of time; she
then stands still.

OUTPUT FORMAT:

* Line 1: An integer specifying the number of "moos" exchanged by the
        two cows.  Their initial shared starting position at the
        origin does not cause a "moo".

SAMPLE OUTPUT (file greetings.out):

3

OUTPUT DETAILS:

Bessie and Elsie meet after being temporarily apart at time 7, time 9, and
time 13.
'''

class MeetAndGreet:
	def __init__( self, movementInfo ):
		self.movementInfo = movementInfo

	def moo( self ):
		mooCount = 0

		time = 0
		movementInfo_A, movementInfo_B = self.movementInfo
		i = j = 0
		triggerTime_A = triggerTime_B = 0
		position_A = position_B = 0
		directionDelta_A = directionDelta_B = None
		
		while True:
			if time == triggerTime_A and i < len( movementInfo_A ):
				timeUnits, direction = movementInfo_A[ i ]
				i += 1
				directionDelta_A = -1 if direction == 'L' else 1
				triggerTime_A += timeUnits
			elif time == triggerTime_A:
				directionDelta_A = 0
			
			if time == triggerTime_B and j < len( movementInfo_B ):
				timeUnits, direction = movementInfo_B[ j ]
				j += 1
				directionDelta_B = -1 if direction == 'L' else 1
				triggerTime_B += timeUnits
			elif time == triggerTime_B:
				directionDelta_B = 0

			position_A += directionDelta_A
			position_B += directionDelta_B

			if position_A == position_B and directionDelta_A != directionDelta_B:
				mooCount += 1
			time += 1
			if time > triggerTime_A and time > triggerTime_B:
				break
		return mooCount

class MeetAndGreetTest( unittest.TestCase ):
	def test_MeetAndGreet( self ):
		for testfile in getTestFileList( tag='greetings' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/greetings/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/greetings/{}.out'.format( testfile ) ) as solutionFile:

			S1, S2 = readIntegers( inputFile )
			movementInfo_A = list()
			for _ in range( S1 ):
				timeUnits, direction = readString( inputFile ).split()
				movementInfo_A.append( (int( timeUnits ), direction) )
			movementInfo_B = list()
			for _ in range( S2 ):
				timeUnits, direction = readString( inputFile ).split()
				movementInfo_B.append( (int( timeUnits ), direction) )

			movementInfo = [ movementInfo_A, movementInfo_B ]
			mooCount = readInteger( solutionFile )

			print( 'Testcase {} [{}, {}] mooCount = {}'.format( testfile, S1, S2, mooCount ) )
			self.assertEqual( MeetAndGreet( movementInfo ).moo(), mooCount )

	def test_MeetAndGreet_Sample( self ):
		movementInfo = [
		[ (3, 'L'), (5, 'R'), (1, 'L'), (2, 'R') ],
		[ (4, 'R'), (1, 'L'), (3, 'L'), (4, 'R'), (2, 'L') ]
		]
		self.assertEqual( MeetAndGreet( movementInfo ).moo(), 3 )

'''
USACO 2012 December Contest, Bronze

Problem 2: Scrambled Letters [Brian Dean, 2012]

Farmer John keeps an alphabetically-ordered list of his N cows (1 <= N
<= 50,000) taped to the barn door.  Each cow name is represented by a
distinct string of between 1 and 20 lower-case characters.

Always the troublemaker, Bessie the cow alters the list by re-ordering
the cows on the list.  In addition, she also scrambles the letters in
each cow's name.  Given this modified list, please help Farmer John
compute, for each entry in the list, the lowest and highest positions
at which it could have possibly appeared in the original list.

PROBLEM NAME: scramble

INPUT FORMAT:

* Line 1: A single integer N.

* Lines 2..1+N: Each of these lines contains the re-ordered name of
        some cow.

SAMPLE INPUT (file scramble.in):

4
essieb
a
xzy
elsie

INPUT DETAILS:

There are 4 cows, with re-ordered names given above.

OUTPUT FORMAT:

* Lines 1..N: Line i should specify, for input string i, the lowest
        and highest positions in Farmer John's original list the
        original version of string i could have possibly appeared.

SAMPLE OUTPUT (file scramble.out):

2 3
1 1
4 4
2 3

OUTPUT DETAILS:

The string "a" would have appeared first on FJ's list no matter what, and
similarly the string "xzy" would have appeared last no matter how its
letters were originally ordered.  The two strings "essieb" and "elsie"
could have both occupied either positions 2 or 3, depending on their
original letter orderings (for example, "bessie" (position 2) and "elsie"
(position 3), versus "sisbee" (position 3) and "ilees" (position 2)).
'''

class ScrambledLetters:
	def __init__( self, nameList ):
		self.nameList = nameList

	def possibleRange( self ):
		numberOfNames = len( self.nameList )

		minimumPositionNameList = list()
		maximumPositionNameList = list()
		for name in self.nameList:
			A = ''.join( sorted( name ) )
			minimumPositionNameList.append( A )
			B = ''.join( sorted( name, reverse=True ) )
			maximumPositionNameList.append( B )
		minimumPositionNameList.sort()
		maximumPositionNameList.sort()

		possibleRangeList = list()
		for name in self.nameList:
			S = ''.join( sorted( name ) )
			minimumIndex = bisect.bisect_left( maximumPositionNameList, S )
			S = ''.join( sorted	( name, reverse=True ) )
			maximumIndex = bisect.bisect_right( minimumPositionNameList, S )
			possibleRangeList.append( (minimumIndex + 1, maximumIndex) )
		return possibleRangeList

class ScrambledLettersTest( unittest.TestCase ):
	def test_ScrambledLetters( self ):
		for testfile in getTestFileList( tag='scramble' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/scramble/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/scramble/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			nameList = [ readString( inputFile ) for _ in range( N ) ]
			possibleRange = [ tuple( readIntegers( solutionFile ) ) for _ in range( N ) ]

			print( 'Testcase {} N = {} [ {} --> {} ]'.format( testfile, N, nameList[ 0 ], nameList[ -1 ] ) )
			self.assertEqual( ScrambledLetters( nameList ).possibleRange(), possibleRange )

	def test_ScrambledLetters_Sample( self ):
		nameList = [ 'essieb', 'a', 'xzy', 'elsie' ]
		possibleRange = [ (2, 3), (1, 1), (4, 4), (2, 3) ]
		self.assertEqual( ScrambledLetters( nameList ).possibleRange(), possibleRange )

'''
USACO 2020 January Contest, Bronze

Problem 1. Word Processor

Bessie the cow is working on an essay for her writing class. Since her handwriting is quite bad, she decides to type the essay using a word processor.
The essay contains N words (1≤N≤100), separated by spaces. Each word is between 1 and 15 characters long, inclusive, and consists only of uppercase or lowercase letters. According to the instructions for the assignment, the essay has to be formatted in a very specific way: each line should contain no more than K (1≤K≤80) characters, not counting spaces. Fortunately, Bessie's word processor can handle this requirement, using the following strategy:

If Bessie types a word, and that word can fit on the current line, put it on that line.
Otherwise, put the word on the next line and continue adding to that line.
Of course, consecutive words on the same line should still be separated by a single space. There should be no space at the end of any line.

Unfortunately, Bessie's word processor just broke. Please help her format her essay properly!

INPUT FORMAT (file word.in):
The first line of input contains two space-separated integers N and K.
The next line contains N words separated by single spaces. No word will ever be larger than K characters, the maximum number of characters on a line.

OUTPUT FORMAT (file word.out):
Bessie's essay formatted correctly.
SAMPLE INPUT:
10 7
hello my name is Bessie and this is my essay
SAMPLE OUTPUT:
hello my
name is
Bessie
and this
is my
essay
Including "hello" and "my", the first line contains 7 non-space characters. Adding "name" would cause the first line to contain 11>7 non-space characters, so it is placed on a new line.

Problem credits: Nathan Pinsker
'''

class WordProcessor:
	@staticmethod
	def format( sentence, width ):
		wordList = list()

		currentLine = list()
		currentWidth = 0

		for word in sentence.split():
			wordLength = len( word )
			if currentWidth + wordLength > width:
				wordList.append( ' '.join( currentLine ) )
				currentLine.clear()
				currentWidth = 0
			currentLine.append( word )
			currentWidth += wordLength
		wordList.append( ' '.join( currentLine ) )
		return wordList

class WordProcessorTest( unittest.TestCase ):
	def test_WordProcessor_Sample( self ):
		sentence = 'hello my name is Bessie and this is my essay'
		width = 7
		wordList = [ 'hello my', 'name is', 'Bessie', 'and this', 'is my', 'essay' ]
		self.assertEqual( WordProcessor.format( sentence, width ), wordList )

	def test_WordProcessor( self ):
		for testfile in getTestFileList( tag='wordprocessor' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/wordprocessor/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/wordprocessor/{}.out'.format( testfile ) ) as solutionFile:

			_, width = readIntegers( inputFile )
			sentence = readString( inputFile )
			wordList = readAllStrings( solutionFile )

			print( 'Testcase {} sentence length = {} width = {}'.format( testfile, len( sentence ), width ) )
			self.assertEqual( WordProcessor.format( sentence, width ), wordList )

'''
USACO 2020 January Contest, Bronze

Problem 2. Photoshoot

Farmer John is lining up his N cows (2≤N≤103), numbered 1…N, for a photoshoot. FJ initially planned for the i-th cow from the left to be the cow numbered ai, and wrote down the permutation a1,a2,…,aN on a sheet of paper. Unfortunately, that paper was recently stolen by Farmer Nhoj!
Luckily, it might still be possible for FJ to recover the permutation that he originally wrote down. Before the sheet was stolen, Bessie recorded the sequence b1,b2,…,bN−1 that satisfies bi=ai+ai+1 for each 1≤i<N.

Based on Bessie's information, help FJ restore the "lexicographically minimum" permutation a that could have produced b. A permutation x is lexicographically smaller than a permutation y if for some j, xi=yi for all i<j and xj<yj (in other words, the two permutations are identical up to a certain point, at which x is smaller than y). It is guaranteed that at least one such a exists.

SCORING:
Test cases 2-4 satisfy N≤8.
Test cases 5-10 satisfy no additional constraints.
INPUT FORMAT (file photo.in):
The first line of input contains a single integer N.
The second line contains N−1 space-separated integers b1,b2,…,bN−1.

OUTPUT FORMAT (file photo.out):
A single line with N space-separated integers a1,a2,…,aN.
SAMPLE INPUT:
5
4 6 7 6
SAMPLE OUTPUT:
3 1 5 2 4
a produces b because 3+1=4, 1+5=6, 5+2=7, and 2+4=6.

Problem credits: Benjamin Qi and Chris Zhang
'''

class Photoshoot:
	def __init__( self, sumList ):
		self.sumList = sumList

	def _tryToConstruct( self, reconstructionList, usedIdSet ):
		for desiredSum in self.sumList:
			possibleId = desiredSum - reconstructionList[ -1 ]
			if possibleId > 0 and possibleId not in usedIdSet:
				usedIdSet.add( possibleId )
				reconstructionList.append( possibleId )
			else:
				return False
		return True

	def reconstruct( self ):
		reconstructionList = list()
		usedIdSet = set()
		
		S, * _ = self.sumList
		for K in range( 1, S ):
			reconstructionList.append( K )
			usedIdSet.add( K )
			if self._tryToConstruct( reconstructionList, usedIdSet ):
				break
			usedIdSet.clear()
			reconstructionList.clear()
		
		return reconstructionList

class PhotoshootTest( unittest.TestCase ):
	def test_Photoshoot( self ):
		for testfile in getTestFileList( tag='photoshoot' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/photoshoot/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/photoshoot/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			sumList = list( readIntegers( inputFile ) )
			constructedList = list( readIntegers( solutionFile ) )

			print( 'Testcase {} N = {}'.format( testfile, N ) )
			self.assertEqual( Photoshoot( sumList ).reconstruct(), constructedList )

	def test_Photoshoot_Sample( self ):
		sumList = [ 4, 6, 7, 6 ]
		self.assertEqual( Photoshoot( sumList ).reconstruct(), [ 3, 1, 5, 2, 4 ] )

'''
USACO 2015 December Contest, Gold

Problem 3. Bessie's Dream

After eating too much fruit in Farmer John's kitchen, Bessie the cow is getting some very strange dreams! In her most recent dream, she is trapped in a maze in the shape of an N×M grid of tiles (1≤N,M≤1,000). She starts on the top-left tile and wants to get to the bottom-right tile. When she is standing on a tile, she can potentially move to the adjacent tiles in any of the four cardinal directions.
But wait! Each tile has a color, and each color has a different property! Bessie's head hurts just thinking about it:

If a tile is red, then it is impassable.
If a tile is pink, then it can be walked on normally.
If a tile is orange, then it can be walked on normally, but will make Bessie smell like oranges.
If a tile is blue, then it contains piranhas that will only let Bessie pass if she smells like oranges.
If a tile is purple, then Bessie will slide to the next tile in that direction (unless she is unable to cross it). If this tile is also a purple tile, then Bessie will continue to slide until she lands on a non-purple tile or hits an impassable tile. Sliding through a tile counts as a move. Purple tiles will also remove Bessie's smell.
(If you're confused about purple tiles, the example will illustrate their use.)

Please help Bessie get from the top-left to the bottom-right in as few moves as possible.

INPUT FORMAT (file dream.in):
The first line has two integers N and M, representing the number of rows and columns of the maze.
The next N lines have M integers each, representing the maze:

The integer '0' is a red tile
The integer '1' is a pink tile
The integer '2' is an orange tile
The integer '3' is a blue tile
The integer '4' is a purple tile
The top-left and bottom-right integers will always be '1'.

OUTPUT FORMAT (file dream.out):
A single integer, representing the minimum number of moves Bessie must use to cross the maze, or -1 if it is impossible to do so.
SAMPLE INPUT:
4 4
1 0 2 1
1 1 4 1
1 0 4 0
1 3 1 1
SAMPLE OUTPUT:
10
In this example, Bessie walks one square down and two squares to the right (and then slides one more square to the right). She walks one square up, one square left, and one square down (sliding two more squares down) and finishes by walking one more square right. This is a total of 10 moves (DRRRULDDDR).

Problem credits: Nathan Pinsker, inspired by the game "Undertale".
'''

class Dream:
	def __init__( self, rows, cols, layout ):
		self.rows, self.cols = rows, cols
		self.layout = layout
		self.startLocation = 0, 0
		self.targetLocation = self.rows - 1, self.cols - 1

		self.redTile, self.pinkTile, self.orangeTile, self.blueTile, self.purpleTile = 0, 1, 2, 3, 4
		self.adjacentLocationDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def go( self ):
		orangeSmellDict = {
		True : 0, False : 1
		}

		visited = [ [ [ False for _ in range( self.cols ) ] for _ in range( self.rows ) ] for _ in range( 2 ) ]
		visitedPurpleTiles = set()

		q = deque()
		q.append( (self.startLocation, False, self.startLocation) )

		visited[ orangeSmellDict[ False ] ][ 0 ][ 0 ] = True

		stepCount = 0
		while len( q ) > 0:
			N = len( q )
			while N > 0:
				N = N - 1

				currentLocation, orangeSmell, previousLocation = q.popleft()
				if currentLocation == self.targetLocation:
					return stepCount

				u, v = currentLocation
				x, y = previousLocation
				du, dv = u - x, v - y
				isPurpleTile = ( self.layout[ u ][ v ] == self.purpleTile )
				if isPurpleTile and (currentLocation, previousLocation) in visitedPurpleTiles:
					continue
				elif isPurpleTile:
					orangeSmell = False
					visitedPurpleTiles.add( (currentLocation, previousLocation) )

				def _applyMovement( du, dv ):
					r, c = adjacentLocation = u + du, v + dv
					smell = orangeSmell
					if not 0 <= r < self.rows or not 0 <= c < self.cols:
						return 'Blocked'
					cellColor = self.layout[ r ][ c ]
					# Red tiles are impassable.
					if cellColor == self.redTile:
						return 'Blocked'
					elif cellColor == self.pinkTile:
						pass
					elif cellColor == self.orangeTile:
						smell = True
					elif cellColor == self.blueTile and not orangeSmell:
						return 'Blocked'
					
					if cellColor == self.purpleTile or not visited[ orangeSmellDict[ smell ] ][ r ][ c ]:
						visited[ orangeSmellDict[ smell ] ][ r ][ c ] = True
						q.append( (adjacentLocation, smell, currentLocation) )

				if ( isPurpleTile and _applyMovement( du, dv ) == 'Blocked' ) or not isPurpleTile:
					for du, dv in self.adjacentLocationDelta:
						_applyMovement( du, dv )
			stepCount += 1
		return -1

class DreamTest( unittest.TestCase ):
	def test_Dream( self ):
		for testfile in getTestFileList( tag='dream' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/dream/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/dream/{}.out'.format( testfile ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			layout = [ list( readIntegers( inputFile ) ) for _ in range( rows ) ]
			stepCount = readInteger( solutionFile )

			print( 'Testcase {} [{} x {}] stepCount = {}'.format( testfile, rows, cols, stepCount ) )
			self.assertEqual( Dream( rows, cols, layout ).go(), stepCount )

	def test_Dream_Sample( self ):
		rows, cols = 4, 4
		layout = [
		[ 1, 0, 2, 1 ],
		[ 1, 1, 4, 1 ],
		[ 1, 0, 4, 0 ],
		[ 1, 3, 1, 1 ]
		]
		self.assertEqual( Dream( rows, cols, layout ).go(), 10 )

'''
USACO 2015 December Contest, Silver

Problem 1. Switching on the Lights

Farmer John has recently built an enormous barn consisting of an N×N grid of rooms (2≤N≤100), numbered from (1,1) up to (N,N). Being somewhat afraid of the dark, Bessie the cow wants to turn on the lights in as many rooms as possible.
Bessie starts in room (1,1), the only room that is initially lit. In some rooms, she will find light switches that she can use to toggle the lights in other rooms; for example there might be a switch in room (1,1) that toggles the lights in room (1,2). Bessie can only travel through lit rooms, and she can only move from a room (x,y) to its four adjacent neighbors (x−1,y), (x+1,y), (x,y−1) and (x,y+1) (or possibly fewer neighbors if this room is on the boundary of the grid).

Please determine the maximum number of rooms Bessie can illuminate.

INPUT FORMAT (file lightson.in):
The first line of input contains integers N and M (1≤M≤20,000).
The next M lines each describe a single light switch with four integers x, y, a, b, that a switch in room (x,y) can be used to toggle the lights in room (a,b). Multiple switches may exist in any room, and multiple switches may toggle the lights of any room.

OUTPUT FORMAT (file lightson.out):
A single line giving the maximum number of rooms Bessie can illuminate.
SAMPLE INPUT:
 
3 6
1 1 1 2
2 1 2 2
1 1 1 3
2 3 3 1
1 3 1 2
1 3 2 1
SAMPLE OUTPUT:
5
Here, Bessie can use the switch in (1,1) to turn on lights in (1,2) and (1,3). She can then walk to (1,3) and turn on the lights in (2,1), from which she can turn on the lights in (2,2). The switch in (2,3) is inaccessible to her, being in an unlit room. She can therefore illuminate at most 5 rooms.

Problem credits: Austin Bannister and Brian Dean
'''

class Lights:
	def __init__( self, N, switchInfo ):
		self.N = N
		
		self.switchInfoDict = defaultdict( lambda : list() )
		for (x, y, a, b) in switchInfo:
			self.switchInfoDict[ (x, y) ].append( (a, b) )
		
		self.adjacentLocationDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def go( self ):
		startLocation = 1, 1
		
		q = deque()
		q.append( startLocation )

		visited = [ [ False for _ in range( self.N + 1 ) ] for _ in range( self.N + 1 ) ]
		visited[ 1 ][ 1 ] = True

		illuminatedRooms = set()
		illuminatedRooms.add( startLocation )

		adjacentUnlitRooms = set()

		while len( q ) > 0:
			u, v = currentLocation = q.popleft()

			for targetRoom in self.switchInfoDict[ currentLocation ]:
				illuminatedRooms.add( targetRoom )
				if targetRoom in adjacentUnlitRooms:
					adjacentUnlitRooms.remove( targetRoom )
					x, y = targetRoom
					visited[ x ][ y ] = True
					q.append( targetRoom )

			for du, dv in self.adjacentLocationDelta:
				x, y = adjacentLocation = u + du, v + dv
				if not 0 < x <= self.N or not 0 < y <= self.N or visited[ x ][ y ]:
					continue
				if adjacentLocation in illuminatedRooms:
					visited[ x ][ y ] = True
					q.append( adjacentLocation )
				else:
					adjacentUnlitRooms.add( adjacentLocation )

		return len( illuminatedRooms )

class LightsTest( unittest.TestCase ):
	def test_Lights( self ):
		for testfile in getTestFileList( tag='lights' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/lights/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/lights/{}.out'.format( testfile ) ) as solutionFile:

			N, numberOfSwitches = readIntegers( inputFile )
			switchInfo = [ tuple( readIntegers( inputFile ) ) for _ in range( numberOfSwitches ) ]
			illuminatedRooms = readInteger( solutionFile )

			formatString = 'Testcase {} N = {} numberOfSwitches = {} illuminatedRooms = {}'
			print( formatString.format( testfile, N, numberOfSwitches, illuminatedRooms ) )

			self.assertEqual( Lights( N, switchInfo ).go(), illuminatedRooms )

	def test_Lights_Sample( self ):
		N = 3
		switchInfo = [
		(1, 1, 1, 2),
		(2, 1, 2, 2),
		(1, 1, 1, 3),
		(2, 3, 3, 1),
		(1, 3, 1, 2),
		(1, 3, 2, 1)
		]
		self.assertEqual( Lights( N, switchInfo ).go(), 5 )

'''
USACO 2019 January Contest, Silver

Problem 2. Icy Perimeter

Farmer John is going into the ice cream business! He has built a machine that produces blobs of ice cream but unfortunately in somewhat irregular shapes, and he is hoping to optimize the machine to make the shapes produced as output more reasonable.
The configuration of ice cream output by the machine can be described using an N×N grid (1≤N≤1000) as follows:

##....
....#.
.#..#.
.#####
...###
....##
Each '.' character represents empty space and each '#' character represents a 1×1 square cell of ice cream.

Unfortunately, the machine isn't working very well at the moment and might produce multiple disconnected blobs of ice cream (the figure above has two). A blob of ice cream is connected if you can reach any ice cream cell from every other ice cream cell in the blob by repeatedly stepping to adjacent ice cream cells in the north, south, east, and west directions.

Farmer John would like to find the area and perimeter of the blob of ice cream having the largest area. The area of a blob is just the number of '#' characters that are part of the blob. If multiple blobs tie for the largest area, he wants to know the smallest perimeter among them. In the figure above, the smaller blob has area 2 and perimeter 6, and the larger blob has area 13 and perimeter 22.

Note that a blob could have a "hole" in the middle of it (empty space surrounded by ice cream). If so, the boundary with the hole also counts towards the perimeter of the blob. Blobs can also appear nested within other blobs, in which case they are treated as separate blobs. For example, this case has a blob of area 1 nested within a blob of area 16:

#####
#...#
#.#.#
#...#
#####
Knowing both the area and perimeter of a blob of ice cream is important, since Farmer John ultimately wants to minimize the ratio of perimeter to area, a quantity he calls the icyperimetric measure of his ice cream. When this ratio is small, the ice cream melts slower, since it has less surface area relative to its mass.

INPUT FORMAT (file perimeter.in):
The first line of input contains N, and the next N lines describe the output of the machine. At least one '#' character will be present.
OUTPUT FORMAT (file perimeter.out):
Please output one line containing two space-separated integers, the first being the area of the largest blob, and the second being its perimeter. If multiple blobs are tied for largest area, print the information for whichever of these has the smallest perimeter.
SAMPLE INPUT:
6
##....
....#.
.#..#.
.#####
...###
....##
SAMPLE OUTPUT:
13 22
Problem credits: Brian Dean
'''

class IcyPerimeter:
	def __init__( self, size, icecreamLayout ):
		self.size = size
		self.icecreamLayout = icecreamLayout

		self.emptyCell, self.icecreamCell = '.#'
		self.adjacentLocationDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def _floodFill( self, r, c, visited ):
		area = perimeter = 0

		q = deque()
		q.append( (r, c) )

		visited[ r ][ c ] = True
		area += 1

		while len( q ) > 0:
			u, v = q.popleft()
			for du, dv in self.adjacentLocationDelta:
				r, c = u + du, v + dv
				if not 0 <= r < self.size or not 0 <= c < self.size or self.icecreamLayout[ r ][ c ] == self.emptyCell:
					perimeter += 1
					continue
				if not visited[ r ][ c ]:
					visited[ r ][ c ] = True
					area += 1
					q.append( (r, c) )
		return area, perimeter

	def go( self ):
		visited = [ [ False for _ in range( self.size ) ] for _ in range( self.size ) ]

		area, perimeter =  0, 0
		for r, c in itertools.product( range( self.size ), range( self.size ) ):
			if self.icecreamLayout[ r ][ c ] == self.icecreamCell and not visited[ r ][ c ]:
				blockArea, blockPerimeter = self._floodFill( r, c, visited )
				if blockArea > area or blockArea == area and blockPerimeter < perimeter:
					area, perimeter = blockArea, blockPerimeter
		return area, perimeter

class IcyPerimeterTest( unittest.TestCase ):
	def test_IcyPerimeter( self ):
		for testfile in getTestFileList( tag='icyperimeter' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/icyperimeter/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/icyperimeter/{}.out'.format( testfile ) ) as solutionFile:

			size = readInteger( inputFile )
			icecreamLayout = [ readString( inputFile ) for _ in range( size ) ]
			area, perimeter = readIntegers( solutionFile )

			print( 'Testcase {} size = {} area = {} perimeter = {}'.format( testfile, size, area, perimeter ) )
			self.assertEqual( IcyPerimeter( size, icecreamLayout ).go(), (area, perimeter) )

	def test_IcyPerimeter_Sample( self ):
		size = 6
		icecreamLayout = [
		'##....',
		'....#.',
		'.#..#.',
		'.#####',
		'...###',
		'....##'
		]
		self.assertEqual( IcyPerimeter( size, icecreamLayout ).go(), (13, 22) )

'''
USACO 2015 December Contest, Bronze

Problem 1. Fence Painting

Several seasons of hot summers and cold winters have taken their toll on Farmer John's fence, and he decides it is time to repaint it, along with the help of his favorite cow, Bessie. Unfortunately, while Bessie is actually remarkably proficient at painting, she is not as good at understanding Farmer John's instructions.
If we regard the fence as a one-dimensional number line, Farmer John paints the interval between x=a and x=b. For example, if a=3 and b=5, then Farmer John paints an interval of length 2. Bessie, misunderstanding Farmer John's instructions, paints the interval from x=c to x=d, which may possibly overlap with part or all of Farmer John's interval. Please determine the total length of fence that is now covered with paint.

INPUT FORMAT (file paint.in):
The first line of the input contains the integers a and b, separated by a space (a<b).
The second line contains integers c and d, separated by a space (c<d).

The values of a, b, c, and d all lie in the range 0…100, inclusive.

OUTPUT FORMAT (file paint.out):
Please output a single line containing the total length of the fence covered with paint.
SAMPLE INPUT:
7 10
4 8
SAMPLE OUTPUT:
6
Here, 6 total units of fence are covered with paint, from x=4 all the way through x=10.

Problem credits: Brian Dean
'''

class FencePainting:
	@staticmethod
	def paint( a, b, c, d ):
		if b <= c or d <= a:
			return (b - a) + (d - c)
		else:
			return max( b, d ) - min( a, c )

class FencePaintingTest( unittest.TestCase ):
	def test_FencePainting( self ):
		for testfile in getTestFileList( tag='fencepainting' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/fencepainting/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/fencepainting/{}.out'.format( testfile ) ) as solutionFile:

			a, b = readIntegers( inputFile )
			c, d = readIntegers( inputFile )
			paintedLength = readInteger( solutionFile )
			
			print( 'Testcase {} [{}, {}] [{}, {}] paintedLength = {}'.format( testfile, a, b, c, d, paintedLength ) )
			self.assertEqual( FencePainting.paint( a, b, c, d ), paintedLength )

	def test_FencePainting_Sample( self ):
		self.assertEqual( FencePainting.paint( 7, 10, 4, 8 ), 6 )

'''
USACO 2015 December Contest, Bronze

Problem 2. Speeding Ticket

Always the troublemaker, Bessie the cow has stolen Farmer John's tractor and taken off down the road!
The road is exactly 100 miles long, and Bessie drives the entire length of the road before ultimately being pulled over by a police officer, who gives Bessie a ticket for exceeding the speed limit, for having an expired license, and for operating a motor vehicle while being a cow. While Bessie concedes that the last two tickets are probably valid, she questions whether the police officer was correct in issuing the speeding ticket, and she wants to determine for herself if she has indeed driven faster than the speed limit for part of her journey.

The road is divided into N segments, each described by a positive integer length in miles, as well as an integer speed limit in the range 1…100 miles per hour. As the road is 100 miles long, the lengths of all N segments add up to 100. For example, the road might start with a segment of length 45 miles, with speed limit 70, and then it might end with a segment of length 55 miles, with speed limit 60.

Bessie's journey can also be described by a series of segments, M of them. During each segment, she travels for a certain positive integer number of miles, at a certain integer speed. For example, she might begin by traveling 50 miles at a speed of 65, then another 50 miles at a speed of 55. The lengths of all M segments add to 100 total miles. Farmer John's tractor can drive 100 miles per hour at its fastest.

Given the information above, please determine the maximum amount over the speed limit that Bessie travels during any part of her journey.

INPUT FORMAT (file speeding.in):
The first line of the input contains N and M, separated by a space.
The next N lines each contain two integers describing a road segment, giving its length and speed limit.

The next M lines each contain two integers describing a segment in Bessie's journey, giving the length and also the speed at which Bessie was driving.

OUTPUT FORMAT (file speeding.out):
Please output a single line containing the maximum amount over the speed limit Bessie drove during any part of her journey. If she never exceeds the speed limit, please output 0.
SAMPLE INPUT:
3 3
40 75
50 35
10 45
40 76
20 30
40 40
SAMPLE OUTPUT:
5
In this example, the road contains three segments (40 miles at 75 miles per hour, followed by 50 miles at 35 miles per hour, then 10 miles at 45 miles per hour). Bessie drives for three segments (40 miles at 76 miles per hour, 20 miles at 30 miles per hour, and 40 miles at 40 miles per hour). During her first segment, she is slightly over the speed limit, but her last segment is the worst infraction, during part of which she is 5 miles per hour over the speed limit. The correct answer is therefore 5.

Problem credits: Austin Bannister and Brian Dean
'''

class SpeedingTicket:
	@staticmethod
	def excessSpeed( speedLimitInfoList, drivingSpeedInfoList ):
		cumulativeDistanceList = list()
		speedLimitList = list()
		cumulativeDistance = 0
		
		for segmentDistance, segmentSpeedLimit in speedLimitInfoList:
			cumulativeDistance += segmentDistance
			cumulativeDistanceList.append( cumulativeDistance )
			speedLimitList.append( segmentSpeedLimit )

		_excessSpeed = 0
		index = 0
		distanceTraveled = 0
		
		for distance, speed in drivingSpeedInfoList:
			distanceTraveled += distance

			while distanceTraveled > cumulativeDistanceList[ index ]:
				_excessSpeed = max( _excessSpeed, speed - speedLimitList[ index ] )
				index += 1
			_excessSpeed = max( _excessSpeed, speed - speedLimitList[ index ] )
			if distanceTraveled == cumulativeDistanceList[ index ]:
				index += 1
		return _excessSpeed

class SpeedingTicketTest( unittest.TestCase ):
	def  test_SpeedingTicket( self ):
		for testfile in getTestFileList( tag='speedingticket' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/speedingticket/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/speedingticket/{}.out'.format( testfile ) ) as solutionFile:

			N, M = readIntegers( inputFile )
			speedLimitInfoList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			drivingSpeedInfoList = [ tuple( readIntegers( inputFile ) ) for _ in range( M ) ]
			excessSpeed = readInteger( solutionFile )

			print( 'Testcase {} N = {} M = {} excessSpeed = {}'.format( testfile, N, M, excessSpeed ) )
			self.assertEqual( SpeedingTicket.excessSpeed( speedLimitInfoList, drivingSpeedInfoList ), excessSpeed )

	def test_SpeedingTicket_Sample( self ):
		speedLimitInfoList = [ (40, 75), (50, 35), (10, 45) ]
		drivingSpeedInfoList = [ (40, 76), (20, 30), (40, 40) ]
		self.assertEqual( SpeedingTicket.excessSpeed( speedLimitInfoList, drivingSpeedInfoList ), 5 )

'''
USACO 2015 December Contest, Silver

Problem 3. Breed Counting

Farmer John's N cows, conveniently numbered 1…N, are all standing in a row (they seem to do so often that it now takes very little prompting from Farmer John to line them up). Each cow has a breed ID: 1 for Holsteins, 2 for Guernseys, and 3 for Jerseys. Farmer John would like your help counting the number of cows of each breed that lie within certain intervals of the ordering.
INPUT FORMAT (file bcount.in):
The first line of input contains N and Q (1≤N≤100,000, 1≤Q≤100,000).
The next N lines contain an integer that is either 1, 2, or 3, giving the breed ID of a single cow in the ordering.

The next Q lines describe a query in the form of two integers a,b (a≤b).

OUTPUT FORMAT (file bcount.out):
For each of the Q queries (a,b), print a line containing three numbers: the number of cows numbered a…b that are Holsteins (breed 1), Guernseys (breed 2), and Jerseys (breed 3).
SAMPLE INPUT:
6 3
2
1
1
3
2
1
1 6
3 3
2 4
SAMPLE OUTPUT:
3 2 1
1 0 0
2 0 1
Problem credits: Nick Wu
'''

class BreedCounting:
	def __init__( self, breedIdList, queryList ):
		self.breedIdList = breedIdList
		self.queryList = queryList
		self.idHolstein, self.idGuernsey, self.idJersey = 1, 2, 3

	def process( self ):
		cumulativeSumList = [ [ 0 ], [ 0 ], [ 0 ] ]

		for breedId in self.breedIdList:
			for index in range( len( cumulativeSumList ) ):
				# index 0..2 is mapped to the breedId from 1..3
				count = 1 if index + 1 == breedId else 0
				cumulativeSumList[ index ].append( count + cumulativeSumList[ index ][ -1 ] )

		resultList = list()
		for low, high in self.queryList:
			countList = list()
			for index in range( len( cumulativeSumList ) ):
				count = cumulativeSumList[ index ][ high ] - cumulativeSumList[ index ][ low - 1 ]
				countList.append( count )
			resultList.append( tuple( countList ) )
		return resultList

class BreedCountingTest( unittest.TestCase ):
	def test_BreedCounting( self ):
		for testfile in getTestFileList( tag='breedcounting' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/breedcounting/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/breedcounting/{}.out'.format( testfile ) ) as solutionFile:

			N, Q = readIntegers( inputFile )
			breedIdList = [ readInteger( inputFile ) for _ in range( N ) ]
			queryList = [ tuple( readIntegers( inputFile ) ) for _ in range( Q ) ]
			resultList = [ tuple( readIntegers( solutionFile ) ) for _ in range( Q ) ]

			print( 'Testcase {} N = {} Q = {}'.format( testfile, N, Q ) )
			self.assertEqual( BreedCounting( breedIdList, queryList ).process(), resultList )

	def test_BreedCounting_Sample( self ):
		breedIdList = [ 2, 1, 1, 3, 2, 1 ]
		queryList = [ (1, 6), (3, 3), (2, 4) ]
		self.assertEqual( BreedCounting( breedIdList, queryList ).process(), [ (3, 2, 1), (1, 0, 0), (2, 0, 1 ) ] )

'''
USACO 2015 December Contest, Silver

Problem 2. High Card Wins

Bessie the cow is a huge fan of card games, which is quite surprising, given her lack of opposable thumbs. Unfortunately, none of the other cows in the herd are good opponents. They are so bad, in fact, that they always play in a completely predictable fashion! Nonetheless, it can still be a challenge for Bessie to figure out how to win.
Bessie and her friend Elsie are currently playing a simple card game where they take a deck of 2N cards, conveniently numbered 1…2N, and divide them into N cards for Bessie and N cards for Elsie. The two then play N rounds, where in each round Bessie and Elsie both play a single card, and the player with the highest card earns a point.

Given that Bessie can predict the order in which Elsie will play her cards, please determine the maximum number of points Bessie can win.

INPUT FORMAT (file highcard.in):
The first line of input contains the value of N (1≤N≤50,000).
The next N lines contain the cards that Elsie will play in each of the successive rounds of the game. Note that it is easy to determine Bessie's cards from this information.

OUTPUT FORMAT (file highcard.out):
Output a single line giving the maximum number of points Bessie can score.
SAMPLE INPUT:
3
1
6
4
SAMPLE OUTPUT:
2
Here, Bessie must have cards 2, 3, and 5 in her hand, and she can use these to win at most 2 points by saving the 5 until the end to beat Elsie's 4.

Problem credits: Austin Bannister and Brian Dean
'''

class HighCardWins:
	def __init__( self, elsieCards ):
		self.elsieCards = elsieCards

	def maximumPoints( self ):
		N = len( self.elsieCards )
		cardsAvailable = [ True for _ in range( 2 * N + 1 ) ]
		
		for card in self.elsieCards:
			cardsAvailable[ card ] = False
		
		elsieCardsSorted = list()
		bessieCardsSorted = list()
		for cardNumber in range( 1, len( cardsAvailable ) ):
			if cardsAvailable[ cardNumber ]:
				bessieCardsSorted.append( cardNumber )
			else:
				elsieCardsSorted.append( cardNumber )

		points = 0
		i = j = 0
		while j < len( bessieCardsSorted ):
			if bessieCardsSorted[ j ] > elsieCardsSorted[ i ]:
				points += 1
				i += 1
			j += 1
		return points

class HighCardWinsTest( unittest.TestCase ):
	def test_HighCardWins( self ):
		for testfile in getTestFileList( tag='highcardwins' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/highcardwins/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/highcardwins/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			elsieCards = [ readInteger( inputFile ) for _ in range( N ) ]
			maximumPoints = readInteger( solutionFile )

			print( 'Testcase {} N = {} maximumPoints = {}'.format( testfile, N, maximumPoints ) )
			self.assertEqual( HighCardWins( elsieCards ).maximumPoints(), maximumPoints )

	def test_HighCardWins_Sample( self ):
		self.assertEqual( HighCardWins( [ 1, 6, 4 ] ).maximumPoints(), 2 )

'''
USACO 2015 December Contest, Gold

Problem 2. Fruit Feast

Bessie has broken into Farmer John's house again! She has discovered a pile of lemons and a pile of oranges in the kitchen (effectively an unlimited number of each), and she is determined to eat as much as possible.
Bessie has a maximum fullness of T (1≤T≤5,000,000). Eating an orange increases her fullness by A, and eating a lemon increases her fullness by B (1≤A,B≤T). Additionally, if she wants, Bessie can drink water at most one time, which will instantly decrease her fullness by half (and will round down).

Help Bessie determine the maximum fullness she can achieve!

INPUT FORMAT (file feast.in):
The first (and only) line has three integers T, A, and B.
OUTPUT FORMAT (file feast.out):
A single integer, representing the maximum fullness Bessie can achieve.
SAMPLE INPUT:
8 5 6
SAMPLE OUTPUT:
8
Problem credits: Nathan Pinsker
'''

class FruitFeast:
	def __init__( self, T, A, B ):
		self.T, self.A, self.B = T, A, B

	def full( self ):
		waterUsageIndexDict = {
		True : 0, False : 1
		}
		visited = [ [ False for _ in range( self.T + 1 ) ] for _ in range( 2 ) ]

		stack = list()
		stack.append( (0, True) )

		bestFullness = 0

		while len( stack ) > 0:
			N, waterUsageRemaining = stack.pop()
			bestFullness = max( bestFullness, N )

			visited[ waterUsageIndexDict[ waterUsageRemaining ] ][ N ] = True

			possibleFullness = [ (N + self.A, waterUsageRemaining), (N + self.B, waterUsageRemaining) ]
			if waterUsageRemaining:
				possibleFullness.append( (N // 2, False) )
			for fullness, waterUsageRemaining in possibleFullness:
				if fullness > self.T:
					continue
				if not visited[ waterUsageIndexDict[ waterUsageRemaining ] ][ fullness ]:
					stack.append( (fullness, waterUsageRemaining) )

		return bestFullness

class FruitFeastTest( unittest.TestCase ):
	def test_FruitFeast( self ):
		for testfile in getTestFileList( tag='fruitfeast' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/fruitfeast/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/fruitfeast/{}.out'.format( testfile ) ) as solutionFile:

			T, A, B = readIntegers( inputFile )
			bestFullness = readInteger( solutionFile )

			print( 'Testcase {} T = {} A = {} B = {} bestFullness = {}'.format( testfile, T, A, B, bestFullness ) )
			self.assertEqual( FruitFeast( T, A, B ).full(), bestFullness )

	def test_FruitFeast_Sample( self ):
		self.assertEqual( FruitFeast( 8, 5, 6 ).full(), 8 )

'''
USACO 2021 January Contest, Bronze

Problem 1. Uddered but not Herd

A little known fact about cows is that they have their own version of the alphabet, the "cowphabet". It consists of the 26 letters 'a' through 'z', but when a cow speaks the cowphabet, she lists these letters in a specific ordering that might be different from the order 'abcdefghijklmnopqrstuvwxyz' we are used to hearing.
To pass the time, Bessie the cow has been humming the cowphabet over and over again, and Farmer John is curious how many times she's hummed it.

Given a lowercase string of letters that Farmer John has heard Bessie say, compute the minimum number of times Bessie must have hummed the entire cowphabet in order for Farmer John to have heard the given string. Farmer John isn't always paying attention to what Bessie hums, and so he might have missed some of the letters that Bessie has hummed. The string you are told consists of just the letters that he remembers hearing.

INPUT FORMAT (input arrives from the terminal / stdin):
The first line of input contains the 26 lowercase letters 'a' through 'z' in the order they appear in the cowphabet. The next line contains the string of lowercase letters that Farmer John heard Bessie say. This string has length at least 1 and at most 1000.
OUTPUT FORMAT (print output to the terminal / stdout):
Print the minimum number of times Bessie must have hummed the entire cowphabet.
SAMPLE INPUT:
abcdefghijklmnopqrstuvwxyz
mood
SAMPLE OUTPUT:
3
In this example, the cowphabet is ordered the same as the normal alphabet.

Bessie must have hummed the cowphabet at least three times. It is possible for Bessie to have only hummed the cowphabet three times, and for Farmer John to have heard the letters in uppercase as denoted below.

abcdefghijklMnOpqrstuvwxyz
abcdefghijklmnOpqrstuvwxyz
abcDefghijklmnopqrstuvwxyz
SCORING:
In test cases 2-5, the cowphabet is the same as the normal alphabet.
Test cases 6-10 satisfy no additional constraints.
Problem credits: Nick Wu
'''

class Uddered:
	def __init__( self, alphabet, inputString ):
		self.alphabet = alphabet
		self.inputString = inputString

	def analyze( self ):
		positionDict = dict()
		for i, letter in enumerate( self.alphabet ):
			positionDict[ letter ] = i

		count = 0
		previousPosition = len( self.alphabet )
		for letter in self.inputString:
			currentPosition = positionDict[ letter ]
			if currentPosition <= previousPosition:
				count += 1
			previousPosition = currentPosition
		return count

class UdderedTest( unittest.TestCase ):
	def test_Uddered( self ):
		for testfile in getTestFileList( tag='uddered' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/uddered/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/uddered/{}.out'.format( testfile ) ) as solutionFile:

			alphabet = readString( inputFile )
			inputString = readString( inputFile )
			count = readInteger( solutionFile )

			formatString = 'Testcase {} alphabet = {} inputString length = {} count = {}'
			print( formatString.format( testfile, alphabet, len( inputString ), count ) )
			self.assertEqual( Uddered( alphabet, inputString ).analyze(), count )

	def test_Uddered_Sample( self ):
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		inputString = 'mood'
		self.assertEqual( Uddered( alphabet, inputString ).analyze(), 3 )

'''
USACO 2013 November Contest, Bronze

Problem 1. Combination Lock

Problem 1: Combination Lock [Brian Dean, 2013]

Farmer John's cows keep escaping from his farm and causing mischief. To try
and prevent them from leaving, he purchases a fancy combination lock to
keep his cows from opening the pasture gate. 

Knowing that his cows are quite clever, Farmer John wants to make sure they
cannot easily open the lock by simply trying many different combinations. 
The lock has three dials, each numbered 1..N (1 <= N <= 100), where 1 and N
are adjacent since the dials are circular.  There are two combinations that
open the lock, one set by Farmer John, and also a "master" combination set
by the lock maker.  The lock has a small tolerance for error, however, so
it will open even if the numbers on the dials are each within at most 2
positions of a valid combination.  For example, if Farmer John's
combination is (1,2,3) and the master combination is (4,5,6), the lock will
open if its dials are set to (1,N,5) (since this is close enough to Farmer
John's combination) or to (2,4,8) (since this is close enough to the master
combination).  Note that (1,5,6) would not open the lock, since it is not
close enough to any one single combination.

Given Farmer John's combination and the master combination, please
determine the number of distinct settings for the dials that will open the
lock.  Order matters, so the setting (1,2,3) is distinct from (3,2,1).

PROBLEM NAME: combo

INPUT FORMAT:

* Line 1: The integer N.

* Line 2: Three space-separated integers, specifying Farmer John's
        combination.

* Line 3: Three space-separated integers, specifying the master
        combination (possibly the same as Farmer John's combination).

SAMPLE INPUT (file combo.in):

50
1 2 3
5 6 7

INPUT DETAILS:

Each dial is numbered 1..50.  Farmer John's combination is (1,2,3), and the
master combination is (5,6,7).

OUTPUT FORMAT:

* Line 1: The number of distinct dial settings that will open the
        lock.

SAMPLE OUTPUT (file combo.out):

249
'''

class CombinationLock:
	def __init__( self, N, combination, masterCombination ):
		self.N = N
		self.combination = combination
		self.masterCombination = masterCombination
		self.tolerance = 2

	def _possibilitySet( self, digit ):
		possibilitySet = set()
		for tolerance in range( - self.tolerance, self.tolerance + 1 ):
			possibleDigit = ( ( digit + tolerance ) % self.N ) + 1
			possibilitySet.add( possibleDigit )
		return possibilitySet

	def dial( self ):
		A = B = AB = 1
		for i in range( len( self.combination ) ):
			S1 = self._possibilitySet( self.combination[ i ] )
			S2 = self._possibilitySet( self.masterCombination[ i ] )
			A = A * len( S1 )
			B = B * len( S2 )
			AB = AB * len( set.intersection( S1, S2 ) )
		return A + B - AB

class CombinationLockTest( unittest.TestCase ):
	def test_CombinationLock( self ):
		for testfile in getTestFileList( tag='combinationlock' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/combinationlock/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/combinationlock/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			combination = list( readIntegers( inputFile ) )
			masterCombination = list( readIntegers( inputFile ) )
			possibleDials = readInteger( solutionFile )

			print( 'Testcase {} N = {} possibleDials = {}'.format( testfile, N, possibleDials ) )
			self.assertEqual( CombinationLock( N, combination, masterCombination ).dial(), possibleDials )

	def test_CombinationLock_Sample( self ):
		self.assertEqual( CombinationLock( 50, [ 1, 2, 3 ], [ 5, 6, 7 ] ).dial(), 249 )

'''
USACO 2016 December Contest, Gold

Problem 2. Cow Checklist

Every day, Farmer John walks through his pasture to check on the well-being of each of his cows. On his farm he has two breeds of cows, Holsteins and Guernseys. His H Holsteins are conveniently numbered 1…H, and his G Guernseys are conveniently numbered 1…G (1≤H≤1000,1≤G≤1000). Each cow is located at a point in the 2D plane (not necessarily distinct).
Farmer John starts his tour at Holstein 1, and ends at Holstein H. He wants to visit each cow along the way, and for convenience in maintaining his checklist of cows visited so far, he wants to visit the Holsteins and Guernseys in the order in which they are numbered. In the sequence of all H+G cows he visits, the Holsteins numbered 1…H should appear as a (not necessarily contiguous) subsequence, and likewise for the Guernseys. Otherwise stated, the sequence of all H+G cows should be formed by interleaving the list of Holsteins numbered 1…H with the list of Guernseys numbered 1…G.

When FJ moves from one cow to another cow traveling a distance of D, he expends D2 energy. Please help him determine the minimum amount of energy required to visit all his cows according to a tour as described above.

INPUT FORMAT (file checklist.in):
The first line of input contains H and G, separated by a space.
The next H lines contain the x and y coordinates of the H Holsteins, and the next G lines after that contain coordinates of the Guernseys. Each coordinate is an integer in the range 0…1000.

OUTPUT FORMAT (file checklist.out):
Write a single line of output, giving the minimum energy required for FJ's tour of all the cows.
SAMPLE INPUT:
3 2
0 0
1 0
2 0
0 3
1 3
SAMPLE OUTPUT:
20
Problem credits: Brian Dean
'''

class CowChecklist:
	def __init__( self, positionList1, positionList2 ):
		self.positionList1 = positionList1
		self.positionList2 = positionList2

	def _energy( self, position1, position2 ):
		x1, y1 = position1
		x2, y2 = position2
		return (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)

	def minimumEnergy( self ):
		M, N = len( self.positionList1 ), len( self.positionList2 )
		endsAtIndex_i, endsAtIndex_j = 0, 1
		energyMatrix = [ [ [ 0 for _ in range( 2 ) ] for _ in range( N + 1 ) ] for _ in range( M + 1 ) ]

		positionList1 = [ self.positionList1[ 0 ] ] + self.positionList1
		positionList2 = [ self.positionList2[ 0 ] ] + self.positionList2

		for i in range( M + 1 ):
			for j in range( N + 1 ):
				if i == j == 0:
					continue
				elif i == 0:
					energyMatrix[ i ][ j ][ endsAtIndex_i ] = energyMatrix[ i ][ j ][ endsAtIndex_j ] = float( 'inf' )
					continue
				elif j == 0:
					energyMatrix[ i ][ j ][ endsAtIndex_i ] = energyMatrix[ i - 1 ][ j ][ endsAtIndex_i ] + \
					self._energy( positionList1[ i ], positionList1[ i - 1 ] )
					energyMatrix[ i ][ j ][ endsAtIndex_j ] = float( 'inf' )
					continue

				energy_i_j = self._energy( positionList1[ i ], positionList2[ j ] )
				energy_i_i = self._energy( positionList1[ i ], positionList1[ i - 1 ] )
				energy_j_j = self._energy( positionList2[ j ], positionList2[ j - 1 ] )

				# Sequence of moves ending at index i.
				A = energyMatrix[ i - 1 ][ j ][ endsAtIndex_i ] + energy_i_i
				B = energyMatrix[ i - 1 ][ j ][ endsAtIndex_j ] + energy_i_j
				energyMatrix[ i ][ j ][ endsAtIndex_i ] = min( A, B )

				# Sequence of moves ending at index j.
				A = energyMatrix[ i ][ j - 1 ][ endsAtIndex_i ] + energy_i_j
				B = energyMatrix[ i ][ j - 1 ][ endsAtIndex_j ] + energy_j_j
				energyMatrix[ i ][ j ][ endsAtIndex_j ] = min( A, B )

		return energyMatrix[ M ][ N ][ endsAtIndex_i ]

class CowChecklistTest( unittest.TestCase ):
	def test_CowChecklist( self ):
		for testfile in getTestFileList( tag='checklist' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/checklist/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/checklist/{}.out'.format( testfile ) ) as solutionFile:

			M, N = readIntegers( inputFile )
			positionList1 = [ tuple( readIntegers( inputFile ) ) for _ in range( M ) ]
			positionList2 = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			minimumEnergy = readInteger( solutionFile )

			print( 'Testcase {} M = {} N = {} minimumEnergy = {}'.format( testfile, M, N, minimumEnergy ) )
			self.assertEqual( CowChecklist( positionList1, positionList2 ).minimumEnergy(), minimumEnergy )

	def test_CowChecklist_Sample( self ):
		positionList1 = [ (0, 0), (1, 0), (2, 0) ]
		positionList2 = [ (0, 3), (1, 3) ]
		self.assertEqual( CowChecklist( positionList1, positionList2 ).minimumEnergy(), 20 )

'''
USACO 2017 January Contest, Bronze

Problem 1. Don't Be Last!

Farmer John owns 7 dairy cows: Bessie, Elsie, Daisy, Gertie, Annabelle, Maggie, and Henrietta. He milks them every day and keeps detailed records on the amount of milk provided by each cow during each milking session. Not surprisingly, Farmer John highly prizes cows that provide large amounts of milk.
Cows, being lazy creatures, don't necessarily want to be responsible for producing too much milk. If it were up to them, they would each be perfectly content to be the lowest-producing cow in the entire herd. However, they keep hearing Farmer John mentioning the phrase "farm to table" with his human friends, and while they don't quite understand what this means, they have a suspicion that it actually may not be the best idea to be the cow producing the least amount of milk. Instead, they figure it's safer to be in the position of producing the second-smallest amount of milk in the herd. Please help the cows figure out which of them currently occupies this desirable position.

INPUT FORMAT (file notlast.in):
The input file for this task starts with a line containing the integer N (1≤N≤100), giving the number of entries in Farmer John's milking log.
Each of the N following lines contains the name of a cow (one of the seven above) followed by a positive integer (at most 100), indicating the amount of milk produced by the cow during one of its milking sessions.

Any cow that does not appear in the log at all is assumed to have produced no milk.

OUTPUT FORMAT (file notlast.out):
On a single line of output, please print the name of the cow that produces the second-smallest amount of milk. More precisely, if M is the minimum total amount of milk produced by any cow, please output the name of the cow whose total production is minimal among all cows that produce more than M units of milk. If several cows tie for this designation, or if no cow has this designation (i.e., if all cows have production equal to M), please output the word "Tie". Don't forget to add a newline character at the end of your line of output. Note that M=0 if one of the seven cows is completely absent from the milking log, since this cow would have produced no milk.
SAMPLE INPUT:
10
Bessie 1
Maggie 13
Elsie 3
Elsie 4
Henrietta 4
Gertie 12
Daisy 7
Annabelle 10
Bessie 6
Henrietta 5
SAMPLE OUTPUT:
Henrietta
In this example, Bessie, Elsie, and Daisy all tie for the minimum by each producing 7 units of milk. The next-largest production, 9 units, is due to Henrietta.

Problem credits: Brian Dean
'''

class Last:
	def __init__( self, milkingLog ):
		self.milkingLog = milkingLog
		self.tie = 'Tie'
		self.totalCows = 7

	def analyze( self ):
		milkDict = dict()
		for cow, amountOfMilk in self.milkingLog:
			if cow not in milkDict:
				milkDict[ cow ] = 0
			milkDict[ cow ] += amountOfMilk

		milkList = [ (amountOfMilk, cow) for cow, amountOfMilk in milkDict.items() ]
		milkList.sort( reverse=True )

		if len( milkList ) < self.totalCows:
			milkList.append( (0, None) )

		minimumMilk, _ = milkList.pop()
		while len( milkList ) > 0:
			amountOfMilk, _ = milkList[ -1 ]
			if amountOfMilk == minimumMilk:
				milkList.pop()
			else:
				break

		if len( milkList ) == 0:
			return self.tie
		optimalMilk, cow = milkList.pop()
		if len( milkList ) == 0:
			return cow
		else:
			amountOfMilk, _ = milkList.pop()
			return cow if amountOfMilk != optimalMilk else self.tie

class LastTest( unittest.TestCase ):
	def test_Last( self ):
		for testfile in getTestFileList( tag='last' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/last/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/last/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			milkingLog = list()
			for _ in range( N ):
				cow, amountOfMilk = readString( inputFile ).split()
				milkingLog.append( (cow, int( amountOfMilk )) )
			bestCow = readString( solutionFile )

			print( 'Testcase {} N = {} bestCow = {}'.format( testfile, N, bestCow ) )
			self.assertEqual( Last( milkingLog ).analyze(), bestCow )

	def test_Last_Sample( self ):
		milkingLog = [
		('Bessie', 1), ('Maggie', 13), ('Elsie', 3), ('Elsie', 4), ('Henrietta', 4), ('Gertie', 12),
		('Daisy', 7), ('Annabelle', 10), ('Bessie', 6,), ('Henrietta', 5)
		]
		self.assertEqual( Last( milkingLog ).analyze(), 'Henrietta' )

'''
USACO 2017 January Contest, Bronze

Problem 2. Hoof, Paper, Scissors

You have probably heard of the game "Rock, Paper, Scissors". The cows like to play a similar game they call "Hoof, Paper, Scissors".
The rules of "Hoof, Paper, Scissors" are simple. Two cows play against each-other. They both count to three and then each simultaneously makes a gesture that represents either a hoof, a piece of paper, or a pair of scissors. Hoof beats scissors (since a hoof can smash a pair of scissors), scissors beats paper (since scissors can cut paper), and paper beats hoof (since the hoof can get a papercut). For example, if the first cow makes a "hoof" gesture and the second a "paper" gesture, then the second cow wins. Of course, it is also possible to tie, if both cows make the same gesture.

Farmer John watches in fascination as two of his cows play a series of N games of "Hoof, Paper, Scissors" (1≤N≤100). Unfortunately, while he can see that the cows are making three distinct types of gestures, he can't tell which one represents "hoof", which one represents "paper" and which one represents "scissors" (to Farmer John's untrained eye, they all seem to be variations on "hoof"...)

Not knowing the meaning of the three gestures, Farmer John assigns them numbers 1, 2, and 3. Perhaps gesture 1 stands for "hoof", or maybe it stands for "paper"; the meaning is not clear to him. Given the gestures made by both cows over all N games, please help Farmer John determine the maximum possible number of games the first cow could have possibly won, given an appropriate mapping between numbers and their respective gestures.

INPUT FORMAT (file hps.in):
The first line of the input file contains N.
Each of the remaining N lines contain two integers (each 1, 2, or 3), describing a game from Farmer John's perspective.

OUTPUT FORMAT (file hps.out):
Print the maximum number of games the first of the two cows could possibly have won.
SAMPLE INPUT:
5
1 2
2 2
1 3
1 1
3 2
SAMPLE OUTPUT:
2
One solution (of several) for this sample case is to have 1 represent "scissors", 2 represent "hoof", and 3 represent "paper". This assignment gives 2 victories to the first cow ("1 3" and "3 2"). No other assignment leads to more victories.

Problem credits: Brian Dean
'''

class HoofPaperScissors:
	def __init__( self, gameResultList ):
		self.gameResultList = gameResultList

	def maximumWins( self ):
		winningMoves = set( [ (1, 2), (2, 3), (3, 1) ] )
		wins = losses = 0
		for (x, y) in self.gameResultList:
			if x == y:
				continue
			if (x, y) in winningMoves:
				wins += 1
			else:
				losses += 1
		return max( wins, losses )

class HoofPaperScissorsTest( unittest.TestCase ):
	def test_HoofPaperScissors( self ):
		for testfile in getTestFileList( tag='hoof' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/hoof/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/hoof/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			gameResultList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			maximumWins = readInteger( solutionFile )

			print( 'Testcase {} N = {} maximumWins = {}'.format( testfile, N, maximumWins ) )
			self.assertEqual( HoofPaperScissors( gameResultList ).maximumWins(), maximumWins )

	def test_HoofPaperScissors_Sample( self ):
		gameResultList = [ (1, 2), (2, 2), (1, 3), (1, 1), (3, 2) ]
		self.assertEqual( HoofPaperScissors( gameResultList ).maximumWins(), 2 )

'''
USACO 2017 January Contest, Silver

Problem 1. Cow Dance Show

After several months of rehearsal, the cows are just about ready to put on their annual dance performance; this year they are performing the famous bovine ballet "Cowpelia".
The only aspect of the show that remains to be determined is the size of the stage. A stage of size K can support K cows dancing simultaneously. The N cows in the herd (1≤N≤10,000) are conveniently numbered 1…N in the order in which they must appear in the dance. Each cow i plans to dance for a specific duration of time d(i). Initially, cows 1…K appear on stage and start dancing. When the first of these cows completes her part, she leaves the stage and cow K+1 immediately starts dancing, and so on, so there are always K cows dancing (until the end of the show, when we start to run out of cows). The show ends when the last cow completes her dancing part, at time T.

Clearly, the larger the value of K, the smaller the value of T. Since the show cannot last too long, you are given as input an upper bound Tmax specifying the largest possible value of T. Subject to this constraint, please determine the smallest possible value of K.

INPUT FORMAT (file cowdance.in):
The first line of input contains N and Tmax, where Tmax is an integer of value at most 1 million.
The next N lines give the durations d(1)…d(N) of the dancing parts for cows 1…N. Each d(i) value is an integer in the range 1…100,000.

It is guaranteed that if K=N, the show will finish in time.

OUTPUT FORMAT (file cowdance.out):
Print out the smallest possible value of K such that the dance performance will take no more than Tmax units of time.
SAMPLE INPUT:
5 8
4
7
8
6
4
SAMPLE OUTPUT:
4
Problem credits: Delphine and Brian Dean
'''

class CowDanceShow:
	def __init__( self, N, Tmax, danceDurationList ):
		self.N, self.Tmax = N, Tmax
		self.danceDurationList = danceDurationList

	def _totalTimeDurationForStageSize( self, stageSize ):
		q = list()
		time = 0
		for i, duration in enumerate( self.danceDurationList ):
			if len( q ) == stageSize:
				time = heapq.heappop( q )
			heapq.heappush( q, time + duration )
		return max( q ) <= self.Tmax

	def optimalStageSize( self ):
		rangeLow, rangeHigh = 1, self.N
		while rangeLow < rangeHigh:
			stageSize = ( rangeLow + rangeHigh ) // 2
			isStageSizeValid = self._totalTimeDurationForStageSize( stageSize )
			if not isStageSizeValid:
				rangeLow = stageSize + 1
			else:
				rangeHigh = stageSize
		return rangeHigh

class CowDanceShowTest( unittest.TestCase ):
	def test_CowDanceShow( self ):
		for testfile in getTestFileList( tag='cowdance' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowdance/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowdance/{}.out'.format( testfile ) ) as solutionFile:

			N, Tmax = readIntegers( inputFile )
			danceDurationList = [ readInteger( inputFile ) for _ in range( N ) ]
			optimalStageSize = readInteger( solutionFile )

			print( 'Testcase {} N = {} Tmax = {} optimalStageSize = {}'.format( testfile, N, Tmax, optimalStageSize ) )
			self.assertEqual( CowDanceShow( N, Tmax, danceDurationList ).optimalStageSize(), optimalStageSize )

	def test_CowDanceShow_Sample( self ):
		N, Tmax = 5, 8
		danceDurationList = [ 4, 7, 8, 6, 4 ]
		self.assertEqual( CowDanceShow( N, Tmax, danceDurationList ).optimalStageSize(), 4 )

'''
USACO 2017 January Contest, Silver

Problem 2. Hoof, Paper, Scissors

You have probably heard of the game "Rock, Paper, Scissors". The cows like to play a similar game they call "Hoof, Paper, Scissors".
The rules of "Hoof, Paper, Scissors" are simple. Two cows play against each-other. They both count to three and then each simultaneously makes a gesture that represents either a hoof, a piece of paper, or a pair of scissors. Hoof beats scissors (since a hoof can smash a pair of scissors), scissors beats paper (since scissors can cut paper), and paper beats hoof (since the hoof can get a papercut). For example, if the first cow makes a "hoof" gesture and the second a "paper" gesture, then the second cow wins. Of course, it is also possible to tie, if both cows make the same gesture.

Farmer John wants to play against his prize cow, Bessie, at N games of "Hoof, Paper, Scissors" (1≤N≤100,000). Bessie, being an expert at the game, can predict each of FJ's gestures before he makes it. Unfortunately, Bessie, being a cow, is also very lazy. As a result, she tends to play the same gesture multiple times in a row. In fact, she is only willing to switch gestures at most once over the entire set of games. For example, she might play "hoof" for the first x games, then switch to "paper" for the remaining N−x games.

Given the sequence of gestures FJ will be playing, please determine the maximum number of games that Bessie can win.

INPUT FORMAT (file hps.in):
The first line of the input file contains N.
The remaining N lines contains FJ's gestures, each either H, P, or S.

OUTPUT FORMAT (file hps.out):
Print the maximum number of games Bessie can win, given that she can only change gestures at most once.
SAMPLE INPUT:
5
P
P
H
P
S
SAMPLE OUTPUT:
4
Problem credits: Mark Chen and Brian Dean
'''

class HoofPaperScissorsSilver:
	def __init__( self, moveInfoList ):
		self.moveInfoList = moveInfoList
		self.winningMoves = set( [ ('H', 'S'), ('S', 'P'), ('P', 'H') ] )
		self.validMoves = 'HSP'

	def maximumWins( self ):
		cumulativeSumList = [ [ 0 ], [ 0 ], [ 0 ] ]
		for farmerMove in self.moveInfoList:
			for index, bessieMove in enumerate( self.validMoves ):
				count = 1 if (bessieMove, farmerMove) in self.winningMoves else 0
				cumulativeSumList[ index ].append( cumulativeSumList[ index ][ -1 ] + count )
		
		N = len( self.moveInfoList )
		bestWinCount = 0
		for K in range( 1, N + 1 ):
			# Make K moves corresponding to self.validMoves[ i ] and N - K moves corresponding to
			# self.validMoves[ j ].
			for i in range( len( self.validMoves ) ):
				for j in range( len( self.validMoves ) ):
					if i == j:
						continue
					winCount = cumulativeSumList[ i ][ K ] + ( cumulativeSumList[ j ][ -1 ] - cumulativeSumList[ j ][ K ] )
					bestWinCount = max( winCount, bestWinCount )
		return bestWinCount

class HoofPaperScissorsSilverTest( unittest.TestCase ):
	def test_HoofPaperScissorsSilver( self ):
		for testfile in getTestFileList( tag='hoof_silver' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/hoof_silver/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/hoof_silver/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			moveInfoList = [ readString( inputFile ) for _ in range( N ) ]
			bestWinCount = readInteger( solutionFile )

			print( 'Testcase {} N = {} bestWinCount = {}'.format( testfile, N, bestWinCount ) )
			self.assertEqual( HoofPaperScissorsSilver( moveInfoList ).maximumWins(), bestWinCount )

	def test_HoofPaperScissorsSilver_Sample( self ):
		moveInfoList = [ 'P', 'P', 'H', 'P', 'S' ]
		self.assertEqual( HoofPaperScissorsSilver( moveInfoList ).maximumWins(), 4 )

'''
USACO 2017 February Contest, Bronze

Problem 1. Why Did the Cow Cross the Road

While the age-old question of why chickens cross roads has been addressed in great depth by the scientific community, surprisingly little has been published in the research literature on the related subject of cow crossings. Farmer John, well-aware of the importance of this issue, is thrilled when he is contacted by a local university asking for his assistance in conducting a scientific study of why cows cross roads. He eagerly volunteers to help.
As part of the study, Farmer John has been asked to document the number of times each of his cows crosses the road. He carefully logs data about his cows' locations, making a series of N observations over the course of a single day. Each observation records the ID number of a cow (an integer in the range 1…10, since Farmer John has 10 cows), as well as which side of the road the cow is on.

Based on the data recorded by Farmer John, please help him count the total number of confirmed crossings. A confirmed crossing occurs when a consecutive sightings of a cow place it on different sides of the road.

INPUT FORMAT (file crossroad.in):
The first line of input contains the number of observations, N, a positive integer at most 100. Each of the next N lines contains one observation, and consists of a cow ID number followed by its position indicated by either zero or one (zero for one side of the road, one for the other side).
OUTPUT FORMAT (file crossroad.out):
Please compute the total number of confirmed crossings.
SAMPLE INPUT:
8
3 1
3 0
6 0
2 1
4 1
3 0
4 0
3 1
SAMPLE OUTPUT:
3
In this example, cow 3 crosses twice -- she first appears on side 1, then later appears on side 0, and then later still appears back on side 1. Cow 4 definitely crosses once. Cows 2 and 6 do not appear to cross.

Problem credits: Brian Dean
'''

class CrossTheRoad:
	@staticmethod
	def countCrossings( infoList ):
		count = 0
		locationDict = dict()
		for cowId, sideOfRoad in infoList:
			currentLocation = locationDict.get( cowId )
			if currentLocation is not None and currentLocation != sideOfRoad:
				count += 1
			locationDict[ cowId ] = sideOfRoad
		return count

class CrossTheRoadTest( unittest.TestCase ):
	def test_CrossTheRoad( self ):
		for testfile in getTestFileList( tag='crosstheroad' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/crosstheroad/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/crosstheroad/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			infoList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			crossings = readInteger( solutionFile )

			print( 'Testcase {} N = {} crossings = {}'.format( testfile, N, crossings ) )
			self.assertEqual( CrossTheRoad.countCrossings( infoList ), crossings )

	def test_CrossTheRoad_Sample( self ):
		infoList = [ (3, 1), (3, 0), (6, 0), (2, 1), (4, 1), (3, 0), (4, 0), (3, 1) ]
		self.assertEqual( CrossTheRoad.countCrossings( infoList ), 3 )

'''
USACO 2017 February Contest, Bronze

Problem 2. Why Did the Cow Cross the Road II

The layout of Farmer John's farm is quite peculiar, with a large circular road running around the perimeter of the main field on which his cows graze during the day. Every morning, the cows cross this road on their way towards the field, and every evening they all cross again as they leave the field and return to the barn.
As we know, cows are creatures of habit, and they each cross the road the same way every day. Each cow crosses into the field at a different point from where she crosses out of the field, and all of these crossing points are distinct from each-other. Farmer John owns exactly 26 cows, which he has lazily named A through Z (he is not sure what he will do if he ever acquires a 27th cow...), so there are precisely 52 crossing points around the road. Farmer John records these crossing points concisely by scanning around the circle clockwise, writing down the name of the cow for each crossing point, ultimately forming a string with 52 characters in which each letter of the alphabet appears exactly twice. He does not record which crossing points are entry points and which are exit points.

Looking at his map of crossing points, Farmer John is curious how many times various pairs of cows might cross paths during the day. He calls a pair of cows (a,b) a "crossing" pair if cow a's path from entry to exit must cross cow b's path from entry to exit. Please help Farmer John count the total number of crossing pairs.

INPUT FORMAT (file circlecross.in):
The input consists of a single line containing a string of 52 upper-case characters. Each letter of the alphabet appears exactly twice.
OUTPUT FORMAT (file circlecross.out):
Please print the total number of crossing pairs.
SAMPLE INPUT:
ABCCABDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ
SAMPLE OUTPUT:
1
In this example, only cows A and B are a crossing pair.

Problem credits: Brian Dean
'''

class CrossTheCircularRoad:
	@staticmethod
	def countCrossingPairs( infoString ):
		crossingPairsCount = 0

		stack = list()
		inStack = set()
		for letter in infoString:
			if letter in inStack:
				removalList = list()
				while True:
					topElement = stack.pop()
					if topElement == letter:
						break
					crossingPairsCount += 1
					removalList.append( topElement )
				for element in reversed( removalList ):
					stack.append( element )
				inStack.remove( letter )
			else:
				inStack.add( letter )
				stack.append( letter )

		return crossingPairsCount

class CrossTheCircularRoadTest( unittest.TestCase ):
	def test_CrossTheCircularRoad( self ):
		for testfile in getTestFileList( tag='crossthecircularroad' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/crossthecircularroad/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/crossthecircularroad/{}.out'.format( testfile ) ) as solutionFile:

			infoString = readString( inputFile )
			crossingPairsCount = readInteger( solutionFile )

			print( 'Testcase {} infoString = {} count = {}'.format( testfile, infoString, crossingPairsCount ) )
			self.assertEqual( CrossTheCircularRoad.countCrossingPairs( infoString ), crossingPairsCount )

	def test_CrossTheCircularRoad_Sample( self ):
		infoString = 'ABCCABDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ'
		self.assertEqual( CrossTheCircularRoad.countCrossingPairs( infoString ), 1 )

'''
USACO 2017 February Contest, Bronze

Problem 3. Why Did the Cow Cross the Road III

Farmer John, in his old age, has unfortunately become increasingly grumpy and paranoid. Forgetting the extent to which bovine diversity helped his farm truly flourish over the years, he has recently decided to build a huge fence around the farm, discouraging cows from neighboring farms from visiting, and completely prohibiting entry from a handful of neighboring farms. The cows are quite upset by this state of affairs, not only since they can no longer visit with their friends, but since it has caused them to cancel participation in the International Milking Olympiad, an event to which they look forward all year.
Neighboring cows that still have the ability to enter Farmer John's property find the process has become more arduous, as they can enter only through a single gate where each cow is subject to intense questioning, often causing the cows to queue up in a long line.

For each of the N cows visiting the farm, you are told the time she arrives at the gate and the duration of time required for her to answer her entry questions. Only one cow can be undergoing questioning at any given time, so if many cows arrive near the same time, they will likely need to wait in line to be processed one by one. For example, if a cow arrives at time 5 and answers questions for 7 units of time, another cow arriving at time 8 would need to wait until time 12 to start answering questions herself.

Please determine the earliest possible time by which all cows are able to enter the farm.

INPUT FORMAT (file cowqueue.in):
The first line of input contains N, a positive integer at most 100. Each of the next N lines describes one cow, giving the time it arrives and the time it requires for questioning; each of these numbers are positive integers at most 1,000,000.
OUTPUT FORMAT (file cowqueue.out):
Please determine the minimum possible time at which all the cows could have completed processing.
SAMPLE INPUT:
3
2 1
8 3
5 7
SAMPLE OUTPUT:
15
Here, first cow arrives at time 2 and is quickly processed. The gate remains briefly idle until the third cow arrives at time 5, and begins processing. The second cow then arrives at time 8 and waits until time 5+7=12 to start answering questions, finishing at time 12+3 = 15.

Problem credits: Brian Dean
'''

class CowWait:
	def __init__( self, waitListInfo ):
		self.waitListInfo = waitListInfo

	def process( self ):
		timeStamp = 0
		for arrivalTime, timeTaken in sorted( self.waitListInfo ):
			startTime = max( timeStamp, arrivalTime )
			timeStamp = startTime + timeTaken
		return timeStamp

class CowWaitTest( unittest.TestCase ):
	def test_CowWait( self ):
		for testfile in getTestFileList( tag='cowwait' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowwait/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowwait/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			waitListInfo = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			timeTaken = readInteger( solutionFile )

			print( 'Testcase {} N = {} timeTaken = {}'.format( testfile, N, timeTaken ) )
			self.assertEqual( CowWait( waitListInfo ).process(), timeTaken )

	def test_CowWait_Sample( self ):
		waitListInfo = [ (2, 1), (8, 3), (5, 7) ]
		self.assertEqual( CowWait( waitListInfo ).process(), 15 )

'''
USACO 2017 February Contest, Silver

Problem 2. Why Did the Cow Cross the Road II

The long road through Farmer John's farm has N crosswalks across it, conveniently numbered 1…N (1≤N≤100,000). To allow cows to cross at these crosswalks, FJ installs electric crossing signals, which light up with a green cow icon when it is ok for the cow to cross, and red otherwise. Unfortunately, a large electrical storm has damaged some of his signals. Given a list of the damaged signals, please compute the minimum number of signals that FJ needs to repair in order for there to exist some contiguous block of at least K working signals.
INPUT FORMAT (file maxcross.in):
The first line of input contains N, K, and B (1≤B,K≤N). The next B lines each describe the ID number of a broken signal.
OUTPUT FORMAT (file maxcross.out):
Please compute the minimum number of signals that need to be repaired in order for there to be a contiguous block of K working signals somewhere along the road.
SAMPLE INPUT:
10 6 5
2
10
1
5
9
SAMPLE OUTPUT:
1
Problem credits: Brian Dean
'''

class BrokenSignal:
	def __init__( self, N, K, brokenSignalList ):
		self.N, self.K = N, K
		self.brokenSignalList = brokenSignalList

	def process( self ):
		brokenSignals = set( self.brokenSignalList )
		i, j = 0, 1

		brokenSignalCount = 0
		minimumSignalsRepaired = float( 'inf' )

		while j <= self.N:
			windowLength = j - i
			if j in brokenSignals:
				brokenSignalCount += 1
			if windowLength == self.K:
				minimumSignalsRepaired = min( minimumSignalsRepaired, brokenSignalCount )
				i = i + 1
				if i in brokenSignals:
					brokenSignalCount -= 1
			j += 1
		return minimumSignalsRepaired

class BrokenSignalTest( unittest.TestCase ):
	def test_BrokenSignal( self ):
		for testfile in getTestFileList( tag='brokensignal' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/brokensignal/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/brokensignal/{}.out'.format( testfile ) ) as solutionFile:

			N, K, B = readIntegers( inputFile )
			brokenSignalList = [ readInteger( inputFile ) for _ in range( B ) ]
			minimumSignalsRepaired = readInteger( solutionFile )

			print( 'Testcase N = {} K = {} minimumSignalsRepaired = {}'.format( N, K, minimumSignalsRepaired ) )
			self.assertEqual( BrokenSignal( N, K, brokenSignalList ).process(), minimumSignalsRepaired )

	def test_BrokenSignal_Sample( self ):
		N, K = 10, 6
		brokenSignalList = [ 2, 10, 1, 5, 9 ]
		self.assertEqual( BrokenSignal( N, K, brokenSignalList ).process(), 1 )

'''
USACO 2017 February Contest, Gold

Problem 1. Why Did the Cow Cross the Road

Why did the cow cross the road? Well, one reason is that Farmer John's farm simply has a lot of roads, making it impossible for his cows to travel around without crossing many of them.
FJ's farm is arranged as an N×N square grid of fields (3≤N≤100), with a set of N−1 north-south roads and N−1 east-west roads running through the interior of the farm serving as dividers between the fields. A tall fence runs around the external perimeter, preventing cows from leaving the farm. Bessie the cow can move freely from any field to any other adjacent field (north, east, south, or west), as long as she carefully looks both ways before crossing the road separating the two fields. It takes her T units of time to cross a road (0≤T≤1,000,000).

One day, FJ invites Bessie to visit his house for a friendly game of chess. Bessie starts out in the north-west corner field and FJ's house is in the south-east corner field, so Bessie has quite a walk ahead of her. Since she gets hungry along the way, she stops at every third field she visits to eat grass (not including her starting field, but including possibly the final field in which FJ's house resides). Some fields are grassier than others, so the amount of time required for stopping to eat depends on the field in which she stops.

Please help Bessie determine the minimum amount of time it will take to reach FJ's house.

INPUT FORMAT (file visitfj.in):
The first line of input contains N and T. The next N lines each contain N positive integers (each at most 100,000) describing the amount of time required to eat grass in each field. The first number of the first line is the north-west corner.
OUTPUT FORMAT (file visitfj.out):
Print the minimum amount of time required for Bessie to travel to FJ's house.
SAMPLE INPUT:
4 2
30 92 36 10
38 85 60 16
41 13 5 68
20 97 13 80
SAMPLE OUTPUT:
31
The optimal solution for this example involves moving east 3 squares (eating the "10"), then moving south twice and west once (eating the "5"), and finally moving south and east to the goal.

Problem credits: Brian Dean
'''

class TimeToCross:
	def __init__( self, T, fieldSize, fieldInfo ):
		self.T, self.fieldSize = T, fieldSize
		self.fieldInfo = fieldInfo
		self.grassEatingInterval = 3

		self.adjacentLocationDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def timeTaken( self ):
		startLocation = 0, 0
		targetLocation = self.fieldSize - 1, self.fieldSize - 1

		q = list()
		q.append( (0, startLocation, 0) )

		timeTakenDict = dict()
		timeTakenDict[ (startLocation, 0) ] = 0

		while len( q ) > 0:
			timeTaken, currentLocation, stepCount = heapq.heappop( q )
			if currentLocation == targetLocation:
				return timeTaken

			if timeTakenDict[ (currentLocation, stepCount) ] < timeTaken:
				continue

			u, v = currentLocation
			stepCount = ( stepCount + 1 ) % self.grassEatingInterval
			for du, dv in self.adjacentLocationDelta:
				x, y = adjacentLocation = u + du, v + dv
				if not 0 <= x < self.fieldSize or not 0 <= y < self.fieldSize:
					continue
				
				newTimeTaken = timeTaken + self.T
				if stepCount == 0:
					newTimeTaken += self.fieldInfo[ x ][ y ]

				if (adjacentLocation, stepCount) not in timeTakenDict or newTimeTaken < timeTakenDict[ (adjacentLocation, stepCount) ]:
					timeTakenDict[ (adjacentLocation, stepCount) ] = newTimeTaken
					heapq.heappush( q, (newTimeTaken, adjacentLocation, stepCount) )

class TimeToCrossTest( unittest.TestCase ):
	def test_TimeToCross( self ):
		for testfile in getTestFileList( tag='timetocross' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/timetocross/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/timetocross/{}.out'.format( testfile ) ) as solutionFile:

			fieldSize, T = readIntegers( inputFile )
			fieldInfo = [ list( readIntegers( inputFile ) ) for _ in range( fieldSize ) ]
			timeTaken = readInteger( solutionFile )

			print( 'Testcase {} fieldSize = {} timeTaken = {}'.format( testfile, fieldSize, timeTaken ) )
			self.assertEqual( TimeToCross( T, fieldSize, fieldInfo ).timeTaken(), timeTaken )

	def test_TimeToCross_Sample( self ):
		T, fieldSize = 2, 4
		fieldInfo = [
		[ 30, 92, 36, 10 ],
		[ 38, 85, 60, 16 ],
		[ 41, 13,  5, 68 ],
		[ 20, 97, 13, 80 ]
		]
		self.assertEqual( TimeToCross( T, fieldSize, fieldInfo ).timeTaken(), 31 )

'''
USACO 2017 US Open Contest, Bronze

Problem 1. The Lost Cow

Farmer John has lost his prize cow Bessie, and he needs to find her!
Fortunately, there is only one long path running across the farm, and Farmer John knows that Bessie has to be at some location on this path. If we think of the path as a number line, then Farmer John is currently at position x and Bessie is currently at position y (unknown to Farmer John). If Farmer John only knew where Bessie was located, he could walk directly to her, traveling a distance of |x−y|. Unfortunately, it is dark outside and Farmer John can't see anything. The only way he can find Bessie is to walk back and forth until he eventually reaches her position.

Trying to figure out the best strategy for walking back and forth in his search, Farmer John consults the computer science research literature and is somewhat amused to find that this exact problem has not only been studied by computer scientists in the past, but that it is actually called the "Lost Cow Problem" (this is actually true!).

The recommended solution for Farmer John to find Bessie is to move to position x+1, then reverse direction and move to position x−2, then to position x+4, and so on, in a "zig zag" pattern, each step moving twice as far from his initial starting position as before. As he has read during his study of algorithms for solving the lost cow problem, this approach guarantees that he will at worst travel 9 times the direct distance |x−y| between himself and Bessie before he finds her (this is also true, and the factor of 9 is actually the smallest such worst case guarantee any strategy can achieve).

Farmer John is curious to verify this result. Given x and y, please compute the total distance he will travel according to the zig-zag search strategy above until he finds Bessie.

INPUT FORMAT (file lostcow.in):
The single line of input contains two distinct space-separated integers x and y. Both are in the range 0…1,000.
OUTPUT FORMAT (file lostcow.out):
Print one line of output, containing the distance Farmer John will travel to reach Bessie.
SAMPLE INPUT:
3 6
SAMPLE OUTPUT:
9
Problem credits: Brian Dean
'''

class LostCow:
	@staticmethod
	def distance( x, y ):
		totalDistance = 0
		delta = 1

		previous_x1 = x
		found = False
		while not found:
			x1 = x + delta
			if previous_x1 < y <= x1 or x1 <= y < previous_x1:
				found = True
				x1 = y
			totalDistance += abs( x1 - previous_x1 )
			previous_x1 = x1
			delta = delta * -2
		return totalDistance

class LostCowTest( unittest.TestCase ):
	def test_LostCow( self ):
		for testfile in getTestFileList( tag='lostcow' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/lostcow/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/lostcow/{}.out'.format( testfile ) ) as solutionFile:

			x, y = readIntegers( inputFile )
			totalDistance = readInteger( solutionFile )

			print( 'Testcase {} x = {} y = {} totalDistance = {}'.format( testfile, x, y, totalDistance ) )
			self.assertEqual( LostCow.distance( x, y ), totalDistance )

	def test_LostCow_Sample( self ):
		self.assertEqual( LostCow.distance( 3, 6 ), 9 )

'''
USACO 2017 US Open Contest, Bronze

Problem 2. Bovine Genomics

Farmer John owns N cows with spots and N cows without spots. Having just completed a course in bovine genetics, he is convinced that the spots on his cows are caused by mutations at a single location in the bovine genome.
At great expense, Farmer John sequences the genomes of his cows. Each genome is a string of length M built from the four characters A, C, G, and T. When he lines up the genomes of his cows, he gets a table like the following, shown here for N=3:

Positions:    1 2 3 4 5 6 7 ... M

Spotty Cow 1: A A T C C C A ... T
Spotty Cow 2: G A T T G C A ... A
Spotty Cow 3: G G T C G C A ... A

Plain Cow 1:  A C T C C C A ... G
Plain Cow 2:  A C T C G C A ... T
Plain Cow 3:  A C T T C C A ... T
Looking carefully at this table, he surmises that position 2 is a potential location in the genome that could explain spottiness. That is, by looking at the character in just this position, Farmer John can predict which of his cows are spotty and which are not (here, A or G means spotty and C means plain; T is irrelevant since it does not appear in any of Farmer John's cows at position 2). Position 1 is not sufficient by itself to explain spottiness, since an A in this position might indicate a spotty cow or a plain cow.

Given the genomes of Farmer John's cows, please count the number of locations that could potentially, by themselves, explain spottiness.

INPUT FORMAT (file cownomics.in):
The first line of input contains N and M, both positive integers of size at most 100. The next N lines each contain a string of M characters; these describe the genomes of the spotty cows. The final N lines describe the genomes of the plain cows.
OUTPUT FORMAT (file cownomics.out):
Please count the number of positions (an integer in the range 0…M) in the genome that could potentially explain spottiness. A location potentially explains spottiness if the spottiness trait can be predicted with perfect accuracy among Farmer John's population of cows by looking at just this one location in the genome.
SAMPLE INPUT:
3 8
AATCCCAT
GATTGCAA
GGTCGCAA
ACTCCCAG
ACTCGCAT
ACTTCCAT
SAMPLE OUTPUT:
1
Problem credits: Brian Dean
'''

class BovineGenomics:
	@staticmethod
	def analyze( M, genomeList ):
		N = len( genomeList )
		count = 0
		for column in range( M ):
			spottyCowSet = set()
			plainCowSet = set()
			for row in range( N // 2 ):
				spottyCowSet.add( genomeList[ row ][ column ] )
				plainCowSet.add( genomeList[ row + ( N // 2 ) ][ column ] )
			if set.isdisjoint( spottyCowSet, plainCowSet ):
				count += 1
		return count

class BovineGenomicsTest( unittest.TestCase ):
	def test_BovineGenomics( self ):
		for testfile in getTestFileList( tag='genomics' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/genomics/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/genomics/{}.out'.format( testfile ) ) as solutionFile:

			N, M = readIntegers( inputFile )
			genomeList = [ readString( inputFile ) for _ in range( 2 * N ) ]
			count = readInteger( solutionFile )

			print( 'Testcase {} N = {} count = {}'.format( testfile, N, count ) )
			self.assertEqual( BovineGenomics.analyze( M, genomeList ), count )

	def test_BovineGenomics_Sample( self ):
		M = 8
		genomeList = [
		'AATCCCAT',
		'GATTGCAA',
		'GGTCGCAA',
		'ACTCCCAG',
		'ACTCGCAT',
		'ACTTCCAT'
		]
		self.assertEqual( BovineGenomics.analyze( M, genomeList ), 1 )

'''
USACO 2017 US Open Contest, Silver

Problem 1. Paired Up

Farmer John finds that his cows are each easier to milk when they have another cow nearby for moral support. He therefore wants to take his M cows (M≤1,000,000,000, M even) and partition them into M/2 pairs. Each pair of cows will then be ushered off to a separate stall in the barn for milking. The milking in each of these M/2 stalls will take place simultaneously.
To make matters a bit complicated, each of Farmer John's cows has a different milk output. If cows of milk outputs A and B are paired up, then it takes a total of A+B units of time to milk them both.

Please help Farmer John determine the minimum possible amount of time the entire milking process will take to complete, assuming he pairs the cows up in the best possible way.

INPUT FORMAT (file pairup.in):
The first line of input contains N (1≤N≤100,000). Each of the next N lines contains two integers x and y, indicating that FJ has x cows each with milk output y (1≤y≤1,000,000,000). The sum of the x's is M, the total number of cows.
OUTPUT FORMAT (file pairup.out):
Print out the minimum amount of time it takes FJ's cows to be milked, assuming they are optimally paired up.
SAMPLE INPUT:
3
1 8
2 5
1 2
SAMPLE OUTPUT:
10
Here, if the cows with outputs 8+2 are paired up, and those with outputs 5+5 are paired up, the both stalls take 10 units of time for milking. Since milking takes place simultaneously, the entire process would therefore complete after 10 units of time. Any other pairing would be sub-optimal, resulting in a stall taking more than 10 units of time to milk.

Problem credits: Brian Dean
'''

class PairedUp:
	def __init__( self, milkOutputList ):
		self.milkOutputList = [ (milkOutput, numberOfCows) for (numberOfCows, milkOutput) in milkOutputList ]
		self.milkOutputList.sort()

	def minimumTime( self ):
		_minimumTime = - float( 'inf' )
		i, j = 0, len( self.milkOutputList ) - 1
		while i <= j:
			milkOutput_A, numberOfCows_A = self.milkOutputList[ i ]
			milkOutput_B, numberOfCows_B = self.milkOutputList[ j ]
			timeTaken = milkOutput_A + milkOutput_B
			_minimumTime = max( _minimumTime, milkOutput_A + milkOutput_B )

			if numberOfCows_A > numberOfCows_B:
				j = j - 1
				self.milkOutputList[ i ] = milkOutput_A, numberOfCows_A - numberOfCows_B
			elif numberOfCows_A < numberOfCows_B:
				i = i + 1
				self.milkOutputList[ j ] = milkOutput_B, numberOfCows_B - numberOfCows_A
			else:
				i = i + 1
				j = j - 1
		return _minimumTime

class PairedUpTest( unittest.TestCase ):
	def test_PairedUp( self ):
		for testfile in getTestFileList( tag='pairedup' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/pairedup/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/pairedup/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			milkOutputList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			minimumTime = readInteger( solutionFile )

			print( 'Testcase {} N = {} minimumTime = {}'.format( testfile, N, minimumTime ) )
			self.assertEqual( PairedUp( milkOutputList ).minimumTime(), minimumTime )

	def test_PairedUp_Sample( self ):
		milkOutputList = [ (1, 8), (2, 5), (1, 2) ]
		self.assertEqual( PairedUp( milkOutputList ).minimumTime(), 10 )

'''
USACO 2011 November Contest, Bronze Division

Problem 2: Awkward Digits [Brian Dean]

Bessie the cow is just learning how to convert numbers between different
bases, but she keeps making errors since she cannot easily hold a pen
between her two front hooves.  

Whenever Bessie converts a number to a new base and writes down the result,
she always writes one of the digits wrong.  For example, if she converts
the number 14 into binary (i.e., base 2), the correct result should be
"1110", but she might instead write down "0110" or "1111".  Bessie never
accidentally adds or deletes digits, so she might write down a number with
a leading digit of "0" if this is the digit she gets wrong.

Given Bessie's output when converting a number N into base 2 and base 3,
please determine the correct original value of N (in base 10). You can
assume N is at most 1 billion, and that there is a unique solution for N.

Please feel welcome to consult any on-line reference you wish regarding
base-2 and base-3 numbers, if these concepts are new to you.

PROBLEM NAME: digits

INPUT FORMAT:

* Line 1: The base-2 representation of N, with one digit written
        incorrectly.

* Line 2: The base-3 representation of N, with one digit written
        incorrectly.

SAMPLE INPUT (file digits.in):

1010
212

INPUT DETAILS:

When Bessie incorrectly converts N into base 2, she writes down
"1010".  When she incorrectly converts N into base 3, she writes down "212".

OUTPUT FORMAT:

* Line 1: The correct value of N.

SAMPLE OUTPUT (file digits.out):

14

OUTPUT DETAILS:

The correct value of N is 14 ("1110" in base 2, "112" in base 3).
'''

class AwkwardDigits:
	@staticmethod
	def analyze( base2String, base3String ):
		base2Digits = '01'
		base3Digits = '012'

		base2PossibilitySet = set()
		for i, digit in enumerate( base2String ):
			for tryDigit in base2Digits:
				if ( i == 0 and tryDigit == '0' ) or tryDigit == digit:
					continue
				possibility = base2String[ : i ] + tryDigit + base2String[ i + 1 : ]
				base2PossibilitySet.add( int( possibility, base=2 ) )

		for i, digit in enumerate( base3String ):
			for tryDigit in base3Digits:
				if ( i == 0 and tryDigit == '0' ) or tryDigit == digit:
					continue
				possibility = base3String[ : i ] + tryDigit + base3String[ i + 1 : ]
				number = int( possibility, base=3 )
				if number in base2PossibilitySet:
					return number

class AwkwardDigitsTest( unittest.TestCase ):
	def test_AwkwardDigits( self ):
		for testfile in range( 1, 11 ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/digits/I.{}'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/digits/O.{}'.format( testfile ) ) as solutionFile:

			base2String = readString( inputFile )
			base3String = readString( inputFile )
			number = readInteger( solutionFile )

			print( 'Testcase {} [{}] [{}] [{}]'.format( testfile, base2String, base3String, number ) )
			self.assertEqual( AwkwardDigits.analyze( base2String, base3String ), number )

	def test_AwkwardDigits_Sample( self ):
		self.assertEqual( AwkwardDigits.analyze( '1010', '212' ), 14 )

'''
USACO 2011 November Contest, Bronze Division

Problem 4: Cow Beauty Pageant (Bronze Level) [Brian Dean]

Hearing that the latest fashion trend was cows with two spots on their
hides, Farmer John has purchased an entire herd of two-spot cows. 
Unfortunately, fashion trends tend to change quickly, and the most popular
current fashion is cows with only one spot!  

FJ wants to make his herd more fashionable by painting each of his cows in
such a way that merges their two spots into one.  The hide of a cow is
represented by an N by M (1 <= N,M <= 50) grid of characters like this:

................
..XXXX....XXX...
...XXXX....XX...
.XXXX......XXX..
........XXXXX...
.........XXX....

Here, each 'X' denotes part of a spot.  Two 'X's belong to the same spot if
they are vertically or horizontally adjacent (diagonally adjacent does not
count), so the figure above has exactly two spots.  All of the cows in FJ's
herd have exactly two spots.

FJ wants to use as little paint as possible to merge the two spots into
one.  In the example above, he can do this by painting only three
additional characters with 'X's (the new characters are marked with '*'s
below to make them easier to see).

................
..XXXX....XXX...
...XXXX*...XX...
.XXXX..**..XXX..
........XXXXX...
.........XXX....

Please help FJ determine the minimum number of new 'X's he must paint in
order to merge two spots into one large spot.

PROBLEM NAME: pageant

INPUT FORMAT:

* Line 1: Two space-separated integers, N and M.

* Lines 2..1+N: Each line contains a length-M string of 'X's and '.'s
        specifying one row of the cow hide pattern.

SAMPLE INPUT (file pageant.in):

6 16
................
..XXXX....XXX...
...XXXX....XX...
.XXXX......XXX..
........XXXXX...
.........XXX....

INPUT DETAILS:

The pattern in the input shows a cow hide with two distinct spots, labeled
1 and 2 below:

................
..1111....222...
...1111....22...
.1111......222..
........22222...
.........222....

OUTPUT FORMAT:

* Line 1: The minimum number of new 'X's that must be added to the
        input pattern in order to obtain one single spot.

SAMPLE OUTPUT (file pageant.out):

3

OUTPUT DETAILS:

Three 'X's suffice to join the two spots into one:

................
..1111....222...
...1111X...22...
.1111..XX..222..
........22222...
.........222....
'''

class CowBeautyPageant:
	def __init__( self, rows, cols, layout ):
		self.rows, self.cols = rows, cols
		self.layout = layout

		self.emptyCell, self.spotCell = '.X'
		self.adjacentCellDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def paint( self ):
		spotLocation = None
		for i, j in itertools.product( range( self.rows ), range( self.cols ) ):
			if self.layout[ i ][ j ] == self.spotCell:
				spotLocation = i, j
				break

		boundaryCells = set()
		
		q = deque()
		q.append( spotLocation )
		
		visited = set()
		visited.add( spotLocation )

		while len( q ) > 0:
			u, v = currentCell = q.popleft()

			for du, dv in self.adjacentCellDelta:
				x, y = adjacentCell = u + du, v + dv
				if not 0 <= x < self.rows or not 0 <= y < self.cols:
					continue
				if self.layout[ x ][ y ] == self.emptyCell:
					boundaryCells.add( adjacentCell )
				elif self.layout[ x ][ y ] == self.spotCell and adjacentCell not in visited:
					visited.add( adjacentCell )
					q.append( adjacentCell )

		for boundaryCell in boundaryCells:
			q.append( (boundaryCell, 1) )

		while len( q ) > 0:
			currentCell, distance = q.popleft()

			u, v = currentCell
			for du, dv in self.adjacentCellDelta:
				x, y = adjacentCell = u + du, v + dv
				if not 0 <= x < self.rows or not 0 <= y < self.cols:
					continue
				if self.layout[ x ][ y ] == self.spotCell and adjacentCell not in visited:
					return distance
				elif self.layout[ x ][ y ] == self.emptyCell and adjacentCell not in visited:
					visited.add( adjacentCell )
					q.append( (adjacentCell, distance + 1) )

class CowBeautyPageantTest( unittest.TestCase ):
	def test_CowBeautyPageant( self ):
		for testfile in range( 1, 11 ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/pageant/I.{}'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/pageant/O.{}'.format( testfile ) ) as solutionFile:

			rows, cols = readIntegers( inputFile )
			layout = [ readString( inputFile ) for _ in range( rows ) ]
			count = readInteger( solutionFile )

			print( 'Testcase {} rows = {} cols = {} count = {}'.format( testfile, rows, cols, count ) )
			self.assertEqual( CowBeautyPageant( rows, cols, layout ).paint(), count )

	def test_CowBeautyPageant_Sample( self ):
		rows, cols = 6, 16
		layout = [
		'................',
		'..XXXX....XXX...',
		'...XXXX....XX...',
		'.XXXX......XXX..',
		'........XXXXX...',
		'.........XXX....'
		]
		self.assertEqual( CowBeautyPageant( rows, cols, layout ).paint(), 3 )

'''
USACO 2011 November Contest, Silver Division

Problem 2: Cow Lineup [Brian Dean]

Farmer John has hired a professional photographer to take a picture of some
of his cows.  Since FJ's cows represent a variety of different breeds, he
would like the photo to contain at least one cow from each distinct breed
present in his herd.

FJ's N cows are all standing at various positions along a line, each
described by an integer position (i.e., its x coordinate) as well as an
integer breed ID.  FJ plans to take a photograph of a contiguous range of
cows along the line.  The cost of this photograph is equal its size -- that
is, the difference between the maximum and minimum x coordinates of the
cows in the range of the photograph.  

Please help FJ by computing the minimum cost of a photograph in which there
is at least one cow of each distinct breed appearing in FJ's herd.

PROBLEM NAME: lineup

INPUT FORMAT:

* Line 1: The number of cows, N (1 <= N <= 50,000).

* Lines 2..1+N: Each line contains two space-separated positive
        integers specifying the x coordinate and breed ID of a single
        cow.  Both numbers are at most 1 billion.

SAMPLE INPUT (file lineup.in):

6
25 7
26 1
15 1
22 3
20 1
30 1

INPUT DETAILS:

There are 6 cows, at positions 25,26,15,22,20,30, with respective breed IDs
7,1,1,3,1,1.

OUTPUT FORMAT:

* Line 1: The smallest cost of a photograph containing each distinct
        breed ID.

SAMPLE OUTPUT (file lineup.out):

4

OUTPUT DETAILS:

The range from x=22 up through x=26 (of total size 4) contains each of the
distinct breed IDs 1, 3, and 7 represented in FJ's herd.
'''

class CowLineup:
	@staticmethod
	def minimumCost( infoList ):
		infoList.sort()

		distinctBreeds = set()
		for _, breedId in infoList:
			distinctBreeds.add( breedId )
		numberOfBreeds = len( distinctBreeds )

		breedCountDict = dict()
		cost = float( 'inf' )
		
		i = j = 0
		while j < len( infoList ):
			x2, breedId = infoList[ j ]
			if breedId not in breedCountDict:
				breedCountDict[ breedId ] = 0
			breedCountDict[ breedId ] += 1

			j += 1

			while len( breedCountDict ) == numberOfBreeds:
				x1, breedId = infoList[ i ]
				cost = min( cost, x2 - x1 )

				breedCountDict[ breedId ] -= 1
				if breedCountDict[ breedId ] == 0:
					del breedCountDict[ breedId ]

				i += 1
		return cost

class CowLineupTest( unittest.TestCase ):
	def test_CowLineup( self ):
		for testfile in range( 1, 13 ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowlineup/I.{}'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowlineup/O.{}'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			infoList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			cost = readInteger( solutionFile )

			print( 'Testcase {} N = {} cost = {}'.format( testfile, N, cost ) )
			self.assertEqual( CowLineup.minimumCost( infoList ), cost )

	def test_CowLineup_Sample( self ):
		infoList = [ (25, 7), (26, 1), (15, 1), (22, 3), (20, 1), (30, 1) ]
		self.assertEqual( CowLineup.minimumCost( infoList ), 4 )

'''
USACO 2012 January Contest, Bronze Division

Problem 2: Haybale Stacking [Brian Dean, 2012]

Feeling sorry for all the mischief she has caused around the farm recently,
Bessie has agreed to help Farmer John stack up an incoming shipment of hay
bales.  

She starts with N (1 <= N <= 1,000,000, N odd) empty stacks, numbered 1..N.
FJ then gives her a sequence of K instructions (1 <= K <= 25,000), each of
the form "A B", meaning that Bessie should add one new haybale to the top
of each stack in the range A..B.  For example, if Bessie is told "10 13",
then she should add a haybale to each of the stacks 10, 11, 12, and 13.

After Bessie finishes stacking haybales according to his instructions, FJ
would like to know the median height of his N stacks -- that is, the height
of the middle stack if the stacks were to be arranged in sorted order
(conveniently, N is odd, so this stack is unique).  Please help Bessie
determine the answer to FJ's question.

PROBLEM NAME: stacking

INPUT FORMAT:

* Line 1: Two space-separated integers, N K.

* Lines 2..1+K: Each line contains one of FJ's instructions in the
        form of two space-separated integers A B (1 <= A <= B <= N).

SAMPLE INPUT (file stacking.in):

7 4
5 5
2 4
4 6
3 5

INPUT DETAILS:

There are N=7 stacks, and FJ issues K=4 instructions.  The first
instruction is to add a haybale to stack 5, the second is to add haybales
to stacks 2..4, etc.

OUTPUT FORMAT:

* Line 1: The median height of a stack after Bessie completes the
        instructions.

SAMPLE OUTPUT (file stacking.out):

1

OUTPUT DETAILS:

After Bessie is finished, the stacks have heights 0,1,2,3,3,1,0.  The median
stack height is 1, since 1 is the middle element in the sorted ordering
0,0,1,1,2,3,3.
'''

class HaybaleStacking:
	def __init__( self, N, K, instructionList ):
		self.N, self.K = N, K
		self.instructionList = instructionList

	def median( self ):
		haybaleStacks = [ 0 for _ in range( self.N + 1 ) ]
		for (i, j) in self.instructionList:
			haybaleStacks[ i - 1 ] += 1
			haybaleStacks[ j ] -= 1
		
		haybaleStacks.pop()
		offset = 0
		for i in range( len( haybaleStacks ) ):
			offset += haybaleStacks[ i ]
			haybaleStacks[ i ] = offset
		haybaleStacks.sort()
		return haybaleStacks[ ( self.N - 1 ) // 2 ]

class HaybaleStackingTest( unittest.TestCase ):
	def test_HaybaleStacking( self ):
		for testfile in getTestFileList( tag='haybalestacking' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/haybalestacking/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/haybalestacking/{}.out'.format( testfile ) ) as solutionFile:

			N, K = readIntegers( inputFile )
			instructionList = [ tuple( readIntegers( inputFile ) ) for _ in range( K ) ]
			median = readInteger( solutionFile )

			print( 'Testcase {} N = {} K = {} median = {}'.format( testfile, N, K, median ) ) 
			self.assertEqual( HaybaleStacking( N, K, instructionList ).median(), median )

	def test_HaybaleStacking_Sample( self ):
		N, K = 7, 4
		instructionList = [ (5, 5), (2, 4), (4, 6), (3, 5) ]
		self.assertEqual( HaybaleStacking( N, K, instructionList ).median(), 1 )

'''
USACO 2013 January Contest, Silver

Problem 3: Party Invitations [Travis Hance, 2012]

Farmer John is throwing a party and wants to invite some of his cows to
show them how much he cares about his herd.  However, he also wants to
invite the smallest possible number of cows, remembering all too well the
disaster that resulted the last time he invited too many cows to a party.

Among FJ's cows, there are certain groups of friends that are hard to
separate.  For any such group (say, of size k), if FJ invites at least k-1
of the cows in the group to the party, then he must invite the final cow as
well, thereby including the entire group.  Groups can be of any size and
may even overlap with each-other, although no two groups contain exactly
the same set of members.  The sum of all group sizes is at most 250,000.

Given the groups among FJ's cows, please determine the minimum number of
cows FJ can invite to his party, if he decides that he must definitely
start by inviting cow #1 (his cows are conveniently numbered 1..N, with N
at most 1,000,000).

PROBLEM NAME: invite

INPUT FORMAT:

* Line 1: Two space-separated integers: N (the number of cows), and G
        (the number of groups).

* Lines 2..1+G: Each line describes a group of cows.  It starts with
        an integer giving the size S of the group, followed by the S
        cows in the group (each an integer in the range 1..N).

SAMPLE INPUT (file invite.in):

10 4
2 1 3
2 3 4
6 1 2 3 4 6 7
4 4 3 2 1

INPUT DETAILS:

There are 10 cows and 4 groups.  The first group contains cows 1 and 3, and
so on.

OUTPUT FORMAT:

* Line 1: The minimum number of cows FJ can invite to his party.

SAMPLE OUTPUT (file invite.out):

4

OUTPUT DETAILS:

In addition to cow #1, FJ must invite cow #3 (due to the first group
constraint), cow #4 (due to the second group constraint), and also cow #2
(due to the final group constraint).
'''

class PartyInvitations:
	def __init__( self, N, groupInfo ):
		self.N = N
		self.groupInfo = [ set( groupInfoList ) for groupInfoList in groupInfo ]
		self.startCowId = 1

	def minimumInvites( self ):
		groupInfoDict = defaultdict( lambda : list() )
		for index, cowIdSet in enumerate( self.groupInfo ):
			for cowId in cowIdSet:
				groupInfoDict[ cowId ].append( index )

		evaluationStack = list()
		evaluationStack.append( self.startCowId )

		processed = set()

		count = 0
		while len( evaluationStack ) > 0:
			cowId = evaluationStack.pop()
			if cowId in processed:
				continue
			processed.add( cowId )

			count += 1
			for index in groupInfoDict[ cowId ]:
				cowIdSet = self.groupInfo[ index ]
				cowIdSet.remove( cowId )
				if len( cowIdSet ) == 1:
					evaluationStack.append( min( cowIdSet ) )
		return count

class PartyInvitationsTest( unittest.TestCase ):
	def test_PartyInvitations( self ):
		for testfile in getTestFileList( tag='partyinvitations' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/partyinvitations/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/partyinvitations/{}.out'.format( testfile ) ) as solutionFile:

			N, groupCount = readIntegers( inputFile )
			groupInfo = list()
			for _ in range( groupCount ):
				groupInfoList = list( readIntegers( inputFile ) )
				groupInfo.append( groupInfoList[ 1 : ] ) # The first element is the length of the list.
			minimumInvites = readInteger( solutionFile )

			print( 'Testcase {} N = {} groupCount = {} minimumInvites = {}'.format( testfile, N, groupCount, minimumInvites ) )
			self.assertEqual( PartyInvitations( 10, groupInfo ).minimumInvites(), minimumInvites )

	def test_PartyInvitations_Sample( self ):
		groupInfo = [ [ 1, 3 ], [ 3, 4 ], [ 1, 2, 3, 4, 6, 7 ], [ 4, 3, 2, 1 ] ]
		self.assertEqual( PartyInvitations( 10, groupInfo ).minimumInvites(), 4 )

'''
USACO 2013 January Contest, Gold

Problem 1: Cow Lineup [Brian Dean and Daniel Dara, 2012]

Farmer John's N cows (1 <= N <= 100,000) are lined up in a row.  Each cow is
identified by an integer "breed ID" in the range 0...1,000,000,000; the
breed ID of the ith cow in the lineup is B(i).  Multiple cows can share the
same breed ID.

FJ thinks that his line of cows will look much more impressive if there is
a large contiguous block of cows that all have the same breed ID.  In order
to create such a block, FJ chooses up to K breed IDs and removes from his
lineup all the cows having those IDs.  Please help FJ figure out
the length of the largest consecutive block of cows with the same breed ID
that he can create by doing this.

PROBLEM NAME: lineup

INPUT FORMAT:

* Line 1: Two space-separated integers: N and K.

* Lines 2..1+N: Line i+1 contains the breed ID B(i).

SAMPLE INPUT (file lineup.in):

9 1
2
7
3
7
7
3
7
5
7

INPUT DETAILS:

There are 9 cows in the lineup, with breed IDs 2, 7, 3, 7, 7, 3, 7, 5, 7. 
FJ would like to remove up to 1 breed ID from this lineup.

OUTPUT FORMAT:

* Line 1: The largest size of a contiguous block of cows with
        identical breed IDs that FJ can create.

SAMPLE OUTPUT (file lineup.out):

4

OUTPUT DETAILS:

By removing all cows with breed ID 3, the lineup reduces to 2, 7, 7, 7, 7,
5, 7.  In this new lineup, there is a contiguous block of 4 cows with the
same breed ID (7).
'''

class CowLineupGold:
	def __init__( self, N, K, breedIdList ):
		self.N, self.K = N, K
		self.breedIdList = breedIdList

	def consecutiveBlock( self ):
		frequencyDict = dict()
		i = j = 0

		maximumBlockSize = 0
		q = deque()
		
		while j < len( self.breedIdList ):
			breedId = self.breedIdList[ j ]
			frequency = frequencyDict.get( breedId, 0 ) + 1
			frequencyDict[ breedId ] = frequency

			while len( q ) > 0:
				breedId_q, frequency_q = q[ -1 ]
				if frequency_q < frequency:
					q.pop()
				else:
					break
			q.append( (breedId, frequency) )

			j = j + 1

			while len( frequencyDict ) > self.K + 1:
				breedId = self.breedIdList[ i ]
				frequencyDict[ breedId ] -= 1
				if frequencyDict[ breedId ] == 0:
					del frequencyDict[ breedId ]

				breedId_q, frequency_q = q[ 0 ]
				if breedId_q == breedId:
					q.popleft()

				i = i + 1

			_, frequency = q[ 0 ]
			maximumBlockSize = max( maximumBlockSize, frequency )
		return maximumBlockSize

class CowLineupGoldTest( unittest.TestCase ):
	def test_CowLineupGold( self ):
		for testfile in getTestFileList( tag='cowlineup_gold' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowlineup_gold/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowlineup_gold/{}.out'.format( testfile ) ) as solutionFile:

			N, K = readIntegers( inputFile )
			breedIdList = [ readInteger( inputFile ) for _ in range( N ) ]
			consecutiveBlock = readInteger( solutionFile )

			print( 'Testcase {} N = {} K = {} consecutiveBlock = {}'.format( testfile, N, K, consecutiveBlock ) )
			self.assertEqual( CowLineupGold( N, K, breedIdList ).consecutiveBlock(), consecutiveBlock )

	def test_CowLineupGold_Sample( self ):
		N, K = 9, 1
		breedIdList = [ 2, 7, 3, 7, 7, 3, 7, 5, 7 ]
		self.assertEqual( CowLineupGold( N, K, breedIdList ).consecutiveBlock(), 4 )

'''
USACO 2013 February Contest, Bronze

Problem 1: Message Relay [Brian Dean, 2013]

Farmer John's N cows (1 <= N <= 1000) are conveniently numbered from 1..N.
Using an old-fashioned communicating mechanism based on tin cans and
strings, the cows have figured out how to communicate between each-other
without Farmer John noticing. 

Each cow can forward messages to at most one other cow: for cow i, the
value F(i) tells you the index of the cow to which cow i will forward any
messages she receives (this number is always different from i).  If F(i) 
is zero, then cow i does not forward messages.  

Unfortunately, the cows have realized the possibility that messages
originating at certain cows might ultimately get stuck in loops, forwarded
around in a cycle forever.  A cow is said to be "loopy" if a message sent
from that cow will ultimately get stuck in a loop.  The cows want to avoid
sending messages from loopy cows.  Please help them by counting the total
number of FJ's cows that are not loopy.

PROBLEM NAME: relay

INPUT FORMAT:

* Line 1: The number of cows, N.

* Lines 2..1+N: Line i+1 contains the value of F(i).

SAMPLE INPUT (file relay.in):

5
0
4
1
5
4

INPUT DETAILS:

There are 5 cows.  Cow 1 does not forward messages.  Cow 2 forwards
messages to cow 4, and so on.

OUTPUT FORMAT:

* Line 1: The total number of non-loopy cows.

SAMPLE OUTPUT (file relay.out):

2

OUTPUT DETAILS:

Cow 1 is not loopy since she does not forward messages.  Cow 3 is also
not loopy since she forwards messages to cow 1, who then does not forward
messages onward.  All other cows are loopy.
'''

class MessageRelay:
	def __init__( self, N, messageRelayInfo ):
		self.numberOfCows = N
		self.messageRelayInfo = [ None ] + messageRelayInfo # Add a dummy element so that indices 1..N are valid.

	def notLoopy( self ):
		loopy = [ None for _ in range( self.numberOfCows + 1 ) ]

		def _analyze( cowId ):
			relay = set()
			while True:
				# A loop is present. All cowId present in the relay are to be marked as loopy.
				if cowId in relay:
					for cowId in relay:
						loopy[ cowId ] = True
					break
				relay.add( cowId )
				if self.messageRelayInfo[ cowId ] == 0:
					for cowId in relay:
						loopy[ cowId ] = False
					break
				cowId = self.messageRelayInfo[ cowId ]
				
		for cowId in range( 1, self.numberOfCows + 1 ):
			_analyze( cowId )
		
		return sum( [ 1 if not loopy[ cowId ] else 0 for cowId in range( 1, self.numberOfCows + 1 ) ] )

class MessageRelayTest( unittest.TestCase ):
	def test_MessageRelay( self ):
		for testfile in getTestFileList( tag='messagerelay' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/messagerelay/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/messagerelay/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			messageRelayInfo = [ readInteger( inputFile ) for _ in range( N ) ]
			notLoopy = readInteger( solutionFile )

			print( 'Testcase {} N = {} notLoopy = {}'.format( testfile, N, notLoopy ) )
			self.assertEqual( MessageRelay( N, messageRelayInfo ).notLoopy(), notLoopy )

	def test_MessageRelay_Sample( self ):
		N = 5
		messageRelayInfo = [ 0, 4, 1, 5, 4 ]
		self.assertEqual( MessageRelay( N, messageRelayInfo ).notLoopy(), 2 )

'''
USACO 2013 February Contest, Bronze

Problem 3: Perimeter [Brian Dean, 2013]

Farmer John has arranged N hay bales (1 <= N <= 10,000) in the middle of
one of his fields.  If we think of the field as a 100 x 100 grid of 1 x 1
square cells, each hay bale occupies exactly one of these cells (no two hay
bales occupy the same cell, of course).

FJ notices that his hay bales all form one large connected region, meaning
that starting from any bale, one can reach any other bale by taking a
series of steps either north, south, east, or west onto directly adjacent
bales.  The connected region of hay bales may however contain "holes" --
empty regions that are completely surrounded by hay bales. 

Please help FJ determine the perimeter of the region formed by his hay
bales.  Note that holes do not contribute to the perimeter.

PROBLEM NAME: perimeter

INPUT FORMAT:

* Line 1: The number of hay bales, N.

* Lines 2..1+N: Each line contains the (x,y) location of a single hay
        bale, where x and y are integers both in the range 1..100. 
        Position (1,1) is the lower-left cell in FJ's field, and
        position (100,100) is the upper-right cell.

SAMPLE INPUT (file perimeter.in):

8
5 3
5 4
8 4
5 5
6 3
7 3
7 4
6 5

INPUT DETAILS:

The connected region consisting of hay bales looks like this:

XX 
X XX
XXX

OUTPUT FORMAT:

* Line 1: The perimeter of the connected region of hay bales.

SAMPLE OUTPUT (file perimeter.out):

14

OUTPUT DETAILS:

The length of the perimeter of the connected region is 14 (for example, the
left side of the region contributes a length of 3 to this total).  Observe
that the hole in the middle does not contribute to this number.
'''

class Perimeter:
	def __init__( self, positionList ):
		maximum_x_or_y = 100
		self.size = maximum_x_or_y + 1
		self.emptyCell, self.haybale, self.blueMark = '.HX'
		self.field = [ [ self.emptyCell for _ in range( self.size + 1 ) ] for _ in range( self.size + 1 ) ]

		for x, y in positionList:
			self.field[ x ][ y ] = self.haybale
		self.anyHaybalePosition = positionList.pop()

		self.adjacentLocationDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]

	def perimeter( self ):
		origin = 0, 0
		q = deque()
		q.append( origin )

		# Using breadth first search, mark empty locations outside the hay.
		while len( q ) > 0:
			u, v = q.popleft()
			if self.field[ u ][ v ] == self.blueMark:
				continue
			self.field[ u ][ v ] = self.blueMark
			for du, dv in self.adjacentLocationDelta:
				adjacentLocation = x, y = u + du, v + dv
				if 0 <= x <= self.size and 0 <= y <= self.size and self.field[ x ][ y ] == self.emptyCell:
					q.append( adjacentLocation )

		# From any position where a haybale is present, do a breadth first search. Count the number
		# of marked cells.
		q = deque()
		q.append( self.anyHaybalePosition )

		visited = set()
		visited.add( self.anyHaybalePosition )

		perimeter = 0
		while len( q ) > 0:
			u, v = q.popleft()
			for du, dv in self.adjacentLocationDelta:
				x, y = adjacentLocation = u + du, v + dv
				if not 0 <= x <= self.size or not 0 <= y <= self.size:
					continue
				if self.field[ x ][ y ] == self.haybale and adjacentLocation not in visited:
					visited.add( adjacentLocation )
					q.append( adjacentLocation )
				elif self.field[ x ][ y ] == self.blueMark:
					perimeter += 1
		return perimeter

class PerimeterTest( unittest.TestCase ):
	def test_Perimeter( self ):
		for testfile in getTestFileList( tag='perimeter' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/perimeter/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/perimeter/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			positionList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			perimeter = readInteger( solutionFile )

			print( 'Testcase {} N = {} perimeter = {}'.format( testfile, N, perimeter ) )
			self.assertEqual( Perimeter( positionList ).perimeter(), perimeter )

	def test_Perimeter_Sample( self ):
		positionList = [ (5, 3), (5, 4), (8, 4), (5, 5), (6, 3), (7, 3), (7, 4), (6, 5) ]
		self.assertEqual( Perimeter( positionList ).perimeter(), 14 )

'''
USACO 2013 February Contest, Silver

Problem 1: Perimeter [Brian Dean, 2013]

Farmer John has arranged N hay bales (1 <= N <= 50,000) in the middle of
one of his fields.  If we think of the field as a 1,000,000 x 1,000,000
grid of 1 x 1 square cells, each hay bale occupies exactly one of these
cells (no two hay bales occupy the same cell, of course).

FJ notices that his hay bales all form one large connected region, meaning
that starting from any bale, one can reach any other bale by taking a
series of steps either north, south, east, or west onto directly adjacent
bales.  The connected region of hay bales may however contain "holes" --
empty regions that are completely surrounded by hay bales. 

Please help FJ determine the perimeter of the region formed by his hay
bales.  Note that holes do not contribute to the perimeter.

PROBLEM NAME: perimeter

INPUT FORMAT:

* Line 1: The number of hay bales, N.

* Lines 2..1+N: Each line contains the (x,y) location of a single hay
        bale, where x and y are integers both in the range
        1..1,000,000. Position (1,1) is the lower-left cell in FJ's
        field, and position (1000000,1000000) is the upper-right cell.

SAMPLE INPUT (file perimeter.in):

8
10005 200003
10005 200004
10008 200004
10005 200005
10006 200003
10007 200003
10007 200004
10006 200005

INPUT DETAILS:

The connected region consisting of hay bales looks like this:

XX 
X XX
XXX

OUTPUT FORMAT:

* Line 1: The perimeter of the connected region of hay bales.

SAMPLE OUTPUT (file perimeter.out):

14

OUTPUT DETAILS:

The length of the perimeter of the connected region is 14 (for example, the
left side of the region contributes a length of 3 to this total).  Observe
that the hole in the middle does not contribute to this number.
'''

class PerimeterSilver:
	def __init__( self, positionList ):
		self.haybaleLocations = set( positionList )
		self.minimumHaybalePosition = min( positionList )

		self.adjacentLocationDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]
		self.diagonalLocationDelta = [ (1, 1), (1, -1), (-1, 1), (-1, -1) ]

	def _adjacentToHay( self, location ):
		u, v = location
		for du, dv in self.adjacentLocationDelta + self.diagonalLocationDelta:
			adjacentLocation = u + du, v + dv
			if adjacentLocation in self.haybaleLocations:
				return True
		return False

	def perimeter( self ):
		x, y = self.minimumHaybalePosition
		x = x - 1
		anyBoundaryCell = x, y

		q = deque()
		q.append( anyBoundaryCell )

		boundaryCells = set()
		boundaryCells.add( anyBoundaryCell )

		while len( q ) > 0:
			u, v = q.popleft()
			for du, dv in self.adjacentLocationDelta:
				x, y = adjacentLocation = u + du, v + dv
				if adjacentLocation in self.haybaleLocations:
					continue
				if adjacentLocation not in boundaryCells and self._adjacentToHay( adjacentLocation ):
					boundaryCells.add( adjacentLocation )
					q.append( adjacentLocation )

		perimeter = 0
		q = deque()
		q.append( self.minimumHaybalePosition )

		visited = set()
		visited.add( self.minimumHaybalePosition )

		while len( q ) > 0:
			u, v = q.popleft()
			for du, dv in self.adjacentLocationDelta:
				adjacentLocation = u + du, v + dv
				if adjacentLocation in boundaryCells:
					perimeter += 1
				elif adjacentLocation in self.haybaleLocations and adjacentLocation not in visited:
					visited.add( adjacentLocation )
					q.append( adjacentLocation )
		return perimeter

class PerimeterSilverTest( unittest.TestCase ):
	def test_PerimeterSilver( self ):
		for testfile in getTestFileList( tag='perimeter_silver' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/perimeter_silver/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/perimeter_silver/{}.out'.format( testfile ) ) as solutionFile:

			N = readInteger( inputFile )
			positionList = [ tuple( readIntegers( inputFile ) ) for _ in range( N ) ]
			perimeter = readInteger( solutionFile )

			print( 'Testcase {} N = {} perimeter = {}'.format( testfile, N, perimeter ) )
			self.assertEqual( PerimeterSilver( positionList ).perimeter(), perimeter )

	def test_PerimeterSilver_Sample( self ):
		positionList = [ (10005, 200003), (10005, 200004), (10008, 200004), (10005, 200005), (10006, 200003),
                         (10007, 200003), (10007, 200004), (10006, 200005) ]
		self.assertEqual( PerimeterSilver( positionList ).perimeter(), 14 )

'''
USACO 2014 March Contest, Bronze

Problem 3: Cow Art [Brian Dean, 2014]

A little known fact about cows is the fact that they are red-green
colorblind, meaning that red and green look identical to them.  This makes
it especially difficult to design artwork that is appealing to cows as well
as humans.

Consider a square painting that is described by an N x N grid of characters
(1 <= N <= 100), each one either R (red), G (green), or B (blue).  A
painting is interesting if it has many colored "regions" that can
be distinguished from each-other.  Two characters belong to the same
region if they are directly adjacent (east, west, north, or south), and
if they are indistinguishable in color.  For example, the painting

RRRBB
GGBBB
BBBRR
BBRRR
RRRRR

has 4 regions (2 red, 1 blue, and 1 green) if viewed by a human, but only 3
regions (2 red-green, 1 blue) if viewed by a cow.  

Given a painting as input, please help compute the number of regions in the
painting when viewed by a human and by a cow.

PROBLEM NAME: cowart

INPUT FORMAT:

* Line 1: The integer N.

* Lines 2..1+N: Each line contains a string with N characters,
        describing one row of a painting.

SAMPLE INPUT (file cowart.in):

5
RRRBB
GGBBB
BBBRR
BBRRR
RRRRR

OUTPUT FORMAT:

* Line 1: Two space-separated integers, telling the number of regions
        in the painting when viewed by a human and by a cow.

SAMPLE OUTPUT (file cowart.out):

4 3
'''

class CowArt:
	def __init__( self, layout ):
		self.size = len( layout )
		self.layout = layout
		self.adjacentLocationDelta = [ (0, 1), (0, -1), (1, 0), (-1, 0) ]
		self.redColor, self.greenColor = 'RG'

	def _floodFill( self, location, visited, cowVision=False ):
		stack = list()
		stack.append( location )

		while len( stack ) > 0:
			u, v = stack.pop()
			if visited[ u ][ v ]:
				continue
			visited[ u ][ v ] = True

			color_A = self.layout[ u ][ v ]

			for du, dv in self.adjacentLocationDelta:
				x, y = adjacentLocation = u + du, v + dv
				if not 0 <= x < self.size or not 0 <= y < self.size:
					continue

				color_B = self.layout[ x ][ y ]

				identicalColor = ( color_A == color_B )
				identicalColorForCows = identicalColor or (color_A, color_B) == (self.redColor, self.greenColor) or \
				                                          (color_A, color_B) == (self.greenColor, self.redColor)

				if not cowVision and identicalColor:
					stack.append( adjacentLocation )
				elif cowVision and identicalColorForCows:
					stack.append( adjacentLocation )

	def analyze( self ):
		visited = [ [ False for _ in range( self.size ) ] for _ in range( self.size ) ]
		visitedCowVision = [ [ False for _ in range( self.size ) ] for _ in range( self.size ) ]

		count = cowVisionCount = 0
		for i, j in itertools.product( range( self.size ), range( self.size ) ):
			location = i, j
			if not visited[ i ][ j ]:
				self._floodFill( location, visited, cowVision=False )
				count += 1
			if not visitedCowVision[ i ][ j ]:
				self._floodFill( location, visitedCowVision, cowVision=True )
				cowVisionCount += 1
		return count, cowVisionCount

class CowArtTest( unittest.TestCase ):
	def test_CowArt( self ):
		for testfile in getTestFileList( tag='cowart' ):
			self._verify( testfile )

	def _verify( self, testfile ):
		with open( 'tests/usaco/cowart/{}.in'.format( testfile ) ) as inputFile, \
		     open( 'tests/usaco/cowart/{}.out'.format( testfile ) ) as solutionFile:

			size = readInteger( inputFile )
			layout = [ readString( inputFile ) for _ in range( size ) ]
			count = tuple( readIntegers( solutionFile ) )

			print( 'Testcase {} size = {} count = {}'.format( testfile, size, count ) )
			self.assertEqual( CowArt( layout ).analyze(), count )

	def test_CowArt_Sample( self ):
		layout = [
		'RRRBB',
		'GGBBB',
		'BBBRR',
		'BBRRR',
		'RRRRR'
		]
		self.assertEqual( CowArt( layout ).analyze(), (4, 3) )

'''
USACO 2011 November Contest, Bronze Division

Problem 3: Moo Sick [Rob Seay]

Everyone knows that cows love to listen to all forms of music.  Almost all
forms, that is -- the great cow composer Wolfgang Amadeus Moozart
once discovered that a specific chord tends to make cows rather ill.  This
chord, known as the ruminant seventh chord, is therefore typically avoided
in all cow musical compositions.

Farmer John, not knowing the finer points of cow musical history, decides
to play his favorite song over the loudspeakers in the barn.  Your task is
to identify all the ruminant seventh chords in this song, to estimate how
sick it will make the cows.

The song played by FJ is a series of N (1 <= N <= 20,000) notes, each an
integer in the range 1..88.  A ruminant seventh chord is specified by a
sequence of C (1 <= C <= 10) distinct notes, also integers in the range
1..88.  However, even if these notes are transposed (increased or decreased
by a common amount), or re-ordered, the chord remains a ruminant seventh
chord!  For example, if "4 6 7" is a ruminant seventh chord, then "3 5 6"
(transposed by -1), "6 8 9" (transposed by +2), "6 4 7" (re-ordered), and
"5 3 6" (transposed and re-ordered) are also ruminant seventh chords.

A ruminant seventh chord is a sequence of C consecutive notes satisfying
the above criteria. It is therefore uniquely determined by its starting
location in the song. Please determine the indices of the starting
locations of all of the ruminant seventh chords.

PROBLEM NAME: moosick

INPUT FORMAT:

* Line 1: A single integer: N.

* Lines 2..1+N: The N notes in FJ's song, one note per line.

* Line 2+N: A single integer: C.

* Lines 3+N..2+N+C: The C notes in an example of a ruminant seventh
        chord.  All transpositions and/or re-orderings of these notes
        are also ruminant seventh chords.

SAMPLE INPUT (file moosick.in):

6
1
8
5
7
9
10
3
4
6
7

INPUT DETAILS:

FJ's song is 1,8,5,7,9,10.  A ruminant seventh chord is some
transposition/re-ordering of 4,6,7.

OUTPUT FORMAT:

* Line 1: A count, K, of the number of ruminant seventh chords that
        appear in FJ's song.  Observe that different instances of
        ruminant seventh chords can overlap each-other.

* Lines 2..1+K: Each line specifies the starting index of a ruminant
        seventh chord (index 1 is the first note in FJ's song, index N
        is the last).  Indices should be listed in increasing sorted
        order.

SAMPLE OUTPUT (file moosick.out):

2
2
4

OUTPUT DETAILS:

Two ruminant seventh chords appear in FJ's song (and these occurrences
actually overlap by one note).  The first is 8,5,7 (transposed by +1 and
reordered) starting at index 2, and the second is 7,9,10 (transposed by +3)
starting at index 4.
'''

class MooSick:
	def __init__( self, noteList, seventhChordList ):
		self.noteList = noteList
		self.seventhChordList = seventhChordList
		self.seventhChordList.sort()

	def _isRuminantSeventhChord( self, chord ):
		chord.sort()
		delta = None
		for i in range( len( chord ) ):
			if delta is None:
				delta = self.seventhChordList[ i ] - chord[ i ]
				continue
			if self.seventhChordList[ i ] - chord[ i ] != delta:
				return False
		return True

	def ruminant( self ):
		ruminantIndexList = list()

		C = len( self.seventhChordList )
		ruminantChordSum = sum( self.seventhChordList )
		_sum = 0
		i = j = 0
		
		while j < len( self.noteList ):
			_sum += self.noteList[ j ]
			j += 1
			if j - i < C:
				continue
			if ( _sum - ruminantChordSum ) % C == 0 and self._isRuminantSeventhChord( self.noteList[ i : j ] ):
				ruminantIndexList.append( i + 1 )
			_sum -= self.noteList[ i ]
			i += 1
		return ruminantIndexList

class MooSickTest( unittest.TestCase ):
	def test_MooSick( self ):
		for testfile in range( 1, 10 + 1 ):
			with open( 'tests/usaco/moosick/I.{}'.format( testfile ) ) as inputFile, \
			     open( 'tests/usaco/moosick/O.{}'.format( testfile ) ) as solutionFile:

				N = readInteger( inputFile )
				noteList = [ readInteger( inputFile ) for _ in range( N ) ]
				C = readInteger( inputFile )
				seventhChordList = [ readInteger( inputFile ) for _ in range( C ) ]
				K = readInteger( solutionFile )
				ruminantIndexList = [ readInteger( solutionFile ) for _ in range( K ) ]

				print( 'Testcase {} N = {} C = {} K = {}'.format( testfile, N, C, K ) )
				self.assertEqual( MooSick( noteList, seventhChordList ).ruminant(), ruminantIndexList )

	def test_MooSick_Sample( self ):
		noteList = [ 1, 8, 5, 7, 9, 10 ]
		seventhChordList = [ 4, 6, 7 ]
		self.assertEqual( MooSick( noteList, seventhChordList ).ruminant(), [ 2, 4 ] ) 

####################################################################################################
####################################################################################################
#
# Test Infrastructure - Each test is registered with the corresponding contestTag and problemTag.
#
####################################################################################################
####################################################################################################

class DuplicateTag( Exception ):
	def __init__( self, contestTag, problemTag ):
		self.contestTag, self.problemTag = contestTag, problemTag

	def __repr__( self ):
		return 'Duplicate Tag ({}, {})'.format( self.contestTag, self.problemTag )

class DuplicateSolutionClass( Exception ):
	pass

class USACO_Contest:
	def __init__( self ):
		self.contestProblemTagSet = set()
		self.solutionTestClassSet = set()
		
		self.problems = list()

	def register( self, contestTag, problemTag, solutionTestClass=None ):
		# (contestTag, problemTag) and solutionTestClass should be unique.
		contestProblemTag = (contestTag, problemTag)
		if contestProblemTag in self.contestProblemTagSet:
			raise DuplicateTag( contestTag, problemTag )
		if solutionTestClass is not None and solutionTestClass in self.solutionTestClassSet:
			raise DuplicateSolutionClass()

		self.contestProblemTagSet.add( contestProblemTag )
		self.solutionTestClassSet.add( solutionTestClass )

		self.problems.append( (contestTag, problemTag, solutionTestClass) )

	def run( self ):
		for index, (contestTag, problemTag, solutionTestClass) in enumerate( self.problems ):
			solutionState = 'OK' if solutionTestClass is not None else 'SOLUTION NOT IMPLEMENTED'
			print( '{} Problem {} : {} [{}]'.format( contestTag, index + 1, problemTag, solutionState ) )
			if solutionTestClass is not None:
				unittest.main( solutionTestClass(), exit=False )

def test():
	contest = USACO_Contest()

	contest.register( 'USACO 2011 November Contest, Bronze Division', 'Awkward Digits', AwkwardDigitsTest )
	contest.register( 'USACO 2011 November Contest, Bronze Division', 'Moo Sick', MooSickTest )
	contest.register( 'USACO 2011 November Contest, Bronze Division', 'Cow Beauty Pageant', CowBeautyPageantTest )
	contest.register( 'USACO 2011 November Contest, Silver Division', 'Cow Lineup', CowLineupTest )

	contest.register( 'USACO 2011 December Contest, Bronze Division', 'Hay Bales', HayBalesTest )
	#contest.register( 'USACO 2011 December Contest, Bronze Division', 'Cow Photography', None )

	contest.register( 'USACO 2012 January Contest, Bronze Division', 'Haybale Stacking', HaybaleStackingTest )

	contest.register( 'USACO 2012 March Contest, Silver Division', 'Tractor', TractorTest )
	
	contest.register( 'USACO 2012 US Open, Bronze Division', 'Cows in a Row', CowsInARowTest )

	contest.register( 'USACO 2012 November Contest, Bronze', 'Find the Cow!', FindTheCowTest )
	contest.register( 'USACO 2012 November Contest, Bronze', 'Horseshoes', HorseShoesTest )

	contest.register( 'USACO 2012 December Contest, Bronze', 'Meet and Greet', MeetAndGreetTest )
	contest.register( 'USACO 2012 December Contest, Bronze', 'Scrambled Letters', ScrambledLettersTest )

	contest.register( 'USACO 2013 January Contest, Silver', 'Party Invitations', PartyInvitationsTest )
	contest.register( 'USACO 2013 January Contest, Gold', 'Cow Lineup', CowLineupGoldTest )

	contest.register( 'USACO 2013 February Contest, Bronze', 'Message Relay', MessageRelayTest )
	contest.register( 'USACO 2013 February Contest, Bronze', 'Perimeter', PerimeterTest )
	contest.register( 'USACO 2013 February Contest, Silver', 'Perimeter', PerimeterSilverTest )

	contest.register( 'USACO 2013 November Contest, Bronze', 'Combination Lock', CombinationLockTest )
	
	#contest.register( 'USACO 2013 US Open, Silver', "What's Up With Gravity", GravityTest )

	contest.register( 'USACO 2014 March Contest, Bronze', 'Cow Art', CowArtTest )

	contest.register( 'USACO 2014 December Contest, Bronze', 'Marathon', MarathonTest )
	contest.register( 'USACO 2014 December Contest, Bronze', 'Crosswords', CrosswordsTest )
	contest.register( 'USACO 2014 December Contest, Bronze', 'Cow Jog', CowJogTest )
	#contest.register( 'USACO 2014 December Contest, Bronze', 'Learning by Example', None )
	contest.register( 'USACO 2014 December Contest, Silver', 'Piggyback', PiggybackTest )

	contest.register( 'USACO 2015 December Contest, Bronze', 'Fence Painting', FencePaintingTest )
	contest.register( 'USACO 2015 December Contest, Bronze', 'Speeding Ticket', SpeedingTicketTest )
	contest.register( 'USACO 2015 December Contest, Silver', 'Switching on the Lights', LightsTest )
	contest.register( 'USACO 2015 December Contest, Silver', 'Breed Counting', BreedCountingTest )
	contest.register( 'USACO 2015 December Contest, Silver', 'High Card Wins', HighCardWinsTest )
	contest.register( 'USACO 2015 December Contest, Gold', 'Fruit Feast', FruitFeastTest )
	contest.register( 'USACO 2015 December Contest, Gold', "Bessie's Dream", DreamTest )

	contest.register( 'USACO 2016 December Contest, Gold', 'Cow Checklist', CowChecklistTest )

	contest.register( 'USACO 2017 January Contest, Bronze', "Don't Be Last!", LastTest )
	contest.register( 'USACO 2017 January Contest, Bronze', 'Hoof, Paper, Scissors', HoofPaperScissorsTest )
	contest.register( 'USACO 2017 January Contest, Silver', 'Cow Dance Show', CowDanceShowTest )
	contest.register( 'USACO 2017 January Contest, Silver', 'Hoof, Paper, Scissors', HoofPaperScissorsSilverTest )

	contest.register( 'USACO 2017 February Contest, Bronze', 'Why Did the Cow Cross the Road', CrossTheRoadTest )
	contest.register( 'USACO 2017 February Contest, Bronze', 'Why Did the Cow Cross the Road II', CrossTheCircularRoadTest )
	contest.register( 'USACO 2017 February Contest, Bronze', 'Why Did the Cow Cross the Road III', CowWaitTest )
	contest.register( 'USACO 2017 February Contest, Silver', 'Why Did the Cow Cross the Road II', BrokenSignalTest )
	contest.register( 'USACO 2017 February Contest, Gold', 'Why Did the Cow Cross the Road', TimeToCrossTest )

	contest.register( 'USACO 2017 US Open Contest, Bronze', 'The Lost Cow', LostCowTest )
	contest.register( 'USACO 2017 US Open Contest, Bronze', 'Bovine Genomics', BovineGenomicsTest )
	contest.register( 'USACO 2017 US Open Contest, Silver', 'Paired Up', PairedUpTest )

	contest.register( 'USACO 2019 January Contest, Silver', 'Icy Perimeter', IcyPerimeterTest )
	
	contest.register( 'USACO 2020 January Contest, Bronze', 'Word Processor', WordProcessorTest )
	contest.register( 'USACO 2020 January Contest, Bronze', 'Photoshoot', PhotoshootTest )

	contest.register( 'USACO 2021 January Contest, Bronze', 'Uddered but not Herd', UdderedTest )

	contest.run()

if __name__ == '__main__':
	test()