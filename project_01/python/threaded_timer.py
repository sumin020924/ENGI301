"""
--------------------------------------------------------------------------
Threaded Timer Driver
--------------------------------------------------------------------------
License:   
Copyright 2024 - Sumin Jeong

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

Threaded Timer Class

  This driver provides a timer that runs in its own execution thread
  
  This driver can take in a display to update the countdown value.



Software API:

  ThreadedTimer(sleep_time=1)
    - Timer will call udpdate_callback every "sleep_time" seconds
    
    start()
      - Starts the timer thread

    is_active()
      - Is the timer active?
    
    set_timer()
      - Set the timer countdown value (in seconds)

    reset_timer()
      - Reset the timer countdown and make the timer inactive

    run()
      - This will run the timer and countdown the time until zero and stop

    Callback Functions:
      - set_update_callback(function)
        - Excuted every "sleep_time" while the timer is active

"""
import time
import threading

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class ThreadedTimer(threading.Thread):
    """ Threaded Timer Class """
    end_time                      = None
    sleep_time                    = None
    timer_active                  = None
    stop_timer                    = None
    update_callback               = None

    def __init__(self, sleep_time=1.0):
        """ Initialize variables """
        # Call parent class constructor
        threading.Thread.__init__(self)
        
        # Initialize Class Variables      
        self.end_time        = 0
        self.sleep_time      = sleep_time
        self.timer_active    = False
        self.stop_timer      = False

        # All callback functions and values set to None if not used        
        
        # Initialize the hardware components        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """ No setup required. """
        pass

    # End def


    def is_active(self):
        """ Is the timer active?
        
           Returns:  True  - Timer is active
                     False - Timer is inactive
        """
        return self.timer_active

    # End def


    def set_timer(self, seconds):
        """ Set the timer value (in seconds) """
        self.end_time = time.time() + seconds + 1
        
    # End def


    def reset_timer(self, seconds):
        """ Reset the timer back to zero """
        self.end_time = 0
        
    # End def
    
    
    def run(self):
        """ Run the timer thread.  Execute callbacks as appropriate. """
        seconds_remaining = 0

        # Run timer monitor until told to stop        
        while(not self.stop_timer):
        
            # If there is time on the timer
            #   - Call the timer update callback
            #   - Sleep for "sleep time"
            #
            seconds_remaining = int(self.end_time - time.time())
            
            if (seconds_remaining > 0):
                self.timer_active = True
                
                if self.update_callback is not None:
                    self.update_callback(seconds_remaining)

            elif (seconds_remaining == 0):
                self.timer_active = True
                
                if self.update_callback is not None:
                    self.update_callback(seconds_remaining)
                
                self.end_time     = 0

            else:
                self.timer_active = False

            time.sleep(self.sleep_time)
            
        
        # Set the flag and press duration to allow the button thread to restart
        self.timer_active = False
        self.stop_timer   = False

    # End def

    
    def cleanup(self):
        """ Clean up the timer. """
        self.stop_timer = True
        
        while (self.stop_timer):
            time.sleep(self.sleep_time)
    
    # End def
    
    
    # -----------------------------------------------------
    # Callback Functions
    # -----------------------------------------------------

    def set_update_callback(self, function):
        """ Function excuted every "sleep_time" while the timer is active """
        self.update_callback = function
    
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Threaded Timer Test")

    # Create instantiation of the timer
    timer = ThreadedTimer()

    # Default update function
    def update_print(seconds_remaining):
        print("Time:  {0}".format(seconds_remaining))

    # Set up callback
    timer.set_update_callback(update_print)

    # Start the timer
    timer.start()
    
    # Print Timer Active
    print("Timer Active ? {0}".format(timer.is_active()))
    
    # Set the timer
    timer.set_timer(10)
    
    # Check active
    while (not timer.is_active()):
        time.sleep(1)
    
    while (timer.is_active()):
        time.sleep(1)

    # Set the timer to a new value
    timer.set_timer(20)

    # Get the main thread
    main_thread = threading.currentThread()
    
    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    try:
        while (True):
            # Do nothing in the main thread
            time.sleep(1)
        
    except KeyboardInterrupt:
        # Clean up the hardware
        timer.cleanup()

    # Wait for threads to complete        
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    print("Test Complete")

