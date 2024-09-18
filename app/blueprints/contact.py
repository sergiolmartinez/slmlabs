from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import ContactForm

contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        # Normally you would handle the form submission here (e.g., send an email or save to DB)
        flash(f'Message from {
              form.name.data} has been sent successfully!', 'success')
        return redirect(url_for('contact.contact_page'))
    return render_template('contact.html', form=form)
