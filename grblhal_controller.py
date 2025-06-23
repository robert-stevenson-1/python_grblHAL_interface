#!/usr/bin/env python3
"""
GRBLhal Controller Class
Handles communication with GRBLhal-controlled BTT SKR Pico over USB serial
"""

import serial
import serial.tools.list_ports
import time

class GRBLController:
    def __init__(self, port=None, baudrate=115200):
        self.serial_conn = None
        self.port = port
        self.baudrate = baudrate
        self.feed_rate = 1000  # Default feed rate in mm/min
        
    def list_ports(self):
        """List available serial ports"""
        ports = serial.tools.list_ports.comports()
        print("Available serial ports:")
        for i, port in enumerate(ports):
            print(f"{i+1}: {port.device} - {port.description}")
        return ports
    
    def connect(self, port=None):
        """Connect to the GRBLhal controller"""
        if port:
            self.port = port
            
        if not self.port:
            ports = self.list_ports()
            if not ports:
                print("No serial ports found!")
                return False
            
            try:
                choice = int(input("Select port number: ")) - 1
                self.port = ports[choice].device
            except (ValueError, IndexError):
                print("Invalid selection!")
                return False
        
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=2,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            time.sleep(2)  # Wait for connection to stabilize
            
            # Send a simple command to test connection
            response = self.send_command("?")
            if response:
                print(f"Connected to GRBLhal on {self.port}")
                print(f"Response: {response}")
                return True
            else:
                print("No response from controller")
                return False
                
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the controller"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected from controller")
    