print('pytorch2/Data_preload')

from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch2/Train_SqueezeNet'])
import Parameters as P


hdf5_runs_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/runs')
hdf5_segment_metadata_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/segment_metadata')


print('\nloading low_steer... (takes awhile)')
low_steer = load_obj(opj(hdf5_segment_metadata_path,'low_steer'))
random.shuffle(low_steer)
print('\nloading high_steer... (takes awhile)')
high_steer = load_obj(opj(hdf5_segment_metadata_path,'high_steer'))
random.shuffle(high_steer)
print('done')
len_high_steer = len(high_steer)
len_low_steer = len(low_steer)
ctr_low = -1
ctr_high = -1
if P.DISPLAY:
    from kzpy3.vis import *
    figure(P.HIGH_LOW_HISTOGRAM_FIGURE_NAME,figsize=(2,1))
    histogram_plot_there = True
    clf()
    plt.hist(array(low_steer)[:,2],bins=range(0,100))
    plt.hist(array(high_steer)[:,2],bins=range(0,100))
    pause(0.001)
    #figure(1)
all_steer = low_steer + high_steer




def prepare_Aruco_trajectory_data():

    CS_('load aruco trajectory data')
    Aruco_Steering_Trajectories = {}
    aruco_data_location = opjD('output_data')
    paths = sggo(aruco_data_location,'*.pkl')
    for i in range(len(paths)):
        o = paths[i]
        ast = lo(o)
        for run_name in ast.keys(): 
            print(d2n(run_name,' (',i+1,' of ',len(paths),')'))
            if run_name not in Aruco_Steering_Trajectories:
                Aruco_Steering_Trajectories[run_name] = {}
            if len(ast[run_name].keys()) > 4:
                print_stars()
                continue
            for mode in ast[run_name].keys():
                print('\t'+mode)
                if mode not in Aruco_Steering_Trajectories[run_name]:
                    Aruco_Steering_Trajectories[run_name][mode] = {}
                timestamps = ast[run_name][mode]['near_t']
                dd = ast[run_name][mode]['desired_direction'][0]
                print('\t\t'+str(dd))
                Aruco_Steering_Trajectories[run_name][mode][dd] = {}
                for i in range(len(timestamps)):
                    t = timestamps[i]
                    Aruco_Steering_Trajectories[run_name][mode][dd][t] = {}
                    for topic in ast[run_name][mode].keys():
                        if topic not in ['near_t','desired_direction']:
                            q = ast[run_name][mode][topic][i]
                            if not(is_number(q)):
                                q = array(q)
                                q = q.astype(np.float16)
                            else:
                                q = np.float16(q)
                            Aruco_Steering_Trajectories[run_name][mode][dd][t][topic] = q
    ctr = 0
    for run_name in Aruco_Steering_Trajectories.keys():
        if 'flip_' in run_name:
            del Aruco_Steering_Trajectories[run_name]
            continue
        flip = 'flip_'+run_name
        print(d2n(flip,' (',ctr+1,' of ',len(paths),')'))
        ctr += 1
        Aruco_Steering_Trajectories[flip]= {}
        for mode in Aruco_Steering_Trajectories[run_name]:
            Aruco_Steering_Trajectories[flip][mode] = {}
            for dd in [0,1]:
                Aruco_Steering_Trajectories[flip][mode][dd] = {}
                for t in Aruco_Steering_Trajectories[run_name][mode][dd].keys():
                    Aruco_Steering_Trajectories[flip][mode][dd][t] = {}
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['steer'] = np.float16(99-Aruco_Steering_Trajectories[run_name][mode][dd][t]['steer'])
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['velocity'] = np.float16(Aruco_Steering_Trajectories[run_name][mode][dd][t]['velocity'])
                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['other_car_inverse_distances'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['other_car_inverse_distances'] = l
                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['marker_inverse_distances'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['marker_inverse_distances'] = l
                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['potential_values'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['potential_values'] = l

                    l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['clock_potential_values'])
                    l.reverse(); l = array(l); l = l.astype(np.float16)
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['clock_potential_values'] = l

                    if dd == 0:
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 1
                    else:
                        Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 0
                    Aruco_Steering_Trajectories[flip][mode][dd][t]['relative_heading'] =  np.float16(360 - Aruco_Steering_Trajectories[run_name][mode][dd][t]['relative_heading'])

    unix('mkdir -p '+opjD('Aruco_Steering_Trajectories'))
    ctr = 0
    for run_name in sorted(Aruco_Steering_Trajectories.keys()):
        print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
        so(Aruco_Steering_Trajectories[run_name],opjD('Aruco_Steering_Trajectories',run_name))
        ctr += 1
    raw_input('enter')




def load_Aruco_Steering_Trajectories():
    print("Loading Aruco_Steering_Trajectories . . .")
    paths = sggo(opjD('Aruco_Steering_Trajectories','*.pkl'))
    Aruco_Steering_Trajectories = {}
    ctr = 0
    for p in paths:
        o = lo(p)
        run_name = fname(p).replace('.pkl','')
        print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
        Aruco_Steering_Trajectories[run_name] = o
        ctr += 1
    return Aruco_Steering_Trajectories






if P.LOAD_ARUCO:
    Aruco_Steering_Trajectories = load_Aruco_Steering_Trajectories()


