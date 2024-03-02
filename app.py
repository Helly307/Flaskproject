from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def fetch_maigret_data(username):
    # Make HTTP request to GitHub API for maigret repository
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url)
    if response.status_code == 200:
        # Parse JSON response and extract relevant information
        data = response.json()
        return {
            'username': data['login'],
            'name': data['name'],
            'email': data['email'],
            'bio': data['bio']
        }
    else:
        return None


def fetch_daprofiler_data(fullname):
    # Split the full name into first name and last name
    name_parts = fullname.split()
    if len(name_parts) != 2:
        return None  # Full name does not contain both first and last name

    first_name, last_name = name_parts

    # Construct the query for searching user profiles
    query = f'{first_name} {last_name} in:fullname'

    # Make HTTP request to GitHub Search API for DaProfiler repository
    url = 'https://api.github.com/search/users'
    params = {
        'q': query
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Parse JSON response and extract relevant information
        data = response.json()
        # Extract information from the first search result
        if data['total_count'] > 0:
            first_result = data['items'][0]
            username = first_result['login']
            bio = first_result['bio']
            location = first_result['location']
            return {
                'username': username,
                'bio': bio,
                'location': location
            }
        else:
            return None
    else:
        return None


def fetch_yesitsme_data(email, phone):
    # Placeholder function for fetching data from yesitsme repository
    # This might involve using external APIs or services
    # Here, we are assuming a hypothetical service named 'user-details-service'
    url = 'https://api.user-details-service.com/user-details'
    params = {
        'email': email,
        'phone': phone
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Parse JSON response and extract relevant information
        data = response.json()
        return {
            'email': data['email'],
            'phone': data['phone'],
            'name': data['name'],
            'address': data['address']
            # Add more fields as needed
        }
    else:
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    # Get user inputs from the form
    username = request.form['username']
    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']

    # Fetch data from the repositories
    maigret_data = fetch_maigret_data(username)
    daprofiler_data = fetch_daprofiler_data(fullname)
    yesitsme_data = fetch_yesitsme_data(email, phone)

    # Pass the fetched data to the template
    return render_template('report.html', maigret_data=maigret_data, daprofiler_data=daprofiler_data,
                           yesitsme_data=yesitsme_data)


if __name__ == '__main__':
    app.run(debug=True)
