
import math_op as mo 
import numpy as np

class Grid(object):

    def __init__(self, dim, data, weights=1, vec=False):
        self.dim        = dim
        self.points(data, vec)
        # implement a rho array seperately
        # think about implementing Lat/lon grid seperately as well
        # can i guarantee that orders are not jumbled up?
        # thus the averaging is done independently from GRIDs 
        # done instead as function on grids. 
 
        
        # automatic weighting
        self.multiply(weights)

    
    def multiply(self, B):
        #multiplying a grid with another grid
        if type(B) is Grid:
            do.grid_mult(self, B)

    def points(self, data, vec):
        dim    = self.dim
        if vec:
            self.data = [[[Dyadic(data[i][j][k])
                            for k in range(dim[2])]
                                for j in range(dim[1])]
                                    for i in range(dim[0])]
          
        else:
            self.data = [[[data[i][j][k]
                            for k in range(dim[2])]
                                for j in range(dim[1])]
                                    for i in range(dim[0])]

    def avg(self, area, center, kind='norm', rho, grid):
        '''computing averages of an area, contained
           within an ortosphere of radius 'area'[m] around 'center'[°].
           Three kinds of averages are possible:
           norm:    simple average of all hexes, whose centers are
                    within the orthosphere
           dist:    distance weigthed average onto the center of orthosphere
                    (to be used, if center of orthosphere is not coinciding 
                    with a hex center)
           hat:     density weighted average of all hexes, whose centers are
                    within the ortosphere'''
        R = earthRadius
        r = area/R
        data    = self.data
        for zdim in range(self.dim[0]):
            # if lon lat grid is independent of zdim we can save one loop here. 
            for ydim in range(self.dim[1]):
                for xdim in range(self.dim[2]):
                    members = in_orthosphere(r, 
                                             grid[zdim][ydim][xdim].data,
                                             grid[zdim], 
                                             self.dim[1:2])
                    if kind == 'norm':
                        avg = 
                        for member in members:



                    elif kind == 'hat':

                    elif kind == 'dist':
                    
                    else:
                        print 'error unknown kind of averaging chosen!'


    def avg(self, area):
        '''computing the average overwriting original data'''
        #where area is number of points in one direction:
        #true area'd be 2*area*2*area
        # this function overwrites the information within!
        data    = self.data
        for zdim in range(self.dim[0]):
            for ydim in range(self.dim[1]):
                for xdim in range(self.dim[2]):
                    self.data[zdim][ydim][xdim]= mo.bar_avg(
                                                            area,
                                                            [zdim,ydim,xdim],
                                                            data
                                                            )

    def hat_avg(self, area, rho_in):
        '''computing the average overwriting original data'''
        if self.dim == rho.dim:

            rho     = rho_in

            # making rho * qty and averaging
            self.multiply(rho)
            self.avg(area)

            # averaging rho
            rho.avg(area)

            for z in range(self.dim[0]):
                for y in range(self.dim[1]):
                   for x in range(self.dim[2]):
                        self.data[z][y][x].mutiply(rho.data[z][y][x]) 


class Dyadic(object):

    def __init__(self, data):
        self.dim    = len(data)
        self.data   = data 
        self.center = [lat,lon]


    def multiply(self, B):
        #multiplying this with anoteher class Dyadic
        if type(B) is Dyadic:
            if type(B.data[0]) is list:
                self.data =  mo.tensor_mult(self, B)
            else:
                self.data =  mo.vector_mult(self, B)
        else:
            #assume a scalar
            if type(self.data[0]) is list:
                self.data   = [[self.data[k][j] * B
                                for j in range(len(self.data[0]))]
                                for k in range(len(self.data))]
            else:
                self.data   = [i*B for i in self.data]

    def add(self, B):
        if type(B) is Dyadic:
            return self.data + B.data

