import inspect
import sys
from typing import Dict, List, Type


RegisterType = Dict[int, List[int]]

class UserModel:

    Users = []

    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.items = []

        UserModel.Users.append(self)


    def add_item(self, item_id: int):
        self.items.append(item_id)


    @classmethod
    def FindUserByCustomer_id(cls, customer_id):
        for x in cls.Users:
            if customer_id == x.customer_id:
                return x
        return None


    @classmethod
    def deleteUser(cls, customer_id: int):
        user = cls.FindUserByCustomer_id(customer_id)
        cls.Users.remove(user)

    @classmethod
    def clear(cls):
        cls.Users = []


    def __repr__(self):
        return f"'{self.customer_id}', {self.items})"



class BaseModel:
    """
    Base class for creating other models.
    """

    def __init__(self, register_count: int):
        self.register_count = register_count
        self.registers: RegisterType = {i: [] for i in range(self.register_count)}

        #self.customer_register_assignments: Dict[int, int] = {}

    def clear(self):
        self.registers = {i: [] for i in range(self.register_count)}
        UserModel.clear()


    def _select_register(self) -> int:

        minUsersInRegister = 100 # Or max number allowed in memory
        tempMin = minUsersInRegister
        register = -1

        for reg in self.registers:
            minUsersInRegister = min(minUsersInRegister, len(self.registers[reg]))

            if minUsersInRegister < tempMin:
                tempMin = minUsersInRegister
                register = reg



        return register


    def _remove_user_from_register(self, customer_id: int) -> int:
        """
        Select a register to use for new customers.
        """

        for _, value in self.registers.items():
            count = 0
            for item in value:
                if item["customer_id"] == customer_id:
                        value.pop(count)
                        break
                count += 1




    def add(self, customer_id: int, item_id: int):

        user = UserModel.FindUserByCustomer_id(customer_id)
        """
            - If the customer is new, select a register using the model.
        """
        if user is None:
            user = UserModel(customer_id)
            user.add_item(item_id)
            user_object = {"customer_id": user.customer_id, "items": user.items}

            register = self._select_register()
            self.registers[register].append(user_object)

        else:
            """
            Add an item to a register using the following rules:
                - If the customer already has items on a register, select that register.
            """
            user.add_item(item_id)





    def checkout(self, customer_id: int):
        """
        Clear the customer's register assignment and remove their items from the register.
        """

        user = UserModel.FindUserByCustomer_id(customer_id)

        if user:
            UserModel.deleteUser(customer_id)
            self._remove_user_from_register(customer_id)


        return self.registers
        # raise NotImplementedError()


    def __repr__(self):
        return f"'{self.register_count}', {self.registers})"


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