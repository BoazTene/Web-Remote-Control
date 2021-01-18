import d3dshot
import datetime
from time import sleep

time = datetime.datetime.now()
d = d3dshot.create()
d.capture()
sleep(5)
image = d.get_latest_frame()
print(image)
print(datetime.datetime.now() - time)
# print(image.save("test.jpg"))
d.stop()

