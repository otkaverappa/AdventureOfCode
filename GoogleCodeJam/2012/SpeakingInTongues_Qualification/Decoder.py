import unittest
import string

class Decoder:
	def __init__( self, ioSampleList ):
		self.decoderMap = dict()

		for sourceList, targetList in ioSampleList:
			assert len( sourceList ) == len( targetList )
			for i in range( len( sourceList ) ):
				S, T = sourceList[ i ], targetList[ i ]
				if S.isspace():
					assert S == T
					continue
				if S in self.decoderMap:
					assert self.decoderMap[ S ] == T
					continue
				self.decoderMap[ S ] = T

		expectedCount = len( string.ascii_lowercase )
		assert len( self.decoderMap ) in (expectedCount, expectedCount - 1)

		if len( self.decoderMap ) == expectedCount - 1:
			S = set.difference( set( string.ascii_lowercase ), set( self.decoderMap.keys() ) ).pop()
			T = set.difference( set( string.ascii_lowercase ), set( self.decoderMap.values() ) ).pop()
			self.decoderMap[ S ] = T

	def decode( self, inputString ):
		decodedCharList = list( inputString )
		for i in range( len( inputString ) ):
			if inputString[ i ].isspace():
				continue
			decodedCharList[ i ] = self.decoderMap[ inputString[ i ] ]
		return ''.join( decodedCharList )

class DecoderTest( unittest.TestCase ):
	def test_decode( self ):
		inputStringList = list()
		with open( 'tests/small.in' ) as inputFile:
			T = int( inputFile.readline().strip() )
			for _ in range( T ):
				inputStringList.append( inputFile.readline().strip() )

		solutionList = list()
		with open( 'tests/small.ans' ) as solutionFile:
			for line in solutionFile.readlines():
				solutionList.append( line.strip() )

		assert len( solutionList ) == T

		ioSampleList = list()
		ioSampleList.append( ('y qee', 'a zoo') )
		ioSampleList.append( ('ejp mysljylc kd kxveddknmc re jsicpdrysi', 'our language is impossible to understand') )
		ioSampleList.append( ('rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd', 'there are twenty six factorial possibilities') )
		ioSampleList.append( ('de kr kd eoya kw aej tysr re ujdr lkgc jv', 'so it is okay if you want to just give up') )
		decoder = Decoder( ioSampleList )

		for i in range( T ):
			decodedText = decoder.decode( inputStringList[ i ] )
			print( 'Testcase {} Text: {}'.format( i + 1, decodedText ) )
			self.assertEqual( 'Case #{}: {}'.format( i + 1, decodedText ), solutionList[ i ] )

if __name__ == '__main__':
	unittest.main()