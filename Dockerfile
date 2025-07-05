# Usa uma imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Adiciona o diretório ao PYTHONPATH (opcional, mas útil para imports)
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe a porta usada pelo Gunicorn
EXPOSE 8080

# Comando para iniciar o app com Gunicorn
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]
