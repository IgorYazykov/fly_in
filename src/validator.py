from pydantic import BaseModel
from .structures import Node, Connection, Nodes_holder
from typing import Any

class Validator(BaseModel):
	def coord_take(self, coord: str, coord_type: str, node: Node, file: Any) -> int:
		try:
			setattr(node, coord_type, int(coord))
		except Exception as err:
			print(f'"{err}" in the file "{file}"\n')
			return (1)
		return (0)

	def save_metadata(self, data_part: str, type: str, node: Node, file: Any) -> int:
		try:
			setattr(node,  type, data_part)
		except Exception:
			if type == 'color':
				print(f'Incorect value for color: "{data_part}"\nIn the file "{file}"\n')
			if type == 'zone':
				print(f'Incorect value for zone: "{data_part}"\nIn the file "{file}"\n')
			if type == 'max_drones':
				print(f'Incorect value for max_drones: "{data_part}"\nIn the file "{file}"\n')
			return(1)

	def dub_error_in_meta(self, type_meta: str, file: Any) -> int:
		print(f'Dublicate of "{type_meta}"!\nIn the file "{file}"\n')
		return (1)

	def metadata_cheker(self, list_metadata: list[str], node: Node, type_hub: str, file: Any) -> int:
		color_detected = False
		max_drones_detected = False
		zone_detected = False
		for metadata in list_metadata:
			data_parts = metadata.split("=")
			if len(data_parts) != 2:
				print(f'Incorrect metadata - "{metadata}"\nIn the file "{file}"\n')
				return (1)
			if data_parts[0] == 'color':
				if not color_detected:
					color_detected = True
				else:
					return self.dub_error_in_meta(data_parts[0], file)
				if self.save_metadata(data_parts[1], 'color', node, file) == 1:
					return (1)
			elif data_parts[0] == 'max_drones':
				if not max_drones_detected:
					max_drones_detected = True
				else:
					return self.dub_error_in_meta(data_parts[0], file)
				if self.save_metadata(data_parts[1], 'max_drones', node, file) == 1:
					return (1)
			elif data_parts[0] == 'zone':
				if not zone_detected:
					zone_detected = True
				else:
					return self.dub_error_in_meta(data_parts[0], file)
				if (type_hub == 'start_hub'
					or type_hub == 'end_hub'
					and data_parts[1] == 'blocked'):
					print(f'{type_hub} can`t be with blocked type of zone!\nIn the file "{file}"\n')
					return (1)
				if self.save_metadata(data_parts[1], 'zone', node, file) == 1:
					return (1)
			else:
				print(f'Incorect name of metadata: "{data_parts[0]}"\nIn the file "{file}"\n')
				return (1)
		return (0)
		
	def check_spec_lines(self, text: list[str], file: Any, type_hub: str) -> int:
		nb_of_target_lines = sum(1 for line in text if line.startswith(type_hub))
		if nb_of_target_lines == 0:
			print(f'File "{file}" has not a "{type_hub}" field!\n')
			return (1)
		elif nb_of_target_lines > 1:
			print(f'Dublicate key of key "{type_hub}" in file "{file}"\n')
			return (1)
		return (0)

	def check_all_lines(self, text: list[str], file: Any) -> int:
		list_spec_line = ['nb_drones:', 'start_hub:', 'end_hub:']
		for spec_line in list_spec_line:
			if self.check_spec_lines(text, file, spec_line) == 1:
				return (1)
		if not any('connection:' in line for line in text):
			print(f'File "{file}" has not a connection field!\n')
			return (1)
		return (0)

	def return_target_node(self, name_node: str, tmp_map: Nodes_holder) -> Node:
		recived_node = next((node for node in tmp_map.nodes if node.name == name_node), None)
		if recived_node != None:
			return recived_node
		if name_node == tmp_map.start.name:
			return tmp_map.start
		if name_node == tmp_map.end.name:
			return tmp_map.end	

	def check_name_connections(self, file: Any, tmp_map: Nodes_holder, connection: Connection, names: list[str]) -> int:
		for name in names:
			if (name not in [node.name for node in tmp_map.nodes]
				and (name != tmp_map.start.name
				and name != tmp_map.end.name)):
				print(f'It`s  wrong name "{name}"! It not exist in hubs.\nIn file "{file}"\n')
				return (1)
		if tmp_map.connections:
			for con in tmp_map.connections:
				if ((names[0] == con.hub_s.name
					and names[1] == con.hub_e.name)
					or (names[1] == con.hub_s.name
					and names[0] == con.hub_e.name)):
					print(f'Connection with names"{names}", already exist!\nIn file "{file}"\n')
					return (1)
		connection.hub_s = self.return_target_node(names[0], tmp_map)
		connection.hub_e = self.return_target_node(names[1], tmp_map)
		return (0)

	def check_meta_for_con(self, file: Any, connection: Connection, capacity: list[str]) -> int:
		if capacity[0] != 'max_link_capacity':
			print(f'Wrong name of metadata parametr - "{capacity[0]}"\nIn the file "{file}"\n')
			return (1)
		try:
			connection.max_link_capacity = int(capacity[1])
		except Exception:
			print(f'Wrong value to metadata - "{capacity[0]}={capacity[1]}"\nIn the file "{file}"\n')
			return (1)
		return (0)