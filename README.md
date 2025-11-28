# 🧠 Agent IA Finance – SmolAgents + Mistral + Langfuse

Agent IA spécialisé dans l'analyse financière, utilisant **SmolAgents**, **Mistral**, **Alpha Vantage**, **Yahoo Finance**, et un suivi complet des interactions via **Langfuse**.

L’application permet d’obtenir en temps réel :
- 📈 Prix des actions  
- 🔍 Indicateurs techniques (RSI, MACD)  
- 💱 Taux de change Forex  
- 🕒 Historique boursier  
- 🤖 Chat intelligent grâce à Mistral AI  
- 📊 Tracking des conversations dans Langfuse  

Application accessible via une interface **Gradio**.

---

## 🚀 Fonctionnalités

### 🔧 **Outils financiers intégrés**
- `get_realtime_price(symbol)` → Prix en temps réel (Alpha Vantage)  
- `get_stock_price(ticker)` → Prix via Yahoo Finance  
- `get_rsi(symbol)` → RSI 14 périodes  
- `get_macd(symbol)` → MACD + Signal + Histogramme  
- `get_forex_rate(pair)` → Taux de change Forex  
- `get_stock_history(symbol)` → Dernier jour d’historique boursier  

### 🤖 **Intelligence**
- Chat basé sur `mistral-small-latest` via API Mistral  
- Agent SmolAgents avec appels d’outils dynamiques  
- Mémoire conversationnelle locale simple  

### 📊 **Monitoring**
- Tracking complet via **Langfuse** : messages, réponses, outils utilisés  
- Observations sous forme de `span` pour faciliter le suivi  

---

## 🏗️ Tech Stack

| Composant | Utilisé pour |
|----------|--------------|
| Python 3.10+ | Langage principal |
| SmolAgents | Moteur d’agent IA |
| Mistral API | Modèle LLM |
| Alpha Vantage | Données boursières |
| Yahoo Finance | Données secondaires |
| Langfuse | Monitoring & analytics |
| Gradio | Interface utilisateur |

---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/TON-UTILISATEUR/TON-REPO.git
cd TON-REPO
### 2. Créer un environnement
bash
Copy code
conda create -n finance_agent python=3.10
conda activate finance_agent
### 3. Installer les dépendances
bash
Copy code
pip install -r requirements.txt
🔐 Variables d’environnement
Créer un fichier .env :

ini
Copy code
API_KEY=ta_clef_huggingface
MISTRAL_API_KEY=ta_clef_mistral
ALPHA_VANTAGE_KEY=ta_clef_alpha_vantage

LANGFUSE_PUBLIC_KEY=ta_clef_public_langfuse
LANGFUSE_SECRET_KEY=ta_clef_secret_langfuse
LANGFUSE_BASE_URL=https://cloud.langfuse.com
⚠️ Ne jamais pousser le fichier .env sur GitHub !

📊 Configuration Langfuse
Crée un projet sur : https://cloud.langfuse.com

Va dans Project Settings → API Keys

Copie public + secret dans ton fichier .env

Dans ton script, l’agent crée automatiquement un span :

python
Copy code
with langfuse.start_as_current_observation(as_type="span", name="agent_chat") as obs:
    obs.update(input={"user_message": message})
    output = str(agent.run(full_prompt))
    obs.update(output={"agent_response": output})
Tu peux suivre :

les prompts

les réponses

les appels d’outils

les erreurs

les tokens utilisés

les temps d’inférence

▶️ Lancer l’application
bash
Copy code
python forlf.py
Une interface Gradio va s’ouvrir automatiquement.

Avec share=True, Gradio génère aussi un lien public.

🧪 Exemples de requêtes
"Donne-moi le prix actuel de AAPL"

"Calcule le RSI de TSLA"

"Quel est le taux EUR/USD ?"

"Analyse-moi la tendance du Bitcoin"

"Affiche-moi le MACD de MSFT"

❗ Notes importantes
🔸 Quotas API
Alpha Vantage → très limité en version gratuite

Mistral → dépend du plan

Gradio share → expire au bout d’un moment

🔸 Sécurité
Ne pas exposer tes clés dans le code

Utiliser .env (déjà prévu)

🛠️ Améliorations à venir (TODO)
 Ajouter des graphiques (matplotlib via Gradio)

 Ajouter une base de données pour stocker l’historique des conversations

 Support des modèles locaux via Ollama

 Ajouter un outil d’analyse technique : Bollinger Bands

 Ajouter un mode "rapport PDF automatique"

 Ajouter une interface web en React

👤 Auteur
Jonathan/ Roockyb225

