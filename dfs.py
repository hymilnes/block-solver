import numpy as np
import time

class Puzzle:
	"""This represents one of the game's puzzles"""

	def __init__(self, rows, cols, universe):
		self.rows = rows
		self.cols = cols
		self.universe = universe
		self.visited = set()

	def solve(self):
		print "Solving puzzle via cached DFS..."
		start = time.clock()
		board = Board(self, frozenset())
		result = board.dfs()
		if result:
			print result.matrix
			print "Nodes visited: {}".format(len(self.visited))
		else:
			print "No solution found"
		end = time.clock()
		print "Time: {} seconds\n".format(end - start)

class Block:
	"""This represents an abstract block to be placed"""

	def __init__(self, config):
		# Sized-to-fit rectangle representing the block
		self.config = np.array(config)
		# The rectangle's dimensions
		self.rows = self.config.shape[0]
		self.cols = self.config.shape[1]


class Placement:
	"""This represents a block placed in the context of a board"""

	def __init__(self, board, block, row, col):
		self.board = board
		self.block = block
		self.row = row
		self.col = col
		self.matrix = self.compute_matrix()
		self.matrix.flags.writeable = False # for hashing

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __hash__(self):
		# http://stackoverflow.com/a/16592241
		return hash(self.matrix.data)

	def compute_matrix(self):
		"""A 'placed' matrix that can be summed with other placement matrices to give a 'board' matrix"""
		matrix = np.zeros((self.board.puzzle.rows, self.board.puzzle.cols))
		matrix[self.row:self.row+self.block.rows, self.col:self.col+self.block.cols] = self.block.config
		return matrix

class Board:
	"""This represents a board with some pieces on it"""

	def __init__(self, puzzle, placements):
		self.placements = placements
		self.puzzle = puzzle
		self.decomp = [placement.matrix for placement in placements]
		self.matrix = sum(self.decomp) if self.decomp else np.zeros((self.puzzle.rows, self.puzzle.cols))
		self.remaining = self.puzzle.universe - {placement.block for placement in placements}

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __hash__(self):
		"""A board state is uniquely determined by its decomposition set (set of the matrices that sum to the total board)"""
		return hash(self.placements)

	def check_legality(self, placement):
		return np.array_equal(np.maximum(self.matrix, placement.matrix), self.matrix + placement.matrix)

	def is_complete(self):
		return np.all(self.matrix != 0)

	def get_child_boards(self):
		# Enumerate legal moves
		# TODO: Rank by 'goodness'
		# TODO: Have a backtracking 'goodness' as well
		for block in self.remaining:
			for row in xrange(self.puzzle.rows - block.rows + 1):
				for col in xrange(self.puzzle.cols - block.cols + 1):
					placement = Placement(self, block, row, col)
					if self.check_legality(placement):
						board = Board(self.puzzle, self.placements.union({placement}))
						yield board

	def dfs(self):
		"""From a board state, returns a complete child board state if it exists"""

		# TODO: Verify this logic once we do backtracking
		if self in self.puzzle.visited:
			# print "We have visited the following before:"
			# print self.matrix
			return False
		self.puzzle.visited.add(self)
		# print self.matrix

		# Am I a complete board?
		if self.is_complete():
			return self

		# Ask children for complete boards
		for board in self.get_child_boards():
			result = board.dfs()
			# Child had complete board, propagate up
			if result:
				return result

		# No complete boards here
		return False

def main():

	# TODO:
	#
	# Benchmarking by DFS is finicky, because changing the code changes how
	# sets are internally generated and thus the order they're iterated on.
	# 
	# Perhaps use randomly sorted lists at each DFS stage and average?

	# Novice puzzle 27
	puzzle = Puzzle(7, 4, frozenset([
		Block([[0, 1], [1, 1], [1, 1], [0, 1]]),
		Block([[0, 2], [0, 2], [2, 2], [2, 2], [2, 0]]),
		Block([[3, 3, 3, 3], [3, 0, 3, 0], [3, 0, 0, 0]]),
		Block([[4, 4, 4]]),
		Block([[0, 5, 0], [5, 5, 5], [0, 0, 5]])
	]))
	puzzle.solve()
	# Intermediate puzzle 1
	puzzle = Puzzle(6, 5, frozenset([
		Block([[0, 1, 0, 0], [1, 1, 0, 0], [1, 1, 1, 1]]),
		Block([[2, 2, 2, 2], [0, 0, 2, 2], [0, 0, 0, 2]]),
		Block([[3], [3]]),
		Block([[4], [4]]),
		Block([[5, 5, 0], [0, 5, 5], [0, 5, 5]]),
		Block([[6, 0, 0], [6, 6, 6], [6, 0, 0], [6, 0, 0]])
	]))
	puzzle.solve()
	# Master puzzle 2 (this takes ~10 min on my MacBook Pro)
	puzzle = Puzzle(11, 4, frozenset([
		Block([[1, 1, 1], [1, 1, 1]]),
		Block([[0, 2], [0, 2], [2, 2], [0, 2]]),
		Block([[0, 3], [3, 3], [3, 3]]),
		Block([[0, 4, 4], [4, 4, 0], [0, 4, 0]]),
		Block([[5, 0], [5, 5], [5, 5], [5, 5]]),
		Block([[6, 6], [6, 0], [6, 6], [6, 0]]),
		Block([[7, 0], [7, 7], [7, 0]]),
		Block([[8, 8, 0], [0, 8, 8], [0, 0, 8], [0, 0, 8]])
	]))
	puzzle.solve()

if __name__ == "__main__":
	main()