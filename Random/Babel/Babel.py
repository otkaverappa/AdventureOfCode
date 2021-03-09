import unittest
import heapq

class Babel:
	def __init__( self, commonWordList, sourceLanguage, targetLanguage ):
		self.sourceLanguage, self.targetLanguage = sourceLanguage, targetLanguage
		self.commonWordGraph = dict()

		for languageA, languageB, word in commonWordList:
			if languageA not in self.commonWordGraph:
				self.commonWordGraph[ languageA ] = list()
			if languageB not in self.commonWordGraph:
				self.commonWordGraph[ languageB ] = list()
			startLetter, * _ = word
			self.commonWordGraph[ languageA ].append( ( languageB, startLetter, len( word ) ) )
			self.commonWordGraph[ languageB ].append( ( languageA, startLetter, len( word ) ) )
 
	def pathLength( self ):
		startLetter = str()

		q = list()
		q.append( (0, self.sourceLanguage, startLetter) )

		pathLengthDict = dict()
		pathLengthDict[ (self.sourceLanguage, startLetter) ] = 0

		while len( q ) > 0:
			currentPathLength, currentLanguage, previousStartLetter = heapq.heappop( q )
			if currentLanguage == self.targetLanguage:
				return currentPathLength

			for language, startLetter, length in self.commonWordGraph.get( currentLanguage, list() ):
				if startLetter == previousStartLetter:
					continue
				newPathLength = currentPathLength + length
				key = (language, startLetter)
				if key not in pathLengthDict or newPathLength < pathLengthDict[ key ]: 
					pathLengthDict[ key ] = newPathLength
					heapq.heappush( q, (newPathLength, language, startLetter) )
		return None

class BabelTest( unittest.TestCase ):
	def test_pathLength( self ):
		solutionList = list()
		with open( 'tests/babel.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( line.strip() )

		index = 0
		with open( 'tests/babel.in' ) as inputFile:
			while True:
				wordPairCount = int( inputFile.readline().strip() )
				if wordPairCount == 0:
					break
				sourceLanguage, targetLanguage = inputFile.readline().strip().split()
				commonWordList = list()
				for _ in range( wordPairCount ):
					commonWordList.append( tuple( inputFile.readline().strip().split() ) )

				formatString = 'Testcase #{} wordPairCount = {} sourceLanguage = {} targetLanguage = {} expectedSolution = {}'
				print( formatString.format( index + 1, wordPairCount, sourceLanguage, targetLanguage, solutionList[ index ] ) )

				babel = Babel( commonWordList, sourceLanguage, targetLanguage )
				expectedSolution = None if solutionList[ index ] == 'impossivel' else int( solutionList[ index ] )
				self.assertEqual( babel.pathLength(), expectedSolution )

				index += 1

if __name__ == '__main__':
	unittest.main()