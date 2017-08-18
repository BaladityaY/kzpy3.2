#!/usr/bin/env python
from kzpy3.vis2 import *
clear_timer = Timer(1)
#clf();plt_square();xysqlim(2.1);
img = zeros((440,440,3),np.uint8)
while True:
	try:
		l = txt_file_to_list_of_strings(opjD('Mr_Black.txt'))
		exec('pose = '+l[0])
		if len(pose) == 4:
			if clear_timer.check():
				img *= 0
				clear_timer.reset()
			img[210+int(100*pose[0]),210+int(100*pose[1]),0]=255;
		mci(img,delay=5)
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		print(d2s('oops',time.time())

