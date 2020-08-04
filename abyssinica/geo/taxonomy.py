import json


class Node:
    def __init__(self, common_name, canonical_name):
        self.common_name = common_name
        self.canonical_name = canonical_name

        self.parent = None
        self.children = []

    def make_edge(self, children):
        self.children += children
        for child in children:
            child.parent = self

    def to_json(self):
        return json.dumps(self, cls=JSONEncoder, indent=4)


class Country(Node):
    def __init__(self, iso_3166_1, common_name, canonical_name):
        super().__init__(common_name, canonical_name)
        self.iso_3166_1 = iso_3166_1

    def __str__(self):
        return f'{self.iso_3166_1}\n{self.common_name}\n{self.canonical_name}'


class Region(Node):
    def __init__(self, iso_3166_2, common_name, canonical_name):
        super().__init__(common_name, canonical_name)
        self.iso_3166_2 = iso_3166_2

    def __str__(self):
        return f'{self.iso_3166_2}\n{self.common_name}\n{self.canonical_name}'


class Zone(Node):
    def __str__(self):
        return f'{self.common_name}'


class City(Node):
    def __str__(self):
        return f'{self.common_name}'


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Country):
            return {
                'type': 'country',
                'iso_3166_1': obj.iso_3166_1,
                'common_name': obj.common_name,
                'children': obj.children,
            }
        elif isinstance(obj, Region):
            return {
                'type': 'region',
                'iso_3166_2': obj.iso_3166_2,
                'common_name': obj.common_name,
                'children': obj.children,
            }
        elif isinstance(obj, Zone):
            return {
                'type': 'zone',
                'common_name': obj.common_name,
                'children': obj.children,
            }
        elif isinstance(obj, City):
            return {
                'type': 'city',
                'common_name': obj.common_name,
                'children': obj.children,
            }
        return json.JSONEncoder.default(self, obj)
