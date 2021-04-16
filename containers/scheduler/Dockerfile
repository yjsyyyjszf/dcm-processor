FROM python:3.7

WORKDIR /app

# Copy requirement file
COPY requirements.txt ./

COPY entrypoint.sh ./

# Install all required dependencies
RUN pip install redis rq flask requests python-dotenv && \
    pip install -r requirements.txt

COPY . .

ENV FLASK_APP="app.py"

CMD ["bash", "entrypoint.sh"]