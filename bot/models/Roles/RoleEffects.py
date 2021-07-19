from typing import Optional


def read_once_bool_property(prop: str, effect: str):
    exec(f'''
class Prop{prop.upper()}:
    def __init__(self):
        super(Prop{prop.upper()}, self).__init__()
        self.__{prop} = False
        
    @property
    def {prop}(self):
        cache = self.__{prop}
        self.__{prop} = False
        return cache
    
    def {effect}(self):
        self.__{prop} = True
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
CheckEffect = read_once_bool_property('checked', 'check')
BlockEffect = read_once_bool_property('blocked', 'block')
AcquitEffect = read_once_bool_property('acquitted', 'acquit')
