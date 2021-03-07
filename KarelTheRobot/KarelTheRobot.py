import unittest

class Direction:
	NORTH, EAST, SOUTH, WEST = range( 4 )

	@staticmethod
	def turnLeft( currentDirection ):
		return ( currentDirection - 1 ) % 4

	@staticmethod
	def turnRight( currentDirection ):
		return ( currentDirection + 1 ) % 4

	@staticmethod
	def toString( direction ):
		return { Direction.NORTH : 'NORTH', Direction.EAST : 'EAST', Direction.SOUTH : 'SOUTH', Direction.WEST : 'WEST' } [ direction ]

class MapInterface:
	def dimensions( self ):
		pass

	def isBlocked( self, x, y ):
		pass

	def isBeeperPresent( self, x, y ):
		pass

	def pickBeeper( self, x, y ):
		pass

	def putBeeper( self, x, y ):
		pass

	def render( self ):
		pass

class BeeperNotPresentException( Exception ):
	pass

class Grid( MapInterface ):
	def __init__( self, gridCellList, emptyCell='.', blockedCell='#', beeperCellDict=None ):
		self.gridCellList = gridCellList
		self.rows, self.cols = len( gridCellList ), len( gridCellList[ 0 ] )

		self.emptyCell, self.blockedCell = emptyCell, blockedCell
		self.beeperCellDict = dict() if beeperCellDict is None else beeperCellDict

	def _convertToRowAndColumn( self, cell ):
		x, y = cell
		return self.rows - y, x - 1

	def _isOutsideGrid( self, row, col ):
		return row < 0 or row >= self.rows or col < 0 or col >= self.cols

	def dimensions( self ):
		return self.cols, self.rows

	def isBlocked( self, cell ):
		row, col = self._convertToRowAndColumn( cell )
		return self._isOutsideGrid( row, col ) or self.gridCellList[ row ][ col ] == self.blockedCell

	def isBeeperPresent( self, cell ):
		row, col = self._convertToRowAndColumn( cell )
		return self.beeperCellDict.get( (row, col), 0 ) > 0

	def pickBeeper( self, cell ):
		row, col = self._convertToRowAndColumn( cell )
		count = self.beeperCellDict.get( (row, col ), 0 )
		if count == 0:
			raise BeeperNotPresentException()
		self.beeperCellDict[ (row, col) ] = count - 1

	def putBeeper( self, cell ):
		row, col = self._convertToRowAndColumn( cell )
		count = self.beeperCellDict.get( (row, col), 0 )
		self.beeperCellDict[ (row, col) ] = count + 1

	def render( self ):
		for row in range( self.rows ):
			for col in range( self.cols ):
				if self.beeperCellDict.get( (row, col), 0 ) > 0:
					token = '*'
				else:
					token = self.gridCellList[ row ][ col ]
				print( ' {} '.format( token ), end='' )
			print()

	def beeperMap( self ):
		_beeperMap = list()
		for row in range( self.rows ):
			beeperMapRow = list()
			for col in range( self.cols ):
				beeperMapRow.append( self.beeperCellDict.get( (row, col), 0 ) )
			_beeperMap.append( beeperMapRow )
		return _beeperMap

class RectangularEmptyGrid( Grid ):
	def __init__( self, rows, cols, **kwargs ):
		gridCellList = [ '.' * cols for _ in range( rows ) ]
		Grid.__init__( self, gridCellList, **kwargs )

class MoveException( Exception ):
	pass

class KarelTheRobot:
	def __init__( self, mapInterfaceObject, initialPosition=(1, 1), initialOrientation=Direction.EAST, initialBeeperCount=0 ):
		self.position, self.orientation = initialPosition, initialOrientation
		self.movementDict = {
		Direction.NORTH : (0, 1), Direction.EAST : (1, 0), Direction.SOUTH : (0, -1), Direction.WEST : (-1, 0)
		}
		self.beeperCount = initialBeeperCount
		self.mapInterfaceObject = mapInterfaceObject
		self.stats = {
		'move' : 0, 'turn_left' : 0, 'pick_beeper' : 0, 'put_beeper' : 0
		}

	def _cellAtFront( self ):
		x, y = self.position
		dx, dy = self.movementDict[ self.orientation ]
		return x + dx, y + dy

	def _cellAtLeft( self ):
		x, y = self.position
		dx, dy = self.movementDict[ Direction.turnLeft( self.orientation ) ]
		return x + dx, y + dy

	def _cellAtRight( self ):
		x, y = self.position
		dx, dy = self.movementDict[ Direction.turnRight( self.orientation ) ]
		return x + dx, y + dy

	def move( self ):
		self.stats[ 'move' ] += 1
		cell = self._cellAtFront()
		if self.mapInterfaceObject.isBlocked( cell ):
			raise MoveException()
		self.position = cell

	def turn_left( self ):
		self.stats[ 'turn_left' ] += 1
		self.orientation = Direction.turnLeft( self.orientation )

	def pick_beeper( self ):
		self.stats[ 'pick_beeper' ] += 1
		if self.mapInterfaceObject.isBeeperPresent( self.position ):
			self.mapInterfaceObject.pickBeeper( self.position )
			self.beeperCount += 1
			return
		raise BeeperNotPresentException()

	def put_beeper( self ):
		self.stats[ 'put_beeper' ] += 1
		if self.beeperCount > 0:
			self.beeperCount -= 1
			self.mapInterfaceObject.putBeeper( self.position )
			return
		raise BeeperNotPresentException()

	def front_is_clear( self ):
		return not self.front_is_blocked()

	def front_is_blocked( self ):
		return self.mapInterfaceObject.isBlocked( self._cellAtFront() )

	def left_is_clear( self ):
		return not self.left_is_blocked()

	def left_is_blocked( self ):
		return self.mapInterfaceObject.isBlocked( self._cellAtLeft() )

	def right_is_clear( self ):
		return not self.right_is_blocked()

	def right_is_blocked( self ):
		return self.mapInterfaceObject.isBlocked( self._cellAtRight() )

	def beepers_present( self ):
		return self.mapInterfaceObject.isBeeperPresent( self.position )

	def no_beepers_present( self ):
		return not self.beepers_present()

	def beepers_in_bag( self ):
		return self.beeperCount > 0

	def no_beepers_in_bag( self ):
		return self.beeperCount == 0

	def facing_north( self ):
		return self.orientation == Direction.NORTH

	def not_facing_north( self ):
		return not self.facing_north()

	def facing_east( self ):
		return self.orientation == Direction.EAST

	def not_facing_east( self ):
		return not self.facing_east()

	def facing_south( self ):
		return self.orientation == Direction.SOUTH

	def not_facing_south( self ):
		return not self.facing_south()

	def facing_west( self ):
		return self.orientation == Direction.WEST

	def not_facing_west( self ):
		return not self.facing_west()

	def render( self ):
		formatString = 'KarelTheRobot: Position = {} Orientation = {} Beeper Count = {}'
		print( formatString.format( self.position, Direction.toString( self.orientation ), self.beeperCount ) )
		self.mapInterfaceObject.render()

	def beeperMap( self ):
		return self.mapInterfaceObject.beeperMap()

	def displayStatistics( self ):
		print( 'Function invocation summary: {}'.format( self.stats ) )

if __name__ == '__main__':
	unittest.main()