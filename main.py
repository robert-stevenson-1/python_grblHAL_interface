#!/usr/bin/env python3
"""
Interactive command line interface for controlling the CNC Controller
NOTE: THIS IS DESIGNED FOR A MACHINE THAT DOES NOT HAVE AN X-AXIS
"""
from grblhal_controller import GRBLController

def main():
    controller = GRBLController()
    
    print("=== GRBLhal Controller ===")
    print("Commands:")
    print("  connect - Connect to controller")
    print("  home [Y|Z|YZ] - Home axes")
    print("  speed <rate> - Set feed rate (mm/min)")
    print("  move <Y|Z> <distance> - Move axis by distance")
    print("  rapid <Y|Z> <distance> - Rapid move axis")
    print("  status - Get machine status")
    print("  stop - Emergency stop")
    print("  quit - Exit program")
    print()
    
    try:
        while True:
            # get the user input command
            command = input(">>> ").strip().split()
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == "quit" or cmd == "exit":
                break
            elif cmd == "connect":
                controller.connect()
            elif cmd == "home":
                axes = command[1] if len(command) > 1 else "YZ"
                controller.home_axes(axes)
            elif cmd == "speed":
                if len(command) < 2:
                    print("Usage: speed <rate>")
                    continue
                controller.set_feed_rate(command[1])
            elif cmd == "move": # This one used speed set via the `speed` command above
                if len(command) < 3:
                    print("Usage: move <Y|Z> <distance>")
                    continue
                controller.move_axis(command[1], command[2], rapid=False)
            elif cmd == "rapid":
                if len(command) < 3:
                    print("Usage: rapid <Y|Z> <distance>")
                    continue
                controller.move_axis(command[1], command[2], rapid=True)
            elif cmd == "status":
                controller.get_status()
            elif cmd == "stop":
                controller.emergency_stop()
            else:
                print(f"Unknown command: {cmd}")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        controller.disconnect()
        print("Goodbye!")

if __name__ == "__main__":
    main()
