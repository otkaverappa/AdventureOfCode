import unittest

class UnionFind:
	def __init__( self ):
		self.numberOfDisjointSets = 0
		self.elementToRepresentativeDict = dict()

	def add( self, element ):
		assert element not in self.elementToRepresentativeDict
		self.elementToRepresentativeDict[ element ] = element
		self.numberOfDisjointSets += 1

	def merge( self, elementA, elementB ):
		assert elementA in self.elementToRepresentativeDict and elementB in self.elementToRepresentativeDict
		_representativeA = self.representative( elementA )
		_representativeB = self.representative( elementB )
		if _representativeA != _representativeB:
			self.elementToRepresentativeDict[ _representativeA ] = _representativeB
			self.numberOfDisjointSets -= 1

	def representative( self, element ):
		assert element in self.elementToRepresentativeDict
		_representative = self.elementToRepresentativeDict[ element ]
		if _representative == element:
			return _representative
		_representative = self.elementToRepresentativeDict[ element ] = self.representative( _representative )
		return _representative

	def getDisjointSets( self ):
		representativeToElementsDict = dict()
		for element in self.elementToRepresentativeDict.keys():
			representative = self.representative( element )
			if representative not in representativeToElementsDict:
				representativeToElementsDict[ representative ] = list()
			representativeToElementsDict[ representative ].append( element )
		return list( representativeToElementsDict.values() )

class CallingCirclesComparator:
	@staticmethod
	def compare( testObject, circleList1, circleList2 ):
		circleSet1 = set()
		circleSet2 = set()

		for circleElementList in circleList1:
			circleSet1.add( '#'.join( sorted( circleElementList ) ) )
		for circleElementList in circleList2:
			circleSet2.add( '#'.join( sorted( circleElementList ) ) )

		testObject.assertEqual( circleSet1, circleSet2 )

class CallingCircles:
	def __init__( self, callLogList ):
		self.callLogDict = dict()
		for caller, callee in callLogList:
			for customer in (caller, callee):
				if customer not in self.callLogDict:
					self.callLogDict[ customer ] = list()
			self.callLogDict[ caller ].append( callee )
		self.uf = UnionFind()
		for caller in self.callLogDict:
			self.uf.add( caller )

	def circles( self ):
		for caller in self.callLogDict.keys():
			self._search( caller, set(), set(), list() )
		return self.uf.getDisjointSets()

	def _search( self, caller, visited, pathTaken, pathTakenStack ):
		if caller in visited:
			return

		if caller in pathTaken:
			index = -1
			while pathTakenStack[ index ] != caller:
				self.uf.merge( caller, pathTakenStack[ index ] )
				index = index - 1
			return

		pathTaken.add( caller )
		pathTakenStack.append( caller )
		for callee in self.callLogDict[ caller ]:
			self._search( callee, visited, pathTaken, pathTakenStack )
		pathTakenStack.pop()
		pathTaken.remove( caller )

		visited.add( caller )

class CallingCirclesTest( unittest.TestCase ):
	def test_callingCircles( self ):
		for datafile in ('example', 'sample', 'callingcircles'):
			self._verify( datafile )

	def _verify( self, datafile ):
		callingCirclesObjectList = list()

		testcaseCount = 0
		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			while True:
				m, n = map( int, inputFile.readline().strip().split() )
				if m == 0 and n == 0:
					break
				testcaseCount += 1
				print( 'datafile = {} testcase = {} CallLog Size = {}'.format( datafile, testcaseCount, n ) )
				callLogList = list()
				for _ in range( n ):
					callLogList.append( tuple( inputFile.readline().strip().split() ) )
				callingCirclesObjectList.append( CallingCircles( callLogList ) )

		index = 0
		currentCallingCircle = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			for line in solutionFile.readlines():
				line = line.strip()
				if 'Calling circles' in line:
					continue
				if len( line ) == 0:
					CallingCirclesComparator.compare( self, currentCallingCircle, callingCirclesObjectList[ index ].circles() )
					index += 1
					currentCallingCircle = list()
				else:
					currentCallingCircle.append( list( map( lambda name : name.strip(), line.split( ',' ) ) ) )
			if len( currentCallingCircle ) > 0:
				CallingCirclesComparator.compare( self, currentCallingCircle, callingCirclesObjectList[ index ].circles() )

if __name__ == '__main__':
	unittest.main()