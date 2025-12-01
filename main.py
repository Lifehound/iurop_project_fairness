import os
import json
import sys
from datetime import datetime

# Import the modified modules
from model_creating_dataset import create_dataset
from oracle import run_oracle_analysis

# Model configurations with base_url, api_key, and model_name
MODEL_CONFIGS = {
    'chatgpt': {
        'base_url': "https://inference.api.nscale.com/v1",
        'api_key': "eyJhbGciOiJBMjU2R0NNS1ciLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiaXYiOiJKM3p6Y2pGNTExTEI3a2VsIiwia2lkIjoiSzRlM0Y3dkNfTzFIZzRzc2RjVVVVeUIySUhLSk1mWlFkTVpuNWx3c1FIdyIsInRhZyI6ImlmZHZWemxkSEhiV1ZUS1VJUy1RWnciLCJ0eXAiOiJhdCtqd3QifQ.dxhWfpjjoM3eFLKkKbXaX8nFljtah3tBL2r4FWMGhuY.-KeGen3iPasYpUy3.TubPcorRbKy6_rDA133SJdQWKIUiN6jerI7-ieTGDL1mDGxWkvNFnUSBD2PRA0cca8DeJRWQJyXGHprlTKOxEHR_0l4iRA8hCr80UiOPaBIrQI6xAd0N_0Fe5syqdRK7Xh252S0aBn9dESQBFVVCEJrqt5Ada4ndEFSet4Cym5lgBdbLr5kE9VP1IDzoHl9sc0snmBrRcTsAJfaKlisnkMTwIj2Gy8pVNM9PAaHNcFLKC0T2dbsiOFU0yym0zvhjQFl_64w0Bsjm5OPKlE4cL3ybL1q3i_PICEoHClL4VdE_ir69YxHI1blxWfW4qpzXTdz8U5JS5MGIBjEOSgBFOy09QwiQvb27pDVMEMlmKzPxBfvKnAHFITrFiHFFCBz5gi4DfbCDEtzkOh4fLTHCz1BnJ_mF8dJhNG4kvF5IMhd0QD7THxqKsebZXAILB68MTM_bk1VlA8Cz3qFnXfWCe88fODX_HqO2RW_cGeFXokHeEFDkuNrFcFUF2xd-qeAINz2COrxTB9WZUDzwqoto87mv8oqVjeihPed9w4wK7uBKfRAnS1V4ueN9TkoWoFapEDrB39pgW2-mHkBltfHgQNsPxSfhepGdkQv4umXKOWmu6hhSauUXpT1Hot-k4SI56o1uSwscq0vKEJzB4pNxyuJ5xdQhEUGm1rTcSVyL_VwGLGBgLKH0gzxWxArso9S8gA-EiHl_AiA7WKnaM0LSEgoC7uqNR028La-LJVDUZk6SlTpMJ6EgXaBN5c4dwWS6qiwp3Y0KzCBcikfdNVCGzin-SeGaS3RhW3wEWOGCG0cS5q36Cr5A1O14BI_L56zDUmpMkvrobK2Rs6fXngOjhgITJ1rvGOzzSjKTt1Fmcftowt5YaJCMhxx0ld6VH5k-.3qYQS9PDIn72fl7Nrv80rQ",
        'model_name': 'openai/gpt-oss-20b'
    },
    'deepseek': {
        'base_url': "https://api.deepseek.com",
        'api_key': "sk-2c08a0d7a3d246bdb77899cc2dbb88d2",
        'model_name': 'deepseek-reasoner'
    },
    'mistral': {
        'base_url': "https://inference.api.nscale.com/v1",
        'api_key': "eyJhbGciOiJBMjU2R0NNS1ciLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiaXYiOiJKM3p6Y2pGNTExTEI3a2VsIiwia2lkIjoiSzRlM0Y3dkNfTzFIZzRzc2RjVVVVeUIySUhLSk1mWlFkTVpuNWx3c1FIdyIsInRhZyI6ImlmZHZWemxkSEhiV1ZUS1VJUy1RWnciLCJ0eXAiOiJhdCtqd3QifQ.dxhWfpjjoM3eFLKkKbXaX8nFljtah3tBL2r4FWMGhuY.-KeGen3iPasYpUy3.TubPcorRbKy6_rDA133SJdQWKIUiN6jerI7-ieTGDL1mDGxWkvNFnUSBD2PRA0cca8DeJRWQJyXGHprlTKOxEHR_0l4iRA8hCr80UiOPaBIrQI6xAd0N_0Fe5syqdRK7Xh252S0aBn9dESQBFVVCEJrqt5Ada4ndEFSet4Cym5lgBdbLr5kE9VP1IDzoHl9sc0snmBrRcTsAJfaKlisnkMTwIj2Gy8pVNM9PAaHNcFLKC0T2dbsiOFU0yym0zvhjQFl_64w0Bsjm5OPKlE4cL3ybL1q3i_PICEoHClL4VdE_ir69YxHI1blxWfW4qpzXTdz8U5JS5MGIBjEOSgBFOy09QwiQvb27pDVMEMlmKzPxBfvKnAHFITrFiHFFCBz5gi4DfbCDEtzkOh4fLTHCz1BnJ_mF8dJhNG4kvF5IMhd0QD7THxqKsebZXAILB68MTM_bk1VlA8Cz3qFnXfWCe88fODX_HqO2RW_cGeFXokHeEFDkuNrFcFUF2xd-qeAINz2COrxTB9WZUDzwqoto87mv8oqVjeihPed9w4wK7uBKfRAnS1V4ueN9TkoWoFapEDrB39pgW2-mHkBltfHgQNsPxSfhepGdkQv4umXKOWmu6hhSauUXpT1Hot-k4SI56o1uSwscq0vKEJzB4pNxyuJ5xdQhEUGm1rTcSVyL_VwGLGBgLKH0gzxWxArso9S8gA-EiHl_AiA7WKnaM0LSEgoC7uqNR028La-LJVDUZk6SlTpMJ6EgXaBN5c4dwWS6qiwp3Y0KzCBcikfdNVCGzin-SeGaS3RhW3wEWOGCG0cS5q36Cr5A1O14BI_L56zDUmpMkvrobK2Rs6fXngOjhgITJ1rvGOzzSjKTt1Fmcftowt5YaJCMhxx0ld6VH5k-.3qYQS9PDIn72fl7Nrv80rQ",
        'model_name': 'mistralai/mixtral-8x22b-instruct-v0.1'
    }
}

