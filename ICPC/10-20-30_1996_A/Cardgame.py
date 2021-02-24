import unittest
from collections import deque

class Cardgame:
	WIN, LOSS, DRAW = 'Win', 'Loss', 'Draw'

	def __init__( self, deckState ):
		self.cardDeck = deque( deckState )
		self.numberOfTurns = 0

		totalSlots = 7
		self.cardSlots = list()
		for _ in range( totalSlots ):
			self.cardSlots.append( [ self._getCardFromDeck() ] )
		
		self.currentCardSlot = 0
		self.stateCache = set()
		self.gameResult = None

	def _encodeCurrentGameState( self ):
		deckState = '#'.join( [ str( card ) for card in self.cardDeck ] )
		slotStateList = list()
		for slot in self.cardSlots:
			slotStateList.append( '#'.join( [ str( card ) for card in slot ] ) )
		slotState = '~'.join( slotStateList )
		return (deckState, slotState)

	def _moveToNextCardSlot( self ):
		if len( self.cardSlots[ self.currentCardSlot ] ) == 0:
			del self.cardSlots[ self.currentCardSlot ]
		else:
			self.currentCardSlot += 1
		if self.currentCardSlot == len( self.cardSlots ):
			self.currentCardSlot = 0

	def _getCardFromDeck( self ):
		self.numberOfTurns += 1
		return self.cardDeck.popleft()

	def _placeCardInTheDeck( self, C1, C2, C3 ):
		self.cardDeck.append( C1 )
		self.cardDeck.append( C2 )
		self.cardDeck.append( C3 )

	def _simulateOneTurn( self ):
		currentSlot = self.cardSlots[ self.currentCardSlot ]
		drawCard = self._getCardFromDeck()
		currentSlot.append( drawCard )

		while True:
			if len( currentSlot ) < 3:
				break
			sumFound = False
			for i, j, k, s, e in [ (0, 1, -1, 2, -1), (0, -2, -1, 1, -2), (-3, -2, -1, 0, -3) ]:
				C1, C2, C3 = currentSlot[ i ], currentSlot[ j ], currentSlot[ k ]
				if C1 + C2 + C3 in (10, 20, 30):
					self.cardSlots[ self.currentCardSlot ] = currentSlot = currentSlot[ s : e ]
					self._placeCardInTheDeck( C1, C2, C3 )
					sumFound = True
					break
			if not sumFound:
				break
		self._moveToNextCardSlot()

		gameState = self._encodeCurrentGameState()

		if len( self.cardSlots ) == 0:
			self.gameResult = Cardgame.WIN
		elif len( self.cardDeck ) == 0:
			self.gameResult = Cardgame.LOSS
		elif gameState in self.stateCache:
			self.gameResult = Cardgame.DRAW
		else:
			self.stateCache.add( gameState )

	def play( self ):
		while self.gameResult is None:
			self._simulateOneTurn()
		return self.gameResult, self.numberOfTurns

class CardgameTest( unittest.TestCase ):
	def test_play( self ):
		for filename in ('sample', 'cardgame'):
			self._verify( filename )

	def _verify( self, filename ):
		print( 'Testcase file = {}'.format( filename ) )
		deckStateList = list()
		deckSize, emptyDeckSize = 52, 1 
		with open( 'tests/{}.in'.format( filename ) ) as inputFile:
			while True:
				deckState = list( map( int, inputFile.readline().strip().split() ) )
				if len( deckState ) == emptyDeckSize:
					break
				assert len( deckState ) == deckSize
				deckStateList.append( deckState )

		resultList = list()
		with open( 'tests/{}.ans'.format( filename ) ) as solutionFile:
			for state in solutionFile.readlines():
				result, numberOfTurns = [ token.strip() for token in state.split( ':' ) ]
				resultList.append( (result, int( numberOfTurns ) ) )

		self.assertEqual( len( deckStateList ), len( resultList ) )
		for i in range( len( deckStateList ) ):
			result, numberOfTurns = resultList[ i ]
			print( 'Testcase = {} Expected result = {}:{}'.format( i + 1, result, numberOfTurns ) )
			self.assertEqual( Cardgame( deckStateList[ i ] ).play(), resultList[ i ] )

if __name__ == '__main__':
	unittest.main()