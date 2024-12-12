# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
EggTimer
--------------------------------------------------------------------------
License:   
Copyright 2024 Sumin Jeong

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------



"""
import time
import threading
import button as BUTTON
import buzzer_music as BUZZER_MUSIC
import spi_screen as SPI_SCREEN
from threaded_timer import ThreadedTimer
from temperature_sensor import TemperatureSensor

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------


class EggTimer:
    """Egg Timer with Threaded Timer Integration"""

    def __init__(self, reset_button="P2_2", stop_button="P2_4",
                 set_6min_button="P2_6", set_8min_button="P2_8",
                 set_10min_button="P2_10", buzzer="P2_1", debug=False):
        """Initialize the Egg Timer."""
        self.debug = debug

        # Initialize buttons and components
        self.reset_button = BUTTON.Button(reset_button)
        self.stop_button = BUTTON.Button(stop_button)
        self.set_6min_button = BUTTON.Button(set_6min_button)
        self.set_8min_button = BUTTON.Button(set_8min_button)
        self.set_10min_button = BUTTON.Button(set_10min_button)
        self.spi_screen = SPI_SCREEN.SPI_Display()
        self.buzzer = BUZZER_MUSIC.BuzzerMusic(buzzer)

        # Initialize the threaded timer
        self.timer = ThreadedTimer(sleep_time=1)
        self.timer.set_update_callback(self._update_display)

        # Initialize temperature sensor
        self.temp_sensor = TemperatureSensor()  
        
        self._setup()

    def _setup(self):
        """Setup the hardware components."""
        self.spi_screen.blank()

    def _update_display(self, seconds_remaining):
        """Callback to update the display."""
        minutes = seconds_remaining // 60
        seconds = seconds_remaining % 60
        time_str = f"{minutes:02}:{seconds:02}"
        self.spi_screen.text(time_str)

        if seconds_remaining == 0:
            self.spi_screen.text("TIME'S UP!", fontsize=48, fontcolor=(255, 0, 0))  # Red "TIME'S UP!"
            self.buzzer.play_tone(880, 1.0, True)  # Play a tone when time is up
            if self.debug:
                print("Timer done!")

    def reset_timer(self):
        """Reset the timer."""
        self.timer.reset_timer(0)
        self.spi_screen.blank()
        if self.debug:
            print("Timer reset")

    def stop_timer(self):
        """Stop the timer."""
        self.timer.reset_timer(0)
        # self.spi_screen.text(time_str)
        if self.debug:
            print("Timer stopped")

    def start_timer(self, duration, label):
        """Start a timer."""
        self.timer.set_timer(duration)
        if not self.timer.is_alive():
            self.timer.start()
        if self.debug:
            print(f"{label} timer started: {duration} seconds")

    def run(self):
        """Run the main loop."""
        if self.debug:
            print("EggTimer is running")

        while True:
            try:
            # Check the water temperature
            current_temp = self.temp_sensor.get_temperature()
            if current_temp >= 100.0:  # Boiling temperature
                self.spi_screen.text("Water is boiling!\nPut eggs in now!", fontsize=32, fontcolor=(0, 255, 0))
                if self.debug:
                    print("Water boiling detected!")
            
            # Handle button interactions        
            if self.set_6min_button.is_pressed():
                self.start_timer(6 * 60, "6-minute")
            elif self.set_8min_button.is_pressed():
                self.start_timer(8 * 60, "8-minute")
            elif self.set_10min_button.is_pressed():
                self.start_timer(10 * 60, "10-minute")
            elif self.reset_button.is_pressed():
                self.reset_timer()
            elif self.stop_button.is_pressed():
                self.stop_timer()

            time.sleep(0.1)

        except Exception as e:
            if self.debug:
                print(f"Error in run loop: {e}")
                
    def cleanup(self):
        """Cleanup the hardware components."""
        self.timer.cleanup()
        self.spi_screen.display.text("Done")
        self.reset_button.cleanup()
        self.stop_button.cleanup()
        self.set_6min_button.cleanup()
        self.set_8min_button.cleanup()
        self.set_10min_button.cleanup()
        self.buzzer.cleanup()

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Program Start")
    egg_timer = EggTimer(debug=True)

    try:
        egg_timer.run()
    except KeyboardInterrupt:
        egg_timer.cleanup()

    print("Program Complete")
