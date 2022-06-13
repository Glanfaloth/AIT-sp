import numpy as np
import random
import argparse
from typing import List
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.oculus_touch import OculusTouch
from tdw.vr_data.oculus_touch_button import OculusTouchButton
from tdw.output_data import Bounds
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


class OculusTouchBathroomScene(Controller):
    def __init__(
        self, port: int = 1071, check_version: bool = True, launch_build: bool = True
    ):
        super().__init__(
            port=port, check_version=check_version, launch_build=launch_build
        )
        self.simulation_done = False
        self.trial_done = False
        self.vr = OculusTouch(set_graspable=False, attach_avatar=True)
        # Quit when the left trigger button is pressed.
        self.vr.listen_to_button(
            button=OculusTouchButton.trigger_button, is_left=True, function=self.quit
        )
        # End the trial when the right trigger button is pressed.
        self.vr.listen_to_button(
            button=OculusTouchButton.trigger_button,
            is_left=False,
            function=self.end_trial,
        )
        self.add_ons.extend([self.vr])
        self.path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("scene_bathroom")
        self.depth_output = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath(
            "scene_bathroom/output.npy"
        )
        self.communicate(
            [
                self.get_add_scene(scene_name="monkey_physics_room"),
            ]
        )
        self.capture = ImageCapture(
            path=self.path, avatar_ids=["vr"], pass_masks=["_img", "_id", "_depth"]
        )
        self.add_ons.append(self.capture)

    def trial(self) -> None:
        self.vr.reset()
        self.trial_done = False
        sink_x = 0
        sink_z = 0.5
        sink_id = self.get_unique_id()

        resp = self.communicate(
            [
                {
                    "$type": "add_object",
                    "name": args.sink,
                    "url": "https://tdw-public.s3.amazonaws.com/models/windows/2020.3/"
                    + args.sink,
                    "scale_factor": 1.0,
                    "position": {"x": sink_x, "y": 0, "z": sink_z},
                    "category": "cabinet",
                    "id": sink_id,
                },
                {
                    "$type": "rotate_object_to_euler_angles",
                    "euler_angles": {"x": 0, "y": 180, "z": 0},
                    "id": sink_id,
                },
                {
                    "$type": "set_kinematic_state",
                    "id": sink_id,
                    "is_kinematic": True,  # kinematic object is non-graspable
                    "use_gravity": True,
                },
                {"$type": "set_mass", "mass": 50, "id": sink_id},
                {
                    "$type": "set_physic_material",
                    "dynamic_friction": 0.45,
                    "static_friction": 0.48,
                    "bounciness": 0.5,
                    "id": sink_id,
                },
                {"$type": "send_bounds", "frequency": "once", "ids": [sink_id]},
            ]
        )
        bounds = Bounds(resp[0])
        sink_center = np.array(bounds.get_center(0))
        sink_top = bounds.get_top(0)
        sink_bottom = TDWUtils.array_to_vector3(bounds.get_bottom(0))
        sink_back = bounds.get_back(0)
        sink_left = bounds.get_left(0)
        sink_right = bounds.get_right(0)

        bottle_ids = []
        toothbrush_id = self.get_unique_id()
        comb1_id = self.get_unique_id()
        comb2_id = self.get_unique_id()
        for i in range(len(BOTTLES) - 1):
            bottle_id = self.get_unique_id()
            bottle_ids.append(bottle_id)
            self.communicate(
                self.get_add_object(
                    model_name=BOTTLES[i],
                    position={
                        "x": sink_left[0] - 0.1 * i - 0.1,
                        "y": sink_top[1],
                        "z": sink_back[2] - 0.2,
                    },
                    rotation={"x": 0, "y": float(random.uniform(-360, 360)), "z": 0},
                    object_id=bottle_id,
                ),
            )
        self.communicate(
            self.get_add_object(
                model_name=args.toothbrush,
                position={"x": sink_left[0] - 0.3, "y": sink_top[1], "z": sink_left[2]},
                rotation={"x": 0, "y": float(random.uniform(-360, 360)), "z": 0},
                object_id=toothbrush_id,
            ),
        )
        self.communicate(
            self.get_add_object(
                model_name="b05_48_body_shop_hair_brush",
                position={
                    "x": sink_right[0] + 0.3,
                    "y": sink_top[1],
                    "z": sink_right[2],
                },
                rotation={"x": 0, "y": float(random.uniform(-360, 360)), "z": 0},
                object_id=comb1_id,
            ),
        )
        self.communicate(
            self.get_add_object(
                model_name="b04_comb",
                position={
                    "x": sink_right[0] + 0.2,
                    "y": sink_top[1],
                    "z": sink_right[2] - 0.1,
                },
                rotation={"x": 90, "y": float(random.uniform(-360, 360)), "z": 0},
                object_id=comb2_id,
            ),
        )

        self.depth_value_dump: List[np.array] = list()

        while not self.trial_done and not self.simulation_done:
            self.images = self.capture.images["vr"]
            for i in range(self.images.get_num_passes()):
                if self.images.get_pass_mask(i) == "_depth":
                    depth_values = TDWUtils.get_depth_values(
                        self.images.get_image(i),
                        depth_pass="_depth",
                        width=self.images.get_width(),
                        height=self.images.get_height(),
                    )
                    self.depth_value_dump.append(depth_values)
            self.communicate([])
        self.communicate(
            [
                {"$type": "destroy_object", "id": sink_id},
                {"$type": "destroy_object", "id": toothbrush_id},
                {"$type": "destroy_object", "id": comb1_id},
                {"$type": "destroy_object", "id": comb2_id},
            ]
        )
        for i in range(len(bottle_ids) - 1):
            self.communicate({"$type": "destroy_object", "id": bottle_ids[i]})

    def run(self) -> None:
        while not self.simulation_done:
            self.trial()
        self.communicate({"$type": "terminate"})

    def quit(self):
        self.simulation_done = True
        np.save(str(self.depth_output.resolve())[:-4], np.array(self.depth_value_dump))

    def end_trial(self):
        self.trial_done = True

if __name__ == "__main__":
    c = OculusTouchBathroomScene()
    c.run()
