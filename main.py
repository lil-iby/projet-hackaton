from machine import Pin, PWM
import network
import urequests
import time

# === WIFI CONFIGURATION ===
WIFI_SSID = "S22 Ultra de Ibrahim"
WIFI_PASS = "mixl4038"

# === REQUEST PARAMETERS ===
latitude = 44.8378
longitude = -0.5792
radius_m = 1000 

# === VALUE TO DEGREE MAPPING ===
value_to_degree = {
    0: 0,
    1: 45,
    2: 90,
    3: 135,
    4: 180
}

# === WIFI CONNECTION ===
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.5)
    print("\nConnected to Wi-Fi:", wlan.ifconfig())

# === API CALL ===
def call_api(lat, lon, radius_m):
    url = f"https://hackathon.mathias-duprat.fr/api/liveTrafic?lat={lat}&long={lon}&radius={radius_m}"
    print("\nCalling API:", url)
    try:
        res = urequests.get(url)
        print("HTTP Code:", res.status_code)
        data = res.json()  # get JSON response
        res.close()
        return data
    except Exception as e:
        print("Error:", e)
        return None

#Servo motor
servo = PWM(Pin(25), freq=50)

def angle_to_duty_ns(angle):
    # convert 0-360° 
    min_ns = 500_000   # 0° → 0.5 
    max_ns = 3_000_000 # 360° → 2.5 ms
    return int(min_ns + (angle / 360) * (max_ns - min_ns))

#Speaker
# set the speaker GPIO25
buzzer = PWM(Pin(32))
# start mut
buzzer.duty(0)

def beep(frequency=2000, duration=0.12):
    buzzer.freq(frequency)
    buzzer.duty(512)
    time.sleep(duration)
    buzzer.duty(0)

# === MAIN LOOP ===
connect_wifi()
previous_value = None  # store previous value

while True:
    # --- Step 1: Call the API to get the latest traffic data ---
    data = call_api(latitude, longitude, radius_m)
    
    # --- Step 2: Check if 'moyenne_etat' exists in the response ---
    if data and 'moyenne_etat' in data:
        current_value = data['moyenne_etat']
        
        # --- Step 3: If first run, just store the value ---
        if previous_value is None:
            previous_value = current_value
            print(f"Initial moyenne_etat = {current_value}")
            angle = value_to_degree.get(current_value, None)
            servo.duty_ns(angle_to_duty_ns(angle))
            for a in range(0, angle, 5):
                servo.duty_ns(angle_to_duty_ns(angle))
            beep()
            time.sleep()
       
        # --- Step 4: Compare current value with previous value ---
        elif current_value != previous_value:
            print(f"Value changed from {previous_value} to {current_value}")
            # --- Step 5: Activate servo if value has changed ---
            angle = value_to_degree.get(current_value, None)
            servo.duty_ns(angle_to_duty_ns(100))
            previous_value = current_value
            beep()          # bip 
            time.sleep(0.12) 
        
        # --- Step 6: If value has not changed, do nothing ---
        else:
            print(f"No change, current value = {current_value}")
    
    # --- Step 7: Handle case where 'moyenne_etat' is missing ---
    else:
        print("'moyenne_etat' not found in API response")
    
    # --- Step 8: Wait before the next API call ---
    print("Waiting 10 seconds before next call...\n")
    time.sleep(10)

