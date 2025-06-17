# Ynet to WhatsApp

This project fetches the latest news flashes from Ynet and sends them to a WhatsApp number.

## Project Structure

- `app.py`: The main Python application script.
- `requirements.txt`: Lists the Python dependencies for the project.
- `render.yaml`: Configuration file for deploying the service on Render.

## How it Works

The `app.py` script likely contains the logic to:
1. Fetch news headlines from Ynet (RSS feed or web scraping).
2. Format the headlines.
3. Send the formatted headlines to a pre-configured WhatsApp number using a WhatsApp API or a library that interacts with WhatsApp.

## Deployment

The project is configured to be deployed on Render as a web service using the `render.yaml` file.
- The service uses Python.
- Dependencies are installed using `pip install -r requirements.txt`.
- The application is started with `python app.py`.
