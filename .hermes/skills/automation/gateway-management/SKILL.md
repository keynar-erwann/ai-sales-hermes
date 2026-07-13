---
name: gateway-management
description: "Gestion des gateways de messagerie pour Hermes Agent."
---

# Gestion des Gateways Hermes

Ce skill aide à configurer, installer et déboguer les gateways de messagerie (Slack, Telegram, etc.) pour Hermes Agent.

## Références
- `references/slack-gateway-setup.md` : Procédure pour Slack (Incoming Webhooks).

## Commandes clés
- `hermes gateway install` : Installe le service systemd.
- `hermes gateway start/stop/status` : Contrôle le service.
- `hermes config set gateway.<platform>.webhook_url <url>` : Configure l'URL de réception.
