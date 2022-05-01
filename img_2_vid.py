import cv2
import os

image_folder = 'cor_images/'
video_name = 'video_pred.avi'

def get_idx(name):
    return int(name.split('.')[0][2:])

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 30, (width,height))

images = sorted(images, key=get_idx)

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()