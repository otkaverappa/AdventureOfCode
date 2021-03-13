import unittest

class DecisionTreeNode:
	def __init__( self ):
		self.probability = None
		self.feature = None
		self.leftTree = self.rightTree = None

	def setProbability( self, probability ):
		assert self.probability is None
		self.probability = probability

	def setFeature( self, feature ):
		assert self.feature is None
		self.feature = feature

	def isLeaf( self ):
		return self.leftTree is None and self.rightTree is None

	def setLeftTree( self, leftTree ):
		assert isinstance( leftTree, DecisionTreeNode )
		self.leftTree = leftTree

	def setRightTree( self, rightTree ):
		assert isinstance( rightTree, DecisionTreeNode )
		self.rightTree = rightTree

	def __repr__( self ):
		return '({:.2f})'.format( self.probability ) if self.isLeaf() else \
		       '({:.2f}) ({}) ({})'.format( self.probability, self.leftTree, self.rightTree )

class DecisionTree:
	def __init__( self, treeDescriptionText ):
		self.root = self._buildTree( treeDescriptionText )

	def _maybeSplitToken( self, tokenString ):
		assert len( tokenString ) > 0

		#The tokenString should be in one of the following forms:
		# '(' -> [ '(' ]
		# ')' -> [ ')' ]
		# '(x' -> [ '(', 'x' ]
		# 'x)' -> [ 'x', ')' ]
		# '(x)' -> [ '(', 'x', ')' ]

		if len( tokenString ) == 1:
			return [ tokenString ]
		elif tokenString[ 0 ] == '(' and tokenString[ -1 ] == ')':
			return [ '(', tokenString[ 1 : -1 ], ')' ]
		elif tokenString[ 0 ] == '(':
			return [ '(', tokenString[ 1 : ] ]
		elif tokenString[ -1 ] == ')':
			return [ tokenString[ : -1 ], ')' ]
		else:
			return [ tokenString ]

	def _getTokens( self, treeDescriptionText ):
		allTokens = list()
		for tokenString in ' '.join( treeDescriptionText ).split():
			for token in self._maybeSplitToken( tokenString ):
				allTokens.append( token )
		return allTokens

	def _buildTree( self, treeDescriptionText ):
		stack = list()
		
		for token in self._getTokens( treeDescriptionText ):
			if token == '(':
				stack.append( DecisionTreeNode() )
			elif token == ')':
				currentTreeNode = stack.pop()
				if len( stack ) > 0:
					topOfStackNode = stack[ -1 ]
					if topOfStackNode.leftTree is None:
						topOfStackNode.leftTree = currentTreeNode
					elif topOfStackNode.rightTree is None:
						topOfStackNode.rightTree = currentTreeNode
			else:
				try:
					probability = float( token )
					stack[ -1 ].setProbability( probability )
				except:
					feature = token
					stack[ -1 ].setFeature( feature )
		assert len( stack ) == 0
		return currentTreeNode

	def _query( self, featureList ):
		_probability = 1.0
		featureSet = set( featureList )
		currentTreeNode = self.root

		while True:
			_probability *= currentTreeNode.probability
			if currentTreeNode.isLeaf():
				break
			if currentTreeNode.feature in featureSet:
				currentTreeNode = currentTreeNode.leftTree
			else:
				currentTreeNode = currentTreeNode.rightTree

		return _probability

	def query( self, queryList ):
		queryResultList = list()

		for tag, featureList in queryList:
			queryResultList.append( self._query( featureList ) )

		return queryResultList

class DecisionTreeTest( unittest.TestCase ):
	def test_decide( self ):
		for testcaseFile in ('tree1', 'tree2'):
			self._verify( testcaseFile )

	def _compare( self, queryResult, expectedSolution ):
		assert len( queryResult ) == len( expectedSolution )
		delta = 1e-6
		for i in range( len( queryResult ) ):
			assert abs( queryResult[ i ] - expectedSolution[ i ] ) <= delta

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if 'Case' in line:
					solutionList.append( list() )
				else:
					solutionList[ -1 ].append( float( line ) )

		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			N = int( inputFile.readline().strip() )
			assert N == len( solutionList )

			index = 0
			for _ in range( N ):
				M = int( inputFile.readline().strip() )
				treeDescriptionText = list()
				for _ in range( M ):
					treeDescriptionText.append( inputFile.readline().strip() )
				
				Q = int( inputFile.readline().strip() )
				queryList = list()
				for _ in range( Q ):
					queryString = inputFile.readline().strip()
					tag, _, * featureList = queryString.split()
					queryList.append( (tag, featureList) )

				expectedSolution = solutionList[ index ]
				index += 1

				tree = DecisionTree( treeDescriptionText )
				queryResult = tree.query( queryList )

				print( 'Testcase {}#{} Query list length = {}'.format( testcaseFile, index, Q ) )
				self._compare( queryResult, expectedSolution )

if __name__ == '__main__':
	unittest.main()