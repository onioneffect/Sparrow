class Config:
	def __init__(self, j: dict):
		self.token = j["token"]
		self.rotation = j["rotation"]
		try:
			self.cycle = j["cycle"]
			self.root = j["root"]
			self.global_status = j["global_status"]
		except KeyError:
			pass

