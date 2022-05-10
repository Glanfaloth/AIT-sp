import numpy as np
import random
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.oculus_touch import OculusTouch
from tdw.vr_data.oculus_touch_button import OculusTouchButton

import matplotlib.pyplot as plt
from tdw.librarian import ModelLibrarian, ModelRecord
from tdw.output_data import Bounds, OutputData, CameraMatrices
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.image_capture import ImageCapture
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH


class OculusTouchTestScene(Controller):
    librarian = ModelLibrarian()

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
        # self.vr.listen_to_button(
        #     button=OculusTouchButton.trigger_button, is_left=True, function=self.quit
        # )
        # End the trial when the right trigger button is pressed.
        self.vr.listen_to_button(
            button=OculusTouchButton.trigger_button,
            is_left=False,
            function=self.end_trial,
        )
        self.add_ons.extend([self.vr])
        self.path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("image_capture_min")
        self.capture = ImageCapture(path=self.path, avatar_ids=["vr"], pass_masks=["_img", "_id", "_depth"])
        self.add_ons.append(self.capture)
        self.communicate(
            [
                TDWUtils.create_empty_room(12, 12),
                {"$type": "set_target_framerate", "framerate": 30},
            ]
        )

    def trial(self) -> None:
        self.vr.reset()
        # Start a new trial.
        self.trial_done = False

        # Add the model.
        object_id=Controller.get_unique_id()
        self.communicate([self.get_add_object(model_name="rh10",
                                object_id=object_id,
                                position={"x": 0, "y": 0, "z": 0.5})])

        images = self.capture.images["vr"]
        # for i in range(images.get_num_passes()):
        #     if images.get_pass_mask(i) == "_depth":
        #         # Get the depth values.
        #         depth_values = TDWUtils.get_depth_values(images.get_image(i), depth_pass="_depth", width=images.get_width(), height=images.get_height())
        #         # path = self.path.joinpath("depth")
        #         # num = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        #         # plt.imshow(depth_values)
        #         # plt.savefig("depth.png")
        #         # plt.show()

        # Wait until the trial is done.
        while not self.trial_done and not self.simulation_done:
            self.communicate([])
        # Destroy the object.
        self.communicate(
            [
                {"$type": "destroy_object", "id": object_id},
            ]
        )

    def run(self) -> None:
        while not self.simulation_done:
            # Run a trial.
            self.trial()
        # End the simulation.
        self.communicate({"$type": "terminate"})

    def quit(self):
        self.simulation_done = True

    def end_trial(self):
        self.trial_done = True


if __name__ == "__main__":
    c = OculusTouchTestScene()
    c.run()