# BBQ subsets
BBQ_SUBSETS = [
    'Age',
    'Disability_status',
    'Gender_identity',
    'Nationality',
    'Physical_appearance',
    'Race_ethnicity',
    'Race_x_SES',
    'Race_x_gender',
    'Religion',
    'SES',
    'Sexual_orientation'
]

def get_user_input():
    """Get user input for model, subset, and ambiguity setting."""
    print("=" * 60)
    print("BBQ Dataset Analysis Pipeline")
    print("=" * 60)
    
    # Get model choice
    print("\nAvailable models:")
    for key in MODEL_CONFIGS:
        print(f"  - '{key}'")
    
    while True:
        model_choice = input("\nSelect model (enter name in quotes): ").strip().lower()
        if model_choice in MODEL_CONFIGS:
            model_config = MODEL_CONFIGS[model_choice]
            print(f"Selected model: {model_config['model_name']}")
            break
        else:
            print(f"Invalid choice. Please enter one of: {list(MODEL_CONFIGS.keys())}")
    
    # Get subset choice
    print("\nAvailable BBQ subsets:")
    for i, subset in enumerate(BBQ_SUBSETS, 1):
        print(f"  {i:2}. {subset}")
    
    while True:
        try:
            subset_choice = input("\nSelect subset (enter name or number): ").strip()
            if subset_choice.isdigit():
                idx = int(subset_choice) - 1
                if 0 <= idx < len(BBQ_SUBSETS):
                    selected_subset = BBQ_SUBSETS[idx]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(BBQ_SUBSETS)}")
            elif subset_choice in BBQ_SUBSETS:
                selected_subset = subset_choice
                break
            else:
                print(f"Invalid subset. Please choose from: {BBQ_SUBSETS}")
        except ValueError:
            print("Invalid input. Please enter a valid number or subset name.")
    
    # Get ambiguity setting
    print("\nAmbiguity setting:")
    print("  - 'y' or 'yes': ambig (ambiguous contexts)")
    print("  - 'n' or 'no': unambig (unambiguous contexts)")
    
    while True:
        ambig_choice = input("\nUse ambiguous contexts? (y/n): ").strip().lower()
        if ambig_choice in ['y', 'yes']:
            context_condition = "ambig"
            print("Selected: ambig (ambiguous contexts)")
            break
        elif ambig_choice in ['n', 'no']:
            context_condition = "disambig"
            print("Selected: unambig (unambiguous contexts)")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")
    
    return model_config, selected_subset, context_condition, model_choice

