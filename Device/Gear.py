from Device.Components import MechanicalComponents

# Interfaces
class Gear(MechanicalComponents):
    def __init__(self, name=None, material=None):
        super().__init__(name, material)
        self.z = None
        self.i = None
        self.i_inverse = None
    def calcParameter(self, input, inverse): pass
    def calcGear(self, z, inverse): pass

# Class
class MultiGear(Gear):
    def __init__(self, multi_gear=None, name=None, material=None):
        super().__init__(name, material)
        self.multi_gear = multi_gear
    
    def calcParameter(self, input, inverse):
        for index_gear in self.multi_gear:
            input *= index_gear.calcParameter(input, inverse)
        return input    
        
class SpurGear(Gear):
    def __init__(self,
                     z=[1, 2], 
                     material=None, 
                     name=None):
        super().__init__(name=name, material=material)
        self.z = z
        self.i = self.calcGear(z, True)
        self.i_inverse = self.calcGear(z, False)
        
    def calcParameter(self, input, inverse=False):
        """ Đây là hàm dùng để tính tham số của bánh răng thông qua tỷ số truyền như: Vòng xoay, vận tốc góc.
        Args:
            input (_type_): Đây là số bất kì của đại lượng nào đó thông qua tỷ số truyền.
            inverse (bool, optional): True - tức tính qua tỷ số truyền i_1n, False - tức tính qua tỷ số truyền i_n1

        Returns:
            _type_: Một giá trị cùng đại lượng với input
        """
        if inverse:
            return [input * self.i_inverse, self.i]
        else:
            return [input * self.i, self.i]
        
    def calcGear(self, z, inverse=False):
        """ Đây là hàm dùng để tính tỷ số truyền của hệ bánh răng thẳng
        Args:
            z (list): Có thể là Số răng, đường kính các vòng trên bánh răng.
            inverse (bool, optional): True - tức tính tỷ số truyền i_1n, False - tức tính tỷ số truyền i_n1

        Returns:
            _type_: Tỷ số truyền của hệ bánh răng thẳng
        """
        i = 1
        for index in range(len(z) - 1):
            i *= z[index + 1] / z[index]
        if inverse : i = 1/i
        return i