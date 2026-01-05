FROM python:3.11-slim

# ishchi papka
WORKDIR /app

# system dependency (ixtiyoriy, lekin xavfsiz)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# project fayllar
COPY . .

# django port
EXPOSE 7009

# run commands
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:7009
