#!/usr/bin/env python3
"""
Test complet du module Timing Verification
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.timing_verifier import TimingVerifier

def test_timing_verification_complet():
    print("=" * 60)
    print("TEST COMPLET DU MODULE TIMING VERIFICATION")
    print("=" * 60)
    
    timing = TimingVerifier()
    tests_reussis = 0
    tests_totaux = 0
    
    # Enregistrement des capteurs
    print("\n📋 Enregistrement des capteurs:")
    timing.register_sensor('temp1', base_interval_ms=100, unique_delay_ms=5)   # 105ms
    timing.register_sensor('pressure1', base_interval_ms=50, unique_delay_ms=12) # 62ms
    timing.register_sensor('speed1', base_interval_ms=20, unique_delay_ms=3)   # 23ms
    
    print("   ✅ Capteur temp1: intervalle 105ms")
    print("   ✅ Capteur pressure1: intervalle 62ms") 
    print("   ✅ Capteur speed1: intervalle 23ms")
    
    # Test 1: Transmissions normales
    print("\n🔹 TEST 1: Transmissions normales")
    tests_totaux += 1
    base_time = 1000
    anomalies_detectees = 0
    
    # Messages temp1 à intervalles corrects (105ms)
    times_temp1 = [base_time, base_time + 105, base_time + 210, base_time + 315]
    for t in times_temp1:
        anomaly = timing.check_timing_anomaly('temp1', t)
        if anomaly:
            anomalies_detectees += 1
        print(f"   temp1 @ {t}ms: {'🚨 ANOMALIE' if anomaly else '✅ OK'}")
    
    if anomalies_detectees == 0:
        print("   ✅ TEST RÉUSSI - Aucune fausse alerte")
        tests_reussis += 1
    else:
        print(f"   ❌ TEST ÉCHOUÉ - {anomalies_detectees} fausses alertes")
    
    # Test 2: Attaque temporelle (message trop tôt)
    print("\n🔹 TEST 2: Attaque temporelle (message trop tôt)")
    tests_totaux += 1
    timing.reset_sensor('temp1')  # Réinitialiser pour test propre
    
    # Message normal
    timing.check_timing_anomaly('temp1', base_time)
    
    # Message d'attaque (10ms trop tôt)
    attack_time = base_time + 95  # Au lieu de 105ms
    anomaly = timing.check_timing_anomaly('temp1', attack_time)
    print(f"   Attaque @ {attack_time}ms: {'🚨 DÉTECTÉE' if anomaly else '❌ MANQUÉE'}")
    
    if anomaly:
        print("   ✅ TEST RÉUSSI - Attaque détectée")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Attaque non détectée")
    
    # Test 3: Attaque temporelle (message trop tard)
    print("\n🔹 TEST 3: Attaque temporelle (message trop tard)")
    tests_totaux += 1
    timing.reset_sensor('pressure1')
    
    timing.check_timing_anomaly('pressure1', base_time)
    
    # Message avec retard important
    late_time = base_time + 80  # 18ms de retard vs 62ms attendu
    anomaly = timing.check_timing_anomaly('pressure1', late_time)
    print(f"   Retard @ {late_time}ms: {'🚨 DÉTECTÉ' if anomaly else '❌ MANQUÉ'}")
    
    if anomaly:
        print("   ✅ TEST RÉUSSI - Retard détecté")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Retard non détecté")
    
    # Test 4: Capteur non enregistré
    print("\n🔹 TEST 4: Capteur non enregistré")
    tests_totaux += 1
    anomaly = timing.check_timing_anomaly('unknown_sensor', base_time)
    print(f"   Capteur inconnu: {'🚨 DÉTECTÉ' if anomaly else '❌ MANQUÉ'}")
    
    if anomaly:
        print("   ✅ TEST RÉUSSI - Capteur inconnu détecté")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Capteur inconnu accepté")
    
    # Test 5: Tolérance aux variations mineures
    print("\n🔹 TEST 5: Tolérance aux variations mineures")
    tests_totaux += 1
    timing.reset_sensor('speed1')
    
    timing.check_timing_anomaly('speed1', base_time)
    
    # Variation dans la tolérance (±2ms)
    minor_variation_time = base_time + 24  # 1ms de différence
    anomaly = timing.check_timing_anomaly('speed1', minor_variation_time)
    print(f"   Variation mineure @ {minor_variation_time}ms: {'🚨 FAUSSE ALERTE' if anomaly else '✅ TOLÉRÉ'}")
    
    if not anomaly:
        print("   ✅ TEST RÉUSSI - Variation tolérée")
        tests_reussis += 1
    else:
        print("   ❌ TEST ÉCHOUÉ - Fausse alerte")
    
    # Affichage du journal des anomalies
    print("\n📋 Journal des anomalies détectées:")
    anomalies = timing.get_anomaly_log()
    if anomalies:
        for i, anomaly in enumerate(anomalies, 1):
            print(f"   {i}. {anomaly['sensor_id']}: écart de {anomaly['diff']}ms (tolérance: ±{anomaly['tolerance']}ms)")
    else:
        print("   Aucune anomalie enregistrée")
    
    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL TIMING VERIFICATION")
    print("=" * 60)
    print(f"Tests réussis: {tests_reussis}/{tests_totaux}")
    print(f"Taux de réussite: {(tests_reussis/tests_totaux)*100:.1f}%")
    print(f"Anomalies détectées: {len(anomalies)}")
    
    if tests_reussis == tests_totaux:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return tests_reussis == tests_totaux

if __name__ == "__main__":
    test_timing_verification_complet()