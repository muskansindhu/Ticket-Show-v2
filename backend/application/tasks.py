from application.workers import celery
from flask import render_template
from jinja2 import Template
from application.models import db, Booking
from application.access import getAdminUsername, getShowsTheater, getAllBookings, getAllAdmin, getAllUser
import csv, os
from application.utils import send_email, generate_html_report
from celery.schedules import crontab
import logging


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=0), 
        reminder_email.s(), 
        name='add every day'
    )

    sender.add_periodic_task(
        crontab(hour=13, minute=0, day_of_month='1'), 
        send_report.s(), 
        name='add every month'
    )


@celery.task()
def export_csv(username, theater_id):
    user_dict = getAdminUsername(username).to_dict()
    shows = getShowsTheater(theater_id)

    
    csv_file_path = os.path.join("./static/csv", "analytics.csv")

    with open(csv_file_path, "w", newline='') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(["Roll", "Show Name", "Rating", "Price", "Tags", "Seats Booked"])
        for show in shows:
            csv_writer.writerow([show.roll, show.show_name, show.rating, show.price, show.tags, show.seats_booked])

    template_str = """
        <p>
            Dear {{ user }},
        </p>
        <p>
            Thank you for using Ticket Show!
        </p>
        <p>
            As requested, we have attached your Theater's Shows analytics CSV file to this email. Please find it attached.
        </p>
        <br />
        <p>
            Best regards,
        </p>
        <p>
            Ticket-Show
        </p>
        """
    template = Template(template_str)

    address = user_dict["email"]
    subject = "Theater's Shows Analytics CSV"
    message = template.render(user=user_dict["username"])

    with open(csv_file_path, "rb") as file:
        send_email(address, subject, message, attachment=file, filename="analytics.csv", subtype="csv")

    os.remove(csv_file_path)


@celery.task()
def send_report():
    admins = getAllAdmin()
    for admin in admins:
        bookings = getAllBookings()
        html_report = generate_html_report(bookings)

        report_file_path = os.path.join("./static/reports", "monthly_report.html")
        with open(report_file_path, "w") as f:
            f.write(html_report)

        template_str = """
            <p>
                Dear {{ admin }},
            </p>
            <p>
                Thank you for using Ticket Show!
            </p>
            <p>
                We hope this message finds you well. 
                We are pleased to inform you that we have prepared our latest monthly entertainment report, 
                and We have attached it to this email for your convenience.
            </p>
            <br />
            <p>
                Best regards,
            </p>
            <p>
                Ticket-Show
            </p>
            """
        template = Template(template_str)
    
        address = admin.email
        subject = "Monthly Report"
        message = template.render(admin=admin.username)

        with open(report_file_path, "rb") as file:
            send_email(address, subject, message, attachment=file, filename="monthly_report.html", subtype="html")

        os.remove(report_file_path)


@celery.task()
def reminder_email():
    template_str = """
    <p>
        Dear {{ user }},
    </p>
    <br />
    <p>
        We hope you're doing well. We wanted to reach out and remind you that it's been some time since your last booking with us. We truly value your patronage and believe that your choice enriches our platform.
    </p>
    <p>
        We understand that life can be hectic, but we encourage you to take a moment to explore and book upcoming events with us. Your preferences and choices are essential to our platform and fellow event-goers.
    </p>
    <p>
        We genuinely appreciate your continued support as part of our ticket booking community, and we eagerly anticipate your next booking.
    </p>
    <br />
    <p>
        Best regards,
    </p>
    <p>
        {{ your_name }}
        """
    users = getAllUser()
    template = Template(template_str)

    for user in users:
        user_dict = user.to_dict()
        if user_dict["booked"] == 0:
            address = user_dict["email"]
            subject = user_dict["username"] + ", a friendly reminder to contribute to Ticket-Show"
            rendered_template = template.render(user=user_dict["username"], your_name="Ticket-Show")

            send_email(address, subject, rendered_template)
            
            user.posted = 0
            db.session.commit()

    return "Reminder Mail Sent"