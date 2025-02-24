"""
Security vulnerabilities script.

Notes
-----
Script for detecting vulnerabilities on a given repo and creating
associated security vulnerability advisories.
"""

import hashlib
import json
import os
import sys
from typing import Any, Dict

import click

DRY_RUN = True if os.environ.get("DEPENDENCY_CHECK_DRY_RUN", None) else False
ERROR_IF_NEW_ADVISORY = (
    True if os.environ.get("DEPENDENCY_CHECK_ERROR_EXIT", None) else False
)


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary.

    Parameters
    ----------
    dictionary : Dict[str, Any]
        Dictionary to hash.

    Returns
    -------
    str
        MD5 hash of the dictionary.
    """
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def check_vulnerabilities():
    """Check library and third-party vulnerabilities.

    Raises
    ------
    RuntimeError
        If the required environment variables are not defined.
    """
    new_advisory_detected = False

    # Check if DRY_RUN or not
    if DRY_RUN:
        print("Dry run... not creating advisories and issues.")
        print("Information will be presented on screen.\n")

    # Load the security checks
    safety_results = {}
    with open("info_safety.json", "r") as json_file:
        safety_results = json.loads(json_file.read())

    # If the security checks have not been loaded... problem ahead!
    if not safety_results:
        raise RuntimeError(
            "Safety results have not been generated... Something went wrong during",
            "the execution of 'safety check -o bare --save-json info_safety.json'. ",
            "Verify workflow logs.",
        )

    ###############################################################################
    # THIRD PARTY SECURITY ADVISORIES
    ###############################################################################

    # Process the detected advisories by Safety
    safety_results_reported = 0
    vulnerability: dict
    for vulnerability in safety_results["vulnerabilities"]:
        # Retrieve the needed values
        v_id = vulnerability.get("vulnerability_id")
        v_package = vulnerability.get("package_name")
        if v_package != "pip":
            v_url = vulnerability.get("more_info_url")
            v_desc = vulnerability.get("advisory")

            # Advisory info
            summary = f"Safety vulnerability {v_id} for package '{v_package}'"
            desc = f"""
    {v_desc}

    #### More information

    Visit {v_url} to find out more information.
    """
            # New safety advisory detected
            safety_results_reported += 1
            new_advisory_detected = True
            print("===========================================\n")
            print(f"{summary}")
            print(f"{desc}")

    ###############################################################################
    # LIBRARY SECURITY ADVISORIES
    ###############################################################################

    # Load the bandit checks
    bandit_results = {}
    with open("info_bandit.json", "r") as json_file:
        bandit_results = json.loads(json_file.read())

    # If the bandit results have not been loaded... problem ahead!
    if not bandit_results:
        raise RuntimeError(
            "Bandit results have not been generated... Something went wrong during",
            "the execution of 'bandit -r <source-directory> -o info_bandit.json -f json'. ",
            "Verify workflow logs.",
        )

    # Process the detected advisories by Bandit
    bandit_results_reported = 0
    vulnerability: dict
    for vulnerability in bandit_results["results"]:
        # Retrieve the needed values
        v_hash = dict_hash(vulnerability)
        v_test_id = vulnerability.get("test_id")
        v_test_name = vulnerability.get("test_name")
        v_filename = vulnerability.get("filename")
        v_code = vulnerability.get("code")
        v_cwe = vulnerability.get("issue_cwe", {"id": "", "link": ""})
        v_url = vulnerability.get("more_info")
        v_desc = vulnerability.get("issue_text")

        # Advisory info
        summary = f"Bandit [{v_test_id}:{v_test_name}] on {v_filename} - Hash: {v_hash}"
        desc = f"""
{v_desc}

#### Code

On file {v_filename}:

```
{v_code}
```

#### CWE - {v_cwe['id']}

For more information see {v_cwe['link']}

#### More information

Visit {v_url} to find out more information.
"""
        # New bandit advisory detected
        bandit_results_reported += 1
        new_advisory_detected = True
        print("===========================================\n")
        print(f"{summary}")
        print(f"{desc}")

    # Print out information
    safety_entries = 0
    for vulnerability in safety_results["vulnerabilities"]:
        if (
            vulnerability.get("package_name") == "pip"
            and len(safety_results["vulnerabilities"]) == 1
        ):
            safety_entries = 0
        else:
            safety_entries = len(safety_results["vulnerabilities"])
    bandit_entries = len(bandit_results["results"])
    print("\n*******************************************")
    print(f"Total 'safety' advisories detected: {safety_entries}")
    print(f"Total 'safety' advisories reported: {safety_results_reported}")
    print(f"Total 'bandit' advisories detected: {bandit_entries}")
    print(f"Total 'bandit' advisories reported: {bandit_results_reported}")
    print("*******************************************")
    print(f"Total advisories detected: {safety_entries + bandit_entries}")
    print(
        f"Total advisories reported: {safety_results_reported + bandit_results_reported}"
    )
    print("*******************************************")

    # Return whether new advisories have been created or not
    if new_advisory_detected:
        exit(1)
    else:
        return new_advisory_detected


def generate_advisory_files():
    """
    Generate advisory files for local purposes.

    This function runs safety and bandit on the user's behalf at the current location
    and generates the necessary advisory files for local testing.

    Notes
    -----
    This function should ONLY be used for local purposes.
    """
    import bandit.cli.main as bandit
    import safety.cli as safety

    # Delete previous advisory files
    if os.path.exists("info_safety.json"):
        os.remove("info_safety.json")
    if os.path.exists("info_bandit.json"):
        os.remove("info_bandit.json")

    # Safety check
    try:
        safety.cli.main(
            ["check", "-o", "bare", "--save-json", "info_safety.json"],
            standalone_mode=False,
        )
    except:  # noqa: E722 B001
        print("Safety check performed.")
        pass

    # Bandit check
    try:
        sys.argv.pop()
        sys.argv.extend(
            [
                "-r",
                "./src",
                "-o",
                "info_bandit.json",
                "-f",
                "json",
                "-c",
                "pyproject.toml",
            ]
        )
        bandit.main()
    except:  # noqa: E722 B001
        pass
    finally:
        print("Bandit check performed.")
        sys.argv = sys.argv[: len(sys.argv) - 5]
        sys.argv.append("--run-local")

    print("Advisory files generated successfully.")


@click.command(short_help="Perform third-party and in-library vulnerability analysis.")
@click.option(
    "--run-local",
    is_flag=True,
    default=False,
    help="Simulate the behavior of the synchronization without performing it.",
)
def main(run_local: bool):
    """Main function."""
    if run_local:
        generate_advisory_files()
        global DRY_RUN
        DRY_RUN = True

    new_advisory_detected = check_vulnerabilities()

    if new_advisory_detected and ERROR_IF_NEW_ADVISORY:
        # New advisories detected - exit with error
        sys.exit(1)
    else:
        # No new advisories detected or no failure requested
        pass


if __name__ == "__main__":
    main()
