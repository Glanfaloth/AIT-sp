from os import chdir
from subprocess import call
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.image_capture import ImageCapture
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH

c = Controller()
camera = ThirdPersonCamera(
    position={"x": 2, "y": 1.6, "z": -1},
    look_at={"x": 0, "y": 0, "z": 0},
    avatar_id="a",
)
c.add_ons.append(camera)
path = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("image_only_video")
print(f"Images will be save to: {path.resolve()}")
capture = ImageCapture(
    path=path,
    avatar_ids=["a"],
    pass_masks=["_img", "_id", "_depth"],
)
c.add_ons.append(capture)
c.communicate(
    [
        TDWUtils.create_empty_room(12, 12),
        {"$type": "set_target_framerate", "framerate": 60},
        c.get_add_object(
            model_name="iron_box",
            position={"x": 1, "y": 3, "z": -0.5},
            object_id=c.get_unique_id(),
        ),
    ]
)
for i in range(100):
    c.communicate([])
c.communicate({"$type": "terminate"})
