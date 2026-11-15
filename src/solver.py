from .structures import Node, Connection, ZoneType
import math


class MyHeap():
	def __init__(self):
		self.elements: list[tuple[float, Node]] = []

	def is_empty(self) -> bool:
		return len(self.elements) == 0

	def add_new(self, node: Node, cost: float):
		self.elements.append((cost, node))

	def take_target(self) -> tuple[float, Node] | None:
		if self.is_empty() == True:
			return None
		
		min_price = self.elements[0][0]
		target_ind = 0

		for i in range(len(self.elements)):
			if min_price > self.elements[i][0]:
				min_price = self.elements[i][0]
				target_ind = i

		price, node = self.elements.pop(target_ind)

		return (price, node)

	def show(self):
		print(self.elements)


class Solver():
	def __init__(self,
	             node_map: list[Node],
				 all_conections: list[Connection],
				 numb_drons: int,
				 start: Node,
				 end: Node):
		self.node_map: list[Node] = node_map
		self.connections: list[Connection] = all_conections
		self.numb_drons: int = numb_drons
		self.start_hub: Node = start
		self.end_hub: Node = end
		self.ways: list[list[Node]] = []
		self.scheduler: list[list[Node]] = []

	def get_all_neighbors(self, current_hub: Node) -> list[Node] | None:
		all_neighbors = []
		for con in self.connections:
			if con.hub_s == current_hub:
				all_neighbors.append(con.hub_e)
			elif con.hub_e == current_hub:
				all_neighbors.append(con.hub_s)
		if not all_neighbors:
			return None
		return all_neighbors

	def get_price_of_zones(self, hub: Node) -> float:
		if hub.zone == ZoneType.BLOCKED:
			return float('inf')
		elif hub.zone == ZoneType.PRIORITY:
			return 0.5
		elif hub.zone == ZoneType.RESTRICTED:
			return 2.0
		else:
			return 1.0

	def calculation_price(self, pri_price: float, hub: Node) -> float:
		price_zone = self.get_price_of_zones(hub)
		total_price = (price_zone + pri_price) + math.sqrt(
			math.pow(self.end_hub.x - hub.x, 2)
			+ math.pow(self.end_hub.y - hub.y, 2))
		return total_price

	def put_neighbors_to_heap(self, list_neigh: list[Node], heap: MyHeap, cur_price: float):
		for neigh in list_neigh:
			heap.add_new(neigh, self.calculation_price(cur_price, neigh))

	def get_shorter_way(self):
		pass
		

