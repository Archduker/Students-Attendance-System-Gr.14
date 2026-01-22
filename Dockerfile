# 1. Base image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements trước (tối ưu cache)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y tk && rm -rf /var/lib/apt/lists/*

# 5. Copy toàn bộ source code
COPY . .

# 6. Expose port (nếu là web, ví dụ FastAPI / Flask)
EXPOSE 8000

# 7. Run app
CMD ["python", "main.py"]