def save_run_log(model_config, model_key, subset, context_condition, 
                 dataset_results, oracle_results):
    """Save run log with statistics."""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Prepare log data
    log_data = {
        "timestamp": timestamp,
        "model_key": model_key,
        "model_name": model_config['model_name'],
        "model_base_url": model_config['base_url'],
        "subset": subset,
        "context_condition": context_condition,
        "dataset_creation_time": datetime.now().isoformat(),
        "statistics": {
            # Dataset creation stats
            "total_pairs_created": dataset_results.get("total_pairs", 0),
            "consistent_pairs": dataset_results.get("consistent_pairs", 0),
            "mixed_cant_determine": dataset_results.get("mixed_cant_determine", 0),
            "both_cant_determine": dataset_results.get("both_cant_determine", 0),
            
            # Oracle analysis stats
            "total_pairs_analyzed": oracle_results.get("total_pairs", 0),
            "fully_consistent_pairs": oracle_results.get("fully_consistent", 0),
            "inconsistent_reasoning_pairs": oracle_results.get("inconsistent_reasoning", 0),
            "biased_interpretation_pairs": oracle_results.get("biased_interpretation", 0),
            "total_flagged_pairs": oracle_results.get("total_flagged", 0),
            
            # Flag breakdown
            "flag_1_count": oracle_results.get("flag_1_count", 0),  # reasoning b doesn't match input a/output a
            "flag_2_count": oracle_results.get("flag_2_count", 0),  # reasoning a doesn't match input b/output b
            "flag_3_count": oracle_results.get("flag_3_count", 0),  # guessed question doesn't resemble question a
            "flag_4_count": oracle_results.get("flag_4_count", 0),  # guessed question doesn't resemble question b
        }
    }
    
    # Calculate percentages
    total_pairs_created = log_data["statistics"]["total_pairs_created"]
    total_pairs_analyzed = log_data["statistics"]["total_pairs_analyzed"]
    
    if total_pairs_created > 0:
        stats = log_data["statistics"]
        stats["consistent_percentage"] = (stats["consistent_pairs"] / total_pairs_created * 100) if total_pairs_created > 0 else 0
        stats["mixed_cant_determine_percentage"] = (stats["mixed_cant_determine"] / total_pairs_created * 100) if total_pairs_created > 0 else 0
        stats["both_cant_determine_percentage"] = (stats["both_cant_determine"] / total_pairs_created * 100) if total_pairs_created > 0 else 0
    
    if total_pairs_analyzed > 0:
        stats = log_data["statistics"]
        stats["fully_consistent_percentage"] = (stats["fully_consistent_pairs"] / total_pairs_analyzed * 100) if total_pairs_analyzed > 0 else 0
        stats["inconsistent_percentage"] = (stats["inconsistent_reasoning_pairs"] / total_pairs_analyzed * 100) if total_pairs_analyzed > 0 else 0
        stats["biased_percentage"] = (stats["biased_interpretation_pairs"] / total_pairs_analyzed * 100) if total_pairs_analyzed > 0 else 0
        stats["flagged_percentage"] = (stats["total_flagged_pairs"] / total_pairs_analyzed * 100) if total_pairs_analyzed > 0 else 0
    
    # Save JSON log
    log_file = f"logs/run_{model_key}_{subset}_{context_condition}_{timestamp}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    # Save markdown summary with table
    md_file = f"logs/run_summary_{model_key}_{subset}_{context_condition}_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# Analysis Run Summary\n\n")
        f.write(f"**Timestamp:** {timestamp}\n")
        f.write(f"**Model:** {model_config['model_name']} ({model_key})\n")
        f.write(f"**Base URL:** {model_config['base_url']}\n")
        f.write(f"**Subset:** {subset}\n")
        f.write(f"**Context Condition:** {context_condition}\n\n")
        
        f.write("## Dataset Creation Results\n")
        f.write("| Metric | Count | Percentage |\n")
        f.write("|--------|-------|------------|\n")
        f.write(f"| Total Pairs Created | {log_data['statistics']['total_pairs_created']} | - |\n")
        f.write(f"| Consistent Answers | {log_data['statistics']['consistent_pairs']} | {log_data['statistics'].get('consistent_percentage', 0):.1f}% |\n")
        f.write(f"| Mixed 'Can\'t Determine' | {log_data['statistics']['mixed_cant_determine']} | {log_data['statistics'].get('mixed_cant_determine_percentage', 0):.1f}% |\n")
        f.write(f"| Both 'Can\'t Determine' | {log_data['statistics']['both_cant_determine']} | {log_data['statistics'].get('both_cant_determine_percentage', 0):.1f}% |\n\n")
        
        f.write("## Oracle Analysis Results\n")
        f.write("| Metric | Count | Percentage |\n")
        f.write("|--------|-------|------------|\n")
        f.write(f"| Total Pairs Analyzed | {log_data['statistics']['total_pairs_analyzed']} | - |\n")
        f.write(f"| Fully Consistent | {log_data['statistics']['fully_consistent_pairs']} | {log_data['statistics'].get('fully_consistent_percentage', 0):.1f}% |\n")
        f.write(f"| Inconsistent Reasoning | {log_data['statistics']['inconsistent_reasoning_pairs']} | {log_data['statistics'].get('inconsistent_percentage', 0):.1f}% |\n")
        f.write(f"| Biased Interpretation | {log_data['statistics']['biased_interpretation_pairs']} | {log_data['statistics'].get('biased_percentage', 0):.1f}% |\n")
        f.write(f"| Total Flagged Pairs | {log_data['statistics']['total_flagged_pairs']} | {log_data['statistics'].get('flagged_percentage', 0):.1f}% |\n\n")
        
        f.write("## Flag Breakdown\n")
        f.write("| Flag Type | Count | Percentage |\n")
        f.write("|-----------|-------|------------|\n")
        f.write(f"| Reasoning B doesn't match Input A/Output A | {log_data['statistics']['flag_1_count']} | {log_data['statistics'].get('flag_1_count', 0)/total_pairs_analyzed*100:.1f}% |\n")
        f.write(f"| Reasoning A doesn't match Input B/Output B | {log_data['statistics']['flag_2_count']} | {log_data['statistics'].get('flag_2_count', 0)/total_pairs_analyzed*100:.1f}% |\n")
        f.write(f"| Guessed Question doesn't resemble Question A | {log_data['statistics']['flag_3_count']} | {log_data['statistics'].get('flag_3_count', 0)/total_pairs_analyzed*100:.1f}% |\n")
        f.write(f"| Guessed Question doesn't resemble Question B | {log_data['statistics']['flag_4_count']} | {log_data['statistics'].get('flag_4_count', 0)/total_pairs_analyzed*100:.1f}% |\n")
    
    print(f"\n✓ Log saved to: {log_file}")
    print(f"✓ Summary saved to: {md_file}")
    
    return log_file, md_file

