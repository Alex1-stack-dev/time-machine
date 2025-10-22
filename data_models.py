class Entry:
    def __init__(self, entry_id, name, heat, lane, status="OK"):
        self.entry_id = entry_id
        self.name = name
        self.heat = heat
        self.lane = lane
        self.status = status

    def as_dict(self):
        return {
            "ID": self.entry_id,
            "Name": self.name,
            "Heat": self.heat,
            "Lane": self.lane,
            "Status": self.status
        }

class Result:
    def __init__(self, place, name, time, heat, dq=""):
        self.place = place
        self.name = name
        self.time = time
        self.heat = heat
        self.dq = dq

    def as_dict(self):
        return {
            "Place": self.place,
            "Name": self.name,
            "Time": self.time,
            "Heat": self.heat,
            "DQ": self.dq
        }
