import unittest
import os
from pathlib import Path

class TreeNode:
	def __init__( self, data ):
		self.data = data
		self.left = self.right = None

class Tree:
	def __init__( self, prototypeElementList ):
		self.root = None
		self._build( prototypeElementList )

	def _build( self, prototypeElementList ):
		for prototypeElement in prototypeElementList:
			if self.root is None:
				self.root = TreeNode( prototypeElement )
				continue
			currentNode = self.root
			while True:
				if prototypeElement < currentNode.data:
					if currentNode.left is None:
						currentNode.left = TreeNode( prototypeElement )
						break
					else:
						currentNode = currentNode.left
				elif prototypeElement > currentNode.data:
					if currentNode.right is None:
						currentNode.right = TreeNode( prototypeElement )
						break
					else:
						currentNode = currentNode.right

	def __repr__( self ):
		preorderRepresentation = list()
		stack = list()
		stack.append( self.root )

		while len( stack ) > 0:
			currentNode = stack.pop()
			if currentNode is None:
				preorderRepresentation.append( '@' )
			else:
				preorderRepresentation.append( '#' )
				stack.append( currentNode.right )
				stack.append( currentNode.left )
		return '_'.join( preorderRepresentation )

class CeilingFunction:
	def __init__( self, prototypeList ):
		self.prototypeList = prototypeList

	def count( self ):
		shapeSet = set()
		for prototype in self.prototypeList:
			shapeSet.add( repr( Tree( prototype ) ) )
		return len( shapeSet )

class CeilingFunctionTest( unittest.TestCase ):
	def test_countTreeShapes( self ):
		testcaseFiles = set()
		for testcaseFile in os.listdir( 'tests/' ):
			testcaseFiles.add( Path( testcaseFile ).stem )

		for testcaseFile in testcaseFiles:
			self._verify( testcaseFile )

	def _verify( self, testcaseFile ):
			prototypeList = list()

			with open( 'tests/{}.in'.format( testcaseFile ) ) as inputFile:
				numberOfPrototypes, layerCount = map( int, inputFile.readline().strip().split() )
				for _ in range( numberOfPrototypes ):
					prototype = list( map( int, inputFile.readline().strip().split() ) )
					assert len( prototype ) == layerCount
					prototypeList.append( prototype )

			assert len( prototypeList ) == numberOfPrototypes

			expectedCount = None
			with open( 'tests/{}.ans'.format( testcaseFile ) ) as solutionFile:
				expectedCount = int( solutionFile.readline().strip() )
			assert expectedCount is not None

			print( 'Testcase file = {} numberOfPrototypes= {} expectedCount = {}'.format( testcaseFile, numberOfPrototypes, expectedCount) )
			self.assertEqual( CeilingFunction( prototypeList ).count(), expectedCount )

if __name__ == '__main__':
	unittest.main()