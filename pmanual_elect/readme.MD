# pmanual_elect

A Flask web application deployed and managed as a 24/7 background service via Gunicorn and `systemd` on an Ubuntu Azure Virtual Machine.

<p align="center">
  <img src="qrcode.png" alt="pmanual_elect QR Code" width="200" />
</p>

<p align="center">
  <strong>Live Deployment:</strong> <a href="http://85.211.241.159:8001">http://85.211.241.159:8001</a>
</p>

---

## Tech Stack

* **Backend:** Python 3, Flask
* **WSGI Server:** Gunicorn
* **Process Manager:** `systemd` (`pmanual_elect.service`)
* **Infrastructure:** Ubuntu Linux (Azure VM)

---

## Project Structure

```text
pmanual_elect/
├── app.py              # Main Flask application entry point
├── qrcode.png          # QR code linking to the live deployment
├── README.md           # Project documentation
├── static/             # Static assets (CSS, JS, images)
├── templates/          # Jinja2 HTML templates
└── venv/               # Isolated Python virtual environment