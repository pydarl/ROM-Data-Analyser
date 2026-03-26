import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
n_patients = 50
n_sessions_per_patient = 12  # 12 weeks of therapy

# Joint types and their typical ROM ranges
joints = {
    'shoulder': {'initial_range': (60, 120), 'final_range': (140, 180), 'healthy': 180},
    'elbow': {'initial_range': (80, 120), 'final_range': (135, 150), 'healthy': 150},
    'wrist': {'initial_range': (40, 60), 'final_range': (70, 85), 'healthy': 85},
    'knee': {'initial_range': (90, 120), 'final_range': (130, 145), 'healthy': 145},
    'ankle': {'initial_range': (15, 30), 'final_range': (40, 50), 'healthy': 50}
}

# Treatment types
treatments = ['Manual Therapy', 'Exercise-Based', 'Combined', 'Home Program']

# Generate data
data = []

for patient_id in range(1, n_patients + 1):
    # Patient characteristics
    age = np.random.randint(25, 75)
    gender = np.random.choice(['M', 'F'])
    joint_type = np.random.choice(list(joints.keys()))
    treatment = np.random.choice(treatments)

    # Initial ROM (injury severity)
    joint_info = joints[joint_type]
    initial_rom = np.random.uniform(*joint_info['initial_range'])

    # Recovery rate (influenced by age and treatment)
    base_recovery_rate = np.random.uniform(0.6, 0.9)
    age_factor = 1 - (age - 25) / 200  # Younger = better recovery
    treatment_factor = {'Manual Therapy': 1.1, 'Exercise-Based': 0.9,
                       'Combined': 1.2, 'Home Program': 0.8}[treatment]
    recovery_rate = base_recovery_rate * age_factor * treatment_factor

    # Target ROM
    target_rom = np.random.uniform(*joint_info['final_range'])
    max_improvement = target_rom - initial_rom

    # Generate session data
    start_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 180))

    for session in range(n_sessions_per_patient):
        # ROM progression with some noise
        progress = session / n_sessions_per_patient
        expected_rom = initial_rom + (max_improvement * progress * recovery_rate)

        # Add realistic variation
        noise = np.random.normal(0, 2)  # ±2 degrees variation
        measured_rom = expected_rom + noise

        # Ensure ROM doesn't exceed joint limits
        measured_rom = min(measured_rom, joint_info['healthy'])
        measured_rom = max(measured_rom, initial_rom)  # Can't go below initial

        # Session date
        session_date = start_date + timedelta(weeks=session)

        # Contact force (for devices like your robotic orthosis)
        contact_force = np.random.uniform(2, 8)  # Newtons

        # Pain level (decreases over time, 0-10 scale)
        pain_level = max(0, 8 - (session * 0.6) + np.random.uniform(-1, 1))

        # Sessions per week (compliance)
        sessions_per_week = np.random.choice([2, 3, 4], p=[0.3, 0.5, 0.2])

        data.append({
            'patient_id': f'P{patient_id:03d}',
            'session_number': session + 1,
            'date': session_date.strftime('%Y-%m-%d'),
            'age': age,
            'gender': gender,
            'joint_type': joint_type,
            'treatment_type': treatment,
            'rom_degrees': round(measured_rom, 1),
            'contact_force_n': round(contact_force, 2),
            'pain_level': round(pain_level, 1),
            'sessions_per_week': sessions_per_week,
            'initial_rom': round(initial_rom, 1),
            'target_rom': round(target_rom, 1)
        })

# Create DataFrame
df = pd.DataFrame(data)

# Add derived features
df['rom_improvement'] = df['rom_degrees'] - df['initial_rom']
df['percent_improvement'] = (df['rom_improvement'] / (df['target_rom'] - df['initial_rom']) * 100).round(1)
df['weeks_in_treatment'] = df['session_number']

# Save to CSV
df.to_csv('../raw/rom_rehabilitation_data.csv', index=False)

print(f"Generated {len(df)} records for {n_patients} patients")
print(f"\nDataset saved to: data/rom_rehabilitation_data.csv")
print(f"\nSample data:")
print(df.head(10))
print(f"\nDataset summary:")
print(df.describe())
