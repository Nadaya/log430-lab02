"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param
from queries.read_order import get_highest_spending_users

def show_highest_spending_users():
    """ Show report of highest spending users """
    users_data = get_highest_spending_users()
    html_content = "<html>"
    html_content += "<h2>Les plus gros acheteurs</h2>"

    if not users_data:
        html_content += "<p>(Aucun utilisateur trouvé)</p>"
    else:
        for user in users_data:
            html_content += f"<p> {user['name']}</p>"
    return get_template(html_content)

def show_best_sellers():
    """ Show report of best selling products """
    html_content = "<html>"
    html_content += "<h2>Les articles les plus vendus</h2>"    
    return get_template(html_content)