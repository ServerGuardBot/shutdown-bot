FROM python:3.11.8

# Copy the files
WORKDIR /app
ADD src .

# Dependencies
RUN pip install -r requirements.txt

VOLUME /tmp

# Run
CMD ["python", "src/base.py"]