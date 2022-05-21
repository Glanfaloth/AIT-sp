import numpy as np
import random
import argparse
import matplotlib.pyplot as plt
from tdw.librarian import ModelLibrarian, ModelRecord
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.output_data import Bounds, OutputData, CameraMatrices
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.image_capture import ImageCapture
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH

parser = argparse.ArgumentParser(description="add obj")
parser.add_argument(
    "--sink", default="sink_cabinet_unit_wood_beech_honey_porcelain_composite"
)
parser.add_argument("--toothbrush", default="toothbrush")
args = parser.parse_args()

BOTTLES = [
    "b05_bathroom_dispenser",
    "blue_edition_liquid_soap02",
    "kosmos_black_soap_dispenser",
    "soap_dispenser_01",
]

class ProcGen(Controller):
    """ """

    def __init__(
        self, port: int = 1071, launch_build: bool = True, random_seed: int = 0
    ):
        super().__init__(port=port, launch_build=launch_build)
        self.rng: np.random.RandomState = np.random.RandomState(random_seed)

    def run(self) -> None:
        sink_x = 0
        sink_z = 0
        sink_id = self.get_unique_id()

        resp = self.communicate(
            [
                # TDWUtils.create_empty_room(12, 12),
                self.get_add_scene(scene_name="monkey_physics_room"),
                self.get_add_object(
                    model_name=args.sink,
                    position={"x": sink_x, "y": 0, "z": sink_z},
                    rotation={"x": 0, "y": 0, "z": 0},
                    object_id=sink_id,
                ),
                {"$type": "send_bounds", "frequency": "once", "ids": [sink_id]},
            ]
        )
        bounds = Bounds(resp[0])
        sink_center = np.array(bounds.get_center(0))
        sink_top = bounds.get_top(0)
        sink_bottom = TDWUtils.array_to_vector3(bounds.get_bottom(0))
        sink_back = bounds.get_back(0)
        sink_left = bounds.get_left(0)
        camera = ThirdPersonCamera(
            position={
                "x": sink_top[0],
                "y": sink_top[1] + 1,
                "z": sink_top[2] + 1,
            },
            look_at=TDWUtils.array_to_vector3(sink_top),
            avatar_id="a",
        )
        for i in range(len(BOTTLES) - 1):
            self.communicate(self.get_add_object(
                    model_name=BOTTLES[i],
                    position={"x": sink_left[0] + 0.1 * i, "y": sink_top[1], "z": sink_back[2] + 0.1},
                    rotation={"x": 0, "y": float(random.uniform(-360, 360)), "z": 0},
                    object_id=self.get_unique_id(),
                ),)
        path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("test")
        capture = ImageCapture(
            avatar_ids=[camera.avatar_id],
            pass_masks=["_img"],
            path=path,
        )
        self.add_ons.extend([camera, capture])
        commands = [
            {"$type": "set_screen_size", "width": 1280, "height": 720},
        ]
        resp = self.communicate(commands)


if __name__ == "__main__":
    c = ProcGen()
    c.run()
