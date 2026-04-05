import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import messagebox, font, simpledialog
from PIL import Image, ImageTk
import time
import pygame
from playsound import playsound
# Initialize pygame mixer for playing sound
pygame.mixer.init()
error_sound = pygame.mixer.Sound("error_beep.mp3")
success_sound = pygame.mixer.Sound("success_sound.mp3")

# Initialize Mediapipe drawing and pose utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Helper function to calculate angles
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Tkinter GUI setup
root = tk.Tk()
root.title("FORMFIT")
root.geometry("400x500")
root.configure(bg="#E6E6FA")

# Fonts
title_font = font.Font(family="Helvetica", size=26, weight="bold")
subtitle_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=12)

# Welcome Screen Frame
welcome_frame = tk.Frame(root, bg='white', bd=2, relief='flat')
welcome_frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=450)

# Load and place logo image
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((250, 250))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(welcome_frame, image=logo_photo, bg="white")
logo_label.pack(pady=(20, 20))

# Show Exercise Selection Screen
def show_exercise_selection():
    welcome_frame.place_forget()
    card = tk.Frame(root, bg='white', bd=2, relief='flat')
    card.place(relx=0.5, rely=0.5, anchor='center', width=350, height=450)

    title_label = tk.Label(card, text="FORMFIT", font=title_font, bg="white", fg="#5D5FEF")
    title_label.pack(pady=(30, 10))

    subtitle_label = tk.Label(card, text="Choose the Exercise", font=subtitle_font, bg="white", fg="#7F7F7F")
    subtitle_label.pack(pady=(0, 20))

    button_frame = tk.Frame(card, bg="white")
    button_frame.pack(pady=10)

    arms_button = tk.Button(button_frame, text="Arms", command=lambda: ask_reps_and_start("Arms"), bg="#D1E8E4", fg="black", font=button_font, width=10, height=2, relief="flat")
    legs_button = tk.Button(button_frame, text="Legs", command=lambda: ask_reps_and_start("Legs"), bg="#D1E8E4", fg="black", font=button_font, width=10, height=2, relief="flat")
    squat_button = tk.Button(button_frame, text="Squat", command=lambda: ask_reps_and_start("Squat"), bg="#D1E8E4", fg="black", font=button_font, width=10, height=2, relief="flat")

    arms_button.pack(pady=10)
    legs_button.pack(pady=10)
    squat_button.pack(pady=10)

# Ask for number of reps and start
def ask_reps_and_start(exercise):
    try:
        target_reps = simpledialog.askinteger("Target Reps", "Enter the number of reps:", parent=root, minvalue=1)
        if target_reps:
            root.withdraw()
            process_exercise(exercise, target_reps)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Show Final Message
def show_final_message(score, total):
    root.deiconify()
    final_frame = tk.Frame(root, bg='white', bd=2, relief='flat')
    final_frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=450)

    pygame.mixer.Sound.play(success_sound)

    accuracy = (score / total) * 100
    if accuracy >= 90:
        result = "Excellent!"
    elif accuracy >= 70:
        result = "Good Job!"
    else:
        result = "Needs Improvement."

    message = f"\n🎉 Congratulations! 🎉\n\nYour Score: {score}/{total}\n{result}\nKeep going!"
    final_label = tk.Label(final_frame, text=message, font=subtitle_font, bg="white", fg="#5D5FEF", justify="center")
    final_label.pack(pady=100)

    close_button = tk.Button(final_frame, text="Close", font=button_font, command=root.quit, bg="#D1E8E4", fg="black", width=10, height=2, relief="flat")
    close_button.pack(pady=20)

# Start Button
def start_app():
    show_exercise_selection()

start_button = tk.Button(welcome_frame, text="Start", command=start_app, font=("Helvetica", 16), padx=20, pady=10)
start_button.pack(pady=(20, 10))

# Pose Instances for Each Exercise
pose_instances = {
    "Arms": mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5),
    "Legs": mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5),
    "Squat": mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
}


