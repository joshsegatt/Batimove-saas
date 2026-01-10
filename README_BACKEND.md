# Batimove Backend API

Backend FastAPI pour la plateforme SaaS Batimove, déployé sur Vercel avec Python Serverless Functions.

## 🏗️ Architecture

- **Framework**: FastAPI (Python 3.11)
- **Database**: Google Firestore (NoSQL)
- **Validation**: Pydantic
- **Hosting**: Vercel Serverless Functions

## 📁 Structure du Projet

```
Batimove/
├── api/
│   ├── __init__.py           # Package initializer
│   ├── index.py              # Main FastAPI application
│   ├── models.py             # Pydantic models for validation
│   └── firebase_config.py    # Firebase initialization
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel deployment configuration
└── .env.example             # Environment variables template
```

## 🚀 Endpoints API

### 1. POST `/api/quote`
Créer une demande de devis.

**Request Body**:
```json
{
  "serviceId": "demenagement",
  "date": "2026-02-15T10:00:00Z",
  "contact": {
    "name": "Jean Dupont",
    "email": "jean.dupont@example.com",
    "phone": "+33612345678"
  },
  "fromZip": "75001",
  "toZip": "75015",
  "rooms": 3,
  "volume": 45,
  "floor": 2
}
```

**Response**:
```json
{
  "success": true,
  "quoteId": "abc123xyz",
  "message": "Votre demande de devis a été enregistrée avec succès..."
}
```

### 2. POST `/api/contact`
Soumettre un message de contact.

**Request Body**:
```json
{
  "name": "Marie Martin",
  "email": "marie.martin@example.com",
  "subject": "Question sur les services",
  "message": "Bonjour, j'aimerais avoir plus d'informations..."
}
```

### 3. POST `/api/business`
Capturer un lead B2B (modal "Sur Mesure").

**Request Body**:
```json
{
  "companyName": "TechCorp SAS",
  "contactName": "Pierre Dubois",
  "email": "p.dubois@techcorp.fr",
  "phone": "+33612345678",
  "employeeCount": "50-100",
  "serviceNeeds": "Nous recherchons un partenaire pour gérer les déménagements..."
}
```

## 🔧 Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet (ou configurez dans Vercel):

```bash
# Firebase - Option 1: Service Account JSON complet (Production)
FIREBASE_CREDENTIALS={"type":"service_account","project_id":"batimove-prod",...}

# Firebase - Option 2: Project ID uniquement (Développement local)
FIREBASE_PROJECT_ID=batimove-prod

# Debug mode (optionnel)
DEBUG=false
```

### Obtenir les Credentials Firebase

1. Allez dans [Firebase Console](https://console.firebase.google.com/)
2. Sélectionnez votre projet
3. **Settings** → **Service Accounts** → **Generate New Private Key**
4. Téléchargez le fichier JSON
5. Pour Vercel: Minifiez le JSON sur une ligne et ajoutez-le comme variable d'environnement

## 💻 Développement Local

### Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'exemple des variables d'environnement
cp .env.example .env

# Éditer .env avec vos credentials
```

### Lancer le Serveur de Développement

```bash
# Avec uvicorn
uvicorn api.index:app --reload --port 8000

# Ou avec Python
python -m uvicorn api.index:app --reload --port 8000
```

L'API sera disponible sur `http://localhost:8000`

Documentation interactive:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 🌐 Déploiement sur Vercel

### Via Vercel CLI

```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Déployer
vercel

# Déployer en production
vercel --prod
```

### Via Vercel Dashboard

1. Connectez votre repository GitHub
2. Configurez les variables d'environnement dans **Settings** → **Environment Variables**:
   - `FIREBASE_CREDENTIALS`
3. Déployez automatiquement à chaque push

### Configuration CORS

Le backend est configuré pour accepter les requêtes de:
- `http://localhost:5173` (Vite dev)
- `https://*.vercel.app` (Vercel previews)
- Votre domaine de production

**Important**: Mettez à jour les origines CORS dans `api/index.py` avec votre domaine de production réel.

## 🗄️ Collections Firestore

Le backend crée automatiquement ces collections:

### `quotes`
```json
{
  "serviceId": "string",
  "date": "string",
  "contact": {
    "name": "string",
    "email": "string",
    "phone": "string"
  },
  "fromZip": "string?",
  "toZip": "string?",
  "volume": "number?",
  "rooms": "number?",
  "housingType": "string?",
  "surface": "number?",
  "duration": "string?",
  "floor": "number?",
  "createdAt": "ISO timestamp",
  "status": "pending"
}
```

### `messages`
```json
{
  "name": "string",
  "email": "string",
  "subject": "string",
  "message": "string",
  "createdAt": "ISO timestamp",
  "status": "unread"
}
```

### `business_leads`
```json
{
  "companyName": "string",
  "contactName": "string",
  "email": "string",
  "phone": "string",
  "employeeCount": "string?",
  "serviceNeeds": "string",
  "createdAt": "ISO timestamp",
  "status": "new",
  "leadType": "b2b"
}
```

## 🔒 Sécurité

- ✅ Validation stricte avec Pydantic
- ✅ CORS configuré pour domaines spécifiques
- ✅ Credentials via variables d'environnement
- ✅ Gestion d'erreurs complète
- ✅ Logging des opérations
- ✅ Pas de données sensibles en hardcode

## 🧪 Tests

### Test Manuel avec cURL

```bash
# Test de santé
curl http://localhost:8000/

# Test de création de devis
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

### Test avec l'Interface Swagger

1. Allez sur `http://localhost:8000/api/docs`
2. Testez chaque endpoint interactivement
3. Visualisez les schémas de validation

## 📊 Monitoring

Les logs sont disponibles:
- **Local**: Console du terminal
- **Vercel**: Dashboard Vercel → Logs

Chaque opération importante est loggée:
- Création de quotes
- Messages de contact
- Requêtes chat
- Leads B2B
- Erreurs

## 🛠️ Troubleshooting

### Erreur: "Firebase credentials not found"
- Vérifiez que `FIREBASE_CREDENTIALS` ou `FIREBASE_PROJECT_ID` est défini
- Pour Vercel: Assurez-vous que la variable d'environnement est bien configurée

### Erreur CORS
- Vérifiez que l'origine du frontend est dans la liste `allow_origins`
- Ajoutez votre domaine de production

### Erreur 500 sur Vercel
- Vérifiez les logs dans le dashboard Vercel
- Assurez-vous que toutes les variables d'environnement sont configurées
- Vérifiez que le JSON Firebase est bien formaté (une seule ligne)

## 📝 Notes Importantes

1. **Ne jamais commiter** les fichiers `.env` ou les credentials Firebase
2. **Toujours utiliser** des variables d'environnement pour les secrets
3. **Mettre à jour** les origines CORS avec votre domaine de production
4. **Monitorer** les quotas Firebase
5. **Sauvegarder** régulièrement Firestore

## 🤝 Support

Pour toute question ou problème:
1. Vérifiez la documentation API: `/api/docs`
2. Consultez les logs Vercel
3. Vérifiez la configuration Firebase

---

**Développé avec ❤️ pour Batimove**
