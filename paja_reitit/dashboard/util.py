import base64
from io import BytesIO
from typing import Tuple
from datetime import datetime
from paja_reitit.route.models import Route
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from paja_reitit.util import GRADES

def get_routes_by_grade_figure() -> Figure:
    routes = Route.get_all_on_wall()
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    counts = [routes.filter_by(grade=grade).count() for grade in GRADES]
    
    # Create the grid 
    ax.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
    ax.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)

    # Reformat x-axis label and tick labels
    # ax.set_xlabel('Grade', fontsize=12, labelpad=10)
    # ax.xaxis.set_label_position("bottom")
    # ax.xaxis.set_major_formatter(lambda s, i : f'{s:,.0f}')
    # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax.xaxis.set_tick_params(pad=2, labelbottom=True, bottom=True, labelsize=12, labelrotation=0)
    ax.set_xticks([i for i in range(len(GRADES))], GRADES)

    # Reformat y-axis
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    bar = ax.bar(GRADES, counts, width=0.6, color="#FA6900")

    # Add label on top of each bar
    ax.bar_label(bar, labels=counts, padding=3, color='black', fontsize=12) 
    return fig

def figure_to_html_img(fig: Figure) -> str:
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True, dpi=256)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img class='w-100' style='object-fit: scale-down;' src='data:image/png;base64,{data}'/>"

def get_current_date_and_time() -> Tuple[str, str]:
    now = datetime.now()
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%A %H:%M")
    return (date, time)
    