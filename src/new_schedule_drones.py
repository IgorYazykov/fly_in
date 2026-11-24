from .structures import Connection, Node, ZoneType

class Schedule_drones():
	def __init__(self,
	             ways: list[tuple[list[Connection], float]],
				 nb_drones: int,
				 start: Node,
				 end: Node) -> None:
		self.all_ways: list[tuple[list[Connection], float]] = ways
		self.nb_drones: int = nb_drones
		self.start: Node = start
		self.end: Node = end
		# count of list it is number of the drone
		self.schedule: list[list[tuple[Node | Connection, int]]] = []

	def sorting_ways_by_price(self) -> None:
		self.all_ways.sort(key=lambda x: x[1])

	def check_type_target_hub(self, target: Node) -> bool:
		return target.zone == ZoneType.RESTRICTED

	def take_cur_con(self, way: list[Connection], cur_node: Node) -> Connection:
		for con in way:
			if cur_node == con.hub_s:
				return con

	def check_next_node_cup(self,
	                        hub: Node,
							step: int,
							shift: int) -> bool:
		if not hub.schedule: 
			return True

		cur_cup = 0
		for item in hub.schedule:
			if item[0] == (step + shift):
				cur_cup += 1
		# if self.check_type_target_hub(hub):
		# 	print(f"on step {step + shift} - cup eqval {cur_cup} and all chedule: {hub.schedule}")

		return cur_cup < hub.max_drones

	def check_conection_cup(self,
	                        con: Connection,
							step: int,
							shift: int) -> bool:
		if not con.schedule:
			return True

		cur_cup = 0
		for item in con.schedule:
			if item[0] == (step + shift):
				cur_cup += 1

		return cur_cup < con.max_link_capacity

	def check_target(self, con: Connection, step: int) -> bool:
		shift = 0

		if not self.check_conection_cup(con, step, shift):
			return False
		if not self.check_next_node_cup(con.hub_e, step, shift):
			return False
		
		if self.check_type_target_hub(con.hub_e):
			shift += 1
			if not self.check_conection_cup(con, step, shift):
				return False
			# print(f"On this step - {step} we decidet to go to the con")
			if not self.check_next_node_cup(con.hub_e, step, shift):
				return False
			# print(f"On this step - {step} we decidet to go")
		
		return True

	def make_note_in_schedule(self,
	                          elem: Node | Connection,
							  step: int,
							  schedule_of_drone: list[tuple[Node | Connection, int]]) -> None:
		item = (elem, step)
		schedule_of_drone.append(item)

	def move_to_target(self,
	                   con: Connection,
					   step: int,
					   drone_id: int,
					   schedule_of_drone: list[tuple[Node | Connection, int]]) -> tuple[Node, int]:
		counter = 0
		con.schedule.append((step + counter, drone_id))
		if self.check_type_target_hub(con.hub_e):
			self.make_note_in_schedule(con, step, schedule_of_drone)
			counter += 1
		self.make_note_in_schedule(con.hub_e, step + counter, schedule_of_drone)
		con.hub_e.schedule.append((step + counter, drone_id))
		counter += 1
		return con.hub_e, counter

	def wait_in_node(self,
	                 node: Node,
					 step: int,
					 drone_id: int,
					 schedule_of_drone: list[tuple[Node | Connection, int]]) -> None:
		if node == self.start:
			return
		item = (step, drone_id)
		node.schedule.append(item)
		self.make_note_in_schedule(node, step, schedule_of_drone)

	def try_change_way(self,
	                   step: int,
	                   cur_price: float,
					   target_con: Connection,
					   posible_ways: list) -> bool:
		for way, price in self.all_ways:
			for con in way:
				if con == target_con:
					continue

				if (con.hub_s == target_con.hub_s
				    and price < (cur_price + 4)
					and self.check_target(con, step)):
					posible_ways.append((way, price))

		if not posible_ways:
			return False
		return True
		
	def take_chipest_way(self,
	                     posible_ways: list[tuple[list[Connection], float]]) -> tuple[list[Connection], float]:
		posible_ways.sort(key=lambda x: x[1])
		return posible_ways[0]
		
	def make_schedule(self) -> None:
		self.sorting_ways_by_price()

		for i in range(self.nb_drones):
			schedule_of_drone = []
			step = 1
			way, price = self.all_ways[0]
			cur_node = self.start

			while step < 100 and cur_node != self.end:
				target_con = self.take_cur_con(way, cur_node)
				if self.check_target(target_con, step):
					# if self.check_type_target_hub(target_con.hub_e):
					# 	print(f"on step {step} - drone {i} start to move ")
					cur_node, counter = self.move_to_target(target_con, step, i, schedule_of_drone)
					step += counter
				else:
					posible_ways = []
					if self.try_change_way(step, price, target_con, posible_ways):
						way, price = self.take_chipest_way(posible_ways)
					else:
						self.wait_in_node(cur_node, step, i, schedule_of_drone)
						step += 1
			self.schedule.append(schedule_of_drone)

			for elem, step in schedule_of_drone:
				if isinstance(elem, Node):
					print(f"cur-node: {elem.name} on step - {step}")
				else:
					print(f"cur-node: {elem.hub_s.name}-{elem.hub_e.name} on step - {step}")
			print("-------------")
				

