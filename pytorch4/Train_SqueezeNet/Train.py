from kzpy3.utils2 import *
from vis2 import *
import torch
import Data
import Batch
import Utils
import Parameters as P

# Set Up PyTorch Environment
torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(P.GPU)
torch.cuda.device(P.GPU)

from SqueezeNet import SqueezeNet
net = SqueezeNet().cuda()
criterion = torch.nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(net.parameters())

if args.resume_path is not None:
    cprint('Resuming w/ ' + args.resume_path, 'yellow')
    save_data = torch.load(args.resume_path)
    net.load_state_dict(save_data)
    # loss_record_loaded = zload_obj({'path':opjD('loss_record')})
    # loss_record = {}
    # for mode in ['train','val']:
    #     loss_record[mode] = Utils.Loss_Record()
    #     for k in loss_record_loaded[mode].keys():
    #         if not callable(loss_record[mode][k]):
    #             loss_record[mode][k] = loss_record_loaded[mode][k]
else:
    loss_record = {}
    loss_record['train'] = Utils.Loss_Record()
    loss_record['val'] = Utils.Loss_Record()

rate_counter = Utils.Rate_Counter()

data = Data.Data()

timer = {}
timer['train'] = Timer(60*30)
timer['val'] = Timer(60*3)
print_timer = Timer(args.print_time)

trial_loss_record = {}

batch = Batch.Batch(net)

while True:
    for mode, data_index in [('train', data.train_index), 
                             ('val', data.val_index)]:
        timer[mode].reset()
        while not timer[mode].check():

            batch.fill(data, data_index)  # Get batches ready
            batch.forward(optimizer, criterion, trial_loss_record) # Run net

            if mode == 'train':  # Backpropagate
                batch.backward(optimizer)

            loss_record[mode].add(batch.loss.data[0])
            Utils.save_net(net, loss_record)
            rate_counter.step()

            if print_timer.check():
                batch = Batch.Batch(net)  # Reinitialiize batch

                print('mode=' + mode)
                print('ctr=' + str(data.ctr))
                print('epoch progress=' + str(100 * data_index.ctr /
                                              len(data_index.all_steer)) + '%')

                batch.display()

                plt.figure('loss')
                plt.clf()  # clears figure
                plt.ylim(0.004, 0.015) # range
                loss_record['train']['plot']('b')  # plot with blue color
                loss_record['val']['plot']('r')  # plot with red color
                print_timer.reset()

# import operator
# sorted_trial_loss_record = sorted(trial_loss_record.items(),key=operator.itemgetter(1))
# 
# for i in range(-1,-100,-1):
#     l =  sorted_trial_loss_record[i]
#     run_code,seg_num,offset = sorted_trial_loss_record[i][0][0]
#     t = sorted_trial_loss_record[i][0][1]
#     o = sorted_trial_loss_record[i][0][2]
#     data = DD['get_data']({'run_code':run_code,'seg_num':seg_num,'offset':offset})
#     figure(22);clf();ylim(0,1)
#     plot(t,'r.')
#     plot(o,'g.')
#     plot([0,20],[0.5,0.5],'k')
#     mi(data['right'][0,:,:],23,img_title=d2s(l[1]))
#     pause(1)

#EOF
