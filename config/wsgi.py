import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise # <--- Buni qo'shdik

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Mana shu qator hamma CSS/JS ni "qo'lidan ushlab" brauzerga ko'rsatadi
application = WhiteNoise(application, root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles'))
application.add_files(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles'), prefix='static/')

app = application # Vercel uchun