from flask import redirect, render_template, request, url_for
from paja_reitit.routesetter import blueprint
from paja_reitit.routesetter.forms import AddRoutesetterForm
from paja_reitit.routesetter.models import Routesetter


@blueprint.route('/', methods=["GET", "POST"])
def routesetters_view():
    """
    """
    add_routesetter_form = AddRoutesetterForm(request.form)
    if "add" in request.form:
        if add_routesetter_form.validate():
            name = add_routesetter_form.name.data
            new_routesetter = Routesetter(name=name)
            new_routesetter.save()
            return redirect('/routesetters')
            
    routesetters = Routesetter.query.all()
    routesetters.sort(key=lambda rs: -1*rs.routes_set)
    return render_template('routesetter/index.html.j2', form=add_routesetter_form, routesetters=routesetters)

@blueprint.route('/delete/<string:setter_id>', methods=["GET", "POST"])
def delete_setter(setter_id: str):
    setter = Routesetter.find_by_id(setter_id)
    if setter:
        setter.delete_from_db()
    return redirect(url_for('routesetter_blueprint.routesetters_view'))