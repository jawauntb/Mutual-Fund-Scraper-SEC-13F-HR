import xml.etree.ElementTree as et

class XMLParser:

    def __init__(self, _xml):
        self.root = et.XML(_xml)

    def parse_root(self, root):
        return [self.parse_element(node) for node in iter(root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()

        for key in element.keys():
            if key not in parsed:
                parsed[key] = element.attrib.get(key)
            else:
                raise ValueError('duplicate attribute {0} at element {1}'.format(key, element.getroottree().getpath(element))

        for child in list(element):
            self.parse_element(child, parsed)

        return parsed

    def process_data(self):
        """ Initiate the root XML, parse it, and return a dataframe"""
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)