from kzpy3.caf.utils import *

model_name = 'VGG_ILSVRC_16_layers'
#model_name = 'bvlc_googlenet'
#model_name = 'bvlc_reference_caffenet'

net = get_net(model_name)
print(np.shape(net.blobs['data'].data))
img_name = 'cat.jpg'
img = imread(opjh('caffe/examples/images',img_name))
img = img[:,:,:3]

if model_name == 'VGG_ILSVRC_16_layers':
    net.blobs['data'].reshape(1,3,224,224)
    img = imresize(img,(224,224,3))
else:
    net.blobs['data'].reshape(1,3,227,227)
    img = imresize(img,(227,227,3))
print(np.shape(net.blobs['data'].data))

net.blobs['data'].data[0,0,:,:] =img[:,:,2]
net.blobs['data'].data[0,1,:,:] =img[:,:,1]
net.blobs['data'].data[0,2,:,:] =img[:,:,0]

net.forward();
activations = {}

for k in net.blobs.keys():
    activations[k] = net.blobs[k].data.copy()
    if len(shape(activations[k])) == 4:
        a = activations[k].mean(axis=2)
        b = a.mean(axis=2)
        for x in range(shape(activations[k])[2]):
            for y in range(shape(activations[k])[3]):
                activations[k][:,:,x,y]=b

    
objective_dic = get_objective_dic(model_name,activations)

ml = sorted(objective_dic.keys(),key=natural_keys)
print(ml)

'''
Layer catelogue

bvlc_googlenet:
    ['conv1', 'conv2', 'conv3', 'conv4', 'conv5', 'fc6', 'fc7', 'fc8', 'prob']

VGG_ILSVRC_16_layers:
    ['conv1_1', 'conv1_2', 'conv2_1', 'conv2_2', 'conv3_1', 'conv3_2', 'conv3_3',
     'conv4_1', 'conv4_2', 'conv4_3', 'conv5_1', 'conv5_2', 'conv5_3', 'fc6', 'fc7', 'fc8', 'prob']

bvlc_googlenet:
    ['conv1/7x7_s2', 'conv2/3x3', 'inception_3a/1x1', 'inception_3a/3x3', 'inception_3a/5x5',
    'inception_3a/output', 'inception_3b/1x1', 'inception_3b/3x3', 'inception_3b/5x5',
    'inception_3b/output', 'inception_4a/1x1', 'inception_4a/3x3', 'inception_4a/5x5',
    'inception_4a/output', 'inception_4b/1x1', 'inception_4b/3x3', 'inception_4b/5x5',
    'inception_4b/output',
    'inception_4c/1x1', 'inception_4c/3x3', 'inception_4c/5x5', 'inception_4c/output',
    'inception_4d/1x1', 'inception_4d/3x3', 'inception_4d/5x5', 'inception_4d/output',
    'inception_4e/1x1', 'inception_4e/3x3', 'inception_4e/5x5', 'inception_4e/output',
    'inception_5a/1x1', 'inception_5a/3x3', 'inception_5a/5x5', 'inception_5a/output',
    'inception_5b/1x1', 'inception_5b/3x3', 'inception_5b/5x5', 'inception_5b/output', 'prob']
'''

inception_outputs = ['conv1/7x7_s2', 'conv2/3x3', 
    'inception_3a/output', 
    'inception_3b/output', 
    'inception_4a/output', 
    'inception_4c/output',
    'inception_4d/output',
    'inception_4e/output',
    'inception_5a/output',
    'inception_5b/output']
VGG_convs = ['conv1_1', 'conv1_2', 'conv2_1', 'conv2_2', 'conv3_1', 'conv3_2', 'conv3_3',
     'conv4_1', 'conv4_2', 'conv4_3', 'conv5_1', 'conv5_2', 'conv5_3']

if __name__ == '__main__':
    backprop_diffs_to_data(
        model_name,
        ['conv3_1'],#ml,#['conv1_1','conv1_2','conv2_1','conv2_2','conv3_1','conv3_2'],#, 'conv2/3x3'],#, 'inception_3a/1x1', 'inception_3a/3x3', 'inception_3a/5x5','inception_3a/output'],# ml,
        objective_dic,
        net,100,
        opjh('scratch/2015/10/17',model_name),
        '.'.join([img_name,'all']))# 'to 10')

