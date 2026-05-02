mkdir final-backend
cd final-backend

python -m venv venv
venv\Scripts\activate   # Windows

pip install django djangorestframework
pip install PyJWT

django-admin startproject backend .

mkdir apps

python manage.py startapp auth
python manage.py startapp appointment
python manage.py startapp doctors
python manage.py startapp hospitals
python manage.py startapp poli
python manage.py startapp profileUser

move auth apps/
move appointment apps/
move doctors apps/
move hospitals apps/
move poli apps/
move profileUser apps/