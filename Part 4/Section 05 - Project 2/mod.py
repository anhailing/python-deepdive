from functools import total_ordering
import operator

@total_ordering
class Mod:
    def __init__(self, value, modulus):
        if not isinstance(value, int):
            raise TypeError('Value must be an integer')
        if not isinstance(modulus, int):
            raise TypeError('Modulus must be an integer')
        if modulus <= 0:
            raise ValueError('Modulus must be positive')
        self._modulus = modulus
        self._value = value % modulus

    @property
    def modulus(self):
        return self._modulus
    
    @property
    def value(self):
        return self._value
    
    # TODO why this?
    @value.setter  
    def value(self, new_value):
        self._value = new_value % self.modulus 
        
    def __repr__(self):
        return f'Mod({self._value}, {self._modulus})'
    
    def __int__(self):
        return self.value
    
    def _get_value(self, other):
        if isinstance(other, Mod) and self.modulus == other.modulus:
            return other.value
        if isinstance(other, int):
            return other % self.modulus
        return NotImplemented
    
    def _perform_operation(self, other, op):
        other_value = self._get_value(other)
        new_value = op(self.value, other_value)
        return Mod(new_value, self.modulus)
    
    def __eq__(self, other):
        other_value = self._get_value(other)
        return self.value == other_value
        
    def __hash__(self):
        return hash((self.value, self.modulus))

    def __neg__(self):
        return Mod(-self.value, self.modulus)
    
    def __add__(self, other):
        return self._perform_operation(other, operator.add)
    
    def __sub__(self, other):
        return self._perform_operation(other, operator.sub)
    
    def __mul__(self, other):
        return self._perform_operation(other, operator.mul)
    
    def __pow__(self, other):
        return self._perform_operation(other, operator.pow)
        
    def _iadd__(self, other):
        return self + other
    
    def _isub__(self, other):
        return self - other
    
    def _imul__(self, other):
        return self * other
    
    def _ipow__(self, other):
        return self ** other
        
    def __lt__(self, other):
        other_value = self._get_value(other)
        return self.value < other_value
    



    
        
