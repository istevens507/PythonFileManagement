#######################################################################################
### scriptStartup.py
#######################################################################################
### Purpose: This script in charge of execute all the scripts that are required to process the remittance files.
###
### Usage: python ScriptStartup.py -scriptPath '<directory of where python scripts are located>'
###

import os
import subprocess
import configuration
from io import StringIO
import datetime
import argparse
import asyncio
import json

# Pretty-print tabular data
from tabulate import tabulate

# Clearing the Screen
os.system("cls || clear")

ap = argparse.ArgumentParser()

ap.add_argument("-scriptPath", "--foperand", required=False, help="first operand")

args = vars(ap.parse_args())

scriptPath = (
    (args["foperand"]).replace("'", "") if args["foperand"] is not None else None
)

jobSummaries = []
jobSummariesCompleted = []

CONST_JOBS = [
    {"jobName": "T40J003", "scriptName": "Assessment_T40"},
]


def getDateFormat() -> str:
    x = datetime.datetime.now()
    return f'{x.strftime("%Y-%m-%d")} {x.strftime("%X")}'


class StringBuilder:
    string = None

    def __init__(self):
        self.string = StringIO()

    def Add(self, str):
        self.string.write(f"\n{str}")

    def __str__(self):
        return self.string.getvalue()


async def main():
    directory_path = f"{configuration.CONST_SOURCE_FOLDER}"
    files = os.listdir(directory_path)

    numberFilesFound = len(files)
    string_builder = StringBuilder()

    string_builder.Add(f"--> === SUMMARY ===")
    string_builder.Add(
        f"--> ({numberFilesFound}) file(s) found in - '{directory_path}'"
    )

    if numberFilesFound > 0:

        for jobObject in CONST_JOBS:

            jobFiles = list(filter(lambda x: (jobObject["jobName"] in x), files))

            if jobFiles is not None:
                numberOfJobFiles = len(jobFiles)
                if numberOfJobFiles > 0:

                    jobSummaries.append(
                        [
                            jobObject["jobName"],
                            numberOfJobFiles,
                        ]
                    )

                for jobFile in jobFiles:

                    scriptCall = (
                        f"{scriptPath}\\{jobObject['scriptName']}.py"
                        if scriptPath is not None
                        else f"{jobObject['scriptName']}.py"
                    )

                    # Get the date modified of the file
                    dateModified = datetime.datetime.fromtimestamp(
                        os.path.getmtime(f"{directory_path}\\{jobFile}")
                    )
                    
                    await CallProcess(
                        scriptCall=scriptCall,
                        scriptName=jobObject["scriptName"],
                        jobFile=jobFile,
                        dateModified=f'{dateModified.strftime("%Y-%m-%d")} {dateModified.strftime("%X")}',
                    )
    print(string_builder)

    if len(jobSummaries) > 0:
        # Generate table
        jobSummaryHeaders = ["Job Name", "Number of Files"]
        print(
            tabulate(
                jobSummaries,
                headers=jobSummaryHeaders,
                tablefmt="grid",
                numalign="center",
                stralign="center",
            )
        )

    if len(jobSummariesCompleted) > 0:
        print(f"\n--> === PROCCESSED JOBS SUMMARY ===")
        # Generate table
        jobSummaryCompletedHeaders = [
            "Script Name",
            "Filename",
            "Completed",
            "Date Modified",
        ]
        print(
            tabulate(
                tabular_data=jobSummariesCompleted,
                headers=jobSummaryCompletedHeaders,
                tablefmt="grid",
                numalign="center",
                stralign="center",
            )
        )

        # Send email notification if enabled
        #if RemittanceConfiguration.CONST_EMAIL_NOTIFICATION.IsEnabled:
        #    notificationScriptPath = "notifications/notification.py"
        #    scriptCall = (
        #        f"{scriptPath}/{notificationScriptPath}"
        #        if scriptPath is not None
        #        else notificationScriptPath
        #    )

        #    print(f"\n==> Sending email notification...")

        #    json_string = json.dumps(jobSummariesCompleted)

        #    process = subprocess.run(
        #        ["python", scriptCall, "-list", json_string],
        #        capture_output=True,
        #        text=True,
        #    )

        #    if process.returncode == 0:  # Process completed successfully
        #        print(f"==> stdout: {process.stdout}")
        #    else:
        #        if process.stderr:
        #            print(f"==> stderr: {process.stderr}")


async def CallProcess(
    scriptCall: str, scriptName: str, jobFile: str, dateModified: str
):
    strBuilder = StringBuilder()

    strBuilder.Add(f"==> Script '{scriptName}.py' details:")
    strBuilder.Add(f"==> {scriptCall} -fileName '{jobFile}'")
    startTime = getDateFormat()

    process = subprocess.run(
        ["python", scriptCall, "-fileName", jobFile], capture_output=True, text=True
    )
    finishTime = getDateFormat()

    strBuilder.Add(f"==> Started on {startTime} | Finished on {finishTime}")
    if process.returncode == 0:  # Process completed successfully
        strBuilder.Add(f"==> stdout: {process.stdout}")
    else:
        strBuilder.Add(
            f"==> { 'stderr: ' + process.stderr if process.stderr else 'stdout: ' + process.stdout}"
        )

    jobSummariesCompleted.append(
        [
            scriptName,
            jobFile,
            (True if process.returncode == 0 else False),
            dateModified,
        ]
    )

    print(strBuilder)


# Call the async function without await
main_coroutine = main()

# Run the coroutine in an event loop
# The event loop is the core of the asynchronous system in Python. It runs coroutines,
# handles I/O operations, and manages the execution of tasks. You can start the event loop using
asyncio.run(main_coroutine)

