from PIL import Image

path = "Training/Train_images/"
im = Image.open(path+"synpic371.jpg")
print(im.format, im.size, im.mode)