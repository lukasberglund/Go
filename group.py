class Group():

	def __init__(self, color, list = []):
		self.list = list
		self.color = color

	def append(self, item):
		self.list.append(item)

	def remove(self, item):
		self.list.remove(item)

	def __add__(self, other_group):
		new_group = Group(self.color, self.list + other_group.list)
