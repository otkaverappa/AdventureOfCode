import unittest

class PetriNetPlace:
	def __init__( self, id_, numberOfTokens=0 ):
		assert id_ >= 1 and numberOfTokens >= 0
		self.id_ = id_
		self.numberOfTokens = numberOfTokens

	def hasTokens( self, count ):
		return self.numberOfTokens >= count

	def putToken( self ):
		self.numberOfTokens += 1

	def getToken( self ):
		assert self.numberOfTokens > 0
		self.numberOfTokens -= 1

class PetriNetTransitionDisabled( Exception ):
	pass

class PetriNetTransition:
	def __init__( self, id_, inputPlaceList, outputPlaceList ):
		assert id_ >= 1 and len( inputPlaceList ) >= 1
		for place in inputPlaceList + outputPlaceList:
			assert isinstance( place, PetriNetPlace )

		self.id_ = id_
		self.inputPlaceList = inputPlaceList
		self.outputPlaceList = outputPlaceList
		
		self.tokenRequirementDict = dict()
		for index, inputPlace in enumerate( self.inputPlaceList ):
			id_ = inputPlace.id_
			count, _ = self.tokenRequirementDict.get( id_, (0, 0) )
			self.tokenRequirementDict[ id_ ] = (count + 1, index)

	def isEnabled( self ):
		for (desiredCount, index) in self.tokenRequirementDict.values():
			if not self.inputPlaceList[ index ].hasTokens( desiredCount ):
				return False
		return True

	def fire( self ):
		if not self.isEnabled():
			raise PetriNetTransitionDisabled()
		for inputPlace in self.inputPlaceList:
			inputPlace.getToken()
		for outputPlace in self.outputPlaceList:
			outputPlace.putToken()

class PetriNet:
	def __init__( self, tokenList, transitionDataList ):
		self.petriNetPlaces = dict()
		self.petriNetTransitions = dict()

		self.enabledTransition = None

		for i in range( len( tokenList ) ):
			id_ = i + 1
			self.petriNetPlaces[ id_ ] = PetriNetPlace( id_, tokenList[ i ] )
		for i in range( len( transitionDataList ) ):
			id_ = i + 1
			inputPlaceList = list()
			outputPlaceList = list()
			for item in transitionDataList[ i ]:
				if item == 0:
					break
				elif item < 0:
					inputPlaceList.append( self.petriNetPlaces[ -item ] )
				else:
					outputPlaceList.append( self.petriNetPlaces[ item ] )
			self.petriNetTransitions[ id_ ] = PetriNetTransition( id_, inputPlaceList, outputPlaceList )

	def _populateEnabledTransition( self ):
		for petriNetTransition in self.petriNetTransitions.values():
			if petriNetTransition.isEnabled():
				self.enabledTransition = petriNetTransition.id_
				return
		self.enabledTransition = None

	def simulate( self, tag, numberOfTurns ):
		count = 0
		petriNetDead = False

		while True:
			self._populateEnabledTransition()
			if self.enabledTransition is None:
				petriNetDead = True
				break

			self.petriNetTransitions[ self.enabledTransition ].fire()

			count += 1
			if count == numberOfTurns:
				break

		tokenSummary = 'Places with tokens:'
		for id_ in sorted( self.petriNetPlaces.keys() ):
			tokenCount = self.petriNetPlaces[ id_ ].numberOfTokens
			if tokenCount > 0:
				tokenSummary += ' {} ({})'.format( id_, tokenCount )
		stateString = 'still live' if not petriNetDead else 'dead'
		stateSummary = 'Case {}: {} after {} transitions'.format( tag, stateString, count )
		return [ stateSummary, tokenSummary ]

class PetriNetSimulationTest( unittest.TestCase ):
	def _verify( self, testcaseNumber, petriNetParameters, expectedResult ):
		tokenList, transitionDataList, simulationTurnCount = petriNetParameters

		petriNetState = PetriNet( tokenList, transitionDataList ).simulate( testcaseNumber, simulationTurnCount )

		print( 'Testcase = {} Expected result:'.format( testcaseNumber ) )
		for expectedResultString in expectedResult:
			print( expectedResultString )
		self.assertEqual( petriNetState, expectedResult )

	def test_simulate( self ):
		petriNetParameterList = list()

		with open( 'tests/sample.in' ) as inputFile:
			while True:
				numberOfPlaces = int( inputFile.readline().strip() )
				if numberOfPlaces == 0:
					break
				tokenList = list( map( int, inputFile.readline().strip().split() ) )
				assert len( tokenList ) == numberOfPlaces
				numberOfTransitions = int( inputFile.readline().strip() )
				assert numberOfTransitions > 0
				transitionDataList = list()
				for _ in range( numberOfTransitions ):
					transitionDataList.append( list( map( int, inputFile.readline().strip().split() ) ) )
				simulationTurnCount = int( inputFile.readline().strip() )

				petriNetParameterList.append( (tokenList, transitionDataList, simulationTurnCount) )

		expectedResultList = list()
		with open( 'tests/sample.ans' ) as solutionFile:
			currentSolution = list()
			for line in solutionFile.readlines():
				line = line.strip()
				if len( line ) == 0:
					expectedResultList.append( currentSolution )
					currentSolution = list()
					continue
				currentSolution.append( line )
			if len( currentSolution ) > 0:
				expectedResultList.append( currentSolution )

		assert len( petriNetParameterList ) == len( expectedResultList )
		for i in range( len( petriNetParameterList ) ):
			self._verify( i + 1, petriNetParameterList[ i ], expectedResultList[ i ] )

if __name__ == '__main__':
	unittest.main()