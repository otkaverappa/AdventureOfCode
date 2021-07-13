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

####################################################################################################
####################################################################################################
#
# Test Infrastructure - Each test is registered with the corresponding contestTag and problemTag.
#
####################################################################################################
####################################################################################################
class USACO_Contest:
	def __init__( self ):
		self.problems = list()

	def register( self, contestTag, problemTag, solutionTestClass=None ):
		self.problems.append( (contestTag, problemTag, solutionTestClass) )

	def run( self ):
		for index, (contestTag, problemTag, solutionTestClass) in enumerate( self.problems ):
			solutionState = 'OK' if solutionTestClass is not None else 'SOLUTION NOT IMPLEMENTED'
			print( '{} Problem {} : {} [{}]'.format( contestTag, index + 1, problemTag, solutionState ) )
			if solutionTestClass is not None:
				unittest.main( solutionTestClass(), exit=False )

def test():
	contest = USACO_Contest()

	contest.register( 'USACO 2011 December Contest, Bronze Division', 'Hay Bales', HayBalesTest )
	contest.register( 'USACO 2011 December Contest, Bronze Division', 'Cow Photography', None )

	contest.register( 'USACO 2012 US Open, Bronze Division', 'Cows in a Row', CowsInARowTest )
	contest.register( 'USACO 2012 March Contest, Silver Division', 'Tractor', TractorTest )

	contest.register( 'USACO 2012 November Contest, Bronze', 'Find the Cow!', FindTheCowTest )
	contest.register( 'USACO 2012 November Contest, Bronze', 'Horseshoes', HorseShoesTest )

	contest.register( 'USACO 2012 December Contest, Bronze', 'Meet and Greet', MeetAndGreetTest )
	contest.register( 'USACO 2012 December Contest, Bronze', 'Scrambled Letters', ScrambledLettersTest )

	contest.register( 'USACO 2014 December Contest, Silver', 'Piggyback', PiggybackTest )
	contest.register( 'USACO 2014 December Contest, Bronze', 'Marathon', MarathonTest )
	contest.register( 'USACO 2014 December Contest, Bronze', 'Crosswords', CrosswordsTest )
	contest.register( 'USACO 2014 December Contest, Bronze', 'Cow Jog', CowJogTest )
	contest.register( 'USACO 2014 December Contest, Bronze', 'Learning by Example', None )
	
	contest.run()

if __name__ == '__main__':
	test()