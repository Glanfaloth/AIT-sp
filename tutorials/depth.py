import matplotlib.pyplot as plt
import numpy as np
from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.image_capture import ImageCapture
from tdw.output_data import OutputData, CameraMatrices
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
from tdw.librarian import ModelLibrarian, ModelRecord

"""
Convert the _depth pass to depth values, plot them using matplotlib, and generate a point cloud
"""
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
c = Controller()
librarian = ModelLibrarian()
tables = librarian.get_all_models_in_wnid("n03201208") # dining table
chairs = librarian.get_all_models_in_wnid("n03001627")
cups = librarian.get_all_models_in_wnid("n03147509") # cup
tables = [record for record in tables if not record.do_not_use]
chairs = [record for record in chairs if not record.do_not_use]
cups = [record for record in cups if not record.do_not_use]
table = tables[0]
chair = chairs[0]
cup = cups[0]
table_extents = get_longest_extent(table)
chair_extents = get_longest_extent(chair)
object_id_0 = c.get_unique_id()
object_id_1 = c.get_unique_id()
object_id_2 = c.get_unique_id()
object_id_3 = c.get_unique_id()
object_names = {object_id_0: table.name,
                object_id_1: chair.name,
                object_id_2: cup.name,}

cam = ThirdPersonCamera(position={"x": 2.478, "y": 1.602, "z": 1.412},
                        look_at={"x": 0, "y": 0.2, "z": 0},
                        avatar_id="a")
output_directory = EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("depth")
print(f"Images will be saved to: {output_directory.resolve()}")
c.add_ons.append(cam)
cap = ImageCapture(path=output_directory, avatar_ids=["a"], pass_masks=["_img", "_depth"])
c.add_ons.append(cap)
resp = c.communicate([TDWUtils.create_empty_room(12, 12),
                      c.get_add_object(object_names[object_id_0],
                                       object_id=object_id_0),
                      c.get_add_object(object_names[object_id_1],
                                       position={"x": 1, "y": 0, "z": 1},
                                       rotation={"x": 0, "y": 30, "z": 0},
                                       object_id=object_id_1),
                      c.get_add_object(model_name=object_names[object_id_2],
                                       position={"x": -0.3, "y": 0.8, "z": 0.2},
                                       object_id=object_id_2),
                      {"$type": "send_camera_matrices",
                       "frequency": "always"}])
# Get the camera matrix.
camera_matrix = None
for i in range(len(resp) - 1):
    r_id = OutputData.get_data_type_id(resp[i])
    if r_id == "cama":
        camera_matrix = CameraMatrices(resp[i]).get_camera_matrix()
images = cap.images["a"]
for i in range(images.get_num_passes()):
    if images.get_pass_mask(i) == "_depth":
        # Get the depth values.
        depth_values = TDWUtils.get_depth_values(images.get_image(i), depth_pass="_depth",
                                                 width=images.get_width(), height=images.get_height())

        # Comment out these two lines on a Linux server.
        plt.imshow(depth_values)
        plt.show()

        # # Convert the depth values to a point cloud.
        # point_cloud_filename = str(output_directory.joinpath("point_cloud.txt").resolve())
        # TDWUtils.get_point_cloud(depth=depth_values, filename=point_cloud_filename, camera_matrix=camera_matrix)
c.communicate({"$type": "terminate"})