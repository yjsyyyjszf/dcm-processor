FROM python:3.9

WORKDIR /app

# Copy requirement file
COPY requirements.txt ./

COPY entrypoint.sh ./

# Install all required dependencies
RUN pip install rq-dashboard && \
    pip install -r requirements.txt

CMD ["bash", "entrypoint.sh"]