from flask import Blueprint, render_template, redirect, url_for, request, flash
import logging
from app.forms import ContactForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from utils.create_assessment import create_assessment
import os

contact = Blueprint('contact', __name__)
logging.basicConfig(level=logging.INFO)


@contact.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        # Get form data
        token = request.form.get('g-recaptcha-response')
        recaptcha_action = 'submit'

        # Verify reCAPTCHA
        if not token:
            flash('Please complete the reCAPTCHA challenge.', 'error')
            return redirect(url_for('contact.contact_page'))

        # Create an assessment to analyze the risk of a UI action
        assessment = create_assessment(
            project_id=os.getenv('GOOGLE_PROJECT_ID'),
            recaptcha_site_key=os.getenv('RECAPTCHA_SITE_KEY'),
            token=token,
            recaptcha_action=recaptcha_action,
            user_ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            ja3='Not provided'
        )

        # print("Assessment: ", assessment)

        # Check if the token is valid
        if not assessment:
            flash('An error occurred while verifying the reCAPTCHA response.', 'error')
            return redirect(url_for('contact.contact_page'))

        # Check if the expected action was executed
        if not assessment.token_properties.valid:
            flash('The reCAPTCHA response was invalid.', 'error')
            return redirect(url_for('contact.contact_page'))

        # Check the risk score
        score = assessment.risk_analysis.score  # Risk score
        # score = .8  # For testing purposes
        # score = .2  # For testing purposes
        reasons = assessment.risk_analysis.reasons  # Reasons for the score

        # Display a message and log the event for low-risk interactions
        if score >= 0.7:
            flash('Your interaction is deemed safe.', 'info')
            logging.info(
                f"Interaction with risk score {score} and reasons: {reasons}")

        elif score < 0.3:  # Adjust the threshold as needed
            # Take additional actions for high-risk interactions, such as sending an email or blocking the interaction
            flash('Your interaction is deemed suspicious.', 'error')
            logging.warning(
                f"Interaction with risk score {score} and reasons: {reasons}")
            return redirect(url_for('contact.contact_page'))

        else:  # Interactions with intermediate scores can be treated normally
            pass

        # Get form data

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
            # Change to your receiving email
            to_email=os.getenv('SENDGRID_DEFAULT_RECEIVER')
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

    # print(request.form)
    # print(form.errors)

    return render_template('contact.html', form=form, site_key=os.getenv('RECAPTCHA_SITE_KEY'))

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
