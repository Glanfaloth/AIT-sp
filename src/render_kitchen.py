from json import loads
from pathlib import Path
from platform import system
from tdw.controller import Controller
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.image_capture import ImageCapture
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
from tdw.backend.platforms import SYSTEM_TO_S3

class RenderKitchenScene(Controller):
    def __init__(
        self, port: int = 1071, check_version: bool = True, launch_build: bool = True
    ):
        super().__init__(
            port=port, check_version=check_version, launch_build=launch_build
        )
        self.camera = ThirdPersonCamera(position={"x": -1.5, "y": 0.8, "z": 0},
                           look_at={"x": 0, "y": 0, "z": 0},
                           avatar_id="a")
        self.add_ons.extend([self.camera])
        self.path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("render_kitchen")
        
        # Load the commands used to initialize the objects in the scene.
        init_commands_text = Path("src\interior_scene.json").read_text()
        # Replace the URL platform infix.
        init_commands_text = init_commands_text.replace("/windows/", "/" + SYSTEM_TO_S3[system()] + "/")
        # Load the commands as a list of dictionaries.
        self.init_commands = loads(init_commands_text)

        self.capture = ImageCapture(
            path=self.path, avatar_ids=["a"], pass_masks=["_img"]
        )
        self.add_ons.append(self.capture)

    def run(self) -> None:
        self.communicate(self.init_commands)
        self.communicate(
           {"$type": "destroy_all_objects"}
        )
        self.communicate({"$type": "terminate"})
       


if __name__ == "__main__":
    c = RenderKitchenScene()
    c.run()
