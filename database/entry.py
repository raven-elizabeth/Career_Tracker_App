class Entry:
    def __init__(self, entry_dict):
        self.entry_dict = entry_dict

    def store_entry(self, repository):
        repository.save_entry(self.entry_dict)

#win=None, challenge=None, work_contribution=None, learning=None, next_steps=None