import base64


# this class is used to calculate the differences between images
class ImageDifferences:
    def __init__(self, new_image, old_image):
        # self.new_image_list = list(str(base64.b64encode(new_image.getvalue())))
        # self.old_image_list = list(str(base64.b64encode(old_image.getvalue())))
        self.old_image_list = list(str(old_image))
        self.new_image_list = list(str(new_image))
        self.result = []

    @staticmethod
    def replace(string, replace, replace_with):
        return replace_with.join(string.split(replace))

    def __str__(self):
        return ImageDifferences.replace(ImageDifferences.replace(ImageDifferences.replace(str(self.result), ', ', ','), "],[", "|"), '[[', '')[:-2]

    def sub(self):
        tmp = self.old_image_list[:len(self.new_image_list)]
        for i in range(len(tmp)):
            if self.old_image_list[i] != self.new_image_list[i]:
                try:
                    # print(self.result[-1][0])
                    if self.result[-1][1] == i-len(self.result[-1][0]):
                        self.result[-1][0] += self.new_image_list[i]
                    else:
                        self.result.append([self.new_image_list[i], i])
                except IndexError:
                    self.result.append([self.new_image_list[i], i])
        if len(self.new_image_list) > len(self.old_image_list):
            self.result.append(self.new_image_list[(-(len(self.new_image_list)-len(tmp))):])

        elif len(self.new_image_list) < len(self.old_image_list):
            self.result.append(['',  len(self.new_image_list) - (len(self.old_image_list) - len(self.new_image_list)) + 1])

        print(len(self.result))


image_diffrences = ImageDifferences("abcd", "abbb")

image_diffrences.sub()

print(str(image_diffrences))