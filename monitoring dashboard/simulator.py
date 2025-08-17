import random
import time
import requests  # 👈 Needed to send data to FastAPI

MACHINES = [
    {"id": 1, "name": "Machine 1"},
    {"id": 2, "name": "Machine 2"},
    {"id": 3, "name": "Machine 3"},
]

def generate_status():
    return random.choice(["Running", "Stopped", "Fault"])

def generate_data(machine):
    status = generate_status()
    production_count = random.randint(100, 200) if status == "Running" else random.randint(0, 100)
    temperature = random.uniform(60, 100) if status == "Running" else random.uniform(20, 60)
    if status == "Fault":
        temperature += random.uniform(20, 50)
    energy = random.uniform(10, 50) if status == "Running" else random.uniform(0, 10)
    return {
        "machine_id": machine["id"],
        "name": machine["name"],
        "status": status,
        "production_count": production_count,
        "temperature": round(temperature, 2),
        "energy": round(energy, 2),
        "timestamp": time.time()
    }

if __name__ == "__main__":
    while True:
        for machine in MACHINES:
            data = generate_data(machine)
            print(data)
            try:
                response = requests.post("http://127.0.0.1:8000/machine-data", json=data)
                print("Sent to backend:", response.status_code)
            except requests.exceptions.RequestException as e:
                print("Failed to send data:", e)
        time.sleep(2)
