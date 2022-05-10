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

import constants


class OculusTouchTestScene(Controller):
    librarian = ModelLibrarian()

    TABLES = constants.TABLES
    CHAIRS = constants.CHAIRS
    CUPS = constants.CUPS

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
        self.path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("image_capture")
        self.capture = ImageCapture(path=self.path, avatar_ids=["vr"], pass_masks=["_depth"])
        self.add_ons.append(self.capture)
        self.communicate(
            [
                TDWUtils.create_empty_room(12, 12),
                {"$type": "set_target_framerate", "framerate": 60},
            ]
        )

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
            position_to_center_normalized * random.uniform(1, 0.25)
        )
        chair_position[1] = 0
        return chair_position

    def trial(self) -> None:
        self.vr.reset()
        # Start a new trial.
        self.trial_done = False
        # Choose a random model.
        table = random.choice(OculusTouchTestScene.TABLES)
        chair = random.choice(OculusTouchTestScene.CHAIRS)
        cup = random.choice(OculusTouchTestScene.CUPS)

        table_extents = OculusTouchTestScene.get_longest_extent(table)
        chair_extents = OculusTouchTestScene.get_longest_extent(chair)
        table_placement_radius = table_extents + chair_extents + 1.15
        table_x = 1
        table_z = 0
        table_id = self.get_unique_id()
        # Add the model.
        resp = self.communicate(
            [
                {
                    "$type": "add_object",
                    "name": table.name,
                    "url": "https://tdw-public.s3.amazonaws.com/models/windows/2018-2019.1/"
                    + table.name,
                    "scale_factor": 1.0,
                    "position": {"x": table_x, "y": 0, "z": table_z},
                    "category": "table",
                    "id": table_id,
                },
                {
                    "$type": "rotate_object_to_euler_angles",
                    "euler_angles": {"x": 0, "y": 0, "z": 0},
                    "id": table_id,
                },
                {
                    "$type": "set_kinematic_state",
                    "id": table_id,
                    "is_kinematic": True,  # kinematic object is non-graspable
                    "use_gravity": True,
                },
                {"$type": "set_mass", "mass": 50, "id": table_id},
                {
                    "$type": "set_physic_material",
                    "dynamic_friction": 0.45,
                    "static_friction": 0.48,
                    "bounciness": 0.5,
                    "id": table_id,
                },
                {"$type": "send_bounds", "frequency": "once", "ids": [table_id]},
            ]
        )
        bounds = Bounds(resp[0])
        table_center = np.array(bounds.get_center(0))

        chair_positions = [
            self.get_chair_position(
                table_center=table_center,
                table_bound_point=np.array(bounds.get_left(0)),
            ),
            self.get_chair_position(
                table_center=table_center,
                table_bound_point=np.array(bounds.get_right(0)),
            ),
        ]
        table_top = bounds.get_top(0)
        table_bottom = TDWUtils.array_to_vector3(bounds.get_bottom(0))

        cup_id = self.get_unique_id()
        commands = []
        commands.extend(
            self.get_add_physics_object(
                model_name=cup.name,
                object_id=cup_id,
                position={"x": table_x - 0.3, "y": table_top[1], "z": table_z - 0.3},
                rotation={"x": 0, "y": 0, "z": 0},
            ),
        )
        chair_ids = []
        for chair_position in chair_positions:
            object_id = self.get_unique_id()
            chair_ids.append(object_id)
            commands.extend(
                self.get_add_physics_object(
                    model_name=chair.name,
                    position=TDWUtils.array_to_vector3(chair_position),
                    object_id=object_id,
                ),
            )
            commands.extend(
                [
                    {
                        "$type": "object_look_at_position",
                        "position": table_bottom,
                        "id": object_id,
                    },
                    {
                        "$type": "rotate_object_by",
                        "angle": float(random.uniform(-20, 20)),
                        "id": object_id,
                        "axis": "yaw",
                    },
                ]
            )

        self.communicate(commands)

        images = self.capture.images["vr"]
        for i in range(images.get_num_passes()):
            if images.get_pass_mask(i) == "_depth":
                # Get the depth values.
                depth_values = TDWUtils.get_depth_values(images.get_image(i), depth_pass="_depth", width=images.get_width(), height=images.get_height())
                # path = self.path.joinpath("depth")
                # num = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
                # plt.imshow(depth_values)
                # plt.savefig("depth.png")
                # plt.show()

        # Wait until the trial is done.
        while not self.trial_done and not self.simulation_done:
            self.communicate([])
        # Destroy the object.
        self.communicate(
            [
                {"$type": "destroy_object", "id": table_id},
                {"$type": "destroy_object", "id": cup_id},
            ]
        )
        for chair_id in chair_ids:
            self.communicate(
                {"$type": "destroy_object", "id": chair_id},
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
