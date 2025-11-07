#!/usr/bin/env python3
"""
Test complet du module Security Escalation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.security_escalation import SecurityEscalation

def test_security_escalation_complet():
    print("=" * 60)
    print("TEST COMPLET DU MODULE SECURITY ESCALATION")
    print("=" * 60)
    
    sec = SecurityEscalation()
    tests_reussis = 0
    tests_totaux = 0
    
    print(f"Niveau initial: {sec.get_level_name()}")
    
    # Test 1: Fonctionnement normal en mode NORMAL
    print("\n🔹 TEST 1: Fonctionnement normal (mode NORMAL)")
    tests_totaux += 1
    action = sec.process_message('temp1', True, True)
    print(f"   Message légitime: action = '{action}'")
    
    if action == "ACCEPT":
        print("   ✅ TEST RÉUSSI - Message accepté")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Message rejeté")
    
    # Test 2: Première anomalie MAC
    print("\n🔹 TEST 2: Première anomalie MAC")
    tests_totaux += 1
    action = sec.process_message('temp1', False, True)
    print(f"   Anomalie MAC: action = '{action}'")
    print(f"   Compteur anomalies: {sec.anomaly_count}")
    
    if action == "REJECT" and sec.anomaly_count == 1:
        print("   ✅ TEST RÉUSSI - Anomalie comptabilisée")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Anomalie non traitée correctement")
    
    # Test 3: Seuil d'anomalies atteint -> Escalade
    print("\n🔹 TEST 3: Escalade après seuil d'anomalies")
    tests_totaux += 1
    action = sec.process_message('temp1', False, True)
    print(f"   Seuil atteint: action = '{action}'")
    print(f"   Niveau sécurité: {sec.get_level_name()}")
    
    if action.startswith("CHALLENGE:") and sec.get_level_name() == "MEDIUM":
        print("   ✅ TEST RÉUSSI - Escalade vers MEDIUM avec challenge")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Escalade manquée")
    
    # Test 4: Challenge-Response réussi
    print("\n🔹 TEST 4: Challenge-Response réussi")
    tests_totaux += 1
    
    # Récupérer le challenge envoyé
    if 'temp1' in sec.challenges:
        challenge = sec.challenges['temp1']
        expected_response = sec._calculate_expected_response(challenge, 'temp1')
        
        # Simuler réponse correcte
        result = sec.verify_challenge_response('temp1', expected_response)
        print(f"   Challenge réponse: {'✅ CORRECTE' if result else '❌ INCORRECTE'}")
        print(f"   Niveau après déescalade: {sec.get_level_name()}")
        
        if result and sec.get_level_name() == "NORMAL":
            print("   ✅ TEST RÉUSSI - Déescalade après challenge réussi")
            tests_reussis += 1
        else:
            print("   ❌ TEST ÉCHOUÉ - Déescalade échouée")
    else:
        print("   ❌ TEST ÉCHOUÉ - Challenge non trouvé")
    
    # Test 5: Escalade vers HIGH et blocage
    print("\n🔹 TEST 5: Escalade vers HIGH et blocage capteur")
    tests_totaux += 1
    
    # Forcer niveau HIGH
    sec.sec_level = sec.SEC_HIGH
    print(f"   Niveau forcé: {sec.get_level_name()}")
    
    # Message avec anomalie en mode HIGH
    action = sec.process_message('malicious1', False, False)
    print(f"   Action en mode HIGH: '{action}'")
    print(f"   Capteur bloqué: {'malicious1' in sec.blocked_sensors}")
    
    if action == "BLOCK_SENSOR" and 'malicious1' in sec.blocked_sensors:
        print("   ✅ TEST RÉUSSI - Capteur bloqué en mode HIGH")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Blocage échoué")
    
    # Test 6: Tentative d'accès après blocage
    print("\n🔹 TEST 6: Accès refusé après blocage")
    tests_totaux += 1
    action = sec.process_message('malicious1', True, True)  # Même avec données valides
    print(f"   Message après blocage: action = '{action}'")
    
    if action == "BLOCKED":
        print("   ✅ TEST RÉUSSI - Accès refusé pour capteur bloqué")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Accès autorisé par erreur")
    
    # Test 7: Challenge-Response échoué
    print("\n🔹 TEST 7: Challenge-Response échoué")
    tests_totaux += 1
    
    # Réescalader pour avoir un challenge
    sec.sec_level = sec.SEC_NORMAL
    sec.anomaly_count = 1
    action = sec.process_message('hacker1', False, True)
    
    if 'hacker1' in sec.challenges:
        # Réponse incorrecte
        wrong_response = 0x12345678
        result = sec.verify_challenge_response('hacker1', wrong_response)
        print(f"   Réponse incorrecte: {'✅ DÉTECTÉE' if not result else '❌ ACCEPTÉE'}")
        print(f"   Capteur bloqué: {'hacker1' in sec.blocked_sensors}")
        
        if not result and 'hacker1' in sec.blocked_sensors:
            print("   ✅ TEST RÉUSSI - Capteur bloqué après échec challenge")
            tests_reussis += 1
        else:
            print("   ❌ TEST ÉCHOUÉ - Échec challenge non traité")
    else:
        print("   ❌ TEST ÉCHOUÉ - Challenge non généré")
    
    # Affichage du journal de sécurité
    print("\n📋 Journal de sécurité:")
    log_entries = sec.get_security_log()
    for i, entry in enumerate(log_entries[-5:], 1):  # 5 dernières entrées
        print(f"   {i}. [{entry['timestamp']}] {entry['sensor_id']}: {entry['event_type']} - {entry['details']}")
    
    # Statut final
    status = sec.get_status()
    print(f"\n📊 Statut final:")
    print(f"   Niveau: {status['security_level']}")
    print(f"   Anomalies: {status['anomaly_count']}")
    print(f"   Capteurs bloqués: {len(status['blocked_sensors'])}")
    print(f"   Événements: {status['total_events']}")
    
    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL SECURITY ESCALATION")
    print("=" * 60)
    print(f"Tests réussis: {tests_reussis}/{tests_totaux}")
    print(f"Taux de réussite: {(tests_reussis/tests_totaux)*100:.1f}%")
    
    if tests_reussis == tests_totaux:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return tests_reussis == tests_totaux

if __name__ == "__main__":
    test_security_escalation_complet()