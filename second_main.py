import os
import json
import sys
from datetime import datetime
from typing import Tuple, Dict, Any

from model_creating_dataset import create_dataset
from oracle import run_oracle_analysis


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


def get_user_input() -> Tuple[Dict[str, Any], str, str, str, int]:
    """
    Collect user-selected model, subset, context ambiguity, and number of pairs.
    Returns:
        model_config: dictionary with API and model metadata
        selected_subset: chosen BBQ subset
        context_condition: either 'ambig' or 'disambig'
        model_key: identifier string in MODEL_CONFIGS
        num_pairs: number of pairs to create
    """
    print("=" * 60)
    print("BBQ Dataset Analysis Pipeline")
    print("=" * 60)

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

    print("\nAvailable BBQ subsets:")
    for i, subset in enumerate(BBQ_SUBSETS, 1):
        print(f"  {i:2}. {subset}")

    while True:
        subset_choice = input("\nSelect subset (enter name or number): ").strip()
        if subset_choice.isdigit():
            idx = int(subset_choice) - 1
            if 0 <= idx < len(BBQ_SUBSETS):
                selected_subset = BBQ_SUBSETS[idx]
                break
        elif subset_choice in BBQ_SUBSETS:
            selected_subset = subset_choice
            break
        else:
            print(f"Invalid subset. Please choose from: {BBQ_SUBSETS}")

    print("\nAmbiguity setting:")
    print("  - 'y' or 'yes': ambig (ambiguous contexts)")
    print("  - 'n' or 'no': disambig (unambiguous contexts)")

    while True:
        ambig_choice = input("\nUse ambiguous contexts? (y/n): ").strip().lower()
        if ambig_choice in ['y', 'yes']:
            context_condition = "ambig"
            break
        elif ambig_choice in ['n', 'no']:
            context_condition = "disambig"
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")

    # Get number of pairs from user
    print("\nNumber of pairs:")
    print("  - Enter a positive integer for the number of pairs to create")
    print("  - Enter 'max' or leave empty to create all possible pairs")

    while True:
        pairs_input = input("\nHow many pairs do you want to create? (or 'max' for all): ").strip()
        
        if pairs_input == "" or pairs_input.lower() == "max":
            num_pairs = None
            print("Will create all possible pairs.")
            break
        
        try:
            num_pairs = int(pairs_input)
            if num_pairs > 0:
                print(f"Will create {num_pairs} pairs.")
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid positive integer or 'max'.")

    return model_config, selected_subset, context_condition, model_choice, num_pairs


