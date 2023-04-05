from dataclasses import dataclass

@dataclass
class PrintInfo():
    file_path: str
    no_of_copies: int
    is_double_side: bool
    is_colour_print: bool
    page_count: int

def calculate_cost(file_info: PrintInfo, cost_per_page: float|int = 2) -> int|float:
    if(file_info.is_colour_print is True):
        cost_per_page = 8
    if(file_info.is_double_side is True):
        return (file_info.page_count//2) * cost_per_page * file_info.no_of_copies
    return file_info.page_count * cost_per_page 

