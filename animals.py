import numpy as np
'''
This file contains the functions used to perform the GUI oriented object tracking analysis calculations.
'''

def displacement(file):
    '''
    Computes the total displacement of the object

    .. math:: R = \\sum_{i=1}^{N}r_{i,i-1}

    where :math: `r_{i,i-1}` is the length of the vector connecting the `i`-th and `i-1`-th positions

    :param file: the trajectory file where the trajectory data was written

    :return displacement_: total displacement as float
    '''
    file = np.loadtxt(str(file),delimiter=',')
    dis = np.sum(np.sqrt(np.sum(np.diff(file[:,1:],axis=0)**2,axis=1)))
    displacement_ = str(np.round(dis,2))
    return displacement_

def time_center(x1,x2,y1,y2,file):
    '''
    Computes the time, in seconds, spent by the object inside the squared/rectangular region bounded by its four corners.
    The corners are mapped by the corresponding x and y cartesian coordinate combinations,

    where :math: `x_1 < x_2` and `y_1 < y_2`

    :param x1: X coordinate of the corner closest to the origin
    :param x2: X coordinate of the corner further away from the origin
    :param y1: Y coordinate of the corner closest to the origin
    :param y2: Y coordinate of the corner further away from the origin
    :param file: the trajectory file where the trajectory data was written

    :return time_inside: returns the time spent within the bounded region as a string
    '''
    tc = 0
    file = np.loadtxt(str(file),delimiter=',')

    for i in range (file.shape[0]-1):
        if (file[i,1] > x1 and file[i,1] < x2 and file[i,2] > y1 and file[i,2] < y2):
            if (file[i+1,1] > x1 and file[i+1,1] < x2 and file[i+1,2] > y1 and file[i+1,2] < y2):
                tc += file[i+1,0] - file[i,0]
    time_inside = str(np.round(tc,2))
    return time_inside

def time_edges(x1,x2,y1,y2,file):
    '''
    Computes the time, in seconds, spent by the object outside the squared/rectangular region bounded by its four corners.
    The corners are mapped by the corresponding x and y cartesian coordinate combinations,

    where :math: `x_1 < x_2` and `y_1 < y_2`

    :param x1: X coordinate of the corner closest to the origin (top left corner)
    :param x2: X coordinate of the corner further away from the origin (top left corner)
    :param y1: Y coordinate of the corner closest to the origin (top left corner)
    :param y2: Y coordinate of the corner further away from the origin (top left corner)
    :param file: the trajectory file where the trajectory data was written

    :return time_outside: returns the time spent outside the bounded region as a string
    '''
    file = np.loadtxt(str(file),delimiter=',')

    te = 0
    for i in range(file.shape[0]-1):
        if (file[i,1] < x1 or file[i,1] > x2): 
            if (file[i+1,1] < x1 or file[i+1,1] > x2): 
                te += file[i+1,0] - file[i,0]
            elif (file[i+1,1] > x1 and file[i+1,1] < x2) and (file[i+1,2] < y1 or file[i+1,2] > y2): 
                te += file[i+1,0] - file[i,0]

        elif (file[i,1] > x1 and file[i,1] < x2) and (file[i,2] < y1 or file[i,2] > y2): 
            if (file[i+1,1] < x1 or file[i+1,1] > x2): 
                te += file[i+1,0] - file[i,0]
            elif (file[i+1,1] > x1 and file[i+1,1] < x2) and (file[i+1,2] < y1 or file[i+1,2] > y2): 
                te += file[i+1,0] - file[i,0]
    time_outside = str(np.round(te,2))
    return time_outside