from dataclasses import dataclass, asdict


@dataclass
class Interest:
    def __init__(self, identifier, name):
        self.id = identifier
        self.name = name

    def get_dict(self):
        return asdict(self)
