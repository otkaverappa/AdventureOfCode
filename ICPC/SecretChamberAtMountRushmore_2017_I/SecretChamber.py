import unittest
from collections import deque
import os
from pathlib import Path

class SecretChamber:
	def __init__( self, translationList ):
		translationDict = dict()
		for letterPair in translationList:
			fromLetter, toLetter = tuple( letterPair )
			if fromLetter not in translationDict:
				translationDict[ fromLetter ] = list()
			translationDict[ fromLetter ].append( toLetter )
		self.translationDict = translationDict
		self.reachabilityCache = dict()

	def _query( self, sourceLetter, targetLetter ):
		if sourceLetter == targetLetter:
			return True
		cacheKey = sourceLetter
		if cacheKey in self.reachabilityCache:
			return targetLetter in self.reachabilityCache[ cacheKey ]

		visited = set()
		q = deque()
		q.append( sourceLetter )

		reachableLetters = set()
		
		while len( q ) > 0:
			letter = q.popleft()
			if letter in visited:
				continue
			visited.add( letter )
			if letter in self.reachabilityCache:
				reachableLetters = set.union( reachableLetters, self.reachabilityCache[ letter ] )
				continue
			for reachableLetter in self.translationDict.get( letter, str() ):
				reachableLetters.add( reachableLetter )
				if reachableLetter not in visited:
					q.append( reachableLetter )
		self.reachabilityCache[ cacheKey ] = list( reachableLetters )
		return targetLetter in self.reachabilityCache[ cacheKey ]

	def query( self, sourceWord, targetWord ):
		if len( sourceWord ) != len( targetWord ):
			return False
		for i in range( len( sourceWord ) ):
			if not self._query( sourceWord[ i ], targetWord[ i ] ):
				return False
		return True

class SecretChamberTest( unittest.TestCase ):
	def test_secretChamber( self ):
		testcaseFiles = set()
		for testcaseFile in os.listdir( 'tests' ):
			testcaseFiles.add( Path( testcaseFile ).stem )

		for testcaseFile in testcaseFiles:
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		print( 'Processing testcase file: {}'.format( testcaseFile ) )
		expectedResultList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for token in solutionFile.readlines():
				token = token.strip()
				assert token in ('yes', 'no')
				expectedResultList.append( True if token == 'yes' else False )
		
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			translationCount, queryCount = map( int, inputFile.readline().strip().split() )
			translationList = list()
			for _ in range( translationCount ):
				fromLetter, toLetter = inputFile.readline().strip().split()
				translationList.append( fromLetter + toLetter )
			assert len( expectedResultList ) == queryCount

			secretChamber = SecretChamber( translationList )
			for index in range( queryCount ):
				sourceWord, targetWord = inputFile.readline().strip().split()
				expectedResult = expectedResultList[ index ]
				print( '{} -> {} ? [{}]'.format( sourceWord, targetWord, expectedResult ) )
				self.assertEqual( secretChamber.query( sourceWord, targetWord ), expectedResult )

if __name__ == '__main__':
	unittest.main()