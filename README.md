🚗 TAP Test Suite – Trusted Automotive Protection
Système de sécurité automobile léger et intelligent pour réseaux CAN/LIN
Implémentation Python complète avec tests de validation

📖 Résumé
Le système TAP (Trusted Automotive Protection) est un framework de sécurité multi-couches conçu pour protéger les réseaux embarqués automobiles contre les attaques par injection, rejeu, falsification et compromission de capteurs. Il combine :

🔐 Micro-MAC Authentication – Signature cryptographique légère (3 octets)

⏱️ Timing Pattern Verification – Empreinte temporelle unique par capteur

🚨 Intelligent Security Escalation – Vérification adaptative selon le niveau de menace

🤝 Collaborative Sensor Voting – Consensus majoritaire entre capteurs redondants

🏗️ Architecture du projet

tap_test_suite/  

├── modules/   

│   ├── micro_mac.py

│   ├── timing_verifier.py

│   ├── security_escalation.py

│   └── sensor_voting.py

├── tests/    

│   ├── test_micro_mac.py

│   ├── test_timing.py

│   ├── test_escalation.py

│   ├── test_voting.py

│   └── test_integration.py

├── run_all_tests.py  

└── README.md

🧩 Modules principaux
1. Micro-MAC Authentication
Signature 24 bits par message CAN

Overhead minimal : 3 octets sur 8 (37,5%)

Anti-rejeu via compteur de séquence

Compatible microcontrôleurs 8 bits

2. Timing Pattern Verification
Chaque capteur a un "rythme cardiaque" unique

Détection d’anomalies temporelles (±2 ms)

Résistant aux attaques par manipulation de timing

3. Intelligent Security Escalation
Machine à états : NORMAL → MEDIUM → HIGH

Challenge-response en cas de suspicion

Blocage automatique des capteurs compromis

4. Collaborative Sensor Voting
Vote majoritaire entre capteurs redondants

Tolère jusqu’à 40% de capteurs compromis

Détection de valeurs aberrantes

🚀 Installation et utilisation
Prérequis
Python 3.7+

Aucune dépendance externe (pur Python)

Lancer les tests
bash
python3 run_all_tests.py
Exemple d’utilisation manuelle
python
from modules.micro_mac import MicroMAC
from modules.timing_verifier import TimingVerifier

# Initialisation
mac = MicroMAC(key=0xABC123)
timing = TimingVerifier()

# Création et vérification d’un message
frame = mac.create_can_frame(data=35, sequence=1)
is_valid, data, seq = mac.verify_can_frame(frame)
📊 Résultats de validation
Métrique	Valeur
Taux de détection d’attaques	97%
Faux positifs	0,82%
Latence moyenne	0,6–1,3 ms
Utilisation RAM	~250 octets
Débit maximal	775–1800 msg/s
Taux de réussite des tests	90% (27/30)
🛡️ Scénarios d’attaque testés
✅ Injection de message malveillant

✅ Rejeu d’anciens messages

✅ Manipulation temporelle

✅ Falsification de données

✅ Compromission de capteurs

🧪 Démonstration matérielle (optionnelle)
Matériel recommandé
Arduino Uno + Shield CAN MCP2515

Raspberry Pi 4 (ECU)

Capteurs I2C/SPI (DHT22, BMP280, etc.)

Bus CAN (paire torsadée H/L)

Scripts inclus
Code Arduino pour capteurs légitimes

Script Python pour validation ECU

Dashboard Web optionnel pour visualisation

📈 Performance
Complexité temporelle : O(1) pour la plupart des modules

Empreinte mémoire : 244 octets RAM, 2560 octets Flash

Coût estimé : ~1$ par nœud capteur

Support : ATmega328P, STM32F0, PIC16F

🧾 Références
ISO 11898-1:2015 – Controller Area Network (CAN)

SAE J1939 – Vehicle Network Standards

ISO/SAE 21434:2021 – Cybersecurity Engineering

NIST SP 800-185 – SHA-3 Derived Functions

👥 Auteurs
Développé dans le cadre d’un projet de hackathon 2025 – Sécurité Automobile.

📄 Licence
Ce projet est fourni à des fins éducatives et de recherche.
Voir le rapport complet pour les détails techniques et les limitations.

🎯 Résumé en une phrase
"Un système de confiance intelligent et stratifié qui protège même les plus petits capteurs automobiles avec une cryptographie légère, des empreintes temporelles et du travail d’équipe."