def _assemble_log_dict(model_config: Dict[str, Any],
                        model_key: str,
                        subset: str,
                        context_condition: str,
                        dataset_results: Dict[str, Any],
                        oracle_results: Dict[str, Any],
                        num_pairs_requested: int
                        ) -> Dict[str, Any]:
    """
    Construct the dictionary that captures statistics for saving.
    Returns:
        Dictionary with metadata and statistics ready for serialization.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_data = {
        "timestamp": timestamp,
        "model_key": model_key,
        "model_name": model_config['model_name'],
        "model_base_url": model_config['base_url'],
        "subset": subset,
        "context_condition": context_condition,
        "num_pairs_requested": num_pairs_requested,
        "dataset_creation_time": datetime.now().isoformat(),
        "statistics": {
            "total_pairs_created": dataset_results.get("total_pairs", 0),
            "consistent_pairs": dataset_results.get("consistent_pairs", 0),
            "mixed_cant_determine": dataset_results.get("mixed_cant_determine", 0),
            "both_cant_determine": dataset_results.get("both_cant_determine", 0),
            "total_pairs_analyzed": oracle_results.get("total_pairs", 0),
            "fully_consistent_pairs": oracle_results.get("fully_consistent", 0),
            "inconsistent_reasoning_pairs": oracle_results.get("inconsistent_reasoning", 0),
            "biased_interpretation_pairs": oracle_results.get("biased_interpretation", 0),
            "total_flagged_pairs": oracle_results.get("total_flagged", 0),
            "flag_1_count": oracle_results.get("flag_1_count", 0),
            "flag_2_count": oracle_results.get("flag_2_count", 0),
            "flag_3_count": oracle_results.get("flag_3_count", 0),
            "flag_4_count": oracle_results.get("flag_4_count", 0),
        }
    }
    return log_data


def save_run_log(model_config: Dict[str, Any],
                model_key: str,
                subset: str,
                context_condition: str,
                dataset_results: Dict[str, Any],
                oracle_results: Dict[str, Any],
                num_pairs_requested: int
                ) -> Tuple[str, str]:
    """
    Save JSON and Markdown logs summarizing dataset and oracle statistics.
    Args:
        model_config: configuration dictionary of selected model
        model_key: identifier key of the model
        subset: selected BBQ subset string
        context_condition: ambiguity option used
        dataset_results: statistics from dataset creation
        oracle_results: statistics from oracle validation
        num_pairs_requested: number of pairs requested by user
    Returns:
        tuple of paths (json_log_file, markdown_log_file)
    """
    os.makedirs("logs", exist_ok=True)
    log_data = _assemble_log_dict(
        model_config, model_key, subset, context_condition,
        dataset_results, oracle_results, num_pairs_requested
    )

    timestamp = log_data["timestamp"]
    total_pairs_created = log_data["statistics"]["total_pairs_created"]
    total_pairs_analyzed = log_data["statistics"]["total_pairs_analyzed"]

    if total_pairs_created > 0:
        stats = log_data["statistics"]
        stats["consistent_percentage"] = stats["consistent_pairs"] / total_pairs_created * 100
        stats["mixed_cant_determine_percentage"] = stats["mixed_cant_determine"] / total_pairs_created * 100
        stats["both_cant_determine_percentage"] = stats["both_cant_determine"] / total_pairs_created * 100

    if total_pairs_analyzed > 0:
        stats = log_data["statistics"]
        stats["fully_consistent_percentage"] = stats["fully_consistent_pairs"] / total_pairs_analyzed * 100
        stats["inconsistent_percentage"] = stats["inconsistent_reasoning_pairs"] / total_pairs_analyzed * 100
        stats["biased_percentage"] = stats["biased_interpretation_pairs"] / total_pairs_analyzed * 100
        stats["flagged_percentage"] = stats["total_flagged_pairs"] / total_pairs_analyzed * 100

    log_file = f"logs/run_{model_key}_{subset}_{context_condition}_{timestamp}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    md_file = f"logs/run_summary_{model_key}_{subset}_{context_condition}_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        s = log_data["statistics"]
        f.write(f"# Analysis Run Summary\n\n")
        f.write(f"**Timestamp:** {timestamp}\n")
        f.write(f"**Model:** {model_config['model_name']} ({model_key})\n")
        f.write(f"**Base URL:** {model_config['base_url']}\n")
        f.write(f"**Subset:** {subset}\n")
        f.write(f"**Context Condition:** {context_condition}\n")
        f.write(f"**Pairs Requested:** {'All available' if num_pairs_requested is None else num_pairs_requested}\n")
        f.write(f"**Pairs Created:** {s['total_pairs_created']}\n\n")

        f.write("## Dataset Creation Results\n")
        f.write("| Metric | Count | Percentage |\n")
        f.write("|--------|-------|------------|\n")
        f.write(f"| Total Pairs Created | {s['total_pairs_created']} | - |\n")
        f.write(f"| Consistent Answers | {s['consistent_pairs']} | {s.get('consistent_percentage', 0):.1f}% |\n")
        f.write(f"| Mixed 'Can't Determine' | {s['mixed_cant_determine']} | {s.get('mixed_cant_determine_percentage', 0):.1f}% |\n")
        f.write(f"| Both 'Can't Determine' | {s['both_cant_determine']} | {s.get('both_cant_determine_percentage', 0):.1f}% |\n\n")

        f.write("## Oracle Analysis Results\n")
        f.write("| Metric | Count | Percentage |\n")
        f.write("|--------|-------|------------|\n")
        f.write(f"| Total Pairs Analyzed | {s['total_pairs_analyzed']} | - |\n")
        f.write(f"| Fully Consistent | {s['fully_consistent_pairs']} | {s.get('fully_consistent_percentage', 0):.1f}% |\n")
        f.write(f"| Inconsistent Reasoning | {s['inconsistent_reasoning_pairs']} | {s.get('inconsistent_percentage', 0):.1f}% |\n")
        f.write(f"| Biased Interpretation | {s['biased_interpretation_pairs']} | {s.get('biased_percentage', 0):.1f}% |\n")
        f.write(f"| Total Flagged Pairs | {s['total_flagged_pairs']} | {s.get('flagged_percentage', 0):.1f}% |\n\n")

        f.write("## Flag Breakdown\n")
        f.write("| Flag Type | Count | Percentage |\n")
        f.write("|-----------|-------|------------|\n")
        f.write(f"| Reasoning B doesn't match Input A/Output A | {s['flag_1_count']} | {s.get('flag_1_count', 0)/total_pairs_analyzed*100:.1f}% |\n")
        f.write(f"| Reasoning A doesn't match Input B/Output B | {s['flag_2_count']} | {s.get('flag_2_count', 0)/total_pairs_analyzed*100:.1f}% |\n")
        f.write(f"| Guessed Question doesn't resemble Question A | {s['flag_3_count']} | {s.get('flag_3_count', 0)/total_pairs_analyzed*100:.1f}% |\n")
        f.write(f"| Guessed Question doesn't resemble Question B | {s['flag_4_count']} | {s.get('flag_4_count', 0)/total_pairs_analyzed*100:.1f}% |\n")

    print(f"\nLog saved to: {log_file}")
    print(f"Summary saved to: {md_file}")

    return log_file, md_file


def main() -> None:
    """
    Execute full pipeline: fetch user input, generate dataset, run oracle, save logs.
    Returns:
        None
    """
    try:
        model_config, subset, context_condition, model_key, num_pairs = get_user_input()

        print(f"\n{'='*60}")
        print(f"Starting Pipeline Configuration:")
        print(f"  Model: {model_config['model_name']} ({model_key})")
        print(f"  Base URL: {model_config['base_url']}")
        print(f"  Subset: {subset}")
        print(f"  Context Condition: {context_condition}")
        print(f"  Number of Pairs: {'All available' if num_pairs is None else num_pairs}")
        print(f"{'='*60}")

        print(f"\nSTEP 1: Creating dataset with {model_key}...")
        dataset_results = create_dataset(
            model_config=model_config,
            subset=subset,
            context_condition=context_condition,
            max_pairs=num_pairs  # Changed from None to num_pairs
        )

        if not dataset_results:
            print("Dataset creation failed. Exiting.")
            return

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

        print(f"\nSTEP 3: Saving run log...")
        log_file, md_file = save_run_log(
            model_config, model_key, subset, context_condition,
            dataset_results, oracle_results, num_pairs
        )

        print(f"\n{'='*60}")
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"{'='*60}")

        total_pairs_created = dataset_results.get('total_pairs', 0)
        total_pairs_analyzed = oracle_results.get('total_pairs', 0)

        print(f"\nResults Summary:")
        print(f"\nDataset Creation:")
        print(f"  Total pairs created: {total_pairs_created}")
        if total_pairs_created > 0:
            print(f"  Consistent answer pairs: {dataset_results.get('consistent_pairs', 0)} ({dataset_results.get('consistent_pairs', 0)/total_pairs_created*100:.1f}%)")
            print(f"  Mixed 'Can't determine' pairs: {dataset_results.get('mixed_cant_determine', 0)} ({dataset_results.get('mixed_cant_determine', 0)/total_pairs_created*100:.1f}%)")
            print(f"  Both 'Can't determine' pairs: {dataset_results.get('both_cant_determine', 0)} ({dataset_results.get('both_cant_determine', 0)/total_pairs_created*100:.1f}%)")

        print(f"\nOracle Analysis:")
        print(f"  Total pairs analyzed: {total_pairs_analyzed}")
        if total_pairs_analyzed > 0:
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