from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum
from abc import ABC, abstractmethod
from .file_handeler import FileHandeler
import pygame
from typing import Any


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
	MAROON = "maroon"
	GOLD = "gold"
	DARKRED = "darkred"
	VIOLET = "violet"
	CRIMSON = "crimson"


class Node(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	name: str = Field(default="")
	x: int = Field(default=0)
	y: int = Field(default=0)
	rel_x: int = Field(default=0)
	rel_y: int = Field(default=0)
	center_x: int = Field(default=0)
	center_y: int = Field(default=0)
	color: ColorType = Field(default="white")
	zone: ZoneType | None = None
	max_drones: int = Field(default=1, gt=0)
	neigbords: list[str] = Field(default_factory=list)


class Connection(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	hub_s: Node = Field(default_factory=Node)
	hub_e: Node = Field(default_factory=Node)
	max_link_capacity: int | None = Field(default=None, gt=0)


class Nodes_holder(BaseModel):
	model_config = ConfigDict(validate_assignment=True)
	name: str = Field(default="")
	nb_drones: int = Field(default=1, gt=0)
	start: Node = Field(default_factory=Node)
	end: Node = Field(default_factory=Node)
	nodes: list[Node] = Field(default_factory=list)
	connections: list[Connection] = Field(default_factory=list)


class MenuGeneral(ABC):
	def __init__(self):
		self.fileOperator = FileHandeler()
		self.names: list[str] = []
		self.links: list[str] = []
		self.list_rect: list[pygame.Rect] = []
		self.list_sur_text: list[Any] = []
		self.list_text_rect: list[Any] = []

	@abstractmethod
	def take_data(self):
		pass

	@abstractmethod
	def update_metric(self, width: int, height: int):
		pass

	@abstractmethod
	def draw_menu(self, surface: pygame.Surface):
		pass

	@abstractmethod
	def handle_click(self, mouse_pos: tuple[int, int]) -> Any:
		pass
