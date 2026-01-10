# 🚀 Início Rápido - Modo Desenvolvimento

## ✅ Pronto para usar SEM Firebase!

O backend está configurado em **modo de desenvolvimento** com banco de dados mock em memória.

## 📋 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor

```bash
# Opção 1: Usar o script automático
python start_dev.py

# Opção 2: Comando direto
uvicorn api.index:app --reload --port 8000
```

### 3. Testar a API

Abra seu navegador em:
- **API**: http://localhost:8000
- **Documentação Interativa**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🎯 Endpoints Disponíveis

Todos funcionam **sem Firebase**:

### POST /api/quote
```bash
curl -X POST http://localhost:8000/api/quote \
  -H "Content-Type: application/json" \
  -d '{
    "serviceId": "demenagement",
    "date": "2026-02-15T10:00:00Z",
    "contact": {
      "name": "Test User",
      "email": "test@example.com",
      "phone": "+33612345678"
    },
    "rooms": 3
  }'
```

### POST /api/contact
```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test",
    "message": "Mensagem de teste"
  }'
```

### POST /api/business
```bash
curl -X POST http://localhost:8000/api/business \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Test Corp",
    "contactName": "Test User",
    "email": "test@example.com",
    "phone": "+33612345678",
    "serviceNeeds": "Teste de serviços"
  }'
```

## ⚙️ Configuração

### Arquivo `.env`

Já está criado e configurado:
```bash
DEV_MODE=true  # Usa banco de dados mock
DEBUG=false
```

## ⚠️ Importante

### Modo Desenvolvimento (DEV_MODE=true)
- ✅ **Não precisa de Firebase**
- ✅ Funciona imediatamente
- ✅ Perfeito para protótipos
- ⚠️ Dados são perdidos ao reiniciar o servidor
- ⚠️ Dados ficam apenas em memória

### Modo Produção (DEV_MODE=false)
- Requer configuração do Firebase
- Dados persistem no Firestore
- Para usar em produção

## 🔄 Mudar para Produção

Quando estiver pronto para usar Firebase:

1. Edite `.env`:
```bash
DEV_MODE=false
FIREBASE_CREDENTIALS={"type":"service_account",...}
```

2. Reinicie o servidor

## 📊 Logs

O servidor mostra claramente em qual modo está rodando:

**Modo Desenvolvimento:**
```
⚠️  Running in DEVELOPMENT MODE with mock database (no Firebase)
⚠️  Data will NOT be persisted and will be lost on restart
```

**Modo Produção:**
```
Running in PRODUCTION MODE with Firebase
```

## 🧪 Testar com Frontend

Seu frontend React pode fazer requisições para:
```
http://localhost:8000/api/quote
http://localhost:8000/api/contact
http://localhost:8000/api/business
```

CORS já está configurado para aceitar requisições de:
- `http://localhost:5173` (Vite)
- `http://localhost:3000`

## ✨ Pronto!

Agora você pode desenvolver e testar seu frontend **sem precisar configurar Firebase**! 🎉
