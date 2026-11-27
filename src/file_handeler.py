import os
from pathlib import Path
from typing import Any


class FileHandeler():
	def __init__(self):
		self.recived_levels: list[Any] = []
		self.names_levels: list[str] = []
		self.recived_maps:list[Any] = []
		self.names_maps: list[str] = []

	def dir_finder(self):
		levels = Path('maps')
		if not levels.is_dir():
			raise Exception('Directory "maps" is not exist!')

		dirs = [file for file in levels.iterdir() if file.is_dir() == True]
		if not dirs:
			raise Exception('Map - directory is not have subdirectories!')
		levels_name = ['challenger', 'easy', 'hard', 'medium', 'custom']

		for dir in dirs:
			if os.path.basename(dir) in levels_name:
				self.names_levels.append(os.path.basename(dir))
				self.recived_levels.append(dir)
		if not self.recived_levels:
			raise Exception('Fly-in can not finde levels directories!'
			                '\n It can have only next names:'
							'\n challenger, easy, hard, medium, custom')

	def take_levels(self):
		return self.recived_levels

	def take_names(self):
		return self.names_levels

	def txt_finder(self, target_dir: Any):
		for file in target_dir.iterdir():
			if file.is_file() and file.suffix == '.txt':
				self.recived_maps.append(file)
				self.names_maps.append(os.path.basename(file))
		if not self.recived_maps:
			print(f"'{target_dir}' has not '.txt' files!\n")

		# for i in range(len(recived_levels)):
		# 	pass_to_files = [file for file in recived_levels[i].iterdir() if file.is_file() and file.suffix == '.txt']
		# 	if not pass_to_files:
		# 		print(f"'{self.names_levels[i]}' has not '.txt' files!\n")
		# 		self.names_levels[i] = None
		# 	else:
		# 		self.target_files.append(pass_to_files)
		# self.names_levels = [level for level in self.names_levels if level]
		# if not self.target_files:
		# 	raise Exception('All level directories don`t have ".txt" files!' )

	def take_maps(self):
		return self.recived_maps

	def take_name_maps(self):
		return self.names_maps