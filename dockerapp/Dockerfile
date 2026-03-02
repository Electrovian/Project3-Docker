FROM python:3.11-alpine

# Keep the image small and predictable.
WORKDIR /app

# Create required grading paths and a non-root user.
RUN addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && mkdir -p /home/data/output \
    && chown -R appuser:appgroup /app /home/data

# Copy script and required input files into the expected container paths.
COPY script.py /app/script.py
COPY IF.txt /home/data/IF.txt
COPY AlwaysRememberUsThisWay.txt /home/data/AlwaysRememberUsThisWay.txt

USER appuser

# Runs the script, writes /home/data/output/result.txt, prints results, then exits.
CMD ["python", "/app/script.py"]
