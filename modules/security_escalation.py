import random

class SecurityEscalation:
    """Module d'escalade intelligente de sécurité"""
    
    SEC_NORMAL = 0
    SEC_MEDIUM = 1
    SEC_HIGH = 2
    
    def __init__(self):
        self.sec_level = self.SEC_NORMAL
        self.anomaly_count = 0
        self.max_anomalies_before_escalation = 2  # Réduit à 2 pour les tests
        self.blocked_sensors = set()
        self.challenges = {}
        self.security_log = []
    
    def process_message(self, sensor_id, is_mac_valid, is_timing_valid):
        """
        Traite un message et ajuste le niveau de sécurité
        
        Returns:
            str: Action a entreprendre
        """
        if sensor_id in self.blocked_sensors:
            self._log_event(sensor_id, "BLOCKED", "Capteur déjà bloqué")
            return "BLOCKED"
        
        # CORRECTION: Anomalie détectée si MAC OU timing invalide
        anomaly_detected = not is_mac_valid or not is_timing_valid
        
        # Niveau NORMAL
        if self.sec_level == self.SEC_NORMAL:
            if anomaly_detected:
                self.anomaly_count += 1
                issue_type = "MAC_INVALID" if not is_mac_valid else "TIMING_INVALID"
                self._log_event(sensor_id, issue_type, f"MAC:{is_mac_valid}, Timing:{is_timing_valid}")
                
                print(f"   [ESCALATION] Anomalie #{self.anomaly_count} - Seuil: {self.max_anomalies_before_escalation}")
                
                if self.anomaly_count >= self.max_anomalies_before_escalation:
                    self.escalate()
                    return self.send_challenge(sensor_id)
                return "REJECT"
            else:
                # Réinitialiser le compteur si tout est valide
                if self.anomaly_count > 0:
                    self.anomaly_count = 0
                return "ACCEPT"
        
        # Niveau MEDIUM
        elif self.sec_level == self.SEC_MEDIUM:
            if anomaly_detected:
                self.anomaly_count += 1
                self._log_event(sensor_id, "ANOMALY_DETECTED", 
                               f"MAC:{is_mac_valid}, Timing:{is_timing_valid}")
                
                if self.anomaly_count >= self.max_anomalies_before_escalation:
                    self.escalate()
                    return self.send_challenge(sensor_id)
                return "REJECT"
            else:
                # Bonne réponse consecutive = déescalade
                if self.anomaly_count > 0:
                    self.anomaly_count -= 1
                    if self.anomaly_count == 0:
                        self.deescalate()
                return "ACCEPT"
        
        # Niveau HIGH
        elif self.sec_level == self.SEC_HIGH:
            if anomaly_detected:
                self._log_event(sensor_id, "BLOCK_SENSOR", "Anomalie en mode HIGH")
                self.block_sensor(sensor_id)
                return "BLOCK_SENSOR"
            return "ACCEPT"
    
    def escalate(self):
        """Monte le niveau de sécurité"""
        if self.sec_level < self.SEC_HIGH:
            self.sec_level += 1
            self.anomaly_count = 0  # Réinitialiser après escalade
            self._log_event("SYSTEM", "ESCALATE", f"Niveau: {self.get_level_name()}")
            print(f"   [ESCALATION] ➡️  Passage au niveau {self.get_level_name()}")
    
    def deescalate(self):
        """Reduit le niveau de sécurité"""
        if self.sec_level > self.SEC_NORMAL:
            self.sec_level -= 1
            self._log_event("SYSTEM", "DEESCALATE", f"Niveau: {self.get_level_name()}")
            print(f"   [ESCALATION] ⬅️  Retour au niveau {self.get_level_name()}")
    
    def send_challenge(self, sensor_id):
        """Envoie un challenge au capteur"""
        challenge = random.randint(0, 0xFFFFFFFF)
        self.challenges[sensor_id] = challenge
        self._log_event(sensor_id, "CHALLENGE_SENT", f"Challenge: 0x{challenge:08X}")
        print(f"   [CHALLENGE] Envoyé à {sensor_id}: 0x{challenge:08X}")
        return f"CHALLENGE:{challenge:08X}"
    
    def verify_challenge_response(self, sensor_id, response):
        """
        Verifie la reponse a un challenge
        
        Returns:
            bool: True si reponse correcte
        """
        if sensor_id not in self.challenges:
            self._log_event(sensor_id, "CHALLENGE_ERROR", "Challenge non trouvé")
            return False
        
        expected = self._calculate_expected_response(self.challenges[sensor_id], sensor_id)
        
        if response == expected:
            del self.challenges[sensor_id]
            self.deescalate()
            self._log_event(sensor_id, "CHALLENGE_PASS", "Réponse correcte")
            return True
        else:
            self.block_sensor(sensor_id)
            self._log_event(sensor_id, "CHALLENGE_FAIL", 
                          f"Attendu: 0x{expected:08X}, Reçu: 0x{response:08X}")
            return False
    
    def _calculate_expected_response(self, challenge, sensor_id):
        """Calcule la reponse attendue (simulation)"""
        sensor_hash = hash(sensor_id) & 0xFFFFFFFF
        return (challenge ^ sensor_hash) & 0xFFFFFFFF
    
    def block_sensor(self, sensor_id):
        """Bloque un capteur compromis"""
        self.blocked_sensors.add(sensor_id)
        self._log_event(sensor_id, "SENSOR_BLOCKED", "Capteur isolé du réseau")
        print(f"   [BLOCK] 🚫 Capteur {sensor_id} bloqué")
    
    def unblock_sensor(self, sensor_id):
        """Débloque un capteur"""
        if sensor_id in self.blocked_sensors:
            self.blocked_sensors.remove(sensor_id)
            self._log_event(sensor_id, "SENSOR_UNBLOCKED", "Capteur débloqué")
    
    def get_level_name(self):
        """Retourne le nom du niveau actuel"""
        names = {
            self.SEC_NORMAL: "NORMAL", 
            self.SEC_MEDIUM: "MEDIUM", 
            self.SEC_HIGH: "HIGH"
        }
        return names[self.sec_level]
    
    def _log_event(self, sensor_id, event_type, details):
        """Journalise les événements de sécurité"""
        event = {
            'timestamp': self._get_current_timestamp(),
            'sensor_id': sensor_id,
            'event_type': event_type,
            'details': details,
            'security_level': self.get_level_name()
        }
        self.security_log.append(event)
    
    def _get_current_timestamp(self):
        """Retourne le timestamp actuel formaté"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_security_log(self):
        """Retourne le journal de sécurité"""
        return self.security_log
    
    def get_status(self):
        """Retourne le statut complet du système"""
        return {
            'security_level': self.get_level_name(),
            'anomaly_count': self.anomaly_count,
            'blocked_sensors': list(self.blocked_sensors),
            'pending_challenges': list(self.challenges.keys()),
            'total_events': len(self.security_log)
        }
    
    # AJOUT DE LA MÉTHODE MANQUANTE
    def force_anomaly(self, sensor_id):
        """Force une anomalie pour les tests (méthode de test)"""
        self.anomaly_count += 1
        self._log_event(sensor_id, "TEST_ANOMALY", "Anomalie forcée pour test")
        print(f"   [TEST] Anomalie forcée - Compteur: {self.anomaly_count}")
        
        # Vérifier si on doit escalader
        if self.anomaly_count >= self.max_anomalies_before_escalation:
            self.escalate()