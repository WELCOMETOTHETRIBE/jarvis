# lightweight image for running Jarvis CLI/web
FROM python:3.11-slim

WORKDIR /app

# copy only what we need first to leverage docker cache
COPY pyproject.toml pyproject.toml
COPY README.md README.md

# install build dependencies and the package
RUN pip install --upgrade pip setuptools wheel
RUN pip install -e .

# copy rest of repository
COPY . .

# expose streamlit port
EXPOSE 8501

# default command runs the web UI, using PORT env variable if provided
CMD streamlit run web/app.py --server.port $PORT --server.address 0.0.0.0
