import unittest
import itertools

class DirectionCode:
	NorthWest, NorthEast, SouthWest, SouthEast = 1, 2, 3, 4

class ImagePrecompute:
	def __init__( self, imagePixels ):
		rows, cols = len( imagePixels ), len( imagePixels[ 0 ] )
		assert rows > 0 and cols > 0

		precomputeList = [ [ 0 for _ in range( cols ) ] for _ in range( rows ) ]

		for col in range( cols ):
			precomputeList[ 0 ][ col ] = int( imagePixels[ 0 ][ col ] ) + ( 0 if col == 0 else precomputeList[ 0 ][ col - 1 ] )
		for row in range( rows ):
			precomputeList[ row ][ 0 ] = int( imagePixels[ row ][ 0 ] ) + ( 0 if row == 0 else precomputeList[ row - 1 ][ 0 ] )

		for row in range( 1, rows ):
			for col in range( 1, cols ):
				precomputeList[ row ][ col ] = int( imagePixels[ row ][ col ] ) + precomputeList[ row - 1 ][ col ] + \
				                                precomputeList[ row ][ col - 1 ] - precomputeList[ row - 1 ][ col - 1 ]
		self.rows, self.cols = rows, cols
		self.precomputeList = precomputeList

	def _query( self, topLeft, bottomRight ):
		# Includes both topLeft and bottomRight pixels.
		x, y = topLeft
		u, v = bottomRight

		assert 0 <= x < self.rows and 0 <= y < self.cols and 0 <= u < self.rows and 0 <= v < self.cols
		S = self.precomputeList[ u ][ v ]
		A = 0 if x == 0 else self.precomputeList[ x - 1 ][ v ]
		B = 0 if y == 0 else self.precomputeList[ u ][ y - 1 ]
		C = 0 if x == 0 or y == 0 else self.precomputeList[ x - 1 ][ y - 1 ]
		return S - A - B + C

	def isSolidBlock( self, topLeft, bottomRight ):
		x, y = topLeft
		u, v = bottomRight
		numberOfPixels = ( u - x + 1 ) * ( v - y + 1 )
		blackPixelCount = self._query( topLeft, bottomRight )
		if blackPixelCount == 0:
			return True, 'WHITE'
		elif blackPixelCount == numberOfPixels:
			return True, 'BLACK'
		else:
			return False, str()

class SpatialStructureNode:
	def __init__( self ):
		self.nextLevelNodes = [ None for _ in range( 4 + 1 ) ]
		self.leafNode = None
		self.color = None

	def setDefault( self ):
		self.leafNode, self.color = True, 'WHITE'

	def __repr__( self ):
		return 'SpatialStructureNode (leaf, {})'.format( self.color ) if self.leafNode else 'SpatialStructureNode (intermediate)'

