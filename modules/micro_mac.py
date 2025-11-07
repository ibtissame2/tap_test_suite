import hashlib
import struct

class MicroMAC:
    """Module d'authentification Micro-MAC pour le système TAP"""
    
    def __init__(self, key=0xABC123):
        self.key = key
    
    def calculate_micro_mac(self, data, sequence):
        """
        Calcule le Micro-MAC (24 bits) pour un message
        
        Args:
            data: Donnees du capteur (16 bits)
            sequence: Compteur anti-rejeu (16 bits)
            
        Returns:
            int: Micro-MAC de 24 bits
        """
        # Combiner data, sequence et cle
        combined = (data << 32) | (sequence << 16) | self.key
        
        # Hachage simple (substitut leger pour AES-CMAC)
        hash_input = struct.pack('>Q', combined & 0xFFFFFFFFFFFFFFFF)
        hash_obj = hashlib.sha256(hash_input)
        hash_value = int.from_bytes(hash_obj.digest()[:4], 'big')
        
        # Réduire a 24 bits
        return hash_value & 0xFFFFFF
    
    def create_can_frame(self, data, sequence):
        """
        Cree une trame CAN complete avec Micro-MAC
        
        Returns:
            bytes: Trame CAN de 8 octets
        """
        micro_mac = self.calculate_micro_mac(data, sequence)
        
        # Structure: [Data(2)] [Seq(2)] [MAC(3)] [Reserved(1)]
        frame = bytearray(8)
        frame[0:2] = struct.pack('>H', data)
        frame[2:4] = struct.pack('>H', sequence)
        frame[4:7] = struct.pack('>I', micro_mac)[1:4]  # 3 octets
        frame[7] = 0  # Reserve
        
        return bytes(frame)
    
    def verify_can_frame(self, frame):
        """
        Verifie l'authenticite d'une trame CAN
        
        Returns:
            tuple: (valide, data, sequence)
        """
        if len(frame) != 8:
            return False, None, None
        
        data = struct.unpack('>H', frame[0:2])[0]
        sequence = struct.unpack('>H', frame[2:4])[0]
        received_mac = int.from_bytes(frame[4:7], 'big')
        expected_mac = self.calculate_micro_mac(data, sequence)
        
        return (received_mac == expected_mac, data, sequence)