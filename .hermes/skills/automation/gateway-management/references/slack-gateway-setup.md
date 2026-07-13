# Note sur la configuration de la Gateway Slack

Cette procédure capture la configuration réussie de la gateway Slack pour le profil `ai-sales`.

## Étapes de configuration

1.  **Vérification/Installation** :
    ```bash
    hermes gateway install
    ```
    Cela crée les services systemd nécessaires pour que la gateway survive aux déconnexions SSH.

2.  **Configuration du Webhook** :
    Utiliser l'URL fournie par Slack (via Incoming Webhooks) :
    ```bash
    hermes config set gateway.slack.webhook_url "https://hooks.slack.com/services/..."
    ```

3.  **Démarrage** :
    ```bash
    hermes gateway start --profile ai-sales
    ```

4.  **Vérification du statut** :
    ```bash
    hermes gateway status --profile ai-sales
    ```

## Pitfalls
- **Gateway service not installed** : Si `hermes gateway start` échoue, il faut systématiquement exécuter `hermes gateway install` avant.
- **Service Linger** : Pour que la gateway reste active après une déconnexion SSH, Hermes active automatiquement `systemd linger` lors de l'installation du service.
- **Tests** : On peut tester la connectivité directement avec `curl` avant de compter sur les commandes `hermes gateway` pour isoler si le problème vient de la config Hermes ou du webhook lui-même.
