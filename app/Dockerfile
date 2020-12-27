FROM python:3.7
ADD "." "/src"
ENV PORT=$PORT
WORKDIR "./src"
COPY "./src/requirements.txt" "."
RUN pip install -r requirements.txt
COPY "./src/" "."
CMD ["sh", "-c", "streamlit run --server.port $PORT app.py"]
