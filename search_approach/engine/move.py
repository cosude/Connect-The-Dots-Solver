class Move:
    def __init__(self, index, new_pos):
        self.index = index # index of pair start - end dots in the positions list
        self.new_pos = new_pos # new indices of the start dot

    def __repr__(self):
        return f"Move(Pair:{self.index}, To:{self.new_pos})"