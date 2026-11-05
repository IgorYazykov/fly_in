from src import FileHandeler, GameCenter


if __name__ == "__main__":
	# fileOperator = FileHandeler()
	# fileOperator.text_file_finder()
	# fileOperator.text_file_handeler()
	gameOperator = GameCenter()
	gameOperator.main_loop()