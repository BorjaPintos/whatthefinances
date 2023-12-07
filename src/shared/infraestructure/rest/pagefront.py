class PageFront:

    def __init__(self, page_n: int, offset_element: int, page_size: int, is_current_page: bool = False):
        self.page_n = page_n
        self.offset_element = offset_element
        self.is_current_page = is_current_page
        self.page_size = page_size
