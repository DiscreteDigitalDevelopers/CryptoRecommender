class Edge:
	def __init__(self, regression_weight = None):
		self.regression_weight = regression_weight

	def __repr__(self):
		return f'{self.regression_weight:.4f}'