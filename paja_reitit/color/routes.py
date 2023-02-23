from flask import redirect, render_template, request, url_for
from paja_reitit.color import blueprint
from paja_reitit.color.forms import AddColorForm
from paja_reitit.color.models import Color


@blueprint.route('/', methods=["GET", "POST"])
def colors_view():
    """
    """
    add_color_form = AddColorForm(request.form)
    if "add" in request.form:
        if add_color_form.validate():
            name = add_color_form.name.data
            code = add_color_form.code.data
            new_color = Color(name=name, code=code)
            new_color.save()
            return redirect('/colors')
            
    all_colors = Color.query.all()
    return render_template('color/index.html.j2', form=add_color_form, colors=all_colors)

@blueprint.route('/delete/<string:color_id>', methods=["GET", "POST"])
def delete_color(color_id: str):
    """
    delete a color
    """

    color = Color.find_by_id(color_id)
    if color:
        color.delete_from_db()
    return redirect(url_for('color.colors_view'))