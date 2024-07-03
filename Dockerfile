FROM python:3.10

WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD streamlit run --server.port 8080 --server.enableCORS false cadastro_de_vendas.py