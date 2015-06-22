import pandas as pd
import numpy as np

# Rectangle, bitmap
# Boards are rectangle

class Point:
    """ Point class represents and manipulates x,y coords. """

    def __init__(self):
        """ Create a new point at the origin """
        self.x = 0
        self.y = 0


class Block:

	config = []
	is_placed = False

	def __init__(self, config):
		self.config = np.array(config)
		self.is_placed = False


class Board:

	# Block positions
	placements = []
	width = 0
	height = 0
	matrix = []

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.matrix = np.zeros((width, height))

	def smart_placer(self, block):
		

	def check_legality(self, placement):
		local_matrix = np.copy(self.matrix)
		local_matrix += placement['matrix']
		# print local_matrix
		legality_matrix = np.logical_or(local_matrix == 0, local_matrix == 1)
		# print legality_matrix
		is_legal = np.all(legality_matrix)
		return is_legal

	def place(self, block, pos_x, pos_y):
		block.is_placed = True
		matrix = np.zeros((self.width, self.height))
		matrix[pos_x:pos_x+block.config.shape[0], pos_y:pos_y+block.config.shape[1]] = block.config
		placement = {'block': block, 'x': pos_x, 'y': pos_y, 'matrix': matrix}
		
		is_legal = self.check_legality(placement)
		if is_legal:
			# print 'legal'
			self.placements.append(placement)
			self.update_board()
		else:
			# print 'illegal'

	# inefficient, don't want to keep summing the board
	def update_board(self):
		self.matrix = np.zeros((self.width, self.height))
		for matrix in [placement['matrix'] for placement in self.placements]:
			self.matrix += matrix

	def print_decomposition(self):
		for i, matrix in enumerate([placement['matrix'] for placement in self.placements]):
			print matrix
			if (i != len(self.placements) - 1):
				print ''
				print '        +'
				print ''
		print ''
		print '======================='
		print ''
		print self.matrix

def init_blocks():
	# Populate our 'blocks' universe
	blocks = [
		Block([[0, 1], [1, 1], [1, 1], [0, 1]]),
		Block([[0, 1], [0, 1], [1, 1], [1, 1], [1, 0]]),
		Block([[1, 1, 1, 1], [1, 0, 1, 0], [1, 0, 0, 0]]),
		Block([[1, 1, 1]]),
		Block([[0, 1, 0], [1, 1, 1], [0, 0, 1]])
	]
	return blocks

def main():
	blocks = init_blocks()
	board = Board(7, 4)
	# board.place(blocks[0], 0, 0)
	# board.place(blocks[0], 0, 0)
	board.place(blocks[0], 1, 2)
	board.place(blocks[1], 1, 0)
	board.place(blocks[2], 0, 0)
	board.place(blocks[3], 6, 0)
	board.place(blocks[4], 4, 1)
	board.print_decomposition()

if __name__ == "__main__":
	main()