import requests
from decouple import config


def test_send_valid():
    """First test. Send valid request """

    gmail = config('GMAIL_TO')
    json = {
        "to": gmail,
        "subject": "Test Subject",
        "message": "Test Text"
    }

    response = requests.post("http://0.0.0.0:8000/send_email", json=json)
    assert response.status_code == 200
    expected_response = {"result": True, "message": "Email send successfully!"}
    assert response.json() == expected_response


def test_not_valid_email():
    """Second test. Send not valid email """

    gmail = config('GMAIL_NOT_VALID')
    json = {
        "to": gmail,
        "subject": "Test Subject",
        "message": "Test Text"
    }

    response = requests.post("http://0.0.0.0:8000/send_email", json=json)
    assert response.status_code == 400
    expected_response = {"detail": f"Email {gmail} is not valid!"}
    assert response.json() == expected_response


def test_email_does_not_exist():
    """First test. Send not exist email """

    gmail = config('GMAIL_DOES_NOT_EXIST')
    json = {
        "to": gmail,
        "subject": "Test Subject",
        "message": "Test Text"
    }

    response = requests.post("http://0.0.0.0:8000/send_email", json=json)
    assert response.status_code == 400
    expected_response = {"detail": f"Email {gmail} does not exist!"}
    assert response.json() == expected_response

