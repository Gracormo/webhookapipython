# Webhook API Project

## Project Overview
This project is a Flask-based API that receives information from a webhook simulator, saves it to a database, and processes the data depending on the payment status. The project includes a login system, a unique URL for each user, and a page with email search options for the received information.

## Features
- **User Authentication**: Secure login and account creation using CSRF tokens and form validation.
- **Webhook Data Processing**: Receives data from a webhook, saves it to a database, and processes it based on the payment status.
- **Unique User URLs**: Each user has a unique URL to view their data.
- **Data Search and Display**: Users can search for specific data using email and view it in a tabular format.

## Project Structure
.
├── Apiproject/
│ ├── static/
│ │ └── styles.css
│ ├── templates/
│ │ ├── base.html
│ │ ├── create_account.html
│ │ ├── login.html
│ │ └── main.html
│ ├── init.py
│ ├── forms.py
│ ├── models.py
│ ├── routes.py
├── instance/
│ └── database.db
├── venv/
│ └── (virtual environment files)
├── main.py
├── Procfile
├── requirements.txt


## Usage

### User Registration
- Go to the `/create_account` URL to create a new account.
- Fill in the email, password, password confirmation, and token fields.
- **Use the following token for registration: `uhdfaAADF123`**

### User Login
- Go to the `/login` URL to log in.
- Fill in the email and password fields.

### Webhook Data
- After logging in, you will see your unique URL.
- Use this URL to receive webhook data.

### Data Search
- Use the search form on the main page to filter data by email.

## Webhook Simulator
This project uses the following webhook simulator:
[Webhook Simulator](https://simuladorwebhook-production.up.railway.app/)

## Deployment
The project is deployed on Heroku. You can test it using the following link:
[API Webhook Project](https://apiwebhook-7280a98c07e3.herokuapp.com/)

## File Descriptions

- **main.py**: The entry point for the application.
- **Apiproject/\_\_init\_\_.py**: Initializes the Flask application and sets up the configurations.
- **Apiproject/forms.py**: Contains form classes for user registration and login.
- **Apiproject/models.py**: Defines the database models.
- **Apiproject/routes.py**: Contains the route handlers for the web application.
- **Apiproject/static/**: Contains static files like CSS.
- **Apiproject/templates/**: Contains the HTML templates.
  - **base.html**: The base template that other templates extend.
  - **create_account.html**: Template for the account creation page.
  - **login.html**: Template for the login page.
  - **main.html**: Template for the main user dashboard.
- **instance/database.db**: The SQLite database file.
- **Procfile**: Used by Heroku to start the application.
- **requirements.txt**: Lists the Python dependencies for the project.

## Contributing
If you want to contribute to this project, please fork the repository and create a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or issues, please contact [your-email@example.com].
