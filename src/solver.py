from .structures import Node, Connection, ZoneType
import math


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

	def add_new(self, node: Node, cur_node: Node,cost: float):
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
		self.all_ways: list[Connection] = []

	def get_all_neighbors(self, current_hub: Node) -> list[Node] | None:
		all_neighbors = []
		for con in self.connections:
			if con.hub_s == current_hub:
				all_neighbors.append(con.hub_e)
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

	def calculation_price(self, price: float, hub: Node) -> float:
		total_price = price + math.sqrt(
					math.pow(self.end_hub.x - hub.x, 2)
					+ math.pow(self.end_hub.y - hub.y, 2))
		return total_price

	def put_neighbors_to_heap(self, list_neigh: list[Node], heap: MyHeap, cur_node: Node):
		for neigh in list_neigh:
			price_zone = self.get_price_of_zones(neigh)
			
			if price_zone == float('inf'):
				continue
 
			new_g = cur_node.g_score + price_zone
			
			if new_g < neigh.g_score:
				neigh.g_score = new_g
				heap.add_new(neigh, cur_node, self.calculation_price(new_g, neigh))

	def reconstruct_pas(self, way: list[tuple[Node, Node]]) -> list[Connection]:
		correct_way = []
		cur_hub = self.end_hub

		while cur_hub != self.start_hub:
			found = False
			for step in way:
				if step[1] == cur_hub:
					for con in self.connections:
						if con.hub_s == step[0] and con.hub_e == cur_hub:
							correct_way.append(con)
							cur_hub = step[0]
							found = True
							break
				if found:
					break
			if not found:
				return []
		correct_way.reverse()
		return correct_way

	def clear_scores(self):
		for hub in self.node_map:
			hub.g_score = float('inf')
		self.start_hub.g_score = 0

	def get_shorter_way(self):
		unvisited_ne = MyHeap()
		not_in_target = True
		current_nod = self.start_hub
		current_nod.g_score = 0
		way = []

		while not_in_target:
			all_heighbords = self.get_all_neighbors(current_nod)
			if all_heighbords:
				self.put_neighbors_to_heap(all_heighbords, unvisited_ne, current_nod)
			from_node, current_nod = unvisited_ne.take_target()
			if not current_nod:
				print("Map hasn`t a solution!")
				break		
			way.append((from_node, current_nod))
			if current_nod == self.end_hub:
				not_in_target = False

		self.reconstruct_pas(way)
		

