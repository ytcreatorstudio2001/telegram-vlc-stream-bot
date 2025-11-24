import re
import sys

def find_errors(log_file="bot.log"):
    """
    Scans the log file for ERROR and WARNING levels and prints them.
    """
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Log file '{log_file}' not found. Run the bot first!")
        return

    error_pattern = re.compile(r"ERROR|WARNING|CRITICAL|Traceback")
    
    print(f"--- Scanning {log_file} for errors ---\n")
    
    found_issues = False
    for i, line in enumerate(lines):
        if error_pattern.search(line):
            found_issues = True
            print(f"Line {i+1}: {line.strip()}")
            # Print a few following lines if it's a traceback
            if "Traceback" in line:
                for j in range(1, 15): # Print next 15 lines of traceback
                    if i + j < len(lines):
                        print(f"    {lines[i+j].strip()}")
                    else:
                        break
    
    if not found_issues:
        print("✅ No errors or warnings found in the logs!")
    else:
        print("\n--- End of Report ---")

if __name__ == "__main__":
    find_errors()
