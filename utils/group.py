class Group:
    def __init__(self):
        self.elements = []

    def __str__(self):
        return f'Group with {len(self)} elements.'

    def __iter__(self):
        return iter(self.elements)
    
    def __getitem__(self, item):
        return self.elements[item]

    def __len__(self):
        return len(self.elements)

    def add(self, element):
        self.elements.append(element)

    def remove(self, element):
        self.elements.remove(element)

    def update(self, *args, **kwargs):
        for element in self:
            element.update(*args, **kwargs)