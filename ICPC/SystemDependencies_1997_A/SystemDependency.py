import unittest

class Program:
	def __init__( self, programName ):
		self.programName = programName
		self.dependencyList = list()
		self.parentList = list()

	def addDependency( self, program ):
		assert isinstance( program, Program )
		self.dependencyList.append( program )
		program.parentList.append( self )

class SystemDependency:
	def __init__( self ):
		self.programNameToObjectDict = dict()
		self.installedPrograms = dict()
		self.token = 0
		self.userInstall = set()

	def _getProgram( self, programName ):
		if programName not in self.programNameToObjectDict:
			self.programNameToObjectDict[ programName ] = Program( programName )
		return self.programNameToObjectDict[ programName ]

	def _recursiveInstall( self, programToInstall, messageList ):
		if programToInstall in self.installedPrograms:
			return
		for program in self._getProgram( programToInstall ).dependencyList:
			self._recursiveInstall( program.programName, messageList )
		messageList.append( 'Installing {}'.format( programToInstall ) )
		self.installedPrograms[ programToInstall ] = self.token
		self.token += 1

	def _install( self, programToInstall, messageList ):
		if programToInstall in self.installedPrograms:
			messageList.append( '{} is already installed.'.format( programToInstall ) )
			return
		self.userInstall.add( programToInstall )
		self._recursiveInstall( programToInstall, messageList )

	def _needed( self, programName ):
		program = self.programNameToObjectDict[ programName ]
		for parentProgram in program.parentList:
			parentProgramName = parentProgram.programName
			if parentProgramName in self.installedPrograms:
				return True
		return False

	def _remove( self, programToRemove, messageList ):
		if self._needed( programToRemove ):
			return
		if programToRemove in self.userInstall:
			return
		messageList.append( 'Removing {}'.format( programToRemove ) )
		del self.installedPrograms[ programToRemove ]
		for dependency in self._getProgram( programToRemove ).dependencyList:
			self._remove( dependency.programName, messageList )

	def apply( self, commandList ):
		responseList = list()

		for command, programList in commandList:
			messageList = list()

			if command == 'DEPEND':
				programName, * dependencyList = programList
				program = self._getProgram( programName )
				for dependency in dependencyList:
					program.addDependency( self._getProgram( dependency ) )
			elif command == 'INSTALL':
				assert len( programList ) == 1
				programToInstall, * _ = programList
				self._install( programToInstall, messageList )
			elif command == 'REMOVE':
				assert len( programList ) == 1
				programToRemove, * _ = programList
				if programToRemove not in self.installedPrograms:
					messageList.append( '{} is not installed.'.format( programToRemove ) )
				elif self._needed( programToRemove ):
					messageList.append( '{} is still needed.'.format( programToRemove ) )
				else:
					if programToRemove in self.userInstall:
						self.userInstall.remove( programToRemove )
					self._remove( programToRemove, messageList )
			elif command == 'LIST':
				assert len( programList ) == 0
				installedProgramList = list()
				for installedProgram, token in self.installedPrograms.items():
					installedProgramList.append( (token, installedProgram ) )
				installedProgramList.sort()
				for _, installedProgram in installedProgramList:
					messageList.append (installedProgram )
			responseList.append( (command, programList, messageList) )
		return responseList

class SystemDependencyTest( unittest.TestCase ):
	def _readCommandList( self, datafile ):
		commandList = list()
		with open( 'tests/{}.in'.format( datafile ) ) as inputFile:
			for line in inputFile.readlines():
				line = line.strip()
				command, * programList = line.split()
				if command == 'END':
					break
				commandList.append( (command, programList) )
		return commandList

	def _readResponseList( self, datafile ):
		responseList = list()
		with open( 'tests/{}.ans'.format( datafile ) ) as solutionFile:
			currentTopLevelCommand, programList, currentMessages = None, list(), list()
			for line in solutionFile.readlines():
				line = line.rstrip()
				if line == 'END':
					responseList.append( (currentTopLevelCommand, programList, currentMessages) )
					break
				if len( line ) > 0 and line[ 0 ].isspace():
					currentMessages.append( line.strip() )
				else:
					if currentTopLevelCommand is not None:
						responseList.append( (currentTopLevelCommand, programList, currentMessages) )
					currentTopLevelCommand, * programList = line.split()
					currentMessages = list()
		return responseList

	def test_dependency( self ):
		for datafile in ('sample', 'dependency'):
			commandList = self._readCommandList( datafile )
			expectedResponseList = self._readResponseList( datafile )

			print( 'Testcase file = {}'.format( datafile ) )
			for command in commandList:
				print( command )
			self.assertEqual( SystemDependency().apply( commandList ), expectedResponseList )			

if __name__ == '__main__':
	unittest.main()