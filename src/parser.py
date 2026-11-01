from pydantic import BaseModel, Field, ConfigDict
import os
from pathlib import Path
from typing import Any
from enum import StrEnum


class ZoneType(StrEnum):
	NORMAL = "normal"
	BLOCKED = "blocked"
	RESTRICTED = "restricted"
	PRIORITY = "priority"


class ColorType(StrEnum):
	RED = "red"
	GREEN = "green"
	BLUE = "blue"
	YELLOW = "yellow"
	ORANGE = "orange"
	PURPLE = "purple"
	PINK = "pink"
	BLACK = "black"
	WHITE = "white"
	GREY = "grey"
	BROWN = "brown"
	CYAN = "cyan"
	MAGENTA = "magenta"


class Node(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	name: str = Field(default="")
	x: int = Field(default=0)
	y: int = Field(default=0)
	color: ColorType = Field(default="white")
	zone: ZoneType | None = None
	max_drones: int = Field(default=1)
	neigbords: list[str] = Field(default_factory=list)


class Graph(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	name: str = Field(default="")
	nb_drones: int = Field(default=1, gt=0)
	start: Node = Field(default_factory=Node)
	end: Node = Field(default_factory=Node)
	map: list[Node] = Field(default_factory=list)


class FileHandeler(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	target_files: list[Any] = Field(default_factory=list)
	files_with_maps: list[Any] = Field(default_factory=list)
	names_levels: list[str] = Field(default_factory=list)
	list_with_maps: list[Graph] = Field(default_factory=list)

	def text_file_finder(self):
		levels = Path('maps_test')
		if not levels.is_dir():
			raise Exception('Directory "maps" is not exist!')

		dirs = [file for file in levels.iterdir() if file.is_dir() == True]
		if not dirs:
			raise Exception('Map - directory is not have subdirectories!')
		levels_name = ['challenger', 'easy', 'hard', 'medium', 'custom']

		recived_levels = []
		for dir in dirs:
			if os.path.basename(dir) in levels_name:
				self.names_levels.append(os.path.basename(dir))
				recived_levels.append(dir)
		if not recived_levels:
			raise Exception('Fly-in can not finde levels directories!'
			                '\n It can have only next names:'
							'\n challenger, easy, hard, medium, custom')

		for i in range(len(recived_levels)):
			pass_to_files = [file for file in recived_levels[i].iterdir() if file.is_file() and file.suffix == '.txt']
			if not pass_to_files:
				print(f"'{self.names_levels[i]}' has not '.txt' files!")
				self.names_levels[i] = None
			else:
				self.target_files.append(pass_to_files)
		self.names_levels = [level for level in self.names_levels if level]
		if not self.target_files:
			raise Exception('All level directories don`t have ".txt" files!' )

	def coord_take(self, coord: str, coord_type: str, node: Node) -> int:
		try:
			setattr(node, coord_type, int(coord))
		except Exception as err:
			print(err)
			return (1)

	def save_metadata(self, data_part: str, type: str, node: Node) -> int:
		try:
			setattr(node,  type, data_part)
		except Exception:
			if type == 'color':
				print(f'Incorect value for color: "{data_part}"')
			if type == 'zone':
				print(f'Incorect value for zone: "{data_part}"')
			if type == 'max_drones':
				print(f'Incorect value for max_drones: "{data_part}"')
			return(1)

	def metadata_cheker(self, list_metadata: list[str], node: Node) -> int:
		for metadata in list_metadata:
			data_parts = metadata.split("=")
			if len(data_parts) != 2:
				print(f'Incorrect metadata - "{metadata}"')
				return (1)
			if data_parts[0] == 'color':
				if self.save_metadata(data_parts[1], 'color', node) == 1:
					return (1)
			if data_parts[0] == 'max_drones':
				if self.save_metadata(data_parts[1], 'max_drones', node) == 1:
					return (1)
			if data_parts[0] == 'zone':
				if self.save_metadata(data_parts[1], 'zone', node) == 1:
					return (1)
		return (0)

	def check_hubs(self, line: str, type_hub: str, tmp_map: Graph, sequence_area: bool) -> int:
		if sequence_area:
			print(f'Wrong sequence! "{line}" - inside of connection area')
			return (1)

		new_node = Node()
		parts = line.split(":", maxsplit=1)
		if not parts[1]:
			print(f'Line "{line}" is incorrect!')
			return (1)
		parts_of_atr = parts[1].strip().split(" ", maxsplit=3)

		if (len(parts_of_atr) > 4 or len(parts_of_atr) < 3 ):
			print(f'Wrong amount of argument in line: "{line}"')
			return (1)
		if "-" in parts_of_atr[0]:
			print(f'Character "-" detectet in name: "{line}"')
			return (1)
		new_node.name = parts_of_atr[0]

		if (self.coord_take(parts_of_atr[1], 'x', new_node) == 1
			or self.coord_take(parts_of_atr[2], 'y', new_node) == 1):
			return (1)

		if len(parts_of_atr) > 3:
			list_metadata = parts_of_atr[3].strip("[]").split(" ")
			if len(list_metadata) > 3:
				print(f'Incorrect metadata - "{list_metadata}"')
				return (1)
			if self.metadata_cheker(list_metadata, new_node) == 1:
				return (1)

		if type_hub == 'start_hub':
			tmp_map.start = new_node
		if type_hub == 'hub':
			tmp_map.map.append(new_node)
		if type_hub == 'end_hub':
			tmp_map.start = new_node
		return (0)

		
	def check_spec_lines(self, text: list[str], file: Any, type_hub: str) -> int:
		nb_of_target_lines = sum(1 for line in text if line.startswith(type_hub))
		if nb_of_target_lines == 0:
			print(f'File "{file}" has not a "{type_hub}" field!')
			return (1)
		elif nb_of_target_lines > 1:
			print(f'Dublicate key of key "{type_hub}" in file "{file}"')
			return (1)
		return (0)

	def check_all_lines(self, text: list[str], file: Any) -> int:
		list_spec_line = ['nb_drones:', 'start_hub:', 'end_hub:']
		for spec_line in list_spec_line:
			if self.check_spec_lines(text, file, spec_line) == 1:
				return (1)
		if not any('connection:' in line for line in text):
			print(f'File "{file}" has not a connection field!')
			return (1)
		return (0)

	def file_checker(self, file: Any) -> int:
		with open(file) as f:
			data = f.read()
			if not data:
				print(f'"{file}" is empty!')
				return (1)

			text = []
			for line in data.splitlines():
				line_s = line.strip()
				if "#" in line_s:
					if line_s.index("#") == 0:
						continue
					else:
						line_s = line_s.split('#', maxsplit = 1)[0]
				if not line_s:
					continue
				text.append(line_s)

			if self.check_all_lines(text, file) == 1:
				return (1)

			tmp_map = Graph()
			sequence_area = False
			for i in range(len(text)):
				if i == 0:
					if text[i].startswith('nb_drones:'):
						text_elem = text[i].split(":", maxsplit = 1)
						try:
							tmp_map.nb_drones = text_elem[1].strip()
						except Exception:
							print('Number of drons must be integer and more then 0!')
							return (1)
					else:
						print(f'"{file}" has not "nb_drones" on first line!')
						return (1)
				if text[i].startswith('start_hub'):
					if self.check_hubs(text[i], 'start_hub', tmp_map, sequence_area) == 1:
						return (1)
				if text[i].startswith('end_hub'):
					if self.check_hubs(text[i], 'end_hub', tmp_map, sequence_area) == 1:
						return (1)
				if text[i].startswith('hub'):
					if self.check_hubs(text[i], 'hub', tmp_map, sequence_area) == 1:
						return (1)

				if text[i].startswith('connection'):
					if not sequence_area:
						sequence_area = True
					pass
		return (0)

	def text_file_handeler(self):
		for files_list in self.target_files:
			for file in files_list:
				if self.file_checker(file) == 1:
					continue
				else:
					self.files_with_maps.append(file)

		if not self.files_with_maps:
			raise Exception('All files are empty or incorrect!')
		print(self.files_with_maps)

		
				