class SpatialStructure:
	base = 5

	def __init__( self, root, rows, cols ):
		assert isinstance( root, SpatialStructureNode )
		self.root = root
		self.rows, self.cols = rows, cols

	@staticmethod
	def fromImage( imagePixels ):
		rows, cols = len( imagePixels ), len( imagePixels[ 0 ] )
		topLeft, bottomRight = (0, 0), (rows, cols)

		rows, cols = rows, cols
		imagePrecompute = ImagePrecompute( imagePixels )

		def createSpatialStructureNode( imagePixels, topLeft, bottomRight ):
			x, y = topLeft
			u, v = bottomRight

			isSolidBlock, color = imagePrecompute.isSolidBlock( (x, y), (u - 1, v - 1) )
			spatialStructureNode = SpatialStructureNode()
			if isSolidBlock:
				spatialStructureNode.leafNode = True
				spatialStructureNode.color = color
			else:
				spatialStructureNode.leafNode = False
				m, n = (u - x) // 2, (v - y) // 2
				northWestNode = createSpatialStructureNode( imagePixels, (x, y), (m + x, n + y) )
				northEastNode = createSpatialStructureNode( imagePixels, (x, n + y), (m + x, v) )
				southWestNode = createSpatialStructureNode( imagePixels, (m + x, y), (u, n + y) )
				southEastNode = createSpatialStructureNode( imagePixels, (m + x, n + y), (u, v) )
				spatialStructureNode.nextLevelNodes[ DirectionCode.NorthWest ] = northWestNode
				spatialStructureNode.nextLevelNodes[ DirectionCode.NorthEast ] = northEastNode
				spatialStructureNode.nextLevelNodes[ DirectionCode.SouthWest ] = southWestNode
				spatialStructureNode.nextLevelNodes[ DirectionCode.SouthEast ] = southEastNode
			return spatialStructureNode

		return SpatialStructure( createSpatialStructureNode( imagePixels, topLeft, bottomRight ), rows, cols )

	@staticmethod
	def fromPathList( pathList, rows, cols ):
		def _getPathCodeList( x ):
			pathCodeList = list()
			while x > 0:
				pathCodeList.append( x % 5 )
				x = x // 5
			return pathCodeList

		root = SpatialStructureNode()
		root.setDefault()

		for pathCodeList in map( _getPathCodeList, pathList ):
			currentNode = root
			for branchCode in pathCodeList:
				for code in range( 1, SpatialStructure.base ):
					if currentNode.nextLevelNodes[ code ] is None:
						spatialStructureNode = SpatialStructureNode()
						spatialStructureNode.setDefault()
						currentNode.nextLevelNodes[ code ] = spatialStructureNode
				currentNode.leafNode, currentNode.color = False, None
				currentNode = currentNode.nextLevelNodes[ branchCode ]
			currentNode.leafNode, currentNode.color = True, 'BLACK'
		return SpatialStructure( root, rows, cols )

	def lookup( self, x, y ):
		return self._lookup( x, y, (0, 0), (self.rows, self.cols), self.root )

	def rootToLeafBlackNodePath( self ):
		rootToLeafPathList = list()
		pathCode, branchCode = str(), None
		self._traverse( self.root, rootToLeafPathList, pathCode, branchCode )
		return rootToLeafPathList

	def _lookup( self, x, y, topLeft, bottomRight, spatialStructureNode ):
		assert isinstance( spatialStructureNode, SpatialStructureNode )
		if spatialStructureNode.leafNode:
			return spatialStructureNode.color
		r1, c1 = topLeft
		r2, c2 = bottomRight
		assert r1 <= x < r2 and c1 <= y < c2

		m, n = (r2 - r1) // 2, (c2 - c1) // 2

		_, northWestNode, northEastNode, southWestNode, southEastNode = spatialStructureNode.nextLevelNodes
		if x < r1 + m and y < c1 + n:
			return self._lookup( x, y, (r1, c1), (r1 + m, c1 + n), northWestNode )
		elif x < r1 + m and y >= c1 + n:
			return self._lookup( x, y, (r1, c1 + n), (r1 + m, c2), northEastNode )
		elif x >= r1 + m and y < c1 + n:
			return self._lookup( x, y, (r1 + m, c1), (r2, c1 + n), southWestNode )
		else:
			return self._lookup( x, y, (r1 + m, c1 + n), (r2, c2), southEastNode )

	def _traverse( self, spatialStructureNode, rootToLeafPathList, pathCode, branchCode ):
		assert isinstance( spatialStructureNode, SpatialStructureNode )

		if branchCode is not None:
			pathCode = str( branchCode ) + pathCode
		if spatialStructureNode.leafNode:
			if spatialStructureNode.color == 'BLACK':
				code = 0
				for letter in pathCode:
					code = code * SpatialStructure.base + int( letter )
				rootToLeafPathList.append( code )
			return
		for branchCode in range( 1, SpatialStructure.base ):
			self._traverse( spatialStructureNode.nextLevelNodes[ branchCode ], rootToLeafPathList, pathCode, branchCode )

class PixelColor:
	White, Black = 0, 1

class BlackAndWhiteImage:
	def __init__( self, imagePixels, dotAndStar=False ):
		self.imagePixels = imagePixels
		self.size = len( self.imagePixels )
		self._verify()
		if dotAndStar:
			newImagePixels = list()
			for imagePixelRow in self.imagePixels:
				newImagePixels.append( imagePixelRow.replace( '.', '0' ).replace( '*', '1' ) )
			self.imagePixels = newImagePixels

	def transform( self ):
		spatialStructure = SpatialStructure.fromImage( self.imagePixels )
		return QuadtreeSequence( spatialStructure.rootToLeafBlackNodePath() )

	def _verify( self ):
		N = self.size
		assert N > 0
		assert N & (N - 1) == 0
		for imagePixelsRow in self.imagePixels:
			assert N == len( imagePixelsRow )

	def __repr__( self ):
		return '\n'.join( self.imagePixels )

	def __eq__( self, other ):
		return self.imagePixels == other.imagePixels

