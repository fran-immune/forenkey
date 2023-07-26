
import unittest
import os
import sys

from interfaz import compress_folder
from interfaz import calculate_sha256_hash
from interfaz import encrypt_folder

class TestCompress(unittest.TestCase):

    def test_compress_folder(self):
        # Preparación
        test_folder = "test_data"
        file_size = 10000 # 10 KB
        
        # Ejecución
        compressed_file = compress_folder(test_folder)
        
        # Validación
        self.assertLess(os.path.getsize(compressed_file), file_size) # Comprueba compresión
        self.assertTrue(os.path.exists(compressed_file)) # Archivo fue creado
    

    #Sugeridas por Copilot
    def test_calculate_sha256_hash():
        assert calculate_sha256_hash("H:/4nsics/videoCCR") == "c0f9d0e4d9b0c0a5d5c9e8d0e4c9c0c9c0e"
        assert calculate_sha256_hash("H:/4nsics/videoCCR") != "c0f9d0e4d9b0c0a5d5c9e8d0e4c9c0c9c0e1"
        assert calculate_sha256_hash("H:/4nsics/videoCCR") != "c0f9d0e4d9b0c0a5d5c9e8d0e4c9c0c9c0e2"

    def test_compress_folder():
        assert compress_folder("H:/4nsics/videoCCR", "1234") == "H:/4nsics/videoCCR.zip"
        assert compress_folder("H:/4nsics/videoCCR", "1234") != "H:/4nsics/videoCCR.zip1"
        assert compress_folder("H:/4nsics/videoCCR", "1234") != "H:/4nsics/videoCCR.zip2"

    def test_encrypt_folder():
        assert encrypt_folder("H:/4nsics/videoCCR.zip", "1234") == "H:/4nsics/videoCCR.zip.enc"
        assert encrypt_folder("H:/4nsics/videoCCR.zip", "1234") != "H:/4nsics/videoCCR.zip.enc1"
        assert encrypt_folder("H:/4nsics/videoCCR.zip", "1234") != "H:/4nsics/videoCCR.zip.enc2"






