from enum import Enum
import copy
import warnings

inf = float('inf')

class hparrayiter:
    def __init__(self, array):
        self._array = array
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index < self._array.shape[0]:
            result = self._array.array[self._index]
            self._index += 1
            return result
        raise StopIteration

class hparray:
    def __init__(self,array=None,shape=None,override=False,this_type=None):
        assert array != None or shape != None
        self.type = this_type
        if override:
            self.array = array
            self.shape = shape
        else:
            self.array = {}
            self.shape = shape
            if array != None:
                if shape == None:
                    self.shape = []
                    current = array
                    while isinstance(current,list):
                        self.shape.append(len(current))
                        current = current[0]
                    self.shape = tuple(self.shape)
                if len(array) != self.shape[0]:
                    raise Exception("Array Shape Error")
                for idx in range(self.shape[0]):
                    i = array[idx]
                    if isinstance(i,list):
                        self.array[idx] = hparray(array=i,shape=self.shape[1:],this_type=self.type)
                    else:
                        if self.type != None:
                            self.array[idx] = self.type(i)
                        else:
                            self.array[idx] = i
        self.ndim = len(self.shape)

    def __setitem(self,item,value):
        assert type(item) is int
        assert item >= 0 and item < self.shape[0]
        if isinstance(self.array[item],hparray):
            assert isinstance(value,hparray)
            assert value.shape == self.array[item].shape
            self.array[item] = value
        else:
            assert not isinstance(value,hparray)
            if self.type != None:
                value = self.type(value)
            self.array[item] = value

    def __getitem__(self, i):
        if isinstance(i,slice):
            step = i.step
            if step == None:
                step = 1
            backwards = step < 0
            start = i.start
            if start == None:
                if backwards:
                    start = self.shape[0]-1
                else:
                    start = 0
            stop = i.stop
            if stop == None:
                if backwards:
                    stop = -1
                else:
                    stop = self.shape[0]
            out = {}
            r = range(start,stop,step)
            new_shape = (len(r),) + self.shape[1:]
            count = 0
            for idx in range(start,stop,step):
                out[count] = self.array[idx]
                count += 1
            return hparray(array = out,shape = new_shape,this_type = self.type,override=True)
        elif isinstance(i,tuple):
            if any(isinstance(x,slice) for x in i):
                current = self
                sliced = False
                for j in i:
                    if not sliced:
                        current = current.__getitem__(j)
                        if isinstance(j,slice):
                            sliced = True
                    else:
                        if j == None:
                            j = 0
                        temp = current
                        def traverse(temp):
                            if temp.ndim == 1:
                                return temp.array[j]
                            else:
                                out = []
                                for i in range(temp.shape[0]):
                                    out.append(traverse(temp.array[i]))
                                return out
                        return hparray(array = traverse(temp),this_type = self.type)
                return current
            else:
                new_shape = (len(i),) + self.shape[1:]
                out = {}
                count = 0
                for idx in i:
                    out[count] = self.array[idx]
                    count += 1
                return hparray(array = out,shape=new_shape,this_type = self.type,override=True)
        else:
            if i < 0:
                i += self.shape[0]
            try:
                return self.array[i]
            except:
                raise Exception("Index out of range")

    def __len__(self):
        return self.shape[0]

    def __iter__(self):
        return hparrayiter(self)

    def __str__(self):
        if len(self.shape) == 1:
            out = "["
            for i in range(self.shape[0]-1):
                out += str(self.array[i]) + ","
            out += str(self.array[self.shape[0]-1])
            return out + "]"
        else:
            out = "["
            for i in range(self.shape[0]-1):
                out += self.array[i].__str__() + ","
            out += self.array[self.shape[0]-1].__str__()
        return out + "]"

    def __add__(self,other):
        out = copy.deepcopy(self)
        if isinstance(other,hparray):
            if len(other.shape) == 1 and other.shape[0] == 1:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] += other.array[0]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__add__(other)
            elif other.shape == out.shape:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] += other.array[i]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__add__(other.array[i])
            else:
                if len(other.shape) == len(out.shape):
                    raise Exception("shape error")
                for i in range(other.shape[0]):
                    if isinstance(out.array[i],hparray):
                        out.array[i].__add__(other.array[i])
                    else:
                        if isinstance(other.array[i],hparray):
                            for j in other.array[i]:
                                out.array[i] += j
                        else:
                            out.array[i] += other.array[i]
        else:
            if len(out.shape) == 1:
                for i in range(out.shape[0]):
                    out.array[i] += other
            else:
                for i in range(out.shape[0]):
                    out.array[i].__add__(other)
        return out

    def __sub__(self,other):
        out = copy.deepcopy(self)
        if isinstance(other,hparray):
            if len(other.shape) == 1 and other.shape[0] == 1:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] -= other.array[0]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__sub__(other)
            elif other.shape == out.shape:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] -= other.array[i]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__sub__(other.array[i])
            else:
                if len(other.shape) == len(out.shape):
                    raise Exception("shape error")
                for i in range(other.shape[0]):
                    if isinstance(out.array[i],hparray):
                        out.array[i].__sub__(other.array[i])
                    else:
                        if isinstance(other.array[i],hparray):
                            for j in other.array[i]:
                                out.array[i] -= j
                        else:
                            out.array[i] -= other.array[i]
        else:
            if len(out.shape) == 1:
                for i in range(out.shape[0]):
                    out.array[i] -= other
            else:
                for i in range(out.shape[0]):
                    out.array[i].__sub__(other)
        return out

    def __mul__(self,other):
        out = copy.deepcopy(self)
        if isinstance(other,hparray):
            if len(other.shape) == 1 and other.shape[0] == 1:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] *= other.array[0]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__mul__(other)
            elif other.shape == out.shape:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] *= other.array[i]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__mul__(other.array[i])
            else:
                if len(other.shape) == len(out.shape):
                    raise Exception("shape error")
                for i in range(other.shape[0]):
                    if isinstance(out.array[i],hparray):
                        out.array[i].__mul__(other.array[i])
                    else:
                        if isinstance(other.array[i],hparray):
                            for j in other.array[i]:
                                out.array[i] *= j
                        else:
                            out.array[i] *= other.array[i]
        else:
            if len(out.shape) == 1:
                for i in range(out.shape[0]):
                    out.array[i] *= other
            else:
                for i in range(out.shape[0]):
                    out.array[i].__mul__(other)
        return out

    def __truediv__(self,other):
        out = copy.deepcopy(self)
        if isinstance(other,hparray):
            if len(other.shape) == 1 and other.shape[0] == 1:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        if other.array[0] == 0:
                            warnings.warn("Div0", RuntimeWarning)
                            out.array[i] = inf
                        else:
                            out.array[i] /= other.array[0]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__truediv__(other)
            elif other.shape == out.shape:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        if other.array[i] == 0:
                            warnings.warn("Div0", RuntimeWarning)
                            out.array[i] = inf
                        else:
                            out.array[i] /= other.array[i]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__truediv__(other.array[i])
            else:
                if len(other.shape) == len(out.shape):
                    raise Exception("shape error")
                for i in range(other.shape[0]):
                    if isinstance(out.array[i],hparray):
                        out.array[i].__truediv__(other.array[i])
                    else:
                        if isinstance(other.array[i],hparray):
                            for j in other.array[i]:
                                if j == 0:
                                    warnings.warn("Div0", RuntimeWarning)
                                    out.array[i] = inf
                                else:
                                    out.array[i] /= j
                        else:
                            if other.array[i] == 0:
                                warnings.warn("Div0", RuntimeWarning)
                                out.array[i] = inf
                            else:
                                out.array[i] /= other.array[i]
        else:
            if len(out.shape) == 1:
                for i in range(out.shape[0]):
                    if other == 0:
                        warnings.warn("Div0", RuntimeWarning)
                        out.array[i] = inf
                    else:
                        out.array[i] /= other
            else:
                for i in range(out.shape[0]):
                    out.array[i].__truediv__(other)
        return out

    def __pow__(self,other):
        out = copy.deepcopy(self)
        if isinstance(other,hparray):
            if len(other.shape) == 1 and other.shape[0] == 1:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] **= other.array[0]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__pow__(other)
            elif other.shape == out.shape:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        out.array[i] **= other.array[i]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__pow__(other.array[i])
            else:
                if len(other.shape) == len(out.shape):
                    raise Exception("shape error")
                for i in range(other.shape[0]):
                    if isinstance(out.array[i],hparray):
                        out.array[i].__pow__(other.array[i])
                    else:
                        if isinstance(other.array[i],hparray):
                            for j in other.array[i]:
                                out.array[i] **= j
                        else:
                            out.array[i] **= other.array[i]
        else:
            if len(out.shape) == 1:
                for i in range(out.shape[0]):
                    out.array[i] **= other
            else:
                for i in range(out.shape[0]):
                    out.array[i].__pow__(other)
        return out

    def __floordiv__(self,other):
        out = copy.deepcopy(self)
        if isinstance(other,hparray):
            if len(other.shape) == 1 and other.shape[0] == 1:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        if other.array[0] == 0:
                            warnings.warn("Div0", RuntimeWarning)
                            out.array[i] = inf
                        else:
                            out.array[i] //= other.array[0]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__floordiv__(other)
            elif other.shape == out.shape:
                if len(out.shape) == 1:
                    for i in range(out.shape[0]):
                        if other.array[i] == 0:
                            warnings.warn("Div0", RuntimeWarning)
                            out.array[i] = inf
                        else:
                            out.array[i] //= other.array[i]
                else:
                    for i in range(out.shape[0]):
                        out.array[i].__floordiv__(other.array[i])
            else:
                if len(other.shape) == len(out.shape):
                    raise Exception("shape error")
                for i in range(other.shape[0]):
                    if isinstance(out.array[i],hparray):
                        out.array[i].__floordiv__(other.array[i])
                    else:
                        if isinstance(other.array[i],hparray):
                            for j in other.array[i]:
                                if j == 0:
                                    warnings.warn("Div0", RuntimeWarning)
                                    out.array[i] = inf
                                else:
                                    out.array[i] //= j
                        else:
                            if other.array[i] == 0:
                                warnings.warn("Div0", RuntimeWarning)
                                out.array[i] = inf
                            else:
                                out.array[i] //= other.array[i]
        else:
            if len(out.shape) == 1:
                for i in range(out.shape[0]):
                    if other == 0:
                        warnings.warn("Div0", RuntimeWarning)
                        out.array[i] = inf
                    else:
                        out.array[i] //= other
            else:
                for i in range(out.shape[0]):
                    out.array[i].__floordiv__(other)
        return out

def array(object,dtype=None):
    return hparray(array=object,this_type=dtype)

def sqrt(x):
    return x ** (1/2)

test = array([10,10,10,10],dtype=int)
yeet = array([1,1,10,100],dtype=int)
print(yeet.shape)
print(test.shape)
test2 = sqrt(test)
print(test2)
