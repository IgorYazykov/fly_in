from .structures import Connection, Drone, Node, ZoneType
from functools import reduce
import pygame


class Schedule_drones():
	def __init__(self, ways: list[tuple[list[Connection], float]], numb_drons: int, start: Node, end: Node) -> None:
		self.all_ways: list[tuple[list[Connection], float]] = ways
		self.numb_drons: int = numb_drons
		self.start: Node = start
		self.end: Node = end
		self.drones: list[Drone] = []
		self.history: list[str] = []
		self.counter_steps: int = 0
		self.number_of_choice: int = 0
		self.curent_elem: int = 0

	def get_price(self, hub: Node) -> int:
		if hub.zone == ZoneType.PRIORITY:
			return 1
		elif hub.zone == ZoneType.RESTRICTED:
			return 2
		else:
			return 1

	def fill_drones(self) -> None:
		for i in range(self.numb_drons):
			self.drones.append(Drone(i,
									 self.start.center_x,
			                         self.start.center_y,
									 False,
									 [self.start]))

	def check_drones(self) -> bool:
		for drone in self.drones:
			if not drone.finished:
				return False
		return True

	def sorting_ways_by_price(self) -> None:
		self.all_ways.sort(key=lambda x: x[1])

	def check_node(self, drone: Drone, node: Node, shift: int) -> bool:
		cur_cup = 0
		for elem in node.schedule:
			if elem[0] == (len(drone.position) + shift):
				cur_cup += 1
		if cur_cup < node.max_drones:
			return True
		return False

	def try_to_take_connection(self, con: Connection, drone: Drone) -> bool:
		if not con.schedule:
			return True
		else:
			cur_cup = 0
			for step, _ in con.schedule:
				if step == (len(drone.position)):
					cur_cup += 1
			if cur_cup == con.max_link_capacity:
				return False
			return True

	def wait_turn(self, drone: Drone) -> None:
		leng_of_way = len(drone.position)
		drone.position.append(drone.position[leng_of_way - 1])
		drone.position[leng_of_way - 1].schedule.append((leng_of_way, drone.id))


	def check_nod_in_ways(self, cur_price: float, cur_con: Connection, drone: Drone) -> int:
		variants = []
		for i in range(len(self.all_ways)):
			if i != self.number_of_choice:
				for con in self.all_ways[i][0]:
					if (con.hub_s == cur_con.hub_s
					    and con.hub_e != cur_con.hub_e
					    and self.try_to_take_connection(con, drone)
						and self.all_ways[i][1] < (cur_price + 3)):
						res = False
						if (con.hub_e.zone == ZoneType.RESTRICTED):
							res = (self.check_node(drone, con.hub_e, 1)	
							       and self.try_to_take_connection(con, drone))
						else:
							res = self.check_node(drone, con.hub_e, 0)

						if res:
							variants.append((self.all_ways[i][1], i))

		if not variants:
			return -1

		variants.sort(key=lambda x: x[0])
		target_conections = self.all_ways[variants[0][1]][0]
		for i in range(len(target_conections)):
			if cur_con.hub_s == target_conections[i].hub_s:
				self.curent_elem = i
				break

		return variants[0][1]

	def take_decision(self,
	                  active_choice: tuple[list[Connection], float],
					  drone: Drone) -> int:
		target = self.check_nod_in_ways(active_choice[1], active_choice[0][self.curent_elem], drone)
		if target == -1:
			self.wait_turn(drone)
			return 0
		self.number_of_choice = target
		return 0

	def try_to_make_step(self,
	                     active_choice: tuple[list[Connection], float],
						 drone: Drone) -> int:

		leng_of_way = len(drone.position)

		if (active_choice[0][self.curent_elem].hub_e.zone != ZoneType.RESTRICTED
		    and self.check_node(drone, active_choice[0][self.curent_elem].hub_e, 0)
			and self.try_to_take_connection(active_choice[0][self.curent_elem], drone)):
				active_choice[0][self.curent_elem].hub_e.schedule.append((leng_of_way, drone.id))
				active_choice[0][self.curent_elem].schedule.append((leng_of_way, drone.id))
				drone.position.append(active_choice[0][self.curent_elem].hub_e)
				return 1
		elif (active_choice[0][self.curent_elem].hub_e.zone == ZoneType.RESTRICTED
		      and self.check_node(drone, active_choice[0][self.curent_elem].hub_e, 1)
			  and self.try_to_take_connection(active_choice[0][self.curent_elem], drone)):
				active_choice[0][self.curent_elem].hub_e.schedule.append((leng_of_way + 1, drone.id))
				active_choice[0][self.curent_elem].schedule.append((leng_of_way, drone.id))
				drone.position.append(active_choice[0][self.curent_elem])
				drone.position.append(active_choice[0][self.curent_elem].hub_e)
				return 1
		else:
			return self.take_decision(active_choice, drone)

	def make_it_same_leng(self) -> None:
		max_leng = 0
		for drone in self.drones:
			len_pos = len(drone.position)
			if max_leng < len_pos:
				max_leng = len_pos

		for drone in self.drones:
			len_pos = len(drone.position)
			if len_pos < max_leng:
				dif = max_leng - len_pos
				for _ in range(dif):
					drone.position.append(drone.position[len_pos - 1])

	def make_schedule(self) -> None:
		self.fill_drones()
		self.sorting_ways_by_price()

		for drone in self.drones:
			self.curent_elem = 0
			self.number_of_choice = 0
			while not drone.finished and len(drone.position) < 100:
				active_choice = self.all_ways[self.number_of_choice]
				self.curent_elem += self.try_to_make_step(active_choice, drone)
				leng_of_way = len(drone.position)
				if (isinstance(drone.position[leng_of_way - 1], Node)):
					if drone.position[(leng_of_way - 1)] == self.end:
						drone.finished = True

		self.make_it_same_leng()

		for i in range(len(self.drones[0].position)):
			for drone in self.drones:
				if isinstance(drone.position[i], Connection):
					print(f"D{drone.id} - {drone.position[i].hub_s.name}-{drone.position[i].hub_e.name}", end=" ")
				else:
					print(f"D{drone.id} - {drone.position[i].name}", end=" ")
			print("\n", end="")
		print("------------------------")
