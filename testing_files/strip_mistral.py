import json
import re
import os
from pathlib import Path

def parse_consistency_from_raw_output(raw_output):
    """
    Parse the raw output to determine if 'yes' or 'no' was actually said.
    """
    if not raw_output:
        return "unknown"
    
    # Look for "Answer: yes" or "Answer: no" patterns in the raw output
    patterns = [
        r'Answer:\s*(yes|no)\s*$',
        r'Answer:\s*(yes|no)[\s\.]',
        r'^Answer:\s*(yes|no)\s*\n',
        r'"Answer":\s*"(yes|no)"',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, raw_output, re.IGNORECASE | re.MULTILINE)
        if match:
            answer = match.group(1).lower()
            return answer
    
    # If not found, search for "yes" or "no" near the beginning
    lines = raw_output.strip().split('\n')
    for line in lines[:3]:
        line_lower = line.lower().strip()
        if line_lower.startswith('yes'):
            return 'yes'
        elif line_lower.startswith('no'):
            return 'no'
        elif 'yes' in line_lower and 'no' not in line_lower:
            return 'yes'
        elif 'no' in line_lower and 'yes' not in line_lower:
            return 'no'
    
    return "unknown"

def analyze_jsonl_file(file_path):
    """
    Analyze a JSONL file and extract cross-consistency information.
    Returns statistics in the requested format.
    """
    total_pairs = 0
    reasoning_b_no_match = 0  # Flag 1: A_to_B inconsistent
    reasoning_a_no_match = 0  # Flag 2: B_to_A inconsistent
    
    detailed_results = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
                
            try:
                data = json.loads(line.strip())
                total_pairs += 1
                
                # Get both cross consistency checks
                checks = data.get('cross_consistency_checks', {})
                a_to_b_check = checks.get('A_to_B', {})
                b_to_a_check = checks.get('B_to_A', {})
                
                # Parse A_to_B check (Reasoning B doesn't match Input A/Output A)
                a_to_b_raw = a_to_b_check.get('raw_output', '')
                a_to_b_actual = parse_consistency_from_raw_output(a_to_b_raw)
                
                # Parse B_to_A check (Reasoning A doesn't match Input B/Output B)
                b_to_a_raw = b_to_a_check.get('raw_output', '')
                b_to_a_actual = parse_consistency_from_raw_output(b_to_a_raw)
                
                # Count "no" responses (inconsistent)
                if a_to_b_actual == 'no':
                    reasoning_b_no_match += 1
                
                if b_to_a_actual == 'no':
                    reasoning_a_no_match += 1
                
                detailed_results.append({
                    'pair_index': data.get('data', {}).get('pair_index', 'N/A'),
                    'a_to_b_actual': a_to_b_actual,
                    'b_to_a_actual': b_to_a_actual,
                    'a_to_b_raw_preview': a_to_b_raw[:100] if a_to_b_raw else '',
                    'b_to_a_raw_preview': b_to_a_raw[:100] if b_to_a_raw else ''
                })
                
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                continue
    
    return {
        'total_pairs': total_pairs,
        'reasoning_b_no_match': reasoning_b_no_match,
        'reasoning_a_no_match': reasoning_a_no_match,
        'detailed_results': detailed_results
    }

