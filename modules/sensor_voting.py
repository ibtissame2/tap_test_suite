class SensorVoting:
    """Module de vote collaboratif entre capteurs"""
    
    def __init__(self, threshold=3, tolerance=5):
        self.threshold = threshold  # Nombre minimum de votes concordants
        self.tolerance = tolerance  # Tolerance de variation acceptable
        self.voting_groups = {}
        self.voting_history = []
    
    def register_voting_group(self, group_name, sensor_ids):
        """Enregistre un groupe de capteurs redondants"""
        self.voting_groups[group_name] = {
            'sensors': sensor_ids,
            'readings': {},
            'consensus_failures': 0,
            'successful_votes': 0,
            'total_votes': 0
        }
    
    def submit_reading(self, group_name, sensor_id, value):
        """Soumet une lecture d'un capteur"""
        if group_name not in self.voting_groups:
            return False
        
        # Vérifier que le capteur appartient au groupe
        if sensor_id not in self.voting_groups[group_name]['sensors']:
            return False
        
        self.voting_groups[group_name]['readings'][sensor_id] = value
        return True
    
    def verify_voting(self, group_name):
        """
        Verifie le consensus du groupe de capteurs
        
        Returns:
            tuple: (consensus_atteint, valeur_consensuelle, details)
        """
        if group_name not in self.voting_groups:
            return False, None, "Groupe inexistant"
        
        group = self.voting_groups[group_name]
        readings_dict = group['readings']
        
        group['total_votes'] += 1
        
        if len(readings_dict) < self.threshold:
            return False, None, f"Lectures insuffisantes ({len(readings_dict)}/{self.threshold})"
        
        readings = list(readings_dict.values())
        sensor_ids = list(readings_dict.keys())
        
        # CORRECTION: Algorithme de consensus amélioré
        # Étape 1: Calculer la médiane (robuste aux valeurs extrêmes)
        sorted_readings = sorted(readings)
        n = len(sorted_readings)
        if n % 2 == 1:
            median = sorted_readings[n//2]
        else:
            median = (sorted_readings[n//2-1] + sorted_readings[n//2]) / 2
        
        # Étape 2: Identifier les lectures cohérentes avec la médiane
        consistent_readings = []
        consistent_sensors = []
        aberrant_sensors = []
        aberrant_values = []
        
        for sensor_id, reading in readings_dict.items():
            if abs(reading - median) <= self.tolerance:
                consistent_readings.append(reading)
                consistent_sensors.append(sensor_id)
            else:
                aberrant_sensors.append(sensor_id)
                aberrant_values.append(reading)
        
        # Étape 3: Vérifier le consensus
        consensus = len(consistent_readings) >= self.threshold
        
        if consensus:
            # Calculer la moyenne des lectures cohérentes seulement
            consensus_value = sum(consistent_readings) / len(consistent_readings)
            group['successful_votes'] += 1
            
            details = {
                'consistent_sensors': consistent_sensors,
                'aberrant_sensors': aberrant_sensors,
                'consistent_readings': len(consistent_readings),
                'total_readings': len(readings),
                'consensus_value': consensus_value,
                'median_reference': median,
                'all_readings': readings_dict.copy()
            }
            
            self._log_vote(group_name, True, details)
            return True, consensus_value, details
        else:
            group['consensus_failures'] += 1
            
            # CORRECTION: Fournir plus de détails en cas d'échec
            if len(consistent_readings) > 0:
                # Il y a des lectures cohérentes mais pas assez pour le consensus
                partial_value = sum(consistent_readings) / len(consistent_readings)
                details = {
                    'consistent_sensors': consistent_sensors,
                    'aberrant_sensors': aberrant_sensors,
                    'consistent_readings': len(consistent_readings),
                    'required_threshold': self.threshold,
                    'partial_value': partial_value,
                    'median_reference': median,
                    'all_readings': readings_dict.copy(),
                    'reason': f"Consensus impossible: {len(consistent_readings)}/{self.threshold} lectures cohérentes"
                }
            else:
                # Aucune lecture cohérente
                details = {
                    'consistent_sensors': [],
                    'aberrant_sensors': aberrant_sensors,
                    'consistent_readings': 0,
                    'required_threshold': self.threshold,
                    'median_reference': median,
                    'all_readings': readings_dict.copy(),
                    'reason': "Aucune lecture cohérente détectée"
                }
            
            self._log_vote(group_name, False, details)
            return False, None, details
    
    def _log_vote(self, group_name, success, details):
        """Journalise les résultats de vote"""
        vote_record = {
            'group_name': group_name,
            'timestamp': self._get_current_timestamp(),
            'success': success,
            'details': details
        }
        self.voting_history.append(vote_record)
    
    def _get_current_timestamp(self):
        """Retourne le timestamp actuel formaté"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_group_stats(self, group_name):
        """Retourne les statistiques d'un groupe"""
        if group_name not in self.voting_groups:
            return None
        
        group = self.voting_groups[group_name]
        total = group['total_votes']
        success = group['successful_votes']
        
        return {
            'total_votes': total,
            'successful_votes': success,
            'consensus_failures': group['consensus_failures'],
            'success_rate': (success / total * 100) if total > 0 else 0,
            'registered_sensors': group['sensors']
        }
    
    def reset_readings(self, group_name):
        """Reinitialise les lectures d'un groupe"""
        if group_name in self.voting_groups:
            self.voting_groups[group_name]['readings'] = {}
    
    def get_voting_history(self, group_name=None, limit=10):
        """Retourne l'historique des votes"""
        if group_name:
            history = [h for h in self.voting_history if h['group_name'] == group_name]
        else:
            history = self.voting_history
        
        return history[-limit:] if limit else history
    
    def set_voting_parameters(self, threshold=None, tolerance=None):
        """Modifie les paramètres de vote"""
        if threshold is not None:
            self.threshold = threshold
        if tolerance is not None:
            self.tolerance = tolerance