from PIL import Image
from CVAlgorithms import CVAlgorithms

# This file is not part of the build and is here solely to
# test the algorithms without the need to run the app.
path = "histReq.png"


CVAlgorithms.histogram_equalization(
    Image.open(path), 100, 500, 100, 500).show()