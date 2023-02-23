from flask import redirect, render_template, request, url_for
from paja_reitit.route.models import Route
from paja_reitit.sector import blueprint
from paja_reitit.sector.models import Sector
from paja_reitit.sector.forms import AddSectorForm

@blueprint.route('/', methods=["GET", "POST"])
def sectors_view():
    """
    Create a new route from the form
    """
    add_sector_form = AddSectorForm(request.form)
    if "add" in request.form:
        if add_sector_form.validate():
            name = add_sector_form.name.data
            new_routesetter = Sector(name=name)
            new_routesetter.save()
            return redirect('/sectors')
            
    sectors = Sector.query.all()
    return render_template('sector/index.html.j2', form=add_sector_form, sectors=sectors)

@blueprint.route('/clear/<string:sector_id>', methods=["GET", "POST"])
def clear_sector(sector_id: str):
    """
    Clear a sector from it's routes
    """

    routes = Route.find_by_sector(sector_id).filter_by(deleted=False)
    for route in routes:
        route.deleted = True
        route.save()
    return redirect('/sectors')

@blueprint.route('/delete/<string:sector_id>', methods=["GET", "POST"])
def delete_sector(sector_id: str):
    """
    Clear a sector from it's routes
    """

    sector = Sector.find_by_id(sector_id)
    if sector:
        sector.delete_from_db()
    return redirect(url_for('sector.sectors_view'))
