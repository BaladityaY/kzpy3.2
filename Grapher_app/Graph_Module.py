from Parameters_Module import *
from vis2 import *
exec(identify_file_str)

_ = dictionary_access

def Image2(*args):
    Args = args_to_dictionary(args)
    D = {}
    D[xmin] = Args[xmin] 
    D[xmax] = Args[xmax]
    D[ymin] = Args[ymin]
    D[ymax] = Args[ymax]
    D[xsize] = Args[xsize]
    D[ysize] = Args[ysize]
    if data_type in Args:
        D[data_type] = Args[data_type]
    else:
        D[data_type] = np.uint8
    True
    D[dic_type] = inspect.stack()[0][3]
    D[purpose] = d2s(D[dic_type],':','An image which translates from float coordinates.')
    D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
    D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
    D[img] = zeros((D[ysize],D[xsize],3),D[data_type]) #!!!
    def _function_floats_to_pixels(*args):
        Args = args_to_dictionary(args)
        xv = array(Args[x])
        yv = array(Args[y])
        xintv = ((xv-D[xmin])*D[xscale]).astype(np.int64)
        yintv = ((yv-D[ymin])*D[yscale]).astype(np.int64)
        return D[ysize]-yintv,xintv #!!!
    D[floats_to_pixels] = _function_floats_to_pixels
    def _function_pixels_to_floats(*args):
        Args = args_to_dictionary(args)
        return 'not implemented'
    D[pixels_to_floats] = _function_pixels_to_floats
    def _function_pts_plot(*args):
        Args = args_to_dictionary(args)
        xv,yv,colorv = Args[x],Args[y],Args[color]
        True
        D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
        D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
        xv,yv = D[floats_to_pixels](x,xv,y,yv)
        indiciesv = np.where(np.logical_and(yv>=0, yv<D[xsize]))
        xv = xv[indiciesv]
        yv = yv[indiciesv]        
        indiciesv = np.where(np.logical_and(xv>=0, xv<D[ysize])) # Note confusing reversals of x and y
        xv = xv[indiciesv]
        yv = yv[indiciesv]          #indiciesv = np.where(np.logical_and(yv>=0, yv<D[ysize]))
        #xv = xv[indiciesv]
        #yv = yv[indiciesv]        
        D[img][xv,yv,:] = colorv
    D[ptsplot] = _function_pts_plot
    return D



#EOF
