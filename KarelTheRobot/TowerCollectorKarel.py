from KarelTheRobot import KarelTheRobot, RectangularEmptyGrid
import unittest
import random

class TowerCollectorKarel( KarelTheRobot ):
	def __init__( self, mapInterfaceObject ):
		KarelTheRobot.__init__( self, mapInterfaceObject )

	'''
	For each column, call collect_column_tower to pick up beepers in that column. Then place all beepers in the
	bottom cell of the last column.
	'''
	def collect( self ):
		while self.front_is_clear():
			self.collect_column_tower()
			self.move()
		self.collect_column_tower()

		while self.beepers_in_bag():
			self.put_beeper()

	'''
	A U-turn.
	'''
	def turn_around( self ):
		for _ in range( 2 ):
			self.turn_left()

	'''
	pre-condition: The robot is facing east, and at the bottom cell of any given column.
	
	Pick up beepers in the current column by moving north, turn around, and move all the way down to the bottom cell.
	Turn once so that the robot is facing east.

	post-condition: The robot is facing east, and at the bottom cell of the given column, having picked up all beepers in the
	given column.
	'''
	def collect_column_tower( self ):
		self.turn_left()
		while self.beepers_present():
			self.pick_beeper()
			self.move()
		self.turn_around()
		while self.front_is_clear():
			self.move()
		self.turn_left()

class TowerCollectorKarelTest( unittest.TestCase ):
	def test_towerCollection( self ):
		for i in range( 5 ):
			self.towerCollection( i + 1 )

	def towerCollection( self, testcaseCount ):
		rows, cols = 8, 15
		totalBeepers = 0
		beeperCellDict = dict()
		
		for col in range( cols ):
			# Fill each column with upto (rows - 1) beepers.
			beeperCount = random.randrange( rows )
			totalBeepers += beeperCount

			row = rows - 1
			while beeperCount > 0:
				beeperCellDict[ (row, col) ] = 1
				row = row - 1
				beeperCount = beeperCount - 1

		kwargs = { 'beeperCellDict' : beeperCellDict }
		robot = TowerCollectorKarel( RectangularEmptyGrid( rows, cols, **kwargs ) )
		
		expectedBeeperList = [ [ 0 for _ in range( cols ) ] for _ in range( rows ) ]
		expectedBeeperList[ -1 ][ -1 ] = totalBeepers

		robot.collect()

		print( 'Testcase {} Total beeper count = {}'.format( testcaseCount, totalBeepers ) )
		robot.displayStatistics()
		self.assertEqual( robot.beeperMap(), expectedBeeperList )

if __name__ == '__main__':
	unittest.main()