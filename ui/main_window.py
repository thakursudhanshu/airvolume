import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading
import time
import tkinter.messagebox as messagebox

from camera.camera import WebcamCapture
from gestures.gesture_detector import GestureDetector
from volume.volume_control import VolumeControl

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AirVolume")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.camera = WebcamCapture()
        self.detector = GestureDetector()
        self.volume_ctrl = VolumeControl()
        self.running = False
        self.sensitivity = 1.0
        self.prev_angle = None
        self.calibrated_angle = None
        self.muted = False
        self.current_vol = self.volume_ctrl.get_volume()
        self.volume_label.configure(text=f"Volume: {int(self.current_vol)}%")
        self.volume_progress.set(self.current_vol / 100)

        self.setup_ui()
        self.check_access()
        self.current_vol = self.volume_ctrl.get_volume()
        self.volume_label.configure(text=f"Volume: {int(self.current_vol)}%")
        self.volume_progress.set(self.current_vol / 100)

    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Webcam preview
        self.preview_label = ctk.CTkLabel(main_frame, text="Webcam Preview", width=400, height=300)
        self.preview_label.pack(pady=10)

        # Controls frame
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", pady=10)

        self.start_btn = ctk.CTkButton(controls_frame, text="Start Detection", command=self.toggle_detection)
        self.start_btn.pack(side="left", padx=10)

        self.calibrate_btn = ctk.CTkButton(controls_frame, text="Calibrate", command=self.calibrate)
        self.calibrate_btn.pack(side="left", padx=10)

        self.mute_btn = ctk.CTkButton(controls_frame, text="Mute", command=self.toggle_mute)
        self.mute_btn.pack(side="left", padx=10)

        # Sensitivity
        sensitivity_frame = ctk.CTkFrame(main_frame)
        sensitivity_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(sensitivity_frame, text="Sensitivity:").pack(side="left")
        self.sensitivity_slider = ctk.CTkSlider(sensitivity_frame, from_=0.1, to=3.0, command=self.set_sensitivity)
        self.sensitivity_slider.set(1.0)
        self.sensitivity_slider.pack(side="left", fill="x", expand=True, padx=10)

        # Info frame
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=10)

        self.volume_label = ctk.CTkLabel(info_frame, text="Volume: 0%")
        self.volume_label.pack(side="left", padx=10)

        self.volume_progress = ctk.CTkProgressBar(info_frame, width=150)
        self.volume_progress.pack(side="left", padx=10)
        self.volume_progress.set(0)

        self.fps_label = ctk.CTkLabel(info_frame, text="FPS: 0")
        self.fps_label.pack(side="left", padx=10)

        self.confidence_label = ctk.CTkLabel(info_frame, text="Confidence: 0%")
        self.confidence_label.pack(side="left", padx=10)

        self.gesture_label = ctk.CTkLabel(info_frame, text="Gesture: None")
        self.gesture_label.pack(side="left", padx=10)

    def check_access(self):
        # Check camera
        test_cap = cv2.VideoCapture(0)
        if not test_cap.isOpened():
            messagebox.showerror("Error", "Camera not accessible")
        test_cap.release()

        # Volume check is in VolumeControl

    def toggle_detection(self):
        if self.running:
            self.running = False
            self.camera.stop()
            self.start_btn.configure(text="Start Detection")
            self.gesture_label.configure(text="Gesture: Stopped")
        else:
            self.running = True
            self.camera.start()
            self.start_btn.configure(text="Stop Detection")
            threading.Thread(target=self.process_loop, daemon=True).start()

    def process_loop(self):
        prev_time = time.time()
        while self.running:
            frame = self.camera.get_frame()
            if frame is not None:
                landmarks, angle, confidence = self.detector.process_frame(frame)
                self.detector.draw_landmarks(frame, landmarks)

                gesture = "None"
                if angle is not None:
                    if self.calibrated_angle is not None:
                        diff = angle - self.calibrated_angle
                        if abs(diff) > 180:
                            if diff > 0:
                                diff -= 360
                            else:
                                diff += 360
                        if abs(diff) > 10:  # threshold
                            change = diff * self.sensitivity * 0.05
                            current_vol = self.volume_ctrl.get_volume()
                            new_vol = max(0, min(100, current_vol + change))
                            if not self.muted:
                                self.volume_ctrl.set_volume(new_vol)
                            self.volume_label.configure(text=f"Volume: {int(new_vol)}%")
                            self.volume_progress.set(new_vol / 100)
                            gesture = "Increasing" if change > 0 else "Decreasing"
                            self.calibrated_angle = angle  # update for continuous
                    else:
                        self.calibrated_angle = angle

                self.confidence_label.configure(text=f"Confidence: {int(confidence*100)}%")
                self.gesture_label.configure(text=f"Gesture: {gesture}")

                # Update preview
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = img.resize((400, 300))
                imgtk = ImageTk.PhotoImage(image=img)
                self.preview_label.configure(image=imgtk)
                self.preview_label.image = imgtk

                # FPS
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if curr_time - prev_time > 0 else 0
                prev_time = curr_time
                self.fps_label.configure(text=f"FPS: {int(fps)}")

            time.sleep(0.01)

    def calibrate(self):
        self.calibrated_angle = None
        self.prev_angle = None
        messagebox.showinfo("Calibrated", "Calibration reset. Start detection to calibrate.")

    def set_sensitivity(self, value):
        self.sensitivity = float(value)

    def toggle_mute(self):
        self.muted = not self.muted
        self.mute_btn.configure(text="Unmute" if self.muted else "Mute")
        if self.muted:
            self.volume_ctrl.set_volume(0)
        else:
            # restore? but for simplicity, just toggle
            pass