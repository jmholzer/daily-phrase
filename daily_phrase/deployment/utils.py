from datetime import datetime


def generate_title_formatted_date():
    """Generate title formatted date."""
    return _custom_date_format(datetime.now())


def _custom_date_format(date_obj):
    """Format date in the required format."""
    day = _ordinal(date_obj.day)
    month = date_obj.strftime("%b")
    year = date_obj.year
    return f"{day} {month} {year}"


def _ordinal(number):
    """Return number with ordinal suffix."""
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"
