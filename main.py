import cv2 as cv
from PIL import Image, ImageDraw
from multiprocessing.pool import ThreadPool
from collections import deque
#Get user input of file
name_of_file = input("What is the video file name ma dude?: ")
print("[+] GOT NAME STARTING PROGRAM")
# Setup.
cap = cv.VideoCapture(name_of_file)
thread_num = cv.getNumberOfCPUs()
pool = ThreadPool(processes=thread_num)
pending_task = deque()
length = cap.get(cv.CAP_PROP_FRAME_COUNT)
Image.MAX_IMAGE_PIXELS = None

print("[+] SETTING UP IMAGE")
#Setup final image
final_im = Image.new("RGB", ( int(length), 20000))
draw = ImageDraw.Draw(final_im)


def resizeImage():
	im = final_im
	resised_im = im.resize((round(im.size[0]/16), round(im.size[1]/16)))
	resised_im.save(f"{name_of_file[:4]}.png")

#Function that loads a movie and gets all the average colors and draws them to the picture
def getAverage(frame, currentFrame):
	b, g, r, a = cv.mean(frame)
	draw.line([(currentFrame,0), (currentFrame,20000)], (round(r), round(g), round(b), 1))
	print(f"Frame {currentFrame}/{length} drawn")
def main():
	while True:
		# Consume the queue.
		while len(pending_task) > 0 and pending_task[0].ready():
			res = pending_task.popleft().get()
		if len(pending_task) < thread_num:
			frame_got, frame = cap.read()
			if frame_got:
				currentFrame = round(cap.get(cv.CAP_PROP_POS_FRAMES))
				task = pool.apply_async(getAverage, (frame.copy(), currentFrame))
				pending_task.append(task)
			else:
				break


print("[+] SETUP COMPLETE STARTING ANALYZING")
main()
print("[+] DRAWING DONE SAVING THE HIGH RES IMAGE....")
final_im.save("final.png")
print("[+] IMAGE CALCULATED RESIZING....")
resizeImage()
print("DONE QUITTING....")
cap.release()
cv.destroyAllWindows()
