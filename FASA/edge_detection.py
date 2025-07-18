from PIL import Image
import numpy as np
import pandas as pd

black_level = '9130_levels\\half_black.png'

im = Image.open(black_level).convert("RGBA")
data = list(im.getdata())
np_data = np.array(data)
np_df = pd.DataFrame(data)
print(data[2000:2100])