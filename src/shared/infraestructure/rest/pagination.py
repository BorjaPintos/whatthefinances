class Pagination:

    def __init__(self, elements, offset: int, pagination_size: int, total_elements: int):
        self.elements = elements
        self.offset = offset
        self.total_elements = total_elements
        self.pagination_size = pagination_size

    def get_elements(self):
        return self.elements

    def set_elements(self, elements):
        self.elements = elements

    def get_has_more_elements(self) -> bool:
        return self.total_elements > self.offset * self.pagination_size + len(self.elements)

    def get_offset(self) -> int:
        return self.offset

    def get_pagination_size(self) -> int:
        return self.pagination_size

    def get_total_elements(self) -> int:
        return self.total_elements
