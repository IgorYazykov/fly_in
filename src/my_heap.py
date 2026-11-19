from .structures import Node


class MyHeap():
	def __init__(self):
		self.elements: list[tuple[float, Node, Node]] = []

	def is_empty(self) -> bool:
		return len(self.elements) == 0

	def already_in(self, hub: Node) -> bool:
		for elem in self.elements:
			if hub == elem[2]:
				return True
		return False

	def add_new(self, node: Node, cur_node: Node, cost: float):
		if not self.already_in(node):
			self.elements.append((cost, cur_node, node))
		else:
			for i in range(len(self.elements)):
				if self.elements[i][2] == node:
					if self.elements[i][0] > cost:
						self.elements[i] = (cost, cur_node, node)

	def take_target(self) -> tuple[Node, Node] | tuple[None, None]:
		if self.is_empty() == True:
			return (None, None)
		
		min_price = self.elements[0][0]
		target_ind = 0

		for i in range(len(self.elements)):
			if min_price > self.elements[i][0]:
				min_price = self.elements[i][0]
				target_ind = i

		_, from_node, node = self.elements.pop(target_ind)
		return (from_node, node)