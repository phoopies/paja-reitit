from flask import render_template, request
from paja_reitit.dashboard import blueprint
from paja_reitit.route.models import Route
from paja_reitit.dashboard.util import get_routes_by_grade_figure, figure_to_html_img, get_current_date_and_time


@blueprint.route('/', methods=["GET"])
def index():
    """
    Display the dashboard
    """
    all_routes = Route.get_all_on_wall()
    route_count = all_routes.count()
    routes = all_routes.limit(9).all()
    grades_fig = get_routes_by_grade_figure()
    img = figure_to_html_img(grades_fig)
    date_now, time_now = get_current_date_and_time()
    return render_template('dashboard/index.html.j2',
                           routes=routes,
                           route_count=route_count,
                           img=img,
                           time_now=time_now,
                           date_now=date_now)

@blueprint.route('/routes', methods=["GET"])
def routes():
    sort_options = {"Newest": "created_at desc", "Easiest": "grade asc", "Hardest": "grade desc", "Oldest": "created_at asc"}
    sort_option = request.args.get('sort_by', None)
    sort_option = sort_option if sort_option in sort_options else "Newest"
    sort_by = sort_options[sort_option]
    routes = Route.get_all_on_wall(sort_by=sort_by).limit(100).all()

    return render_template('dashboard/routes.html.j2',
                           routes=routes, sort_by=sort_option, sort_options=sort_options.keys())
