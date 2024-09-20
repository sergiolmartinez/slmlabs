from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import ContactForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data if form.phone.data else 'Not provided'
        message = form.message.data
        send_copy = form.send_copy.data  # Checkbox for sending a copy to the user

        # Create email content
        email_body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}

        Message:
        {message}
        """

        # Send email to you
        send_email(
            subject=f"New contact form submission from {name}",
            body=email_body,
            to_email='sergio@slmlabs.com'  # Change to your receiving email
        )

        # Optionally send a copy to the user
        if send_copy:
            send_email(
                subject="Copy of your message to SLM Labs",
                body=email_body,
                to_email=email
            )

        # Flash success message
        flash(
            f'Thank you, {name}. Your message has been sent successfully!', 'success')
        return redirect(url_for('contact.contact_page'))

    return render_template('contact.html', form=form)

# Function to send email using SendGrid


def send_email(subject, body, to_email):
    message = Mail(
        from_email=os.getenv('SENDGRID_DEFAULT_SENDER'),
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
    except Exception as e:
        flash(
            'An error occurred while sending your message. Please try again later.', 'error')
        print(e)