class QuadtreeSequence:
	def __init__( self, numberList, size=None ):
		self.numberList = sorted( numberList )
		self.size = size

	def transform( self ):
		rows = cols = self.size
		spatialStructure = SpatialStructure.fromPathList( self.numberList, rows, cols )
		imagePixels = [ [ 0 for _ in range( self.size ) ] for _ in range( self.size ) ]

		for row in range( self.size ):
			for col in range( self.size ):
				if spatialStructure.lookup( row, col ) == 'BLACK':
					imagePixels[ row ][ col ] = 1
		imagePixelStringList = list()
		for imagePixelRow in imagePixels:
			imagePixelStringList.append( ''.join( list( map( str, imagePixelRow ) ) ) )
		return BlackAndWhiteImage( imagePixelStringList )

	def __eq__( self, other ):
		return self.numberList == other.numberList

	def __repr__( self ):
		return str( self.numberList )

class SpatialStructureTest( unittest.TestCase ):
	def test_sample( self ):
		imagePixels = [
		'00000000',
		'00000000',
		'00001111',
		'00001111',
		'00011111',
		'00111111',
		'00111100',
		'00111000'
		]
		quadtreeSequence = BlackAndWhiteImage( imagePixels ).transform()
		blackPixelPathList = [ 9, 14, 17, 22, 23, 44, 63, 69, 88, 94, 113 ]
		self.assertEqual( quadtreeSequence, QuadtreeSequence( blackPixelPathList ) )

		rows, cols = len( imagePixels ), len( imagePixels[ 0 ] )
		spatialStructure = SpatialStructure.fromPathList( blackPixelPathList, rows, cols )
		for i in range( rows ):
			for j in range( cols ):
				color = 'WHITE' if imagePixels[ i ][ j ] == '0' else 'BLACK'
				self.assertEqual( spatialStructure.lookup( i, j ), color )

	def test_spatialStructure( self ):
		solutionList = list()
		with open( 'tests/spatial.ans' ) as solutionFile:
			while True:
				header = solutionFile.readline().strip()
				if len( header ) == 0:
					break
				tag, testcaseNumber = header.split()
				assert tag == 'Image'

				chunkList = list()
				while True:
					line = solutionFile.readline().strip()
					if len( line ) == 0:
						break
					chunkList.append( line )

				if 'Total' in chunkList[ -1 ]:
					footer = chunkList.pop()
					_, blackNodeCount = footer.split( '=' )

					numberList = list()
					for chunkLine in chunkList:
						for element in map( int, chunkLine.split() ):
							numberList.append( element )
					assert len( numberList ) == int( blackNodeCount )
					solutionList.append( QuadtreeSequence( numberList ) )
					representation = 'NUMBER SEQUENCE'
				else:
					imagePixels = chunkList
					solutionList.append( BlackAndWhiteImage( imagePixels, dotAndStar=True ) )
					representation = 'IMAGE PIXELS'
				print( 'Processing testcase = {} Representation = {}'.format( int( testcaseNumber ), representation ) )

		inputList = list()
		with open( 'tests/spatial.in' ) as inputFile:
			while True:
				size = int( inputFile.readline().strip() )
				if size == 0:
					break
				if size < 0:
					numberList = list()
					endOfStream = False
					while not endOfStream:
						chunkList = list( map( int, inputFile.readline().strip().split() ) )
						if chunkList[ -1 ] == -1:
							endOfStream = True
							chunkList.pop()
						for element in chunkList:
							numberList.append( element )
					inputList.append( QuadtreeSequence( numberList, -size ) )
				else:
					imagePixels = list()
					for _ in range( size ):
						imagePixels.append( inputFile.readline().strip() )
					inputList.append( BlackAndWhiteImage( imagePixels ) )

		assert len( inputList ) == len( solutionList )
		for index, imageRepresentation in enumerate( inputList ):
			print( 'Testcase {}'.format( index ) )
			print( imageRepresentation )
			self.assertEqual( imageRepresentation.transform(), solutionList[ index ] )

if __name__ == '__main__':
	unittest.main()