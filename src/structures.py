from pydantic import BaseModel, Field, ConfigDict
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
