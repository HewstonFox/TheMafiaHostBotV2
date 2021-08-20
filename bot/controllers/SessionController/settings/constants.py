registration_min = 60
registration_change_time_min = 5
night_min = 10
day_min = 60
poll_min = 30
vote_min = 10
min_players = 4
min_role_n = 4


class DisplayType(object):
    show = 'show'
    hide = 'hide'
    partially = 'partially'

    @classmethod
    def values(cls):
        return cls.show, cls.partially, cls.hide
