import os
import argparse
from src.agent import GADashboardAgent

def main():
    parser = argparse.ArgumentParser(description="Google Analytics Dashboard Agent")
    parser.add_argument("input_file", help="Path to the Google Analytics CSV export")
    parser.add_argument("--output-dir", default="output", help="Directory to save the dashboard (default: output)")
    parser.add_argument("--format", choices=['json', 'html', 'markdown', 'all'], default='all', help="Output format (default: all)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Initialize the agent
    agent = GADashboardAgent()
    
    try:
        # Process GA CSV export
        dashboard = agent.process(args.input_file)
        
        # Determine formats to export
        formats = ['json', 'html', 'markdown'] if args.format == 'all' else [args.format]
        
        base_filename = os.path.splitext(os.path.basename(args.input_file))[0]
        
        for fmt in formats:
            output_content = agent.export_dashboard(dashboard, format=fmt)
            output_path = os.path.join(args.output_dir, f"{base_filename}_dashboard.{'md' if fmt == 'markdown' else fmt}")
            
            with open(output_path, 'w') as f:
                f.write(output_content)
            
            print(f"Exported {fmt.upper()} dashboard to: {output_path}")
            
        print("\nAll tasks completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
