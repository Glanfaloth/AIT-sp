import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
from tdw.tdw_utils import TDWUtils
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
parser = argparse.ArgumentParser(description="which scene")
parser.add_argument("--scene", default="office")
args = parser.parse_args()
data = np.load(EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("scene_" + args.scene + "/output.npy"))
for i in range(len(data)):
    path = os.path.join(
                        EXAMPLE_CONTROLLER_OUTPUT_PATH.joinpath("scene_office"),
                        "vr",
                        "depth_value_" + TDWUtils.zero_padding(i, 4) + ".png",
                    )
    plt.imshow(data[i])
    plt.savefig(path)