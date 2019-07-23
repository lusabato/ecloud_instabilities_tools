import numpy as np


class obj_from_dict:
    def __init__(self, dictto):
        for kk in dictto.keys():
            exec 'self.'+kk +'= dictto[kk]'
            
            
def obj_to_dict(obj):
    dict_out={}
    members = dir(obj)
    for member in members:
        exec "dict_out['%s'] = obj.%s"%(member,member)
    return dict_out
            
def myloadmat(filename, squeeze = True):
    import scipy.io as sio
    dict_var=sio.loadmat(filename)
    if squeeze:
        for kk in dict_var.keys():
            try:
                dict_var[kk]=np.squeeze(dict_var[kk])
            except:
                pass
    return dict_var
    
            
            
def myloadmat_to_obj(filename, squeeze = True):
    return  obj_from_dict(myloadmat(filename, squeeze=squeeze))
    
    
def dict_of_arrays_and_scalar_from_h5(filename):
    import h5py
    with h5py.File(filename) as fid:
        f_dict = {}
        for kk in fid.keys():
            f_dict[kk] = np.array(fid[kk]).copy()
            if f_dict[kk].shape == ():
                f_dict[kk] = f_dict[kk].tolist()
    return  f_dict
    
def object_with_arrays_and_scalar_from_h5(filename):
    return  obj_from_dict(dict_of_arrays_and_scalar_from_h5(filename))
    
def monitorh5_to_dict(filename, key= 'Bunch'):
    import h5py
    with h5py.File(filename, 'r') as monitor_ev:
        monitor = monitor_ev[key]
        monitor_dict = {}
        for kk in monitor.keys():
            monitor_dict[kk] = np.array(monitor[kk]).copy()
        
    return monitor_dict
    

def monitorh5_to_obj(filename, key= 'Bunch'):
    return  obj_from_dict(monitorh5_to_dict(filename, key))
    

def monitorh5list_to_dict(filename_list, key= 'Bunch', flag_transpose=False):
    monitor_dict = monitorh5_to_dict(filename_list[0], key)
    for i_file in xrange(1,len(filename_list)):
        monitor_dict_curr = monitorh5_to_dict(filename_list[i_file], key)
        if flag_transpose:
            for kk in monitor_dict.keys():
                monitor_dict[kk] = np.array(list(monitor_dict[kk].T)+list(monitor_dict_curr[kk].T)).T
        else:
            for kk in monitor_dict.keys():
                monitor_dict[kk] = np.array(list(monitor_dict[kk])+list(monitor_dict_curr[kk]))
    return monitor_dict
    

def monitorh5list_to_obj(filename_list, key= 'Bunch', flag_transpose=False):
    return  obj_from_dict(monitorh5list_to_dict(filename_list, key, flag_transpose))

