import csv
import random
import os

# Define the features and target careers
CAREERS = [
    "Software Engineer",
    "Data Scientist",
    "Product Manager",
    "UX/UI Designer",
    "Marketing Specialist",
    "Sales Executive",
    "HR Manager",
    "Financial Analyst"
]

def generate_profile(career):
    """Generates a random profile of scores (1-10) weighted towards a specific career."""
    profile = {
        "logical_reasoning": random.randint(1, 10),
        "coding_ability": random.randint(1, 10),
        "communication_skills": random.randint(1, 10),
        "creativity": random.randint(1, 10),
        "leadership": random.randint(1, 10),
        "data_analysis": random.randint(1, 10),
        "target_career": career
    }
    
    # Add weights to scores based on target career to make the dataset learnable
    if career == "Software Engineer":
        profile["coding_ability"] = random.randint(7, 10)
        profile["logical_reasoning"] = random.randint(6, 10)
    elif career == "Data Scientist":
        profile["data_analysis"] = random.randint(8, 10)
        profile["coding_ability"] = random.randint(6, 10)
        profile["logical_reasoning"] = random.randint(7, 10)
    elif career == "Product Manager":
        profile["communication_skills"] = random.randint(7, 10)
        profile["leadership"] = random.randint(7, 10)
        profile["logical_reasoning"] = random.randint(6, 10)
    elif career == "UX/UI Designer":
        profile["creativity"] = random.randint(8, 10)
        profile["communication_skills"] = random.randint(6, 10)
    elif career == "Marketing Specialist":
        profile["creativity"] = random.randint(7, 10)
        profile["communication_skills"] = random.randint(7, 10)
    elif career == "Sales Executive":
        profile["communication_skills"] = random.randint(8, 10)
        profile["leadership"] = random.randint(6, 10)
    elif career == "HR Manager":
        profile["communication_skills"] = random.randint(8, 10)
        profile["leadership"] = random.randint(7, 10)
    elif career == "Financial Analyst":
        profile["data_analysis"] = random.randint(7, 10)
        profile["logical_reasoning"] = random.randint(7, 10)
        
    return profile

def generate_dataset(filename="careers_dataset.csv", num_samples=2000):
    fields = [
        "logical_reasoning", "coding_ability", "communication_skills", 
        "creativity", "leadership", "data_analysis", "target_career"
    ]
    
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        
        for _ in range(num_samples):
            career = random.choice(CAREERS)
            profile = generate_profile(career)
            writer.writerow(profile)
            
    print(f"Successfully generated {num_samples} samples in {filename}")

if __name__ == "__main__":
    generate_dataset("ai/careers_dataset.csv")
