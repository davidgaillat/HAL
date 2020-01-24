from hal_expression import HalExpression
from hal_treeparser import HalTreeParser
from hal_sql import HalSQL
from flask import Flask, escape, request, render_template, flash
from flask_wtf import Form 
from flask_bootstrap import Bootstrap
from wtforms import StringField, TextField, validators, SubmitField
import os

app = Flask(__name__)
Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class ReusableForm(Form):
    search = TextField('Search:', validators=[validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def search():
    form = ReusableForm(request.form)
    print(form.errors)

    if form.validate_on_submit():
        try:
            gen_sql = ""
            name = request.form['search']
            parser = HalTreeParser()
            tree = parser.get_tree(name)
            expr = HalExpression(tree)
            gen_sql = expr.gen_sql()
            query = name
            results = HalSQL().ExecuteQuery(gen_sql)
            columns = results[1]
            results = results[0]
            items = []
            for item in results:
                items.append(list(item))
            return render_template('search.html', form=form, query=query, columns=columns , results=items)
        except:        
            error = 'There is an error in the search.' + gen_sql
            return render_template('search.html', form=form, error=error)
    return render_template('search.html', form=form)

if __name__ == "__main__":
    app.run()