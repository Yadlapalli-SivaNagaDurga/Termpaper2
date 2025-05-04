import json
import os

def extract_high_severity_ids(report_path):
    """
    Extracts high-severity vulnerability IDs from the given report file (JSON).
    Assumes that vulnerabilities are classified as 'high' based on CVSSv3 score.
    """
    ids = set()
    try:
        # Check if the file is empty before attempting to read
        if os.path.getsize(report_path) > 0:
            with open(report_path, 'r') as f:
                data = json.load(f)

            if isinstance(data, list):  # Docker report
                for item in data:
                    for vuln in item.get("vulnerabilities", []):
                        cvss_score = vuln.get("CVSSv3", "")
                        if "H" in cvss_score:  # Check if 'H' (high) is in the CVSS score
                            ids.add(vuln.get("id"))
            else:  # Code report
                for vuln in data.get("vulnerabilities", []):
                    cvss_score = vuln.get("CVSSv3", "")
                    if "H" in cvss_score:  # Check if 'H' (high) is in the CVSS score
                        ids.add(vuln.get("id"))
    except Exception as e:
        # Skipping errors silently without printing
        pass
    return ids

def write_snyk_template(ids, filename=".snyk"):
    """
    Writes the high-severity vulnerability IDs to the .snyk file.
    If no IDs exist, it informs the user.
    """
    if not ids:
        return  # Do nothing if no high-severity vulnerabilities are found.

    # Open the file in write mode, creating it if it doesn't exist.
    with open(filename, 'w') as f:
        for vid in sorted(ids):
            f.write(f"{vid}:\n")

def load_ignored_ids(filename=".snyk"):
    """
    Loads the ignored vulnerability IDs from the .snyk file.
    """
    ignored = set()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    ignored.add(line.split(':')[0].strip())
    return ignored

def evaluate_and_decide(code_ids, docker_ids, ignored_ids):
    """
    Evaluates the high-severity vulnerabilities and makes a decision to either block or allow deployment.
    """
    total_ids = code_ids.union(docker_ids)
    unignored_ids = total_ids - ignored_ids

    # If there are unignored high-severity vulnerabilities
    if unignored_ids:
        print("\n❌ Unignored High-Severity Vulnerabilities Found:")
        for vid in sorted(unignored_ids):
            print(f" - {vid}")
        print("\n🚦 Final Decision: ❌ BLOCK DEPLOYMENT - Unignored high-severity vulnerabilities found!")
    else:
        print("\n✅ No unignored high-severity vulnerabilities found.")
        print("🚦 Final Decision: ✅ DEPLOY - No critical issues to block the deployment.")

def main():
    """
    Main function to process the Snyk reports, generate the .snyk file, and make a deployment decision.
    """
    print("🔍 Starting Snyk report scan...\n")

    # Extract high-severity vulnerability IDs from the reports
    code_ids = extract_high_severity_ids("snyk_report.json")
    docker_ids = extract_high_severity_ids("snyk_docker_report.json")

    # Combine all vulnerability IDs
    all_ids = code_ids.union(docker_ids)

    # Write the high-severity vulnerability IDs to the .snyk file
    write_snyk_template(all_ids)

    # Load ignored vulnerability IDs from the .snyk file
    ignored_ids = load_ignored_ids()

    # Evaluate the findings and decide whether to deploy or block deployment
    evaluate_and_decide(code_ids, docker_ids, ignored_ids)

if __name__ == "__main__":
    main()
