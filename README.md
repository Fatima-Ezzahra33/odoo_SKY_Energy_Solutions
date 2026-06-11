# ☀️ Sky Energy — Module Odoo de Supervision Énergétique

> Module custom Odoo développé pour **SKY Energy Solutions** — Plateforme de gestion et de supervision des installations solaires photovoltaïques.

---

## 📋 Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Architecture technique](#architecture-technique)
- [Prérequis](#prérequis)
- [Installation & Démarrage](#installation--démarrage)
- [Structure du module](#structure-du-module)
- [Modèles de données](#modèles-de-données)
- [Sécurité et droits d'accès](#sécurité-et-droits-daccès)
- [Auteurs](#auteurs)

---

## À propos

**Sky Energy Monitoring** est un module Odoo 19 développé sur mesure pour répondre aux besoins opérationnels de **SKY Energy Solutions**, entreprise spécialisée dans la conception, l'installation et la maintenance de centrales solaires photovoltaïques.

Le module centralise l'ensemble du cycle de vie des actifs énergétiques au sein d'un seul outil ERP :

- **Gestion des actifs physiques** : inventaire des installations et des capteurs IoT déployés sur le terrain.
- **Supervision de la production** : collecte et historisation des relevés énergétiques horodatés.
- **Analyse de performance** : calcul automatique du Performance Ratio (PR) et classification par seuils.
- **Maintenance proactive** : système d'alertes métier et planification des interventions de terrain.
- **Contractualisation** : gestion des contrats de garantie de production énergétique avec calcul des pénalités.

---

## Fonctionnalités

| Fonctionnalité | Description |
| :--- | :--- |
| 🏭 **Gestion des installations** | Suivi du cycle de vie complet des parcs solaires (Brouillon → Actif → Maintenance → Arrêté) |
| 📡 **Inventaire des capteurs IoT** | Référencement des capteurs physiques (production, irradiation, température, onduleur) avec support des protocoles Modbus, MQTT, API et Manuel |
| ⚡ **Relevés énergétiques** | Saisie et historisation des mesures horodatées avec validation physique des données (plages de température et énergie positive) |
| 📊 **Calcul du Performance Ratio** | Calcul automatique du PR et de l'écart (%) avec classification d'état : Normal (≥90%), Avertissement (75–90%), Critique (<75%) |
| 🚨 **Système d'alertes** | Détection et qualification des anomalies (production basse, panne capteur, température haute, perte de communication) avec niveaux de sévérité |
| 🔧 **Interventions terrain** | Planification et suivi des missions de maintenance (corrective, préventive, inspection) avec assignation de techniciens |
| 📄 **Contrats de garantie** | Gestion des engagements contractuels de production annuelle avec paramétrage des seuils de tolérance et taux de pénalités |
| 🔐 **Sécurité par rôles** | Matrice d'accès différenciée pour les profils Manager, Technicien et Client (Portail) |

---

## Architecture technique

```
Odoo 19 (Docker)
    │
    ├── addons/sky_energy/          ← Module custom
    │   ├── models/                 ← 7 modèles de données Python
    │   ├── views/                  ← 8 fichiers XML de vues
    │   ├── security/               ← ACLs CSV + groupes & Record Rules XML
    │   └── data/                   ← Séquences automatiques (INST, ALT, INT)
    │
    └── Infrastructure Docker
        ├── Odoo 19.0               ← Port 8069
        └── PostgreSQL 18.3         ← Base de données
```

---

## Prérequis

- [Docker](https://www.docker.com/) et [Docker Compose](https://docs.docker.com/compose/) installés
- Git

---

## Installation & Démarrage

### 1. Cloner le dépôt

```bash
git clone https://github.com/Fatima-Ezzahra33/odoo_SKY_Energy_Solutions.git
cd odoo_SKY_Energy_Solutions
```

### 2. Lancer les conteneurs

```bash
docker compose up -d
```

Cette commande démarre deux services :
- **`web`** : Instance Odoo 19 accessible sur [http://localhost:8069](http://localhost:8069)
- **`db`** : Base de données PostgreSQL 18.3

### 3. Installer le module

1. Ouvrir le navigateur sur [http://localhost:8069](http://localhost:8069)
2. Créer ou sélectionner une base de données
3. Activer le **Mode développeur** (`Paramètres → Activer le mode développeur`)
4. Aller dans `Applications`, chercher **"Sky Energy Monitoring"** et cliquer sur **Installer**

### 4. Arrêter les conteneurs

```bash
docker compose down
```

> Pour réinitialiser complètement les données (volumes inclus) :
> ```bash
> docker compose down -v
> ```

---

## Structure du module

```
addons/sky_energy/
├── __init__.py                         # Point d'entrée Python du module
├── __manifest__.py                     # Déclaration du module (nom, version, dépendances)
│
├── models/
│   ├── __init__.py
│   ├── sky_installation.py             # Modèle central : Installation Solaire
│   ├── sky_capteur.py                  # Capteurs physiques IoT
│   ├── sky_lecture.py                  # Relevés énergétiques temporels
│   ├── sky_rendement.py                # Calcul du Performance Ratio
│   ├── sky_alerte.py                   # Alertes métier et supervision
│   ├── sky_contrat_garantie.py         # Contrats de garantie de production
│   └── sky_intervention.py            # Interventions de maintenance terrain
│
├── views/
│   ├── sky_installation_views.xml      # Vues formulaire + liste + action
│   ├── sky_capteur_views.xml
│   ├── sky_lecture_views.xml
│   ├── sky_rendement_views.xml
│   ├── sky_alerte_views.xml
│   ├── sky_contrat_garantie_views.xml
│   ├── sky_intervention_views.xml
│   └── sky_energy_menus.xml            # Menu racine et sous-menus
│
├── security/
│   ├── sky_energy_security.xml         # Groupes Odoo + Record Rules portail
│   └── ir.model.access.csv            # Matrice ACL par rôle (Manager, Technicien, Client)
│
└── data/
    └── sky_energy_sequence.xml         # Séquences auto (INST, ALT, INT)
```

---

## Modèles de données

### `sky.installation` — Installation Solaire
Modèle central du module. Représente un parc photovoltaïque physique lié à un client.

**Champs clés** : `reference` (auto), `partner_id`, `puissance_crete` (kWc), `orientation`, `inclinaison`, `date_mise_service`, `localisation`

**Cycle de vie** : `Brouillon` → `Active` → `En maintenance` → `Arrêtée`

---

### `sky.capteur` — Capteur Physique IoT
Inventaire des équipements de mesure déployés sur chaque installation.

**Types** : Production · Irradiation · Température · Onduleur

**Protocoles** : Modbus · MQTT · API · Manuel

---

### `sky.lecture` — Relevé Énergétique
Série temporelle des mesures collectées. Valide l'intégrité physique des données (énergie ≥ 0, température entre -30°C et +90°C).

**Champs clés** : `date_lecture`, `energie_kwh`, `irradiation`, `temperature`, `puissance_instantanee`, `source`

---

### `sky.rendement` — Performance Ratio
Analyse périodique automatique de la performance énergétique.

**Formules** :
- `PR = (Énergie Réelle / Énergie Prévue) × 100`
- `Écart = ((Réelle - Prévue) / Prévue) × 100`

**États automatiques** : `Normal` (PR ≥ 90%) · `Avertissement` (75–90%) · `Critique` (< 75%)

---

### `sky.alerte` — Alerte Métier
Anomalies détectées sur les installations avec niveaux de sévérité.

**Types** : Production basse · Capteur en panne · Température haute · Communication perdue

**Action intégrée** : Génération automatique d'une intervention corrective depuis la fiche alerte.

---

### `sky.contrat.garantie` — Contrat de Garantie
Engagements contractuels de production annuelle entre SKY Energy Solutions et ses clients.

**Paramètres financiers** : `energie_garantie_annuelle`, `tolerance_percent` (défaut 5%), `penalite_percent` (défaut 10%)

---

### `sky.intervention` — Intervention Terrain
Planification et suivi des missions de maintenance.

**Types** : Corrective · Préventive · Inspection

**Cycle de vie** : `Brouillon` → `Planifiée` → `Réalisée` / `Annulée`

---

## Sécurité et droits d'accès

### Groupes Odoo

| Groupe | Héritage | Description |
| :--- | :--- | :--- |
| **Manager** | Hérite de Technicien | Accès complet (CRUD) à toutes les entités, gestion des contrats et validation des interventions |
| **Technicien** | `base.group_user` | Saisie des relevés et interventions, lecture seule des installations et capteurs, aucun accès aux contrats |
| **Client (Portail)** | `base.group_portal` | Lecture seule de ses propres installations et relevés uniquement |

### Record Rules (Isolation Multitenant)

Le portail client est protégé par des règles d'accès dynamiques qui filtrent les enregistrements par propriétaire (`partner_id = user.partner_id`) afin de garantir qu'un client ne peut jamais consulter les données d'un autre.

---

## Auteurs

Développé par **SKY Energy Solutions**

Licence : `LGPL-3`
