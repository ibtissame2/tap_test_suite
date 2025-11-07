import time

class TimingVerifier:
    """Module de verification des patterns temporels"""
    
    def __init__(self):
        self.sensors = {}
        self.anomaly_log = []
    
    def register_sensor(self, sensor_id, base_interval_ms, unique_delay_ms):
        """
        Enregistre un nouveau capteur avec son profil temporel
        
        Args:
            sensor_id: Identifiant du capteur
            base_interval_ms: Periode de transmission de base (ms)
            unique_delay_ms: Delai spécifique au capteur (ms)
        """
        self.sensors[sensor_id] = {
            'base_interval': base_interval_ms,
            'unique_delay': unique_delay_ms,
            'last_timestamp': None,
            'message_count': 0,
            'expected_interval': base_interval_ms + unique_delay_ms
        }
    
    def check_timing_anomaly(self, sensor_id, current_time_ms, tolerance_ms=2):
        """
        Verifie si un message arrive dans la fenêtre temporelle attendue
        
        Returns:
            bool: True si anomalie detectee, False sinon
        """
        if sensor_id not in self.sensors:
            return True  # Capteur non enregistre = anomalie
        
        sensor = self.sensors[sensor_id]
        
        # Premier message du capteur
        if sensor['last_timestamp'] is None:
            sensor['last_timestamp'] = current_time_ms
            sensor['message_count'] = 1
            return False
        
        # Calculer le temps attendu
        expected_interval = sensor['base_interval'] + sensor['unique_delay']
        expected_time = sensor['last_timestamp'] + expected_interval
        
        # Calculer l'ecart
        diff = current_time_ms - expected_time
        
        # Detecter anomalie
        is_anomaly = abs(diff) > tolerance_ms
        
        if is_anomaly:
            self.anomaly_log.append({
                'sensor_id': sensor_id,
                'expected': expected_time,
                'actual': current_time_ms,
                'diff': diff,
                'tolerance': tolerance_ms
            })
        
        # Mettre a jour le timestamp
        sensor['last_timestamp'] = current_time_ms
        sensor['message_count'] += 1
        
        return is_anomaly
    
    def get_sensor_stats(self, sensor_id):
        """Retourne les statistiques d'un capteur"""
        if sensor_id not in self.sensors:
            return None
        return self.sensors[sensor_id]
    
    def get_anomaly_log(self):
        """Retourne le journal des anomalies"""
        return self.anomaly_log
    
    def reset_sensor(self, sensor_id):
        """Reinitialise un capteur"""
        if sensor_id in self.sensors:
            self.sensors[sensor_id]['last_timestamp'] = None
            self.sensors[sensor_id]['message_count'] = 0