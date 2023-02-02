from paja_reitit.color.models import Color
from paja_reitit.route.models import Route

GRADES = ["?", "4", "5", "6A", "6B", "6C", "7A", "7B", "7C", "8A"]

def init_colors():
    colors = [
        ("Red", "#ff0000"),
        ("Green", "#00ff00"),
        ("Blue", "#0000ff"),
        ("Yellow", "#fcd00a"),
        ("Orange", "#fc730a"),
        ("White", "#ffffff"),
        ("Grey", "#878787"),
        ("Black", "#000000"),
        ("Pink", "#fc28ae"),
        ("Purple", "#8811bf"),
        ("Teal", "#48d1cc"),

    ]
    for (name, code) in colors:
        exists = Color.find_by_name(name) != None
        if not exists:
            color = Color(name=name, code=code)
            color.save()
