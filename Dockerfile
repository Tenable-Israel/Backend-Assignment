FROM python:3.11.2-slim

WORKDIR /backend

COPY requirments.txt .

RUN pip install -r requirments.txt

COPY ./backend .

ENV PYTHONPATH=/


EXPOSE 80

CMD ["uvicorn", "main:app","--app-dir=/backend/", "--host", "0.0.0.0", "--port", "80"]