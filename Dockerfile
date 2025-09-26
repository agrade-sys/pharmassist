FROM python:3.12

WORKDIR /app
COPY pyproject.toml /app/

# Install uv (Astral) and dependencies
RUN pip install uv && uv pip install -r <(uv pip compile -q pyproject.toml)

COPY . /app
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
