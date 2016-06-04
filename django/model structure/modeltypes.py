import datetime
import json


# Utility functions
def _make_init(fields):
    '''
    Give a list of field names, make an __init__ method
    '''
    code = 'def __init__(self, %s):\n' % \
        ','.join(fields)

    for name in fields:
        code += '    self.%s = %s\n' % (name, name)
    return code



def _make_setter(dcls):
    code = 'def __set__(self, instance, value):\n'
    for d in dcls.__mro__:
        if 'set_code' in d.__dict__:
            for line in d.set_code():
                code += '    ' + line + '\n'
    return code



class DescriptorMeta(type):    
    def __init__(self, clsname, bases, clsdict):
        if '__set__' not in clsdict:
            code = _make_setter(self)
            exec(code, globals(), clsdict)
            setattr(self, '__set__', clsdict['__set__'])
        else:
            raise TypeError('Define set_code(), not __set__()')


class Descriptor(object):
    __metaclass__ = DescriptorMeta
    def __init__(self, name=None):
        self.name = name
    @staticmethod
    def set_code():
        return [
            'instance.__dict__[self.name] = value'
            ]
    def __delete__(self, instance):
        raise AttributeError("Can't delete")











class StructMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, clsname, bases, clsdict):
        fields = [key for key, val in clsdict.items()
                  if isinstance(val, Descriptor) ]
        for name in fields:
            clsdict[name].name = name

        # Make the init function
        if fields:
            exec(_make_init(fields), globals(), clsdict)

        clsobj = super(StructMeta,cls).__new__(cls, clsname, bases, dict(clsdict))
        setattr(clsobj, '_fields', fields)
        return clsobj


class Typed(Descriptor):
    ty = object
    @staticmethod
    def set_code():
        return [
            'if not isinstance(value, self.ty):',
            '    raise TypeError("Expected %s" % self.ty)'
            ]

# Specialized types
class Integer(Typed):
    ty = int

class Float(Typed):
    ty = float

class String(Typed):
    ty = str


class DateTime(Typed):
    ty = datetime.datetime

class Date(Typed):
    ty = datetime.datetime.date
        
class JSON(Typed):
    ty = json.load


class List(Typed):
    ty=list

# Value checking
class Positive(Descriptor):
    @staticmethod
    def set_code():
        return [
            'if value < 0:',
            '    raise ValueError("Expected >= 0")',
            ]
        super().__set__(instance, value)

# More specialized types
class PosInteger(Integer, Positive):
    pass

class PosFloat(Float, Positive):
    pass



