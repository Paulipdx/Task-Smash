FROM ubuntu

RUN apt update && apt install -y python3-pip python3-venv

# Create and use a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install Flask

WORKDIR /app
COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
