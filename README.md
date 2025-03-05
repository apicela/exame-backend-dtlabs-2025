# exame-backend-dtlabs-2025
## ⚙️ Como configurar para teste da aplicação
### Método 1 - Utilizando Docker (recomendado) - não requer Java e Gradle instalados em sua máquina:
1. Clone este repositório: 
2. Execute o seguinte comando no terminal: ```docker-compose up --build```

# Documentação da API de Autenticação

## Endpoints

### Registro de Usuário

**Rota:** `POST /auth/register`

**Descrição:**
Registra um novo usuário na aplicação.

**Requisição:**
```json
{
  "email": "usuario@example.com",
  "password": "senha_segura"
}
```

**Respostas:**
- **201 Created**: Registro realizado com sucesso.
  ```json
  {
    "message": "Usuário registrado com sucesso"
  }
  ```
- **400 Bad Request**: Erro de validação ou usuário já existente.
  ```json
  {
    "message": "Erro na solicitação"
  }
  ```
- **500 Internal Server Error**: Erro interno do servidor.
  ```json
  {
    "message": "Erro interno",
    "error": "Detalhes do erro"
  }
  ```

---

### Login de Usuário

**Rota:** `POST /auth/login`

**Descrição:**
Autentica um usuário e retorna um token de acesso.

**Requisição:**
```json
{
  "email": "usuario@example.com",
  "password": "senha_segura"
}
```

**Respostas:**
- **200 OK**: Login realizado com sucesso.
  ```json
  {
    "message": {
      "token": "token_de_acesso"
    }
  }
  ```
- **401 Unauthorized**: Credenciais inválidas.
  ```json
  {
    "message": "Credenciais inválidas"
  }
  ```
- **500 Internal Server Error**: Erro interno do servidor.
  ```json
  {
    "message": "Erro interno",
    "error": "Detalhes do erro"
  }
  ```

### Inserção de Dados

**Rota:** `POST /data`

**Descrição:**
Insere dados de sensores (temperatura, umidade, voltagem e corrente) para um servidor.

**Requisição:**
```json
{
  "server_ulid": "ulid_do_servidor",
  "timestamp": "2025-03-05 12:00:00.000",
  "temperature": 25.5,
  "humidity": 60.0,
  "voltage": 220.0,
  "current": 5.0
}
```

**Respostas:**
- **201 Created**: Dados inseridos com sucesso.
  ```json
  {
    "message": "Data inserted successfully"
  }
  ```
- **400 Bad Request**: Erro de validação ou dados inválidos.
  ```json
  {
    "message": "Erro na solicitação"
  }
  ```
- **500 Internal Server Error**: Erro interno do servidor.
  ```json
  {
    "message": "Erro interno",
    "error": "Detalhes do erro"
  }
  ```

---

### Consulta de Dados

**Rota:** `GET /data`

**Descrição:**
Consulta dados de sensores para um servidor específico dentro de um intervalo de tempo. É possível aplicar agregação por minuto, hora ou dia.

**Parâmetros da Requisição:**
- `server_ulid` (opcional): ID único do servidor.
- `start_time` (opcional): Início do intervalo de tempo.
- `end_time` (opcional): Fim do intervalo de tempo.
- `sensor_type` (obrigatório): Tipo de sensor (`temperature`, `humidity`, `voltage`, `current`).
- `aggregation` (opcional): Tipo de agregação (`minute`, `hour`, `day`).

**Exemplo de Requisição:**
```json
{
  "server_ulid": "ulid_do_servidor",
  "start_time": "2025-03-05 00:00:00",
  "end_time": "2025-03-05 23:59:59",
  "sensor_type": "temperature",
  "aggregation": "hour"
}
```

**Respostas:**
- **200 OK**: Consulta realizada com sucesso.
  ```json
  [
    {
      "timestamp": "2025-03-05T01:00:00",
      "temperature": 25.5
    },
    {
      "timestamp": "2025-03-05T02:00:00",
      "temperature": 26.0
    }
  ]
  ```
- **400 Bad Request**: Erro de validação ou parâmetros inválidos.
  ```json
  {
    "message": "Erro na solicitação"
  }
  ```
- **500 Internal Server Error**: Erro interno do servidor.
  ```json
  {
    "message": "Erro interno",
    "error": "Detalhes do erro"
  }
  ```

---



## Documentação da API de Servidores



### Criação de Servidor

**Rota:** `POST /servers`

**Descrição:**
Cria um novo servidor para um usuário.

**Requisição:**
```json
{
  "server_name": "Nome do Servidor"
}
```

**Respostas:**
- **201 Created**: Servidor criado com sucesso.
  ```json
  {
    "message": "Server created successfully",
    "server": {
      "server_name": "Nome do Servidor",
      "ownerUlid": "user_ulid",
      "ulid": "server_ulid"
    }
  }
  ```
- **400 Bad Request**: Erro de validação ou nome do servidor ausente.
  ```json
  {
    "message": "Server name is required"
  }
  ```
- **409 Conflict**: O nome do servidor já está registrado.
  ```json
  {
    "message": "Server name already registered"
  }
  ```
- **500 Internal Server Error**: Erro interno do servidor.
  ```json
  {
    "message": "Erro interno",
    "error": "Detalhes do erro"
  }
  ```

---

### Verificação de Saúde do Servidor

**Rota:** `GET /health/<ulid>`

**Descrição:**
Verifica a saúde de um servidor específico.

**Parâmetros da Requisição:**
- `ulid` (obrigatório): ID único do servidor.

**Respostas:**
- **200 OK**: Dados do servidor retornados com sucesso.
  ```json
  {
    "server_name": "Nome do Servidor",
    "ownerUlid": "user_ulid",
    "ulid": "server_ulid"
  }
  ```
- **404 Not Found**: Servidor não encontrado.
  ```json
  {
    "message": "Server not found"
  }
  ```
- **500 Internal Server Error**: Erro interno do servidor.
  ```json
  {
    "message": "Erro interno",
    "error": "Detalhes do erro"
  }
  ```

---

### Verificação de Saúde de Todos os Servidores

**Rota:** `GET /health/all`

**Descrição:**
Verifica a saúde de todos os servidores pertencentes ao usuário atual.

**Respostas:**
- **200 OK**: Lista de servidores retornada com sucesso.
  ```json
  [
    {
      "server_name": "Nome do Servidor",
      "ownerUlid": "user_ulid",
      "ulid": "server_ulid"
    },
    {
      "server_name": "Outro Servidor",
      "ownerUlid": "user_ulid",
      "ulid": "another_server_ulid"
    }
  ]
  ```
- **500 Internal Server Error**: Erro interno do servidor.
  ```json
  {
    "message": "Erro interno",
    "error": "Detalhes do erro"
  }
  ```

---