def main():
    """Main pipeline execution."""
    try:
        # Get user input
        model_config, subset, context_condition, model_key = get_user_input()
        
        print(f"\n{'='*60}")
        print(f"Starting Pipeline Configuration:")
        print(f"  Model: {model_config['model_name']} ({model_key})")
        print(f"  Base URL: {model_config['base_url']}")
        print(f"  Subset: {subset}")
        print(f"  Context Condition: {context_condition}")
        print(f"{'='*60}")
        
        # Step 1: Create dataset using the selected model
        print(f"\nSTEP 1: Creating dataset with {model_key}...")
        dataset_results = create_dataset(
            model_config=model_config,
            subset=subset,
            context_condition=context_condition,
            max_pairs=None  # Use all available pairs
        )
        
        if not dataset_results:
            print("Dataset creation failed. Exiting.")
            return
        
        # Step 2: Run oracle analysis using the same model configuration
        print(f"\nSTEP 2: Running oracle analysis with {model_key}...")
        oracle_results = run_oracle_analysis(
            model_config=model_config,
            model_key=model_key,
            subset=subset,
            context_condition=context_condition
        )
        
        if not oracle_results:
            print("Oracle analysis failed. Exiting.")
            return
        
        # Step 3: Save run log
        print(f"\nSTEP 3: Saving run log...")
        log_file, md_file = save_run_log(
            model_config, model_key, subset, context_condition,
            dataset_results, oracle_results
        )
        
        # Display summary
        print(f"\n{'='*60}")
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"{'='*60}")
        
        total_pairs_created = dataset_results.get('total_pairs', 0)
        total_pairs_analyzed = oracle_results.get('total_pairs', 0)
        
        print(f"\nResults Summary:")
        print(f"\nDataset Creation:")
        print(f"  Total pairs created: {total_pairs_created}")
        print(f"  Consistent answer pairs: {dataset_results.get('consistent_pairs', 0)} ({dataset_results.get('consistent_pairs', 0)/total_pairs_created*100:.1f}%)")
        print(f"  Mixed 'Can't determine' pairs: {dataset_results.get('mixed_cant_determine', 0)} ({dataset_results.get('mixed_cant_determine', 0)/total_pairs_created*100:.1f}%)")
        print(f"  Both 'Can't determine' pairs: {dataset_results.get('both_cant_determine', 0)} ({dataset_results.get('both_cant_determine', 0)/total_pairs_created*100:.1f}%)")
        
        print(f"\nOracle Analysis:")
        print(f"  Total pairs analyzed: {total_pairs_analyzed}")
        print(f"  Fully consistent pairs: {oracle_results.get('fully_consistent', 0)} ({oracle_results.get('fully_consistent', 0)/total_pairs_analyzed*100:.1f}%)")
        print(f"  Inconsistent reasoning pairs: {oracle_results.get('inconsistent_reasoning', 0)} ({oracle_results.get('inconsistent_reasoning', 0)/total_pairs_analyzed*100:.1f}%)")
        print(f"  Biased interpretation pairs: {oracle_results.get('biased_interpretation', 0)} ({oracle_results.get('biased_interpretation', 0)/total_pairs_analyzed*100:.1f}%)")
        print(f"  Total flagged pairs: {oracle_results.get('total_flagged', 0)} ({oracle_results.get('total_flagged', 0)/total_pairs_analyzed*100:.1f}%)")
        
        print(f"\nFlag Breakdown:")
        print(f"  Flag 1 (Reasoning B mismatch): {oracle_results.get('flag_1_count', 0)} ({oracle_results.get('flag_1_count', 0)/total_pairs_analyzed*100:.1f}%)")
        print(f"  Flag 2 (Reasoning A mismatch): {oracle_results.get('flag_2_count', 0)} ({oracle_results.get('flag_2_count', 0)/total_pairs_analyzed*100:.1f}%)")
        print(f"  Flag 3 (Question A bias): {oracle_results.get('flag_3_count', 0)} ({oracle_results.get('flag_3_count', 0)/total_pairs_analyzed*100:.1f}%)")
        print(f"  Flag 4 (Question B bias): {oracle_results.get('flag_4_count', 0)} ({oracle_results.get('flag_4_count', 0)/total_pairs_analyzed*100:.1f}%)")
        
        print(f"\nLog files saved in 'logs/' directory")
        
    except KeyboardInterrupt:
        print("\nPipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError in pipeline: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()