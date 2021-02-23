import unittest
import string

class SpreadsheetCalculator:
	def __init__( self, rows, cols, cellList ):
		assert rows <= len( string.ascii_uppercase )

		self.cellDict = dict()

		for i in range( rows ):
			for j in range( cols ):
				key = self._getKey( i, j )
				self.cellDict[ key ] = cellList[ i * cols + j ]

		self.cyclicDependencyCells = set()
		self.evaluationCache = dict()
		self.rows, self.cols = rows, cols

	def _getKey( self, row, col ):
		return string.ascii_uppercase[ row ] + str( col )

	def _tryConversionToInteger( self, token ):
		try:
			x = int( token )
			return x
		except:
			pass
		return None

	def _parseExpression( self, token ):
		tokenList = list()
		currentSymbol = str()
		for ch in token:
			if ch in ('+-'):
				tokenList.append( currentSymbol )
				tokenList.append( ch )
				currentSymbol = str()
			else:
				currentSymbol += ch
		assert len( currentSymbol ) > 0
		tokenList.append( currentSymbol )
		return tokenList

	def _evaluate( self, symbol, currentSymbolSet ):
		literal = self._tryConversionToInteger( symbol )
		if literal is not None:
			return literal

		if symbol in self.evaluationCache:
			return self.evaluationCache[ symbol ]
		if symbol in self.cyclicDependencyCells or symbol in currentSymbolSet or symbol not in self.cellDict:
			self.cyclicDependencyCells = set.union( self.cyclicDependencyCells, currentSymbolSet )
			return None
		
		tokenList = self._parseExpression( self.cellDict[ symbol ] )
		accumulator, previousOperation = 0, '+'
		
		currentSymbolSet.add( symbol )
		for token in tokenList:
			if token in '+-':
				previousOperation = token
			else:
				x = self._evaluate( token, currentSymbolSet )
				if x is None:
					accumulator = None
					break
				accumulator = ( accumulator + x ) if previousOperation == '+' else ( accumulator - x )
		currentSymbolSet.remove( symbol )

		if accumulator is not None:
			self.evaluationCache[ symbol ] = accumulator
		return accumulator

	def calculate( self ):
		for key in self.cellDict.keys():
			self._evaluate( key, set() )

		resultList = list()
		if len( self.cyclicDependencyCells ) == 0:
			assert len( self.cellDict ) == len( self.evaluationCache )
			for row in range( self.rows ):
				rowData = list()
				for col in range( self.cols ):
					rowData.append( self.evaluationCache[ self._getKey( row, col ) ] )
				resultList.append( rowData )
		else:
			for key in sorted( self.cyclicDependencyCells ):
				resultList.append( '{}: {}'.format( key, self.cellDict[ key ] ) )
		return resultList

class SpreadsheetCalculatorTest( unittest.TestCase ):
	def test_spreadsheet( self ):
		for testfile in ('sample0', 'sample1', 'spreadsheet'):
			self._verify( testfile )

	def _verify( self, testfile ):
		spreadsheetList = list()

		with open( 'tests/{}.in'.format( testfile ) ) as inputFile:
			while True:
				rows, cols = map( int, inputFile.readline().strip().split() )
				if rows == 0 and cols == 0:
					break
				cellList = list()
				for _ in range( rows * cols ):
					cellList.append( inputFile.readline().strip() )
				spreadsheetList.append( SpreadsheetCalculator( rows, cols, cellList ) )

		index = 0
		currentSolution = list()
		with open( 'tests/{}.ans'.format( testfile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if len( line ) == 0:
					self._process( index + 1, spreadsheetList[ index ], currentSolution )
					currentSolution.clear()
					index += 1
				else:
					marker, * rest = line.split()
					if marker.isalpha():
						currentSolution.append( list( map( int, rest ) ) )
					elif ':' in line:
						currentSolution.append( line )

			if len( currentSolution ) > 0:
				self._process( index + 1, spreadsheetList[ index ], currentSolution )

	def _process( self, testcaseNumber, spreadsheetCalculator, expectedSolution ):
		print( 'Testcase = {} expectedSolution = {}'.format( testcaseNumber, expectedSolution ) )
		self.assertEqual( spreadsheetCalculator.calculate(), expectedSolution )

if __name__ == '__main__':
	unittest.main()