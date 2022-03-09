import inspect
import sys
from typing import Dict, List, Type


RegisterType = Dict[int, List[int]]

class BaseModel:
    """
    Base class for creating other models.
    """

    def __init__(self, register_count: int):
        self.register_count = register_count
        self.registers: RegisterType = {i: [] for i in range(self.register_count)}
        self.customer_register_assignments: Dict[int, int] = {}

    def clear(self):
        self.registers = {i: [] for i in range(self.register_count)}
        self.customer_register_assignments = {}

    def _select_register(self, customer_id: int) -> int:
        """
        Select a register to use for new customers.
        """
        raise NotImplementedError()

    def add(self, customer_id: int, item_id: int):
        """
        Add an item to a register using the following rules:
            - If the customer already has items on a register, select that register.
        """

        """
            - If the customer is new, select a register using the model.
        """
     
        raise NotImplementedError()

    def checkout(self, customer_id: int):
        """
        Clear the customer's register assignment and remove their items from the register.
        """
        raise NotImplementedError()

    @staticmethod
    def get_model(model_name: str) -> Type["BaseModel"]:
        """
        Search this module for a subclass of BaseModel with a name that matches the given model name.
        """
        matches = (
            cls
            for name, cls in inspect.getmembers(
                object=sys.modules[__name__], predicate=inspect.isclass
            )
            if issubclass(cls, BaseModel) and name == model_name
        )
        cls = next(matches, None)
        if not cls:
            raise TypeError(f"{model_name} is not a subclass of BaseModel or it does not exist.")
        return cls
