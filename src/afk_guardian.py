import cv2
import time
import threading
import numpy as np
from datetime import datetime, timedelta
from pynput import mouse, keyboard
from plyer import notification
import matplotlib.pyplot as plt
import os

class AFKGuardian:
    def __init__(self, afk_threshold=60):
        """
        Initialize the AFK Guardian.
        
        Args:
            afk_threshold: Time in seconds before user is considered AFK
        """
        self.afk_threshold = afk_threshold
        self.last_activity = time.time()
        self.is_face_present = False
        self.is_running = False
        self.activity_log = []
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = None
        
        # Create data directory if it doesn't exist
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def start(self):
        """Start monitoring user activity."""
        self.is_running = True
        
        # Start keyboard and mouse listeners
        self.keyboard_listener = keyboard.Listener(on_press=self._on_activity)
        self.mouse_listener = mouse.Listener(on_move=self._on_activity, 
                                            on_click=self._on_activity, 
                                            on_scroll=self._on_activity)
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        # Start webcam monitoring in a separate thread
        self.webcam_thread = threading.Thread(target=self._monitor_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()
        
        # Start AFK checking in a separate thread
        self.afk_thread = threading.Thread(target=self._check_afk)
        self.afk_thread.daemon = True
        self.afk_thread.start()
        
        print("AFK Guardian started. Press Ctrl+C to stop.")
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop monitoring user activity."""
        self.is_running = False
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        self._save_activity_log()
        print("AFK Guardian stopped.")
    
    def _on_activity(self, *args):
        """Update last activity timestamp when keyboard or mouse activity is detected."""
        self.last_activity = time.time()
    
    def _monitor_webcam(self):
        """Monitor webcam for face presence."""
        self.cap = cv2.VideoCapture(0)
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame from webcam")
                time.sleep(1)
                continue
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Update face presence status
            self.is_face_present = len(faces) > 0
            
            # Draw rectangle around faces (for debugging)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Display the resulting frame (comment out for production)
            cv2.imshow('AFK Guardian', frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.is_running = False
                break
                
            time.sleep(0.1)  # Reduce CPU usage
    
    def _check_afk(self):
        """Check if user is AFK and log activity."""
        last_status = "active"
        
        while self.is_running:
            current_time = time.time()
            time_since_activity = current_time - self.last_activity
            
            # Determine current status
            if time_since_activity > self.afk_threshold and not self.is_face_present:
                current_status = "afk"
                if last_status == "active":
                    self._send_notification("AFK Alert", "You've been away for too long!")
            else:
                current_status = "active"
            
            # Log status change
            if current_status != last_status:
                self.activity_log.append({
                    'timestamp': datetime.now(),
                    'status': current_status
                })
                last_status = current_status
            
            time.sleep(1)
    
    def _send_notification(self, title, message):
        """Send a desktop notification."""
        notification.notify(
            title=title,
            message=message,
            app_name="AFK Guardian",
            timeout=10
        )
    
    def _save_activity_log(self):
        """Save activity log to a file."""
        if not self.activity_log:
            return
            
        filename = os.path.join(self.data_dir, f"activity_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        with open(filename, 'w') as f:
            f.write("timestamp,status\n")
            for entry in self.activity_log:
                f.write(f"{entry['timestamp']},{entry['status']}\n")
        
        print(f"Activity log saved to {filename}")
    
    def generate_report(self, log_file=None):
        """Generate productivity report from activity log."""
        if log_file:
            # Load activity log from file
            self._load_activity_log(log_file)
        
        if not self.activity_log:
            print("No activity data available")
            return
        
        # Calculate active and AFK durations
        active_duration = timedelta()
        afk_duration = timedelta()
        
        for i in range(1, len(self.activity_log)):
            prev_entry = self.activity_log[i-1]
            curr_entry = self.activity_log[i]
            
            duration = curr_entry['timestamp'] - prev_entry['timestamp']
            
            if prev_entry['status'] == 'active':
                active_duration += duration
            else:
                afk_duration += duration
        
        # Plot the results
        labels = ['Active', 'AFK']
        sizes = [active_duration.total_seconds(), afk_duration.total_seconds()]
        
        plt.figure(figsize=(10, 6))
        
        # Pie chart
        plt.subplot(1, 2, 1)
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Activity Distribution')
        
        # Bar chart
        plt.subplot(1, 2, 2)
        plt.bar(labels, sizes, color=['green', 'red'])
        plt.ylabel('Time (seconds)')
        plt.title('Activity Duration')
        
        plt.tight_layout()
        
        # Save the plot
        plot_file = os.path.join(self.data_dir, f"activity_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(plot_file)
        plt.close()
        
        print(f"Report generated and saved to {plot_file}")
        
        # Print summary
        total_time = active_duration + afk_duration
        active_percentage = (active_duration.total_seconds() / total_time.total_seconds()) * 100 if total_time.total_seconds() > 0 else 0
        
        print("\nActivity Summary:")
        print(f"Total monitoring time: {total_time}")
        print(f"Active time: {active_duration} ({active_percentage:.1f}%)")
        print(f"AFK time: {afk_duration} ({100-active_percentage:.1f}%)")
        
        return plot_file
    
    def _load_activity_log(self, log_file):
        """Load activity log from a file."""
        self.activity_log = []
        
        with open(log_file, 'r') as f:
            # Skip header
            next(f)
            
            for line in f:
                timestamp_str, status = line.strip().split(',')
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                
                self.activity_log.append({
                    'timestamp': timestamp,
                    'status': status
                })