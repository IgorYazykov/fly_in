from .structures import Node, Connection, ZoneType
from .my_heap import MyHeap
import math


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
		self.all_ways: list[tuple[list[Connection], float]] = []

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

	def mark_node_in_way(self, way: list[tuple[Node, Node]] | None):
		if not way:
			for way in self.all_ways:
				for step_con in way[0]:
					step_con.hub_e.checked = True
					step_con.hub_s.checked = True
		else:
			for step in way:
				step[0].checked = True
				step[1].checked = True

	def a_star_algoritm(self, part_of_way: list[tuple[Node, Node]] | None, start_node: Node | None) -> list[Connection]:
		unvisited_ne = MyHeap()
		not_in_target = True
		way = []
		if start_node == None:
			current_nod = self.start_hub
		else:
			current_nod = start_node
			way = part_of_way
		current_nod.g_score = 0

		while not_in_target:
			all_heighbords = self.get_all_neighbors(current_nod)
			if all_heighbords:
				self.put_neighbors_to_heap(all_heighbords, unvisited_ne, current_nod)
			from_node, current_nod = unvisited_ne.take_target()
			if not current_nod:
				self.mark_node_in_way(way)
				return []	
			way.append((from_node, current_nod))
			if current_nod == self.end_hub:
				not_in_target = False

		return self.reconstruct_pas(way)

	def check_for_new_heighbords(self) -> list[tuple[Node, Node]] | None:
		part_way = []
		self.mark_node_in_way(None)

		for way in self.all_ways:
			for corect_con in way[0]:
				for con in self.connections:
					if (corect_con.hub_s == con.hub_s
					    and con.hub_e.checked != True):
						part_way.append((con.hub_s, con.hub_e))
						return part_way
				part_way.append((corect_con.hub_s, corect_con.hub_e))
		return None

	def calculate_g_score(self) -> list[tuple[Connection, float]]:
		updated_ways = []
		for way in self.all_ways:
			self.clear_scores()
			way[0][0].hub_s.g_score = 0
			for con in way[0]:
				price = self.get_price_of_zones(con.hub_e)
				new_g = con.hub_s.g_score + price
				con.hub_e.g_score = new_g
			final_price = way[0][-1].hub_e.g_score
			updated_ways.append((way[0], final_price))
		
		for way in updated_ways:
			for con in way[0]:
				print(f"{con.hub_s.name} -> {con.hub_e.name}")
			print(f"{way[1]}")
			print("---------------")

		return updated_ways
			
		
	def yen_algoritm(self) -> list[tuple[Connection, float]]:
		find_way = self.a_star_algoritm(None, None)
		if not find_way:
			print("Map hasn`t a solution!")
			return []

		# for con in find_way:
		# 	print(f"{con.hub_s.name} -> {con.hub_e.name} / {con.hub_s.g_score} -> {con.hub_e.g_score}")
		# print("---------------")

		self.all_ways.append((find_way, 0))
		
		for _ in range(10):
			self.clear_scores()
			part_way = self.check_for_new_heighbords()
			if part_way == None:
				break
			posible_pass = self.a_star_algoritm(part_way, part_way[-1][1])
			if not posible_pass:
				continue
			# for con in posible_pass:
			# 	print(f"{con.hub_s.name} -> {con.hub_e.name} / {con.hub_s.g_score} -> {con.hub_e.g_score}")
			# print("---------------")
			self.all_ways.append((posible_pass, 0))

		return self.calculate_g_score()

		# for way in self.all_ways:
		# 	for con in way[0]:
		# 		print(f"{con.hub_s.name} -> {con.hub_e.name} / {con.hub_s.g_score} -> {con.hub_e.g_score}")
		# 	print("---------------")
		# for way in self.all_ways:
		# 	for con in way[0]:
		# 		print(f"{con.hub_s.name} -> {con.hub_e.name}")
		# 	print(f"{way[1]}")
		# 	print("---------------")


