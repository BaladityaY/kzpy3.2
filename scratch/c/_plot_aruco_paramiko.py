#!/usr/bin/env python
from kzpy3.vis2 import *
clear_timer = Timer(1)
#clf();plt_square();xysqlim(2.1);
import kzpy3.Cars.robot_car_6Aug2017_temp.nodes.runtime_parameters as rp

#  b=cv2.blur(a,(40,40)) 

from kzpy3.Grapher_app.Graph_Image_Module import *
wall_length = 4*107.0/100.0
half_wall_length = wall_length/2.0
hw = half_wall_length
#img_ = z2o(cv2.blur(lo(opjD('Potential_graph_img')),(rp.potential_graph_blur,rp.potential_graph_blur)))
img_ = ((np.array(lo(opjD('Potential_graph_img'))))*255.0).astype(np.int)
#img_[18:21,10:15] = 255
#mi(img_);spause()
x_min = -(6.03/2.0)#-6.03+hw
x_max = (6.03/2.0)#hw
y_min = -(6.03/2.0)#-hw#
y_max = 6.03/2.0#hw#
Gi = Graph_Image(xmin,x_min, xmax,x_max, ymin,y_min, ymax,y_max, xsize,35, ysize,35)
for i in range(3):
	Gi[img][:,:,i] = img_.copy()#imresize(img_,(400,400))

Colors = {'Mr_Black':(0,0,0),'Mr_Blue':(0,0,255)}



done = False
while not done:
	try:
		something_happened = False

		for car in sggo(opjD('*.car.txt')): #['Mr_Black.car.txt','Mr_New.car.txt']:
			car_name = fname(car).split('.')[0]
			new_car = car.replace('car','')
			unix('mv '+car+' '+new_car)
			l = txt_file_to_list_of_strings(new_car)#opjD(car))
			for ll in l:
				exec(ll)
			if len(pose) == 4:

				if clear_timer.check():

					clear_timer.reset()


				heading_floats = np.array(heading_floats)
				#Gi[ptsplot]( x,heading_floats[:,0], y,heading_floats[:,1], color,(255,255,255), NO_REVERSE,False)

				for xxyy in xy:
					#print xxyy
					#print xxyy
					Gi[img][int(xxyy[0]),int(xxyy[1]),:] = [0,255,255]
					#print Gi[img][xxyy[0],xxyy[1],:]
				car_color = Colors[car_name]
				Gi[ptsplot](x,[pose[0]],y,[pose[1]],color,car_color)
				Gi[ptsplot](x,[pose[0]+pose[2]],y,[pose[1]+pose[3]],color,(0,255,0))
				something_happened = True

		if something_happened:
			k = mci(Gi[img],delay=5,scale=30)
			if k == ord('q'):
				done = True
				break
		if True:#k == ord('r'):
				for i in range(3):
					Gi[img][:,:,i] = img_.copy()#imresize(img_,(400,400))
	
	except (KeyboardInterrupt, SystemExit):
		raise
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
	