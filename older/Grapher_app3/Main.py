###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Grapher_app','kzpy3/teg9'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *
import Graph_Module
from Car_Data_app.Names_Module import *
exec(identify_file_str)
"""
	Animate advance/retreat n seconds at r rate
	Put in baseline
	Put in second markers, both absolute and relative to verticle line
	Put in playback time multiple (e.g., 1.43 X)
	Take out or comment out unused features
"""
_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]

L = h5r(P[L_FILE])
O = h5r(P[O_FILE])
xpixelsv = P[X_PIXEL_SIZE]
ypixelsv = P[Y_PIXEL_SIZE]
screen_xv = P[SCREEN_X]
screen_yv = P[SCREEN_Y]

cv2.destroyAllWindows()


def mouse_event(event, x, y, buttons, user_param):
	P[MOUSE_X] = x
	P[MOUSE_Y] = y
	if event == cv2.EVENT_MOUSEMOVE:
		P[MOUSE_MOVE_TIME] = time.time()
	elif event == cv2.EVENT_LBUTTONDOWN:
		do_center_time('center_time',I[pixel_to_float](xint,x, yint,0)[0])


def do_center_time(*args):
	Args = args_to_dictionary(args)
	center_timev = Args['center_time']
	True
	time_widthv = P[END_TIME] - P[START_TIME]
	P[START_TIME] = center_timev - time_widthv/2
	P[END_TIME] = center_timev + time_widthv/2



tsv = L[ts]
tsv -= tsv[0]
Timestamp_to_left_image = {}
for iv in rlen(tsv):
	Timestamp_to_left_image[tsv[iv]] = iv

P[END_TIME] =  max(tsv)

for kv in P[TOPICS].keys():
	print(kv)
	valsv = L[kv][:]
	if P[TOPICS][kv][minval] == minval:
		yminv = min(valsv)
	else:
		yminv = P[TOPICS][kv][minval]
	if P[TOPICS][kv][maxval] == maxval:
		ymaxv = max(valsv)
	else:
		ymaxv = P[TOPICS][kv][maxval]


	P[START_TIME_INIT],P[END_TIME_INIT] = P[START_TIME],P[END_TIME]
	yminv_init,ymaxv_init,xpixelsv_init,ypixelsv_init = yminv,ymaxv,xpixelsv,ypixelsv
	screen_xv_init,screen_yv_init = screen_xv,screen_yv
	show_menuv = True
	first_timev = True

	while True:
		I = Graph_Module.Image2(
			xmin,P[START_TIME],
			xmax,P[END_TIME],
			ymin,yminv,
			ymax,ymaxv,
			xsize,xpixelsv,
			ysize,ypixelsv)
		I[ptsplot](x,tsv,y,valsv,color,(0,255,0))

		if np.abs(P[MOUSE_Y]-ypixelsv/2) > 100:
			ref_xv = int(P[VERTICAL_LINE_PROPORTION]*xpixelsv)
		else:
			ref_xv = P[MOUSE_X]
			cv2.line(
				I[img],
				(P[MOUSE_X],0),
				(P[MOUSE_X],ypixelsv),
				(255,0,0))
		time_from_pixelv = I[pixel_to_float](xint,ref_xv, yint,0)[0]
		ts_from_pixelv = find_nearest(tsv,time_from_pixelv)
		cv2.putText(
			I[img],
			d2n(dp(ts_from_pixelv,3),'s'),
			(10,30),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.75,(255,0,0),1)
		cv2.line(
			I[img],
			(int(P[VERTICAL_LINE_PROPORTION]*xpixelsv),0),
			(int(P[VERTICAL_LINE_PROPORTION]*xpixelsv),ypixelsv),
			(0,0,255))

		keyv = mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=33,title=kv)
		mci(O[left_image][vals][Timestamp_to_left_image[ts_from_pixelv]][:],
			title=left_image,scale=4)
		if first_timev:
			first_timev = False
			cv2.moveWindow(kv,screen_xv,screen_yv)
			cv2.setMouseCallback(kv,mouse_event)
		dtv = (P[START_TIME]-P[END_TIME])*0.001
		dvalv = (ymaxv-yminv)*0.001
		dxpixelsv = max(1,xpixelsv*0.1)
		dypixelsv = max(1,ypixelsv*0.1)

		if show_menuv:
			show_menuv = False
			print('Key command menu')
			for lv in P[CV2_KEY_COMMANDS]:
				print_lv = lv
				if len(lv) == 0 or lv == ' ':
					print_lv = "\'"+lv+"\'"
				print(d2s('\t',print_lv,'-',P[CV2_KEY_COMMANDS][lv][1]))
				
		key_decodedv = False

		for mv in P[CV2_KEY_COMMANDS]:
			if len(mv) > 0:
				if keyv == ord(mv):
					cmd_tuplev = P[CV2_KEY_COMMANDS][mv]
					exec(cmd_tuplev[0])
					key_decodedv = True

		if not key_decodedv:
			if keyv != -1:
				print(d2s(str(unichr(keyv)), '=',keyv))







#EOF