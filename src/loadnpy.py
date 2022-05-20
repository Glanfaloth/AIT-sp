import numpy as np
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
data = np.load(EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("image_capture/output.npy"))
print(data)