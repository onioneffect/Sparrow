class Config:
	def __init__(self, j: dict):
		self.token = j["token"]
		self.cycle = j["cycle"]
		self.root = j["root"]
		self.rotation = j["rotation"]

