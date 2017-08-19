#!/usr/bin/env python
from kzpy3.vis2 import *
clear_timer = Timer(1)
#clf();plt_square();xysqlim(2.1);


#  b=cv2.blur(a,(40,40)) 

from kzpy3.Grapher_app.Graph_Image_Module import *
wall_length = 4*107.0/100.0
half_wall_length = wall_length/2.0
hw = half_wall_length
img_ = lo(opjD('Potential_graph_img'))
Gi = Graph_Image(xmin,-hw, xmax,hw, ymin,-hw, ymax,hw, xsize,400, ysize,400)
for i in range(3):
	Gi[img][:,:,i] = imresize(img_,(400,400))

done = False
while not done:
	try:
		for car in ['Mr_Black.car.txt','Mr_New.car.txt']:
			l = txt_file_to_list_of_strings(opjD(car))
			exec('pose = '+l[0])
			if len(pose) == 4:
				#print pose
				if clear_timer.check():
					#img *= 0
					clear_timer.reset()
				Gi[ptsplot](x,[pose[0]],y,[pose[1]],color,(255,0,0))
				Gi[ptsplot](x,[pose[0]+pose[2]],y,[pose[1]+pose[3]],color,(0,255,0))
				k = mci(Gi[img],delay=5,scale=2)
			if k == ord('q'):
				done = True
				break
			if k == ord('r'):
				for i in range(3):
					Gi[img][:,:,i] = imresize(img_,(400,400))
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		#raise
		print(d2s('oops',time.time()))
