FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend

ENV DATABASE_URL=postgres://user:pass@db:5432/p2px
ENV WALLET_KEY=CHANGE_ME_32_BYTES
ENV JWT_SECRET=CHANGE_ME_SECRET

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
