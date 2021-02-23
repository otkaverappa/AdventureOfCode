import unittest
import itertools
import copy

class DominoMap:
	def __init__( self, dominoMap ):
		self.dominoMap = dominoMap

	def __repr__( self ):
		return '$'.join( [ '#'.join( map( str, dominoMapRow ) ) for dominoMapRow in self.dominoMap ] )

class DominoEffect:
	def __init__( self ):
		self.dominoSet = dict()
		self._setupDominoSet()

		self.dominoSetReverseMap = dict()
		for pieceId, (i, j) in self.dominoSet.items():
			self.dominoSetReverseMap[ (i, j) ] = self.dominoSetReverseMap[ (j, i) ] = pieceId
		self.rows, self.cols = 7, 8

	def _setupDominoSet( self ):
		pieceId = 1
		maxPipCount = 6
		for i in range( maxPipCount + 1 ):
			for j in range( i, maxPipCount + 1 ):
				self.dominoSet[ pieceId ] = (i, j)
				pieceId += 1

	def _verify( self, pipGrid ):
		assert len( pipGrid ) == self.rows
		for pipGridRow in pipGrid:
			assert len( pipGridRow ) == self.cols

	def assemble( self, pipGrid ):
		self._verify( pipGrid )
		
		solutionList = list()
		partialSolution = [ [ None for _ in range( self.cols ) ] for _ in range( self.rows ) ]
		self._assemble( pipGrid, solutionList, partialSolution, set() )
		return solutionList

	def _assemble( self, pipGrid, solutionList, partialSolution, usedPipSet ):
		if len( usedPipSet ) == len( self.dominoSet ):
			solutionList.append( copy.deepcopy( partialSolution ) )
			return
		A = B = None
		for i, j in itertools.product( range( self.rows ), range( self.cols ) ):
			if partialSolution[ i ][ j ] is None:
				A, B = i, j
				break
		for du, dv in [ (0, 1), (1, 0) ]:
			C, D = A + du, B + dv
			if not 0 <= C < self.rows or not 0 <= D < self.cols or partialSolution[ C ][ D ] is not None:
				continue
			i, j = pipGrid[ A ][ B ], pipGrid[ C ][ D ]
			token = self.dominoSetReverseMap[ (i, j) ]
			if token in usedPipSet:
				continue
			usedPipSet.add( token )
			partialSolution[ A ][ B ] = partialSolution[ C ][ D ] = token
			self._assemble( pipGrid, solutionList, partialSolution, usedPipSet )
			partialSolution[ A ][ B ] = partialSolution[ C ][ D ] = None
			usedPipSet.remove( token ) 

class DominoEffectTest( unittest.TestCase ):
	def _readPipGrid( self, file ):
		pipRows = 7

		pipGrid = list()
		for _ in range( pipRows ):
			line = file.readline().strip()
			if len( line ) == 0:
				raise Exception()
			pipGrid.append( list( map( int, line.split() ) ) )
		return pipGrid

	def _readAllPipGrids( self, fileName ):
		pipGridList = list()

		with open( fileName ) as inputFile:
			while True:
				try:
					pipGridList.append( self._readPipGrid( inputFile ) )
				except Exception:
					break
		return pipGridList

	def _readSolutionFile( self, fileName ):
		pipRows = 7
		allSolutionList = list()

		readLayout, layoutLineCount = False, 0
		currentSolutionList = list()
		currentSolution, currentSolutionLineCount = list(), 0

		with open( fileName ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if len( line ) == 0:
					continue
				if 'Layout' in line:
					assert not readLayout
					readLayout = True
				elif readLayout:
					layoutLineCount += 1
					if layoutLineCount == pipRows:
						readLayout, layoutLineCount = False, 0
				elif 'Maps' in line:
					continue
				elif 'There' in line:
					allSolutionList.append( currentSolutionList )
					currentSolutionList = list()
				else:
					currentSolution.append( list( map( int, line.split() ) ) )
					currentSolutionLineCount += 1
					if currentSolutionLineCount == pipRows:
						currentSolutionList.append( currentSolution )
						currentSolution, currentSolutionLineCount = list(), 0
		return allSolutionList

	def _test( self, pipGridList, allSolutionList ):
		assert len( pipGridList ) == len( allSolutionList )
		for i in range( len( pipGridList ) ):
			pipGrid = pipGridList[ i ]
			expectedSolutionList = allSolutionList[ i ]

			expectedSolutionSet = set()
			for expectedSolution in expectedSolutionList:
				expectedSolutionSet.add( repr( DominoMap( expectedSolution ) ) )
			
			solutionSet = set()
			for solution in DominoEffect().assemble( pipGrid ):
				solutionSet.add( repr( DominoMap( solution ) ) )
			print( 'Testcase = {}  Number of Solutions = {}'.format( i + 1, len( expectedSolutionSet ) ) )
			self.assertEqual( solutionSet, expectedSolutionSet )

	def test_assemble_sample( self ):
		pipGridList = self._readAllPipGrids( 'tests/sample.in' )
		allSolutionList = self._readSolutionFile( 'tests/sample.ans' )
		self._test( pipGridList, allSolutionList )

	def test_assemble( self ):
		pipGridList = self._readAllPipGrids( 'tests/dominoeffect.in' )
		allSolutionList = self._readSolutionFile( 'tests/dominoeffect.ans' )
		self._test( pipGridList, allSolutionList )

if __name__ == '__main__':
	unittest.main()