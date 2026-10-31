from pydantic import BaseModel, Field, ConfigDict
import os
from pathlib import Path
from typing import Any


class Node(BaseModel):
	name: str
	x: int
	y: int
	color: str
	zone: str
	capacity: int
	neigbords: list[str] = Field(default_factory=list)


class Graph(BaseModel):
	name: str
	nb_drones: int
	start: Node
	end: Node
	map: list[Node] = Field(default_factory=list)


class FileHandeler(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	target_files: list[Any] = Field(default_factory=list)
	files_with_maps: list[Any] = Field(default_factory=list)
	names_levels: list[str] = Field(default_factory=list)
	nb_drones: int = Field(default=1, gt=0)

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

	def text_file_handeler(self):
		for files_list in self.target_files:
			for file in files_list:
				with open(file) as f:
					data = f.read()
					if not data:
						print(f'"{file}" is empty!')
						continue

					text = []
					for line in data.splitlines():
						line_s = line.strip()
						if "#" in line_s:
							if line_s.index("#") == 0:
								continue
						if not line_s:
							continue
						text.append(line_s)

					for i in range(len(text)):
						if i == 0:
							if text[i].startswith('nb_drones:'):
								text_elem = text[i].split(":", maxsplit = 1)
								try:
									self.nb_drones = text_elem[1].strip()
								except Exception:
									raise Exception('Number of drons must be integer and more then 0!')
							else:
								print(f'"{file}" has not "nb_drones" on first line!')
								continue
						# elif i == 1:
						# 	if text[i].startswith('start_hub:'):

		if not self.files_with_maps:
			raise Exception('All files are empty or incorrect!')

		
				
