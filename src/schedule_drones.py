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

	def try_to_take_connection(self, con: Connection, drone: Drone, shift: int) -> bool:
		if not con.schedule:
			return True
		else:
			cur_cup = 0
			for step, _ in con.schedule:
				if step == (len(drone.position) + shift):
					cur_cup += 1
			return cur_cup < con.max_link_capacity

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
						and self.all_ways[i][1] < (cur_price + 3)):
						res = False
						if (con.hub_e.zone == ZoneType.RESTRICTED):
							res = (self.check_node(drone, con.hub_e, 0)
							       and self.check_node(drone, con.hub_e, 1)
							       and self.try_to_take_connection(con, drone, 0)	
							       and self.try_to_take_connection(con, drone, 1))
						else:
							res = (self.check_node(drone, con.hub_e, 0)
							       and self.try_to_take_connection(con, drone, 0))

						if res:
							variants.append((self.all_ways[i][1], i))

		if not variants:
			return -1
		
		# variants: list[tuple[float, int, int]] = []  # (price, way_idx, elem_idx)

		# for way_idx, (con_list, way_price) in enumerate(self.all_ways):
		# 	if way_idx == self.number_of_choice or way_price >= (cur_price + 3):
		# 		continue

		# 	for elem_idx, con in enumerate(con_list):
		# 		if con.hub_s == cur_con.hub_s and con.hub_e != cur_con.hub_e:
		# 			if con.hub_e.zone == ZoneType.RESTRICTED:
		# 				can_go = (
		# 					self.check_node(drone, con.hub_e, 0)
		# 					and self.check_node(drone, con.hub_e, 1)
		# 					and self.try_to_take_connection(con, drone, 0)
		# 					and self.try_to_take_connection(con, drone, 1)
		# 				)
		# 			else:
		# 				can_go = (
		# 					self.check_node(drone, con.hub_e, 0)
		# 					and self.try_to_take_connection(con, drone, 0)
		# 				)

		# 			if can_go:
		# 				variants.append((way_price, way_idx, elem_idx))
		# 				break

		# if not variants:
		# 	return -1

		# variants.sort(key=lambda x: x[0])
		# _, best_way_idx, best_elem_idx = variants[0]
		# self.curent_elem = best_elem_idx
		# return best_way_idx
		# ----------------------------------
		variants.sort(key=lambda x: x[0])
		target_conections = self.all_ways[variants[0][1]][0]
		for i in range(len(target_conections)):
			if cur_con.hub_s == target_conections[i].hub_s:
				self.curent_elem = i
				break

		if drone.id in {15, 16, 17, 20, 21, 22} and 20 <= len(drone.position) <= 32:
			print(
				f"  [SWITCH] D{drone.id} turn={len(drone.position)} "
				f"from_way={self.number_of_choice} -> to_way={variants[0][1]} "
				f"new_idx={self.curent_elem} at={cur_con.hub_s.name}"
			)

		return variants[0][1]
		# ----------------------------------

	def take_decision(self,
	                  active_choice: tuple[list[Connection], float],
					  drone: Drone) -> int:
		target = self.check_nod_in_ways(active_choice[1], active_choice[0][self.curent_elem], drone)
		if target == -1:
			self.wait_turn(drone)
			return 0
		self.number_of_choice = target
		return 0

	def check_hub_on_next_turn(self, drone: Drone, hub: Node, con: Connection) -> bool:
		return(self.check_node(drone, hub, 0)
		       and self.try_to_take_connection(con, drone, 0))

	def try_to_make_step(self,
	                     active_choice: tuple[list[Connection], float],
						 drone: Drone) -> int:
		# ----------------------------------
		debug_drones = {15, 16, 17, 20, 21, 22}
		leng_of_way = len(drone.position)
		cur_con = active_choice[0][self.curent_elem]

		if drone.id in debug_drones and 20 <= leng_of_way <= 32:
			print(
				f"[STEP] D{drone.id} turn={leng_of_way} way={self.number_of_choice} "
				f"idx={self.curent_elem} edge={cur_con.hub_s.name}->{cur_con.hub_e.name} "
				f"(zone={cur_con.hub_e.zone})"
			)
		# ----------------------------------
		leng_of_way = len(drone.position)

		if (active_choice[0][self.curent_elem].hub_e.zone != ZoneType.RESTRICTED
		    and self.check_hub_on_next_turn(drone,
		                                    active_choice[0][self.curent_elem].hub_e,
											active_choice[0][self.curent_elem])):
				active_choice[0][self.curent_elem].hub_e.schedule.append((leng_of_way, drone.id))
				active_choice[0][self.curent_elem].schedule.append((leng_of_way, drone.id))
				drone.position.append(active_choice[0][self.curent_elem].hub_e)
				return 1
		elif (active_choice[0][self.curent_elem].hub_e.zone == ZoneType.RESTRICTED
		      and self.check_hub_on_next_turn(drone,
		                                      active_choice[0][self.curent_elem].hub_e,
											  active_choice[0][self.curent_elem])
		      and self.check_node(drone, active_choice[0][self.curent_elem].hub_e, 1)
			  and self.try_to_take_connection(active_choice[0][self.curent_elem], drone, 1)):
				active_choice[0][self.curent_elem].hub_e.schedule.append((leng_of_way + 1, drone.id))
				active_choice[0][self.curent_elem].schedule.append((leng_of_way, drone.id))
				drone.position.append(active_choice[0][self.curent_elem])
				drone.position.append(active_choice[0][self.curent_elem].hub_e)
				return 1
		else:
			return self.take_decision(active_choice, drone)

		# leng_of_way = len(drone.position)
		# cur_con = active_choice[0][self.curent_elem]
		# hub_e = cur_con.hub_e

		# if hub_e.zone != ZoneType.RESTRICTED:
		# 	if self.check_hub_on_next_turn(drone, hub_e, cur_con):
		# 		hub_e.schedule.append((leng_of_way, drone.id))
		# 		cur_con.schedule.append((leng_of_way, drone.id))
		# 		drone.position.append(hub_e)
		# 		return 1
		# 	return self.take_decision(active_choice, drone)

		# # Ветка ZoneType.RESTRICTED: 1-й ход на связи (leng_of_way), 2-й ход в узле (leng_of_way + 1)
		# can_enter_restricted = (
		# 	self.check_node(drone, hub_e, 0)
		# 	and self.check_node(drone, hub_e, 1)
		# 	and self.try_to_take_connection(cur_con, drone, 0)
		# 	and self.try_to_take_connection(cur_con, drone, 1)
		# )
		# if can_enter_restricted:
		# 	cur_con.schedule.append((leng_of_way, drone.id))
		# 	hub_e.schedule.append((leng_of_way + 1, drone.id))
		# 	drone.position.append(cur_con)
		# 	drone.position.append(hub_e)
		# 	return 1

		# return self.take_decision(active_choice, drone)

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
	# ----------------------------------
	def validate_schedule(self, check_end_hub: bool = False) -> list[str]:
		errors: list[str] = []
		if not self.drones or not self.drones[0].position:
			return ["Empty drone positions"]

		total_turns = len(self.drones[0].position)
		restricted_names: set[str] = set()
		for ways_list, _ in self.all_ways:
			for con in ways_list:
				if con.hub_e.zone == ZoneType.RESTRICTED:
					restricted_names.add(con.hub_e.name)

		for t in range(total_turns):
			node_occupants: dict[str, list[int]] = {}
			node_limits: dict[str, int] = {}
			conn_occupants: dict[tuple[str, str], list[int]] = {}
			conn_limits: dict[tuple[str, str], int] = {}
			conn_targets: dict[tuple[str, str], str] = {}

			for drone in self.drones:
				if t >= len(drone.position):
					errors.append(f"Turn {t}: Drone {drone.id} has shorter position list")
					continue
				pos = drone.position[t]
				if isinstance(pos, Node):
					node_occupants.setdefault(pos.name, []).append(drone.id)
					node_limits[pos.name] = pos.max_drones
				elif isinstance(pos, Connection):
					key = (pos.hub_s.name, pos.hub_e.name)
					conn_occupants.setdefault(key, []).append(drone.id)
					conn_limits[key] = pos.max_link_capacity
					conn_targets[key] = pos.hub_e.name

			# 1. Проверка max_drones на узлах
			for n_name, d_ids in node_occupants.items():
				if n_name == self.end.name and not check_end_hub:
					continue
				limit = node_limits[n_name]
				if len(d_ids) > limit:
					errors.append(
						f"Turn {t}: Node '{n_name}' overflow: {len(d_ids)}/{limit} "
						f"(drones {d_ids})"
					)

			# 2. Проверка max_link_capacity на связях
			for key, d_ids in conn_occupants.items():
				limit = conn_limits[key]
				if len(d_ids) > limit:
					errors.append(
						f"Turn {t}: Connection '{key[0]}-{key[1]}' overflow: "
						f"{len(d_ids)}/{limit} (drones {d_ids})"
					)

			# 3. Проверка правила RESTRICTED: если в restricted-хабе кто-то есть на тике t,
			# никто другой не должен входить в связь к этому хабу на том же тике t
			for r_name in restricted_names:
				in_r_node = node_occupants.get(r_name, [])
				if in_r_node:
					for key, c_drones in conn_occupants.items():
						if conn_targets.get(key) == r_name:
							other_drones = [d for d in c_drones if d not in in_r_node]
							if other_drones:
								errors.append(
									f"Turn {t}: RESTRICTED '{r_name}' occupied by {in_r_node}, "
									f"while drones {other_drones} are on incoming link "
									f"'{key[0]}-{key[1]}'"
								)

		return errors
	# ----------------------------------
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
		# ----------------------------------
		errors = self.validate_schedule()
		if errors:
			print("VALIDATION ERRORS:")
			for err in errors:
				print("  -", err)
		else:
			print("VALIDATION PASSED: 0 errors")

		for node in self.drones[0].position:
			pass  # если узлов нет в position, возьми их из all_ways
		seen_nodes: dict[str, Node] = {}
		for ways_list, _ in self.all_ways:
			for con in ways_list:
				seen_nodes[con.hub_s.name] = con.hub_s
				seen_nodes[con.hub_e.name] = con.hub_e

		for name in ("micro_gate1", "overflow_hell1"):
			if name in seen_nodes:
				sched = sorted(x for x in seen_nodes[name].schedule if 20 <= x[0] <= 32)
				print(f"[SCHED {name} 20..32]: {sched}")
		# ----------------------------------
		for i in range(len(self.drones[0].position)):
			for drone in self.drones:
				if isinstance(drone.position[i], Connection):
					print(f"D{drone.id}-{drone.position[i].hub_s.name}-{drone.position[i].hub_e.name}", end=" ")
				else:
					print(f"D{drone.id}-{drone.position[i].name}", end=" ")
			print("\n", end="")
		print("------------------------")
