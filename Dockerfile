# Usa a imagem do Python
FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para dentro do contêiner
COPY . .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.app

# Expõe a porta que o Flask vai usar
EXPOSE 5000

# Define o comando para rodar o Flask
CMD ["flask", "run", "--host=0.0.0.0"]