def process_exercise(exercise, target_reps):
    cap = cv2.VideoCapture(0)
    counter = 0 
    stage = "Nothing"
    form_status = ""
    bad_form_start_time = None
    error_played = False
    rep_start_time = None  
    speed_feedback = ""
    last_speed_time = 0
    show_speed_duration = 2  


    pose = pose_instances[exercise]
    

    while cap.isOpened():
        speed_feedback = ""
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            if exercise == "Arms":
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                angle = calculate_angle(shoulder, elbow, wrist)

                if angle > 160:
                    if stage in ["up", "Nothing"]:
                       rep_start_time = time.time() 
                    stage = "down"
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                    if rep_start_time:
                       duration = time.time() - rep_start_time
                       if duration < 1:
                           speed_feedback = "Fast Pace"
                       elif duration > 3:
                           speed_feedback = "Slow Pace"
                       else:
                            speed_feedback = "Good Pace"
                       speed_to_display = speed_feedback    
                       last_speed_time = time.time()



                if 18 <= angle <= 38:
                    if bad_form_start_time is None:
                        bad_form_start_time = time.time()
                        error_played = False
                    elif time.time() - bad_form_start_time >= 1:
                        form_status = "Bad Form"
                        if not error_played:
                            pygame.mixer.Sound.play(error_sound)
                            error_played = True
                else:
                    form_status = "Good Form"
                    bad_form_start_time = None
                    error_played = False

            elif exercise == "Legs":
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                angle_knee = calculate_angle(hip, knee, ankle)

                if 'leg_start_time' not in locals():
                    leg_start_time = None
                    leg_error_played = False

                if angle_knee > 160:
                   if stage in ["up", "Nothing"]:
                      rep_start_time = time.time()
                   stage = "down"
                if angle_knee <= 90 and stage == 'down':
                   stage = "up"
                   counter += 1
                   if rep_start_time:
                     duration = time.time() - rep_start_time
                     if duration < 1:
                        speed_feedback = "Fast Pace"
                     elif duration > 3:
                        speed_feedback = "Slow Pace"
                     else:
                        speed_feedback = "Good Pace"
                     speed_to_display = speed_feedback
                     last_speed_time = time.time()

                if 32 <= angle_knee < 90:
                    if leg_start_time is None:
                        leg_start_time = time.time()
                        leg_error_played = False
                    elif time.time() - leg_start_time > 1:
                        form_status = "Bad Form"
                        if not leg_error_played:
                            playsound("error_beep.mp3")
                            leg_error_played = True
                else:
                    if angle_knee > 90 or angle_knee < 30:
                        form_status = "Good Form"
                    else:
                        form_status = ""  
                    leg_start_time = None
                    leg_error_played = False



            elif exercise == "Squat":
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                angle_knee = calculate_angle(hip, knee, ankle)
                angle_hip = calculate_angle(shoulder, hip, knee)
                hip_angle = 180 - angle_hip

                if angle_knee > 160 and stage == "Nothing":
                    stage = "UP"
                    rep_start_time = time.time()
                
                if stage == "UP" and hip_angle <= 90:
                    stage = "DOWN"
                    counter += 1  # increment rep counter
                    rep_start_time = time.time()  # reset rep timer for next movement
    
                if angle_knee < 90 and stage == "DOWN":
                   stage = "UP"
                   rep_start_time = time.time()

                if  130 > angle_knee > 90 :
                   if bad_form_start_time is None:
                       bad_form_start_time = time.time()
                       error_played = False
                   elif time.time() - bad_form_start_time >= 1:
                       form_status = "Bad Form"
                       if not error_played:
                          playsound("error_beep.mp3")
                          error_played = True    
                else:
                    form_status = "Good Form"
                    bad_form_start_time = None
                    error_played = False

            # Draw landmarks and display information
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Display repetition counter and form status
            cv2.rectangle(image, (0,0), (290,73), (245,117,16), -1)
            cv2.putText(image, 'REPS', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, 'STAGE', (65,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, (60,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            cv2.putText(image, form_status, (400, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,0,255) if form_status=="Bad Form" else (0,255,0), 2, cv2.LINE_AA)
            if speed_feedback:
                color = (0,255,0) if "Good" in speed_feedback else (0,0,255) if "Fast" in speed_feedback else (255,0,0)
                cv2.putText(image, speed_feedback, (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)

                        # Display speed feedback if available and still within display duration
            if speed_to_display and (time.time() - last_speed_time < show_speed_duration):
                color = (0,255,0) if "Good" in speed_to_display else (0,0,255) if "Fast" in speed_to_display else (255,0,0)
                cv2.putText(image, speed_to_display, (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
            elif time.time() - last_speed_time >= show_speed_duration:
                speed_to_display = ""  # Clear the feedback after showing it for duration


        except:
            pass

        cv2.imshow('Exercise Feed', image)

        if counter >= target_reps:
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    show_final_message(counter, target_reps)

# Start button event
start_button.config(command=show_exercise_selection)
start_button.pack(pady=(100, 20))  # Moved Start button lower

root.mainloop()
