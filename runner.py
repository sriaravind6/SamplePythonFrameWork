"""
runner.py - IntelliJ / PyCharm Test Execution Wrapper

This script allows you to easily execute and debug your Behave tests directly from
within your IDE without needing to configure complex Run Configurations or terminal commands.

HOW TO USE IN INTELLIJ / PYCHARM:
---------------------------------
1. Right-click this file (`runner.py`) in your Project explorer.
2. Select "Run 'runner'" (or "Debug 'runner'" to hit breakpoints).
3. The tests will execute and automatically generate output to the 'reports/' folder.
"""

import sys
from behave.__main__ import main as behave_main

if __name__ == "__main__":
    # Ensure Windows console handles UTF-8 characters correctly (like emojis)
    sys.stdout.reconfigure(encoding='utf-8')

    # Default arguments to run behave and format output to Allure
    args = [
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", "reports/"
    ]

    # If you want to run specific tags from IntelliJ, uncomment and modify the line below:
    # args.append("--tags=smoke")

    print(f"🚀 Starting Test Execution with args: {args}\n")
    
    # Execute Behave with the constructed arguments
    exit_code = behave_main(args)
    print(f"\n✅ Execution Finished with exit code: {exit_code}")
    sys.exit(exit_code)
