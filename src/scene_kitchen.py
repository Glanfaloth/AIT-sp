import numpy as np
import os
import argparse
from json import loads
from pathlib import Path
from platform import system
import matplotlib.pyplot as plt
from typing import List
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.oculus_touch import OculusTouch
from tdw.vr_data.oculus_touch_button import OculusTouchButton
from tdw.add_ons.image_capture import ImageCapture
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
from tdw.backend.platforms import SYSTEM_TO_S3

parser = argparse.ArgumentParser(description="add obj")
parser.add_argument(
    "--sink", default="sink_cabinet_unit_wood_beech_honey_porcelain_composite"
)
parser.add_argument("--microwave", default="microwave")
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
        self.path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("scene_kitchen")
        self.depth_output = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath(
            "scene_kitchen/output.npy"
        )
        
        # Load the commands used to initialize the objects in the scene.
        init_commands_text = Path("src\interior_scene.json").read_text()
        # Replace the URL platform infix.
        init_commands_text = init_commands_text.replace("/windows/", "/" + SYSTEM_TO_S3[system()] + "/")
        # Load the commands as a list of dictionaries.
        self.init_commands = loads(init_commands_text)

        self.capture = ImageCapture(
            path=self.path, avatar_ids=["vr"], pass_masks=["_img", "_id", "_depth"]
        )
        self.add_ons.append(self.capture)

    def trial(self) -> None:
        self.vr.reset()
        self.trial_done = False
        self.communicate(self.init_commands)
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
           {"$type": "destroy_all_objects"}
        )

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
