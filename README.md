# **Ticket Show Web Application**

# Description 
Ticket Show is a Flask-based web application that allows users to make bookings for multiple shows at different theatres. The app has a feature where users can search for different shows and have a look at the bookings made by them. This app allows the admin to perform CRUD operations on theatres and shows and to view a summary chart for the number of bookings made for different shows.

# Technologies Used
- **Python**: Responsible for creating controllers and serving as the primary programming language for hosting the application.

- **Vue.js**: Utilized for crafting the front-end of the application, allowing for interactive and user-friendly interfaces.

- **HTML**: Responsible for building the necessary Vue components and templates, forming the structure of the web pages.

- **CSS**: In charge of web page styling, ensuring a visually appealing and well-organized layout.

- **Bootstrap**: Used to enhance the front-end, making it visually attractive and user-friendly.

- **SQLite**: Serves as the application's database, storing and managing data.

- **Flask**: Acts as the web framework, handling the backend logic and routing of the application.

- **Flask-Restful**: This extension is employed to create a RESTful API, enabling communication with the application via HTTP methods.

- **Flask-SQLAlchemy**: Utilized to interact with and modify the SQLite database, facilitating database operations.

- **Flask-Celery**: Used for executing asynchronous background tasks in the backend, enhancing application efficiency.

- **Flask-Caching**: Employed for caching the outputs of the API to improve performance by reducing redundant computations.

- **Redis**: Serves as an in-memory database for caching API data and functions as a message broker for managing tasks executed by Celery.

# API Design
The Flask-Restful library for Python was used to create a RESTful API. All database tables have CRUD operations available through the API. Authentication tokens are used for specific requests that require them. These tokens can only be obtained from the user's account page or the admin's account page when signed in.

# Architecture and Features:
The architecture of Ticket-Show follows a client-server model, where Vue.js serves as the front-end framework and Python-Flask as the back-end framework. Vue.js handles the presentation layer and manages user interactions through its MVVM architecture, while Python-Flask handles the server-side logic, such as HTTP requests and responses, asynchronous tasks, and database interactions.

The features of the application are as follows:


-   **User authentication**: Signup and Login

-   **Admin authentication**: Signup and Login

-   **User dashboard**: View available shows, access book show option, redirection to bookings page

-   **Admin dashboard**: CRUD on theater, CRUD on shows, redirection to analytics page

-   **Search Functionality**: Search for shows

-   **Show analytics**: View show's analytics for a particular theater

-   **Data export**: Download analytics as a CSV file

-   **Show management**: Create, view, edit, and delete shows

-   **Theater management**: Create, view, edit, and delete theater

-   **RESTful API**: API available for theater, shows, admin, user, booking

-   **Reminders**: Receive daily reminders to book

-   **Monthly enetrtainment report**: Receive an enetertainment report as an email (HTML)


# Installation and Usage

## Video:

For the video, click
[here](https://drive.google.com/file/d/1sDCBLkwpuO4RPtE5tMH7XQmsmDK2kToM/view?usp=sharing)!

## Instructions for running the application

1. Clone the repo.
2. Navigate to the root folder of the application.
3. Navigate to the backend folder and open three separate terminals. Execute the following commands in each:

    * `python main.py`
    * `celery -A app.celery worker -l info`
    * `celery -A app.celery beat --max-interval 1 -l info`
4. Navigate to the frontend folder.
5. In the terminal, execute the following command:

    * `npm install`
    * `npm run serve`

These steps will successfully run the application, allowing you to access it from your web browser at [http://localhost:8080](http://localhost:8080).
