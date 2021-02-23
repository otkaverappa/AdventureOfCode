import unittest
import itertools

class Othello:
	def __init__( self, initialState, initialMove, commandList ):
		self.board = list()
		self.boardSize = 8
		for row in initialState:
			assert len( row ) == self.boardSize
			self.board.append( list( row ) )
		self.oppositeMove = {
		'W' : 'B', 'B' : 'W'
		}
		self.emptyToken = '-'
		assert initialMove in self.oppositeMove
		self.currentMove = initialMove
		self.commandList = commandList
		self.cacheLegalMoves = None

	def _count( self ):
		white = black = 0
		for i, j in itertools.product( range( self.boardSize ), range( self.boardSize ) ):
			if self.board[ i ][ j ] == 'W':
				white += 1
			elif self.board[ i ][ j ] == 'B':
				black += 1
		return (white, black)

	def play( self ):
		statusList = list()

		for command in self.commandList:
			statusList += self._apply( command )

		return statusList

	def _applyQuit( self ):
		commandStatusList = list()
		for row in self.board:
			commandStatusList.append( ''.join( row ) )
		return commandStatusList

	def _withinBoard( self, u, v ):
		return 0 <= u < self.boardSize and 0 <= v < self.boardSize

	def _applyList( self ):
		noLegalMove = 'No legal move.'
		locationSet = set()
		for i, j in itertools.product( range( self.boardSize ), range( self.boardSize ) ):
			if self.board[ i ][ j ] == self.currentMove:
				locationSet.add( (i, j) )
		legalMoves = set()
		for i, j in locationSet:
			for du, dv in itertools.product( range( -1, 2 ), range( -1, 2 ) ):
				if du == 0 and dv == 0:
					continue
				m, n = i + du, j + dv
				if not self._withinBoard( m, n ) or self.board[ m ][ n ] != self.oppositeMove[ self.currentMove ]:
					continue
				m, n = m + du, n + dv
				while self._withinBoard( m, n ) and self.board[ m ][ n ] == self.oppositeMove[ self.currentMove ]:
					m, n = m + du, n + dv
				if self._withinBoard( m, n ) and self.board[ m ][ n ] == self.emptyToken:
					legalMoves.add( (m, n) )
		self.cacheLegalMoves = legalMoves
		legalMoveList = list()
		for u, v in sorted( legalMoves ):
			legalMoveList.append( '({},{})'.format( u + 1, v + 1 ) )
		moveDescription = noLegalMove if len( legalMoveList ) == 0 else ' '.join( legalMoveList )
		return [ moveDescription ]

	def _applyMove( self, row, col ):
		if self.cacheLegalMoves is None or len( self.cacheLegalMoves ) == 0:
			self._applyList()
			assert self.cacheLegalMoves is not None
			if (row, col) not in self.cacheLegalMoves:
				self.currentMove = self.oppositeMove[ self.currentMove ]
				self._applyList()
				assert (row, col) in self.cacheLegalMoves

		paintLocations = set()
		paintLocations.add( (row, col) )
		for du, dv in itertools.product( range( -1, 2 ), range( -1, 2 ) ):
			if du == 0 and dv == 0:
				continue
			m, n = row, col
			possibleLocations = list()
			while True:
				m, n = m + du, n + dv
				if not self._withinBoard( m, n ) or self.board[ m ][ n ] != self.oppositeMove[ self.currentMove ]:
					break
				possibleLocations.append( (m, n) )
			if self._withinBoard( m, n ) and self.board[ m ][ n ] == self.currentMove:
				for possibleLocation in possibleLocations:
					paintLocations.add( possibleLocation )
		for u, v in paintLocations:
			self.board[ u ][ v ] = self.currentMove

		self.cacheLegalMoves = None
		self.currentMove = self.oppositeMove[ self.currentMove ]
		white, black = self._count()
		return [ 'Black - {:2d} White - {:2d}'.format( black, white ) ]

	def _apply( self, command ):
		if command == 'Q':
			return self._applyQuit()
		elif command == 'L':
			return self._applyList()
		else:
			moveCommand, row, col = tuple( command )
			assert moveCommand == 'M'
			row, col = int( row ) - 1, int( col ) - 1
			assert 0 <= row < self.boardSize and 0 <= col < self.boardSize
			return self._applyMove( row, col )

class OthelloTest( unittest.TestCase ):
	def test_game( self ):
		for datafile in ('example', 'sample'):
			self._verify( datafile )

	def _verify( self, datafile ):
		gameList = list()
		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			testcaseCount = int( inputFile.readline().strip() )
			for _ in range( testcaseCount ):
				initialState = list()
				for _ in range( 8 ):
					initialState.append( inputFile.readline().strip() )
				initialMove = inputFile.readline().strip()
				commandList = list()
				while True:
					command = inputFile.readline().strip()
					commandList.append( command )
					if command == 'Q':
						break
				gameList.append( Othello( initialState, initialMove, commandList ) )

		gameStatusList = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			currentStatusList = list()
			for line in solutionFile.readlines():
				line = line.strip()
				if len( line ) == 0:
					gameStatusList.append( currentStatusList )
					currentStatusList = list()
				else:
					currentStatusList.append( line )
			if len( currentStatusList ) > 0:
				gameStatusList.append( currentStatusList )

		assert len( gameList ) == len( gameStatusList )
		for i in range( len( gameList ) ):
			print( 'Testcase {}'.format( i + 1 ) )
			for expectedStatus in gameStatusList[ i ]:
				print( expectedStatus )

			statusList = gameList[ i ].play()
			self.assertEqual( statusList, gameStatusList[ i ] )
			print( 'Successfully verified Testcase {}'.format( i + 1 ) )

if __name__ == '__main__':
	unittest.main()