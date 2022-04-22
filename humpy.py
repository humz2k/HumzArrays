class hparrayiter:
    def __init__(self, array):
        self._array = array
        self._index = 0
    def __next__(self):
        if self._index < self._array.shape[0]:
            result = self._array.array[self._index]
            self._index += 1
            return result
        raise StopIteration

class hparray:
    def __init__(self,array=None,shape=None,override=False):
        assert array != None or shape != None
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
                        self.array[idx] = hparray(array=i,shape=self.shape[1:])
                    else:
                        self.array[idx] = i

    def __getitem__(self, i):
        print(i)
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
            return hparray(array = out,shape = new_shape,override=True)
        elif isinstance(i,tuple):
            if any(isinstance(x,slice) for x in i):
                raise Exception("NOT IMPLEMENTED")
            else:
                new_shape = (len(i),) + self.shape[1:]
                out = {}
                count = 0
                for idx in i:
                    out[count] = self.array[idx]
                    count += 1
                return hparray(array = out,shape=new_shape,override=True)
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
        if isinstance(other,hparray):
            if len(other.shape) == 1 and other.shape[0] == 1:
                if len(self.shape) == 1:
                    for i in range(self.shape[0]):
                        self.array[i] += other.array[0]
                else:
                    for i in range(self.shape[0]):
                        self.array[i].__add__(other)
            elif other.shape == self.shape:
                if len(self.shape) == 1:
                    for i in range(self.shape[0]):
                        self.array[i] += other.array[i]
                else:
                    for i in range(self.shape[0]):
                        self.array[i].__add__(other.array[i])
            else:
                if len(other.shape) == len(self.shape):
                    raise Exception("shape error")
                for i in range(other.shape[0]):
                    self.__add__(other.array[i])
        else:
            if len(self.shape) == 1:
                for i in range(self.shape[0]):
                    self.array[i] += other
            else:
                for i in range(self.shape[0]):
                    self.array[i].__add__(other)
        return self


test = hparray([1,2,3])
test2 = hparray([[1,1,1],[2,2,2],[3,3,3]])
print(hparray([test]))