def print_results_in_requested_format(results, filename):
    """
    Print results in the specific format requested.
    """
    total = results['total_pairs']
    b_no_match = results['reasoning_b_no_match']
    a_no_match = results['reasoning_a_no_match']
    
    if total > 0:
        b_percentage = (b_no_match / total) * 100
        a_percentage = (a_no_match / total) * 100
    else:
        b_percentage = 0
        a_percentage = 0
    
    print("\n" + "="*60)
    print(f"ANALYSIS RESULTS: {filename}")
    print("="*60)
    print("\nCheck Type                           Count    Percentage")
    print("-" * 60)
    print(f"Reasoning B doesn't match Input A/Output A\t{b_no_match}\t{b_percentage:.1f}%")
    print(f"Reasoning A doesn't match Input B/Output B\t{a_no_match}\t{a_percentage:.1f}%")
    print("-" * 60)
    print(f"Total pairs analyzed: {total}")
    
    # Also show yes counts for completeness
    if total > 0:
        b_yes_count = total - b_no_match
        a_yes_count = total - a_no_match
        print(f"\nConsistency counts:")
        print(f"A→B consistent (Reasoning B matches Input A/Output A): {b_yes_count} ({(b_yes_count/total)*100:.1f}%)")
        print(f"B→A consistent (Reasoning A matches Input B/Output B): {a_yes_count} ({(a_yes_count/total)*100:.1f}%)")

def save_detailed_results(results, output_file):
    """
    Save detailed results to a JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: {output_file}")

def main():
    """
    Main function to analyze JSONL files.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze cross-consistency check results in JSONL files')
    parser.add_argument('--input', '-i', type=str, required=True,
                       help='Input JSONL file or directory containing JSONL files')
    parser.add_argument('--output', '-o', type=str, default='consistency_analysis.json',
                       help='Output file for detailed results (default: consistency_analysis.json)')
    parser.add_argument('--summary-only', '-s', action='store_true',
                       help='Show only summary without detailed results')
    
    args = parser.parse_args()
    
    # Find JSONL files
    input_path = Path(args.input)
    jsonl_files = []
    
    if input_path.is_file() and input_path.suffix == '.jsonl':
        jsonl_files = [input_path]
    elif input_path.is_dir():
        jsonl_files = list(input_path.glob('*.jsonl'))
    else:
        print(f"Error: {args.input} is not a valid JSONL file or directory")
        return
    
    if not jsonl_files:
        print(f"No JSONL files found in {args.input}")
        return
    
    print(f"Found {len(jsonl_files)} JSONL file(s)")
    
    all_results = []
    file_results = []
    
    for jsonl_file in jsonl_files:
        print(f"\nAnalyzing: {jsonl_file}")
        
        results = analyze_jsonl_file(jsonl_file)
        filename = jsonl_file.name
        
        # Print results in requested format
        print_results_in_requested_format(results, filename)
        
        # Store results for overall summary
        file_results.append({
            'filename': str(jsonl_file),
            'results': results
        })
        
        # Add to all detailed results
        for detail in results['detailed_results']:
            detail['source_file'] = filename
            all_results.append(detail)
    
    # Generate overall summary if multiple files
    if len(jsonl_files) > 1:
        total_pairs = sum(r['results']['total_pairs'] for r in file_results)
        total_b_no_match = sum(r['results']['reasoning_b_no_match'] for r in file_results)
        total_a_no_match = sum(r['results']['reasoning_a_no_match'] for r in file_results)
        
        if total_pairs > 0:
            total_b_percentage = (total_b_no_match / total_pairs) * 100
            total_a_percentage = (total_a_no_match / total_pairs) * 100
        else:
            total_b_percentage = 0
            total_a_percentage = 0
        
        print("\n" + "="*60)
        print("OVERALL SUMMARY (All Files)")
        print("="*60)
        print("\nCheck Type                           Count    Percentage")
        print("-" * 60)
        print(f"Reasoning B doesn't match Input A/Output A\t{total_b_no_match}\t{total_b_percentage:.1f}%")
        print(f"Reasoning A doesn't match Input B/Output B\t{total_a_no_match}\t{total_a_percentage:.1f}%")
        print("-" * 60)
        print(f"Total pairs analyzed: {total_pairs}")
        print(f"Number of files: {len(jsonl_files)}")
    
    # Save detailed results
    if not args.summary_only:
        output_data = {
            'file_results': file_results,
            'all_detailed_results': all_results
        }
        save_detailed_results(output_data, args.output)

if __name__ == "__main__":
    main()