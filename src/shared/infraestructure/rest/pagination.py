

class Pagination:

    def __init__(self, elements, has_more_elements, offset):
        self.elements = elements
        self.has_more_elements = has_more_elements
        self.offset = offset

    def get_elements(self):
        return self.elements

    def set_elements(self, elements):
        self.elements = elements

    def get_has_more_elements(self):
        return self.has_more_elements

    def set_has_more_elements(self, has_more_elements):
        self.has_more_elements = has_more_elements

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
