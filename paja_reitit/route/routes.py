from flask import  redirect, render_template, request
from paja_reitit.route import blueprint
from paja_reitit.route.models import Route
from paja_reitit.route.forms import CreateRouteForm

@blueprint.route('/', methods=["GET", "POST"])
def index():
    """
    Create a new route from the form
    """
    create_route_form = CreateRouteForm(request.form)
    new_route = None
    if "create" in request.form:
        if create_route_form.validate():
            setter = create_route_form.setter.data
            grade = create_route_form.grade.data
            color = create_route_form.color.data
            sector = create_route_form.sector.data
            print(setter, sector, color)
            new_route = Route(setter_id=setter, grade=grade, color_id=color, sector_id=sector)
            new_route.save()
    routes = Route.get_all_on_wall()
    return render_template('route/index.html.j2', form=create_route_form, new_route=new_route, routes=routes)

@blueprint.route('/route/delete/<string:route_id>', methods=["GET", "POST"])
def delete_route(route_id: str):
    """
    Mark a route as deleted
    """
    route = Route.find_by_id(route_id)
    if route:
        route.deleted = True
        route.save()
    return redirect('/')
