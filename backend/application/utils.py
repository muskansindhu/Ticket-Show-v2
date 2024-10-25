from PIL import Image
import io
import seaborn as sns
import matplotlib.pyplot as plt
import os, smtplib
import pandas as pd
from application.config import UPLOAD_FOLDER
from application.access import getShowsTheater, getTheaterName, getUserBooking, getShowRoll
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication


def create_plot(data, plot_type, theater_name):
    import matplotlib
    matplotlib.use('Agg')

    sns.set_style("whitegrid")
    sns.set(rc={"figure.figsize":(18, 10)})
    
    # Create the bar plot
    ax = sns.barplot(x=plot_type, y="Show Name", data=data, color="skyblue")

    # Add the view numbers to the bars
    for i, v in enumerate(data[plot_type]):
        ax.text(v + 0.5, i, str(v), color='black', fontweight='bold', rotation=270)

    # Add labels and a title
    ax.set_xlabel(plot_type)
    ax.set_ylabel("Theater")
    ax.set_title("Show " + plot_type, fontsize=20)

    folder_name = UPLOAD_FOLDER+ "Analytics/" + theater_name
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    plt.savefig(folder_name + "/" + plot_type +".png")
    plt.clf()



def create_show_analytics(theater_id):
    shows = getShowsTheater(theater_id)
    theater_name = getTheaterName(theater_id)
    show_names = [show.show_name for show in shows]
    seats_booked = [show.seats_booked for show in shows]
    ratings = [show.rating for show in shows]

    seats_booked_data = pd.DataFrame({
        'Show Name': show_names,
        'Seats Booked': seats_booked
    })

    ratings_data = pd.DataFrame({
        'Show Name': show_names,
        'Rating': ratings
    })

    create_plot(seats_booked_data, "Seats Booked", theater_name)
    create_plot(ratings_data, "Rating", theater_name)


def send_email(address, subject, message, attachment=None, filename=None, subtype=None):
    SENDER_ADDRESS = "moonpiedummyacc@gmail.com"
    SENDER_PASSWORD ="schpyvauaerwwred"

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    if attachment:
        part = MIMEApplication(attachment.read(), _subtype=subtype)
        part.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(part)
    
    try:
        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        s.starttls()
        s.login(SENDER_ADDRESS,SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


def generate_html_report(bookings):
    html_report = "<html><head><title>Monthly Entertainment Report</title></head><body>"
    html_report += "<h1>Monthly Entertainment Report</h1>"

    html_report += "<table border='1'><tr><th>Booking ID</th><th>Show ID</th><th>User ID</th><th>Tickets Booked</th></tr>"
    for booking in bookings:
        html_report += f"<tr><td>{booking.roll}</td><td>{booking.show_id}</td><td>{booking.user_id}</td><td>{booking.tickets_booked}</td></tr>"
    html_report += "</table>"
    html_report += "</body></html>"

    return html_report


def convert_to_webp(image_file):
    with Image.open(image_file) as img:
        width, height = img.size
        max_size = 800
        if width > max_size or height > max_size:
            ratio = max_size / max(width, height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), resample=Image.LANCZOS)
        output = io.BytesIO()
        img.save(output, format='webp', quality=80)
        return output.getvalue()