from abc import ABC, abstractmethod
from typing import Any
from src.GraphBuilder.GraphBuilder import GraphBuilder


class Algo(ABC):
    """Base class of Algo All algos inherit this class
        work on graph in this time
    """
    def __init__(self, graph: GraphBuilder) -> None:
        """ constructor of Algo need graph and initial
            list of visited to track visited nodes

        Args:
            graph: (GraphBuilder): graph for running algo on it
        returns:
            None
        """
        self.visited: list[str] = []
        self._graph = graph

    @abstractmethod
    def run(self) -> Any:
        """this method is abstract method all classes inherit this class
        must be implement this method run

        Args:
            None
        return:
            Any: any how behave and return different data
        """
        pass
