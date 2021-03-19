import unittest

class DLLNode:
	def __init__( self, data='EMPTY' ):
		self.previous = self.next = None
		self.data = data

class Cache:
	CACHE_HIT, CACHE_MISS = 0, 1

	def __init__( self, size ):
		assert size >= 1
		self.size = size

		self.head = DLLNode( data='HEADER' )
		self.tail = DLLNode( data='FOOTER' )

		previousNode = self.head
		for _ in range( size ):
			newDLLNode = DLLNode()
			previousNode.next = newDLLNode
			newDLLNode.previous = previousNode
			self.tail.previous = previousNode = newDLLNode
		self.tail.previous.next = self.tail

		self.keyToDLLNodeDict = dict()
		self.cacheMissCount = 0

		self.nextAvailableNode = self.head.next

	def _populateCache( self, itemList ):
		assert len( itemList ) == self.size
		self.keyToDLLNodeDict.clear()
		dllNode = self.head.next
		for item in itemList:
			dllNode.data = item
			self.keyToDLLNodeDict[ item ] = dllNode
			dllNode = dllNode.next
		self.nextAvailableNode = self.tail

	def stat( self ):
		cacheMissSoFar = self.cacheMissCount
		self.cacheMissCount = 0
		return cacheMissSoFar

	def rangeAccess( self, dataRefRange ):
		for key in dataRefRange[ : self.size ]:
			self.access( key )

		self.cacheMissCount += len( dataRefRange[ self.size : ] )

		if len( dataRefRange ) >= self.size:
			self._populateCache( dataRefRange[ -1 : - ( self.size + 1 ) : -1 ] )

	def access( self, key ):
		def _moveToListHead( dllNode ):
			if dllNode == self.head.next:
				return
			dllNode.previous.next = dllNode.next
			dllNode.next.previous = dllNode.previous
			dllNode.next = self.head.next
			dllNode.previous = self.head
			self.head.next.previous = dllNode
			self.head.next = dllNode

		if key in self.keyToDLLNodeDict:
			dllNode = self.keyToDLLNodeDict[ key ]
			_moveToListHead( dllNode )
			return Cache.CACHE_HIT

		self.cacheMissCount += 1

		# If the cache is full, then evict the least recently used entry.
		if self.nextAvailableNode == self.tail:
			dllNode = self.tail.previous
			keyToDelete = dllNode.data
			assert keyToDelete in self.keyToDLLNodeDict
			del self.keyToDLLNodeDict[ keyToDelete ]

			dllNode.data = key
			self.keyToDLLNodeDict[ key ] = dllNode
		else:
			dllNode = self.nextAvailableNode
			dllNode.data = key
			self.keyToDLLNodeDict[ key ] = dllNode
			self.nextAvailableNode = dllNode.next

		_moveToListHead( dllNode )
		return Cache.CACHE_MISS

class CacheSimulator:
	def __init__( self, numberOfCacheUnits, cacheSizeList ):
		self.numberOfCacheUnits = numberOfCacheUnits
		self.cacheSizeList = cacheSizeList

		self.cache = [ Cache( cacheSize ) for cacheSize in self.cacheSizeList ]

	def _applyAccess( self, dataRef ):
		for cache in self.cache:
			cache.access( dataRef )

	def _applyStat( self ):
		return [ cache.stat() for cache in self.cache ]

	def _applyRangeAccess( self, dataRefRange ):
		for cache in self.cache:
			cache.rangeAccess( dataRefRange )

	def apply( self, commandList ):
		resultList = list()

		for index, commandString in enumerate( commandList ):
			command, * argumentList = commandString.split()
			if command == 'STAT':
				resultList.append( self._applyStat() )
			elif command == 'ADDR':
				dataRef = int( argumentList.pop() )
				self._applyAccess( dataRef )
			elif command == 'RANGE':
				dataRefStart, delta, N = map( int, argumentList )
				self._applyRangeAccess( range( dataRefStart, dataRefStart + delta * N, delta ) )

		return resultList

class CacheSimulatorTest( unittest.TestCase ):
	def test_sample( self ):
		numberOfCacheUnits = 2
		cacheSizeList = [ 4, 8 ]
		commandList = [
		'RANGE 1 1 5',
		'RANGE 2 1 2',
		'ADDR 99',
		'STAT',
		'ADDR 2',
		'RANGE 5 -1 2',
		'STAT',
		'RANGE 0 10000 10',
		'RANGE 0 20000 5',
		'RANGE 0 30000 4',
		'STAT',
		'END'
		]
		expectedOutput = [
		[6, 6], [1, 0], [18, 13]
		]
		
		cacheSimulator = CacheSimulator( numberOfCacheUnits, cacheSizeList )
		self.assertEqual( cacheSimulator.apply( commandList ), expectedOutput )

	def test_cache( self ):
		expectedOutput = list()
		with open( 'tests/cache.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				expectedOutput.append( list( map( int, line.strip().split() ) ) )

		with open( 'tests/cache.in' ) as inputFile:
			numberOfCacheUnits = int( inputFile.readline().strip() )
			cacheSizeList = list( map( int, inputFile.readline().strip().split() ) )
			commandList = list()
			while True:
				command = inputFile.readline().strip()
				if command == 'END':
					break
				commandList.append( command )

			print( 'Number of cache units: {} Number of commands: {}'.format( numberOfCacheUnits, len( commandList ) ) )
			cacheSimulator = CacheSimulator( numberOfCacheUnits, cacheSizeList )
			self.assertEqual( cacheSimulator.apply( commandList ), expectedOutput )

if __name__ == '__main__':
	unittest.main()