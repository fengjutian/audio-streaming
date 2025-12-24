def parse_range(range_header: str | None, file_size: int):
    if not range_header:
        return 0, file_size - 1

    units, value = range_header.split("=")
    start_str, end_str = value.split("-")

    start = int(start_str)
    end = int(end_str) if end_str else file_size - 1

    if start >= file_size:
        raise ValueError("Range start out of bounds")

    return start, min(end, file_size - 1)
