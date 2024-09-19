from flask import Blueprint, render_template, Response, url_for
from datetime import datetime

sitemap = Blueprint('sitemap', __name__)


@sitemap.route('/sitemap.xml', methods=['GET'])
def sitemap_page():
    pages = []
    ten_days_ago = (datetime.now()).strftime('%Y-%m-%d')

    # Add static pages
    pages.append({
        # Adjust route name as per your blueprint
        'loc': url_for('home.homepage', _external=True),
        'lastmod': ten_days_ago,
        'priority': '1.00'
    })
    pages.append({
        # Adjust route name as per your blueprint
        'loc': url_for('about.about_page', _external=True),
        'lastmod': ten_days_ago,
        'priority': '0.80'
    })
    pages.append({
        # Adjust route name as per your blueprint
        'loc': url_for('contact.contact_page', _external=True),
        'lastmod': ten_days_ago,
        'priority': '0.60'
    })

    # Render the sitemap template
    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = Response(sitemap_xml, mimetype='application/xml')
    return response
