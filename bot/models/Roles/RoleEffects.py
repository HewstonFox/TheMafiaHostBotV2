from typing import Optional


def read_once_bool_property(prop: str, effect: str):
    exec(f'''
class Prop{prop.upper()}:
    def __init__(self):
        super(Prop{prop.upper()}, self).__init__()
        self._{prop} = False
        
    @property
    def {prop}(self):
        cache = self._{prop}
        self._{prop} = False
        return cache
    
    @property
    def {prop.upper()}(self):
        return self._{prop}
    
    def {effect}(self):
        self._{prop} = True
    ''', globals(), globals())

    return globals()['Prop' + prop.upper()]


class KillEffect(read_once_bool_property('just_killed', 'kill')):
    def __init__(self):
        super(KillEffect, self).__init__()
        self.killed_by: Optional[str] = None

    def kill(self, by: str):
        super(KillEffect, self).kill()
        self.killed_by = by


CureEffect = read_once_bool_property('cured', 'cure')
BlockEffect = read_once_bool_property('blocked', 'block')


class CheckEffect(read_once_bool_property('just_checked', 'check')):
    def __init__(self):
        super(CheckEffect, self).__init__()
        self.checked = False

    def check(self):
        super(CheckEffect, self).check()
        self.checked = True


AcquitEffect = read_once_bool_property('acquitted', 'acquit')
