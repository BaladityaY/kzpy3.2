from kzpy3.vis import *
import h5py

import caffe
USE_GPU = True
gpu = 1
if USE_GPU:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()
from kzpy3.caf6.Caffe_Net import *


def plot_performance(steer,motor,loss1000):
	figure('loss1000')
	clf()
	plot(loss1000)
	plt.ylim(0.04,0.06)
	plt.title(time_str('Pretty'))
	plt.xlabel(solver_file_path)
	figure('steer')
	clf()

	s1000 = steer[-(min(len(steer),10000)):]
	s = array(s1000)
	plot(s[:,0],s[:,1],'o')
	plt.xlim(0,1.0)
	plt.ylim(0,1.0)
	plot([-1,5,1.5],[-1,5,1.5],'r')
	plt_square()
	plt.title(time_str('Pretty'))
	plt.xlabel(solver_file_path)

#solver_file_path = opjh("kzpy3/caf6/z2_color/solver_"+str(gpu)+"_a.prototxt")
solver_file_path = opjh("kzpy3/caf6/z2_color_small/solver.prototxt")
version = 'version 1b'
weights_file_mode = 'most recent' #None #'this one' #None #'most recent' #'this one'  #None #'most recent'
weights_file_path = opjD('z2_color_small') #None #opjh('kzpy3/caf6/z2_color/z2_color.caffemodel') #None #'/home/karlzipser/Desktop/z2_color' # None #opjD('z2_color')

caffe_net = Caffe_Net(solver_file_path,version,weights_file_mode,weights_file_path,True)





runs_folder = '/media/karlzipser/ExtraDrive1/runs'
run_names = sorted(gg(opj(runs_folder,'*.hdf5')),key=natural_keys)
solver_inputs_dic = {}
keys = {}
k_ctr = 0
for hdf5_filename in run_names:
	try:
		solver_inputs_dic[hdf5_filename] = h5py.File(hdf5_filename,'r')
		print hdf5_filename
		kk = solver_inputs_dic[hdf5_filename].keys()
		for k in kk:
			keys[k] = hdf5_filename
			k_ctr += 1
	except Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)

ks = keys.keys()




cprint(d2s('Using',len(ks),'data entries'),'red','on_yellow')
ctr = 0

steer = []
motor = []

T = 6
timer = Timer(T)
id_timer = Timer(3*T)
while True:
	random.shuffle(ks)
	for k in ks:
		hdf5_filename = keys[k]
		solver_inputs = solver_inputs_dic[hdf5_filename]
		caffe_net.solver.net.blobs['ZED_data_pool2'].data[:] = solver_inputs[k]['ZED_data_pool2'][:]/255.-0.5
		caffe_net.solver.net.blobs['metadata'].data[:] = solver_inputs[k]['metadata'][:]
		caffe_net.solver.net.blobs['steer_motor_target_data'].data[:] = solver_inputs[k]['steer_motor_target_data'][:]
		caffe_net.train_step()
		steer.append([caffe_net.solver.net.blobs['steer_motor_target_data'].data[0,9],caffe_net.solver.net.blobs['ip2'].data[0,9]])
		motor.append([caffe_net.solver.net.blobs['steer_motor_target_data'].data[0,19],caffe_net.solver.net.blobs['ip2'].data[0,19]])
		ctr += 1
		if timer.check():
			plot_performance(steer,motor,caffe_net.loss1000)
			timer.reset()
		if id_timer.check():
			cprint(solver_file_path,'blue','on_yellow')
			id_timer.reset()
pass	






