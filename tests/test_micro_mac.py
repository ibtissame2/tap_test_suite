#!/usr/bin/env python3
"""
Test complet du module Micro-MAC Authentication
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.micro_mac import MicroMAC

def test_micro_mac_complet():
    print("=" * 60)
    print("TEST COMPLET DU MODULE MICRO-MAC")
    print("=" * 60)
    
    # Initialisation avec clé secrète
    mac_system = MicroMAC(key=0xABC123)
    tests_reussis = 0
    tests_totaux = 0
    
    # Test 1: Message légitime
    print("\n🔹 TEST 1: Message légitime")
    tests_totaux += 1
    data = 45  # Température 45°C
    sequence = 123
    
    frame = mac_system.create_can_frame(data, sequence)
    print(f"   Trame générée: {frame.hex()}")
    
    valide, data_recu, seq_recu = mac_system.verify_can_frame(frame)
    print(f"   Vérification: {'✅ VALIDE' if valide else '❌ INVALIDE'}")
    print(f"   Data reçu: {data_recu}, Sequence: {seq_recu}")
    
    if valide and data_recu == data and seq_recu == sequence:
        print("   ✅ TEST RÉUSSI")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ")
    
    # Test 2: Attaque par modification de données
    print("\n🔹 TEST 2: Attaque par modification de données")
    tests_totaux += 1
    frame_corrompu = bytearray(frame)
    frame_corrompu[0] ^= 0xFF  # Corruption des données
    valide, _, _ = mac_system.verify_can_frame(bytes(frame_corrompu))
    print(f"   Attaque détectée: {'✅ OUI' if not valide else '❌ NON'}")
    
    if not valide:
        print("   ✅ TEST RÉUSSI")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ")
    
    # Test 3: Attaque par modification du MAC
    print("\n🔹 TEST 3: Attaque par modification du MAC")
    tests_totaux += 1
    frame_mac_corrompu = bytearray(frame)
    frame_mac_corrompu[5] ^= 0xFF  # Corruption du MAC
    valide, _, _ = mac_system.verify_can_frame(bytes(frame_mac_corrompu))
    print(f"   MAC corrompu détecté: {'✅ OUI' if not valide else '❌ NON'}")
    
    if not valide:
        print("   ✅ TEST RÉUSSI")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ")
    
    # Test 4: Rejeu de message
    print("\n🔹 TEST 4: Détection de rejeu")
    tests_totaux += 1
    ancien_frame = mac_system.create_can_frame(data, 100)  # Ancienne séquence
    nouveau_frame = mac_system.create_can_frame(data, 150)  # Nouvelle séquence
    
    valide_ancien, _, _ = mac_system.verify_can_frame(ancien_frame)
    valide_nouveau, _, _ = mac_system.verify_can_frame(nouveau_frame)
    
    print(f"   Ancienne séquence (100): {'✅ VALIDE' if valide_ancien else '❌ INVALIDE'}")
    print(f"   Nouvelle séquence (150): {'✅ VALIDE' if valide_nouveau else '❌ INVALIDE'}")
    
    if valide_nouveau:
        print("   ✅ TEST RÉUSSI")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ")
    
    # Test 5: Attaquant avec mauvaise clé
    print("\n🔹 TEST 5: Attaquant avec mauvaise clé")
    tests_totaux += 1
    attaquant_mac = MicroMAC(key=0xDEADBEEF)  # Mauvaise clé
    frame_attaque = attaquant_mac.create_can_frame(data, sequence)
    
    valide, _, _ = mac_system.verify_can_frame(frame_attaque)
    print(f"   Attaque clé invalide détectée: {'✅ OUI' if not valide else '❌ NON'}")
    
    if not valide:
        print("   ✅ TEST RÉUSSI")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ")
    
    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL MICRO-MAC")
    print("=" * 60)
    print(f"Tests réussis: {tests_reussis}/{tests_totaux}")
    print(f"Taux de réussite: {(tests_reussis/tests_totaux)*100:.1f}%")
    
    if tests_reussis == tests_totaux:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return tests_reussis == tests_totaux

if __name__ == "__main__":
    test_micro_mac_complet()