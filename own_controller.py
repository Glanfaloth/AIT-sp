from typing import Union, List
from tdw.controller import Controller

class MyController(Controller):
    def communicate(self, commands: Union[dict, List[dict]]) -> list:
        print(commands)
        return super().communicate(commands=commands)
 

if __name__ == "__main__":
    c = MyController()
    c.communicate({"$type": "terminate"})
