from pydantic import BaseModel, Field, ConfigDict
from typing import Any
from .structures import Node, Connection, Nodes_holder
from .validator import Validator

# class FileHandeler(BaseModel):
# 	model_config = ConfigDict(validate_assignment=True)
# 	validator: Validator = Field(default_factory=Validator)
# 	target_files: list[Any] = Field(default_factory=list)
# 	files_with_maps: list[Any] = Field(default_factory=list)
# 	names_levels: list[str] = Field(default_factory=list)
# 	list_with_maps: list[Nodes_holder] = Field(default_factory=list)

# 	def text_file_finder(self):
# 		levels = Path('maps_test')
# 		if not levels.is_dir():
# 			raise Exception('Directory "maps" is not exist!')

# 		dirs = [file for file in levels.iterdir() if file.is_dir() == True]
# 		if not dirs:
# 			raise Exception('Map - directory is not have subdirectories!')
# 		levels_name = ['challenger', 'easy', 'hard', 'medium', 'custom']

# 		recived_levels = []
# 		for dir in dirs:
# 			if os.path.basename(dir) in levels_name:
# 				self.names_levels.append(os.path.basename(dir))
# 				recived_levels.append(dir)
# 		if not recived_levels:
# 			raise Exception('Fly-in can not finde levels directories!'
# 			                '\n It can have only next names:'
# 							'\n challenger, easy, hard, medium, custom')

# 		for i in range(len(recived_levels)):
# 			pass_to_files = [file for file in recived_levels[i].iterdir() if file.is_file() and file.suffix == '.txt']
# 			if not pass_to_files:
# 				print(f"'{self.names_levels[i]}' has not '.txt' files!\n")
# 				self.names_levels[i] = None
# 			else:
# 				self.target_files.append(pass_to_files)
# 		self.names_levels = [level for level in self.names_levels if level]
# 		if not self.target_files:
# 			raise Exception('All level directories don`t have ".txt" files!' )

class Parser(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	validator: Validator = Field(default_factory=Validator)
	target_files: list[Any] = Field(default_factory=list)
	files_with_maps: list[Any] = Field(default_factory=list)
	names_levels: list[str] = Field(default_factory=list)
	tmp_map: Nodes_holder = Field(default_factory=Nodes_holder)

	def check_hubs(self, line: str, type_hub: str, sequence_area: bool, file: Any) -> int:
		if sequence_area:
			print(f'Wrong sequence! "{line}" - inside of connection area\nIn the file "{file}"\n')
			return (1)

		new_node = Node()
		parts = line.split(":", maxsplit=1)
		if not parts[1]:
			print(f'Line "{line}" is incorrect!\nIn file "{file}"')
			return (1)
		parts_of_atr = parts[1].strip().split(" ", maxsplit=3)

		if (len(parts_of_atr) > 4 or len(parts_of_atr) < 3 ):
			print(f'Wrong amount of argument in line: "{line}"\nIn the file "{file}"\n')
			return (1)
		if "-" in parts_of_atr[0]:
			print(f'Character "-" detectet in name: "{line}"\nIn the file "{file}"\n')
			return (1)
		if any(parts_of_atr[0]
		       in name for name in [self.tmp_map.start.name,
		                            *(node.name for node in self.tmp_map.nodes),
									self.tmp_map.end.name]):
			print(f'Dyplicate of name - "{parts_of_atr[0]}"\nIn the file "{file}"\n')
			return(1)
		new_node.name = parts_of_atr[0]

		if (self.validator.coord_take(parts_of_atr[1], 'x', new_node, file) == 1
			or self.validator.coord_take(parts_of_atr[2], 'y', new_node, file) == 1):
			return (1)

		if len(parts_of_atr) > 3:
			list_metadata = parts_of_atr[3].strip("[]").split(" ")
			if len(list_metadata) > 3:
				print(f'Incorrect metadata - "{list_metadata}"\nIn the file "{file}"\n')
				return (1)
			if self.validator.metadata_cheker(list_metadata, new_node, type_hub, file) == 1:
				return (1)

		if type_hub == 'start_hub':
			self.tmp_map.start = new_node
		if type_hub == 'hub':
			self.tmp_map.nodes.append(new_node)
		if type_hub == 'end_hub':
			self.tmp_map.end = new_node
		return (0)

	def conection_checker(self, file: Any, line: str) -> int:
		parts = line.split(":", maxsplit=1)
		parts_of_data = parts[1].strip().split(" ")
		if len(parts_of_data) > 2:
			print(f'Incorrect metadata in line: "{line}"\nIn the file "{file}"\n')
			return (1)
		if len(parts_of_data) == 1 and not parts_of_data[0]:
			print(f'Field of conection is empty: "{line}"\nIn the file "{file}"\n')
			return (1)
		if "-" not in parts_of_data[0]:
			print(f'Incorrect connections! The line: "{line}" hasn`t separator "-"\nIn the file "{file}"\n')
			return (1)

		connection = Connection()
		names = parts_of_data[0].split("-")
		if self.validator.check_name_connections(file, self.tmp_map, connection, names) == 1:
			return (1)
		if len(parts_of_data) > 1:
			meta_data = parts_of_data[1].strip("[]").split("=")
			if len(meta_data) != 2:
				print(f'Incorect metadata - "{parts_of_data[1]}"\nIn the file "{file}"\n')
				return (1)
			if self.validator.check_meta_for_con(file, connection, meta_data) == 1:
				return (1)
		self.tmp_map.connections.append(connection)


	def file_checker(self, file: Any) -> int:
		with open(file) as f:
			data = f.read()
			if not data:
				print(f'"{file}" is empty!\n')
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

			if self.validator.check_all_lines(text, file) == 1:
				return (1)

			self.tmp_map = Nodes_holder()
			self.tmp_map.name = str(file.name)
			sequence_area = False
			for i in range(len(text)):
				if i == 0:
					if text[i].startswith('nb_drones:'):
						text_elem = text[i].split(":", maxsplit = 1)
						try:
							self.tmp_map.nb_drones = text_elem[1].strip()
						except Exception:
							print(f'Number of drons must be integer and more then 0!\nIn file "{file}"\n')
							return (1)
					else:
						print(f'"{file}" has not "nb_drones" on first line!\n')
						return (1)
				if text[i].startswith('start_hub:'):
					if self.check_hubs(text[i], 'start_hub', sequence_area, file) == 1:
						return (1)
				if text[i].startswith('end_hub:'):
					if self.check_hubs(text[i], 'end_hub', sequence_area, file) == 1:
						return (1)
				if text[i].startswith('hub:'):
					if self.check_hubs(text[i], 'hub', sequence_area, file) == 1:
						return (1)

				if text[i].startswith('connection:'):
					if not sequence_area:
						sequence_area = True
					if self.conection_checker(file, text[i]) == 1:
						return (1)
		return (0)

	def get_map(self) -> Nodes_holder:
		return self.tmp_map

	# def text_file_handeler(self):
	# 	for files_list in self.target_files:
	# 		for file in files_list:
	# 			if self.file_checker(file) == 1:
	# 				continue
	# 			else:
	# 				self.files_with_maps.append(file)

	# 	if not self.files_with_maps:
	# 		raise Exception('All files are empty or incorrect!')

