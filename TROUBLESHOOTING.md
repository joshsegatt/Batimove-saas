# 🚨 Troubleshooting Vercel Deployment

## Problema Atual

Backend continua crashando na Vercel com erro `FUNCTION_INVOCATION_FAILED` mesmo com código mínimo.

## Tentativas Realizadas

1. ✅ Código mínimo (só FastAPI básico)
2. ✅ Requirements simplificado (só fastapi + uvicorn)
3. ✅ Removido Python version constraint
4. ✅ Movido entry point para `main.py` na raiz

## Próximas Ações

### Opção 1: Verificar Logs da Vercel

No dashboard da Vercel:
1. Vá em **Deployments**
2. Clique no último deployment
3. Vá em **Functions** → Clique na função
4. Veja os **Runtime Logs**

**Procure por:**
- Erros de import
- Mensagens de erro do Python
- Problemas de dependências

### Opção 2: Testar Localmente com Vercel CLI

```bash
cd C:\Users\josh\Desktop\Batimove
npm install -g vercel
vercel dev
```

Isso roda exatamente como na Vercel e mostra erros detalhados.

### Opção 3: Usar Template Oficial

Clonar template oficial da Vercel que funciona:

```bash
git clone https://github.com/vercel/examples
cd examples/python
# Copiar estrutura para nosso projeto
```

### Opção 4: Deploy Alternativo

Considerar outras plataformas:
- **Railway**: Mais simples, suporta Python melhor
- **Render**: Free tier generoso
- **Fly.io**: Bom para APIs

## Checklist de Verificação

- [ ] Root Directory na Vercel está correto (vazio ou `.`)
- [ ] Build Command está vazio
- [ ] Output Directory está vazio
- [ ] Framework Preset está em "Other"
- [ ] Variáveis de ambiente configuradas (DEV_MODE=true)
- [ ] Logs da Vercel verificados

## Estrutura Atual

```
Batimove/
├── api/
│   ├── __init__.py
│   └── index.py (FastAPI app)
├── main.py (entry point)
├── requirements.txt
├── vercel.json
└── README.md
```

## Código Atual (Mínimo)

**main.py:**
```python
from api.index import app
handler = app
```

**api/index.py:**
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "OK"}

handler = app
```

**requirements.txt:**
```
fastapi
uvicorn
```

**vercel.json:**
```json
{
  "builds": [{"src": "main.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "main.py"}]
}
```

---

**Se nada funcionar**, o problema pode ser:
1. Região da Vercel incompatível
2. Limitação da conta free tier
3. Bug da Vercel com Python

**Recomendação**: Testar em outra plataforma (Railway/Render) para confirmar que o código está correto.
