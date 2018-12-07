def none_list(maybe_list):
    if maybe_list is None:
        return []
    return maybe_list

class Rule:
    def __init__(self, sec_id, comm=None, f2f=None, total=None):
        comm = none_list(comm)
        f2f = none_list(f2f)
        total = none_list(total)
        if comm is None:
            comm = []
        if f2f is None:
            f2f = []
        if total is None:
            total = []

        self.sec_id = sec_id
        self.comm = comm
        self.f2f = f2f
        self.total = total

    def append_year(self, comm, f2f, total):
        self.comm.append(comm)
        self.f2f.append(f2f)
        self.total.append(total)
    
    def year_cnt(self):
        return len(self.comm)

class World:
    def __init__(self, student_group, sec_id, world_id,
                 alba=None, batia=None, capita=None):
        alba = none_list(alba)
        batia = none_list(batia)
        capita = none_list(capita)
        
        self.student_group = student_group
        self.sec_id = sec_id
        self.world_id = world_id
        self.alba = alba
        self.batia = batia
        self.capita = capita

    def append_year(self, alba, batia, capita):
        self.alba.append(alba)
        self.batia.append(batia)
        self.capita.append(capita)

    def year_cnt(self):
        return len(self.alba)
