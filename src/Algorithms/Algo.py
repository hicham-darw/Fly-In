from abc import ABC, abstractmethod
from typing import Any
from src.GraphBuilder.GraphBuilder import GraphBuilder


class Algo(ABC):

	def __init__(self, graph: GraphBuilder) -> None:
		self.visited = []
		self._graph = graph
	
	@abstractmethod
	def run(self) -> Any:
		pass
