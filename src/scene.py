import numpy as np
import random
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.oculus_touch import OculusTouch
from tdw.vr_data.oculus_touch_button import OculusTouchButton

# import matplotlib.pyplot as plt
from tdw.librarian import ModelLibrarian, ModelRecord
from tdw.output_data import Bounds, OutputData, CameraMatrices
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.image_capture import ImageCapture
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH

class OculusTouchTestScene(Controller):
    librarian = ModelLibrarian()
    tables = librarian.get_all_models_in_wnid("n03201208")  # dining table
    chairs = librarian.get_all_models_in_wnid("n03001627")
    cups = librarian.get_all_models_in_wnid("n03147509")  # cup
    TABLES = [record for record in tables if not record.do_not_use]
    CHAIRS = [record for record in chairs if not record.do_not_use]
    CUPS = [record for record in cups if not record.do_not_use]

    def __init__(self, port: int = 1071, check_version: bool = True, launch_build: bool = True):
        super().__init__(port=port, check_version=check_version, launch_build=launch_build)
        self.simulation_done = False
        self.trial_done = False
        self.vr = OculusTouch()
        # Quit when the left trigger button is pressed.
        self.vr.listen_to_button(button=OculusTouchButton.trigger_button, is_left=True, function=self.quit)
        # End the trial when the right trigger button is pressed.
        self.vr.listen_to_button(button=OculusTouchButton.trigger_button, is_left=False, function=self.end_trial)
        self.add_ons.extend([self.vr])
        self.communicate(TDWUtils.create_empty_room(12, 12))

    @staticmethod
    def get_longest_extent(record: ModelRecord) -> float:
        left = TDWUtils.vector3_to_array(record.bounds["left"])
        right = TDWUtils.vector3_to_array(record.bounds["right"])
        front = TDWUtils.vector3_to_array(record.bounds["front"])
        back = TDWUtils.vector3_to_array(record.bounds["back"])
        left_right: float = np.linalg.norm(left - right)
        front_back: float = np.linalg.norm(front - back)
        if left_right > front_back:
            return left_right
        else:
            return front_back

    def get_table_placement_coordinate(self, radius: float) -> float:
        q = float(random.uniform(0, 6 - radius))
        if random.random() < 0.5:
            q *= -1
        return q

    def get_chair_position(
        self, table_center: np.array, table_bound_point: np.array
    ) -> np.array:
        position_to_center = table_bound_point - table_center
        position_to_center_normalized = position_to_center / np.linalg.norm(
            position_to_center
        )
        chair_position = table_bound_point + (
            position_to_center_normalized * random.uniform(0.5, 0.125)
        )
        chair_position[1] = 0
        return chair_position
    def trial(self) -> None:
        self.vr.reset()
        # Start a new trial.
        self.trial_done = False
        # Choose a random model.
        cup = random.choice(OculusTouchTestScene.CUPS)
        # Add the model.
        object_id = self.get_unique_id()
        self.communicate(self.get_add_object(model_name=cup.name,
                                             object_id=object_id,
                                             position={"x": 0, "y": 0, "z": 1.2}))
        # Wait until the trial is done.
        while not self.trial_done and not self.simulation_done:
            self.communicate([])
        # Destroy the object.
        self.communicate({"$type": "destroy_object",
                          "id": object_id})

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