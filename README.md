# Batimove Backend API

Backend FastAPI para a plataforma SaaS Batimove.

## 🚀 Deploy Rápido na Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/joshsegatt/Batimove-saas)

## 📋 Variáveis de Ambiente Necessárias

Configure estas variáveis no dashboard da Vercel:

```bash
# Modo de Desenvolvimento (use false em produção)
DEV_MODE=false

# Firebase Credentials (obrigatório se DEV_MODE=false)
FIREBASE_CREDENTIALS={"type":"service_account","project_id":"seu-projeto",...}
```

## 🛠️ Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Modo desenvolvimento (sem Firebase)
python start_dev.py

# API disponível em http://localhost:8000
# Docs em http://localhost:8000/api/docs
```

## 📚 Documentação

Veja [README_BACKEND.md](README_BACKEND.md) para documentação completa.

## 🔗 Endpoints

- `POST /api/quote` - Submeter pedido de orçamento
- `POST /api/contact` - Enviar mensagem de contato
- `POST /api/business` - Capturar lead B2B

## 📦 Stack

- FastAPI
- Google Firestore
- Pydantic
- Vercel Serverless
