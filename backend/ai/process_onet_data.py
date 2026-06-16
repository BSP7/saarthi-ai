import pandas as pd
import os
import random

SOC_DOMAINS = {
    "11": "Management",
    "13": "Business and Financial Operations",
    "15": "Computer and Mathematical",
    "17": "Architecture and Engineering",
    "19": "Life, Physical, and Social Science",
    "21": "Community and Social Service",
    "23": "Legal",
    "25": "Educational Instruction and Library",
    "27": "Arts, Design, Entertainment, Sports, and Media",
    "29": "Healthcare Practitioners and Technical",
    "31": "Healthcare Support",
    "33": "Protective Service",
    "35": "Food Preparation and Serving Related",
    "37": "Building and Grounds Cleaning and Maintenance",
    "39": "Personal Care and Service",
    "41": "Sales and Related",
    "43": "Office and Administrative Support",
    "45": "Farming, Fishing, and Forestry",
    "47": "Construction and Extraction",
    "49": "Installation, Maintenance, and Repair",
    "51": "Production",
    "53": "Transportation and Material Moving",
    "55": "Military Specific"
}

# The exactly 30 features the V2 assessment will use
FEATURES = {
    "Interests": ["Realistic", "Investigative", "Artistic", "Social", "Enterprising", "Conventional"],
    "Skills": ["Critical Thinking", "Programming", "Active Listening", "Reading Comprehension", "Speaking", "Writing", "Complex Problem Solving", "Decision Making"], # ONET uses "Judgment and Decision Making", but we will map if needed
    "Abilities": ["Deductive Reasoning", "Inductive Reasoning", "Problem Sensitivity", "Oral Comprehension", "Mathematical Reasoning", "Information Ordering", "Visualization", "Selective Attention"],
    "Knowledge": ["Computers and Electronics", "Mathematics", "Engineering and Technology", "Business", "Psychology", "Education and Training", "Medicine and Health", "Communications"]
}

# Mappings to catch slight name differences in ONET
ONET_NAME_MAPPING = {
    "Decision Making": "Judgment and Decision Making",
    "Business": "Administration and Management", # Close enough proxy if exact 'Business' doesn't exist
    "Medicine and Health": "Medicine and Dentistry",
    "Communications": "Communications and Media"
}

def process_onet():
    print("Loading O*NET datasets...")
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "datasets", "raw", "onet")
    
    # Load data
    df_occ = pd.read_excel(os.path.join(base_dir, "Occupation Data.xlsx"))
    df_ab = pd.read_excel(os.path.join(base_dir, "Abilities.xlsx"))
    df_kn = pd.read_excel(os.path.join(base_dir, "Knowledge.xlsx"))
    df_sk = pd.read_excel(os.path.join(base_dir, "Essential Skills.xlsx"))
    df_int = pd.read_excel(os.path.join(base_dir, "Career Interest Types.xlsx"))
    
    # Combine datasets
    df_combined = pd.concat([df_ab, df_kn, df_sk], ignore_index=True)
    df_im = df_combined[df_combined['Scale ID'] == 'IM'].copy()
    
    # For interests, scale is different (usually 1-7 or 'OI' for Occupational Interest)
    # The scale ID for interests is 'OI' usually, and data value is 1-7.
    df_int = df_int[df_int['Scale ID'] == 'OI'].copy()
    
    df_all_features = pd.concat([df_im, df_int], ignore_index=True)
    
    # Get all target ONET element names
    target_elements = []
    element_to_feature = {}
    for cat, items in FEATURES.items():
        for item in items:
            onet_name = ONET_NAME_MAPPING.get(item, item)
            target_elements.append(onet_name)
            element_to_feature[onet_name] = item
            
    df_filtered = df_all_features[df_all_features['Element Name'].isin(target_elements)].copy()
    df_pivot = df_filtered.pivot_table(index='O*NET-SOC Code', columns='Element Name', values='Data Value', aggfunc='mean')
    
    occ_map = df_occ.set_index('O*NET-SOC Code')['Title'].to_dict()
    desc_map = df_occ.set_index('O*NET-SOC Code')['Description'].to_dict()
    
    results = []
    
    for code, row in df_pivot.iterrows():
        title = occ_map.get(code, "Unknown Career")
        desc = desc_map.get(code, "")
        
        # Extract Domain
        major_group_code = code.split('-')[0]
        domain = SOC_DOMAINS.get(major_group_code, "Other")
        
        base_profile = {
            "soc_code": code,
            "occupation_title": title,
            "target_domain": domain,
            "description": desc
        }
        
        for onet_name, feature_name in element_to_feature.items():
            val = row.get(onet_name)
            if pd.isna(val):
                score = 1
            else:
                # Interests are usually out of 7, others out of 5
                if feature_name in FEATURES["Interests"]:
                    score = (val / 7.0) * 10
                else:
                    score = (val / 5.0) * 10
            base_profile[feature_name] = score
            
        # Data Augmentation (jitter) for ML training
        for _ in range(10):
            profile = base_profile.copy()
            for feature in element_to_feature.values():
                jitter = random.uniform(-0.5, 0.5)
                final_score = min(10, max(1, round(profile[feature] + jitter, 2)))
                profile[feature] = final_score
            results.append(profile)
            
    final_df = pd.DataFrame(results)
    
    # Save mapping of domains
    domain_mapping_path = os.path.join(os.path.dirname(__file__), "career_domains_mapping.csv")
    domains_df = final_df[['target_domain', 'soc_code', 'occupation_title']].drop_duplicates()
    domains_df.to_csv(domain_mapping_path, index=False)
    
    # Save main dataset
    output_path = os.path.join(os.path.dirname(__file__), "careers_dataset_v2.csv")
    final_df.to_csv(output_path, index=False)
    
    print(f"Successfully generated {len(final_df)} career profiles at {output_path}")
    print(f"Saved domains mapping to {domain_mapping_path}")

if __name__ == "__main__":
    process_onet()
