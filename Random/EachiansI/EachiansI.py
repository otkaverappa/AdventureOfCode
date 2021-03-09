import unittest

class EachiansI:
	def __init__( self, text, queryList ):
		self.text = text
		self.queryList = queryList

	def _addToIndex( self, indexDict, word, position ):
		if word not in indexDict:
			indexDict[ word ] = list()
		indexDict[ word ].append( position )

	def process( self ):
		indexDict = dict()

		i = j = 0

		while j < len( self.text ):
			if self.text[ j ].isspace():
				word = self.text[ i : j ]
				self._addToIndex( indexDict, word, i )
				i = j + 1
			j += 1

		word = self.text[ i : j ]
		self._addToIndex( indexDict, word, i )

		solutionList = list()
		for queryString in self.queryList:
			if queryString in indexDict:
				solutionList.append( indexDict[ queryString ] )
			else:
				solutionList.append( [ -1 ] )
		return solutionList

class EachiansITest( unittest.TestCase ):
	def test_process( self ):
		for testcaseFile in ('sample', 'eachiansI'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			text = inputFile.readline().strip()
			N = int( inputFile.readline().strip() )
			queryList = inputFile.readline().strip().split()
			assert len( queryList ) == N

		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for _ in range( N ):
				solutionList.append( list( map( int, solutionFile.readline().strip().split() ) ) )

		print( 'Testcase {} queryList = {}'.format( testcaseFile, queryList ) )
		self.assertEqual( EachiansI( text, queryList ).process(), solutionList )

if __name__ == '__main__':
	unittest.main()