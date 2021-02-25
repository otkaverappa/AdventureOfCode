import unittest

class PageSelection:
	def __init__( self ):
		self.pageNumber = 1
		self.keywordToPageAndIndexDict = dict()
		self.maxKeywordCount = 8
		self.maxResultSetSize = 5

	def page( self, keywordList ):
		weight = self.maxKeywordCount
		for keyword in map( lambda word : word.lower(), keywordList ):
			if keyword not in self.keywordToPageAndIndexDict:
				self.keywordToPageAndIndexDict[ keyword ] = list()
			self.keywordToPageAndIndexDict[ keyword ].append( (self.pageNumber, weight) )
			weight -= 1
		self.pageNumber += 1

	def query( self, queryWordsList ):
		scoreDict = dict()

		weight = self.maxKeywordCount
		for queryWord in map( lambda word : word.lower(), queryWordsList ):
			for (pageNumber, pageWeight) in self.keywordToPageAndIndexDict.get( queryWord, list() ):
				if pageNumber not in scoreDict:
					scoreDict[ pageNumber ] = 0
				scoreDict[ pageNumber ] += pageWeight * weight
			weight -= 1

		reverseScoreDict = dict()
		for pageNumber, score in scoreDict.items():
			if score not in reverseScoreDict:
				reverseScoreDict[ score ] = list()
			reverseScoreDict[ score ].append( pageNumber )

		queryResult = list()
		for score in sorted( reverseScoreDict.keys(), reverse=True ):
			for pageNumber in sorted( reverseScoreDict[ score ] ):
				queryResult.append( 'P{}'.format( pageNumber ) )
				if len( queryResult ) == self.maxResultSetSize:
					return queryResult
		return queryResult

class PageSelectionTest( unittest.TestCase ):
	def test_pageSelection( self ):
		for datafile in ('sample', 'pageselection1', 'pageselection2'):
			self._verify( datafile )

	def _verify( self, datafile ):
		print( 'Testcase datafile = {}'.format( datafile ) )

		expectedResultList = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			header_query, header_pages = solutionFile.readline().strip().split()
			assert header_query == 'Query' and header_pages == 'Pages'
			while True:
				line = solutionFile.readline().strip()
				if len( line ) == 0:
					break
				_, pageString = line.split( ':' )
				expectedResultList.append( pageString.split() )
		
		index = 0
		pageSelection = PageSelection()
		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			while True:
				command, * keywordList = inputFile.readline().strip().split()
				if command == 'P':
					print( 'PageInfo = [{}]'.format( ' '.join( keywordList ) ) )
					pageSelection.page( keywordList )
				elif command == 'Q':
					print( 'Query = [{}] Expected result = {}'.format( ' '.join( keywordList ), expectedResultList[ index ] ) )
					queryResult = pageSelection.query( keywordList )
					self.assertEqual( queryResult, expectedResultList[ index ] )
					index += 1
				elif command == 'E':
					break

if __name__ == '__main__':
	unittest.main()