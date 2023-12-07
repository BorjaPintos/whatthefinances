from src.shared.infraestructure.rest.pagefront import PageFront


def calculate_pages_front(offset, pagination_size, total_elements, max_pages: int):
    n_paginas_totales = int(total_elements / pagination_size) + (total_elements % pagination_size > 0)
    current_page = 1 + int(offset / pagination_size) + (offset % pagination_size > 0)
    paginas = []
    medio = int(max_pages / 2)

    start_page = max(1, min(current_page - medio, n_paginas_totales - (medio + 1)))
    end_page = min(start_page + medio + 1, n_paginas_totales) + 1

    for i in range(start_page, end_page):
        paginas.append(PageFront(i, (i - 1) * pagination_size, pagination_size, i == current_page))

    return paginas
