class hparray:
    def __init__(self,array=None,shape=None):
        assert array != None or shape != None
        if isinstance(array,list):
            self.array = {}
            self.__shape__ = len(array)
            self.end = False
            if array != None:
                for idx,i in enumerate(array):
                    self.array[idx] = hparray(i)
            self.__shape__ = [self.__shape__]
            to_add = []
            for i in self.array.keys():
                if self.array[i].__shape__ != 0:
                    to_add.append(self.array[i].__shape__)
            to_add = list(set(map(tuple,to_add)))

            if len(to_add) == 1:
                self.__shape__.append(to_add[0])
            elif len(to_add) == 0:
                pass
            else:
                exception("ARRAY ERROR")
            #print(list(self.shape))

            self.__shape__ = tuple(self.__shape__)
            temp = []
            current = self.__shape__
            while type(current) is tuple:
                temp.append(current[0])
                if len(current) == 1:
                    break
                if len(current) > 1:
                    current = current[1]
            self.shape = tuple(temp)

        else:
            self.array = {0:array}
            self.__shape__ = 0
            self.end = True

    def __getshape__(self):
        shapes = []
        for i in self.array.keys():
            if isinstance(self.array[i],hparray):
                print(self.array[i].shape)
        return shapes

test = hparray([[[1],[1],[3]],[[2],[2],[3]],[[3],[3],3]])
print(test.shape)
