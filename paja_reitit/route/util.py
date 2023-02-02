from datetime import datetime

def get_name(route):
    return f"{route.sector or ''}{route.id:>04}"

def get_date_ago(route):
    created_at: datetime = route.created_at
    created_at_rounded_down = datetime(created_at.year, created_at.month, created_at.day)
    today = datetime.now()

    dt = today - created_at_rounded_down
    if dt.days < 1:
        return "Today"
    if dt.days < 2:
        return "yesterday"
    if dt.days < 365:
        return f"{dt.days} ago"
    years = dt.days / 365
    if years == 1:
        return "A year ago"
    return f"{years} ago"
