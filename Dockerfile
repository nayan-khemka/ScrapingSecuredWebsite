FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask pandas pytz lxml openpyxl
CMD ["python", "app.py"]
