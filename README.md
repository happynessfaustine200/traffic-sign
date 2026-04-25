# Traffic Sign Recognition (Django)

A Django app for training on traffic-sign images and detecting sign meaning from new uploads.

## Features
- Upload labeled traffic sign images to build your dataset.
- Save classes (`name` + `meaning`) and extracted image features.
- Detect meaning by uploading another image and matching against database samples.
- View recent training samples and detection history.

## Quick Start
1. Create and activate a virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Apply migrations:
   - `python manage.py migrate`
4. Create admin user (optional):
   - `python manage.py createsuperuser`
5. Run server:
   - `python manage.py runserver`
6. Open:
   - `http://127.0.0.1:8000/train/` (training)
   - `http://127.0.0.1:8000/detect/` (detection)

## How Training Works
- Each uploaded training image is resized and converted to features (histograms + downsampled pixels).
- Features are saved in the DB with the selected class.
- During detection, uploaded image features are compared with stored vectors.
- The closest match provides predicted sign and confidence.

## Notes
- This is a lightweight baseline recognizer. Accuracy improves as you upload more class examples.
- Future upgrades can replace the matcher with scikit-learn or deep learning models.

## PythonAnywhere Static Setup
1. Run: `python manage.py collectstatic --noinput`
2. In PythonAnywhere Web tab, add static mapping:
   - URL: `/static/`
   - Directory: `/home/<your-username>/HappyProject/staticfiles`
3. Reload your PythonAnywhere web app after `collectstatic`.
