import unittest

class MarbleTreeNode:
	def __init__( self ):
		self.marbleCount = 0
		self.childNodeList = list()

	def addMarbles( self, marbleCount ):
		self.marbleCount += marbleCount

	def removeExcessMarbles( self ):
		excessMarbles = self.marbleCount - 1
		self.marbleCount = 1
		return excessMarbles

class MarbleTree:
	def __init__( self, N, nodeInfoList ):
		self.idToTreeNode =  dict()

		possibleRootNodeId = set( range( 1, N + 1 ) )
		for id_, marbleCount, _, * childIdList in nodeInfoList:
			treeNode = self._getTreeNode( id_ )
			treeNode.addMarbles( marbleCount )
			for childId in childIdList:
				treeNode.childNodeList.append( self._getTreeNode( childId ) )
				if childId in possibleRootNodeId:
					possibleRootNodeId.remove( childId )

		assert len( possibleRootNodeId ) == 1
		self.rootNodeId = possibleRootNodeId.pop()

		self.totalMoveCount = 0

	def _getTreeNode( self, id_ ):
		if id_ not in self.idToTreeNode:
			self.idToTreeNode[ id_ ] = MarbleTreeNode()
		return self.idToTreeNode[ id_ ]

	def _process( self, treeNode ):
		assert treeNode is None or isinstance( treeNode, MarbleTreeNode )
		if treeNode is None:
			return
		for childNode in treeNode.childNodeList:
			self._process( childNode )
		moveCount = 0
		for childNode in treeNode.childNodeList:
			count = childNode.removeExcessMarbles()
			moveCount += abs( count )
			treeNode.addMarbles( count )
		self.totalMoveCount += moveCount

	def move( self ):
		rootNode = self._getTreeNode( self.rootNodeId )
		self._process( rootNode )

		assert rootNode.marbleCount == 1

		return self.totalMoveCount

class MarblesOnATreeTest( unittest.TestCase ):
	def test_move( self ):
		for testcaseFile in ('tree1', 'tree2', 'tree3'):
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
		solutionList = list()
		with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( int( line.strip() ) )

		index = 0
		with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
			while True:
				N = int( inputFile.readline().strip() )
				if N == 0:
					break
				nodeInfoList = list()
				for _ in range( N ):
					nodeInfoList.append( map( int, inputFile.readline().strip().split() ) )

				marbleTree = MarbleTree( N, nodeInfoList )
				expectedMoveCount = solutionList[ index ]
				index += 1

				print( 'Testcase {}#{} Expected move count = {}'.format( testcaseFile, index, expectedMoveCount ) )
				self.assertEqual( marbleTree.move(), expectedMoveCount )

if __name__ == '__main__':
	unittest.main()