"""Lab 5 Part II reports reuse the existing MySQL connection and page styles."""
from flask import Blueprint, abort, redirect, render_template, url_for
from lab4 import rows
from lab5_queries import PAGES, QUERIES

lab5 = Blueprint('lab5', __name__)


@lab5.route('/')
def index():
    return redirect(url_for('lab5.report', page='above-average'))


@lab5.route('/<page>')
def report(page):
    if page not in PAGES:
        abort(404)
    title, subtitle, definitions, bonus = PAGES[page]
    sections = [(heading, rows(QUERIES[key])) for heading, key in definitions]
    return render_template('lab5.html', title=title, subtitle=subtitle,
                           active=page, sections=sections, bonus=bonus)


@lab5.route('/discussion')
def discussion():
    return render_template('lab5_discussion.html')
