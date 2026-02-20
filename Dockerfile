# Stage 1: Build frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend with frontend static files
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ ./backend/

# Copy built frontend into backend/static
COPY --from=frontend-builder /app/frontend/dist ./backend/static

# Expose port
EXPOSE 8000

# Start app
WORKDIR /app/backend
CMD python seed_data.py && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
