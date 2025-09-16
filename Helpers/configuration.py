#######################################################################################
### configuration.py
#######################################################################################
### Purpose: This file contains the configuration for the Remittance files,
###          and gets used by importing it into the files that wants to consume it.
### Usage: import Configuration
import json

import os
import time
import math
from datetime import timedelta
from pathlib import Path

# The following refers
# temp --> this folder is refers as to where the source files are going to be dropped
# data --> this folder is where the processed files are going to be stored

#__file__ is a special built-in variable that holds the pathname of the file from which the module was loaded. 
# Get the directory containing the current script
CONST_DIRECTORY_LOCATION = os.path.dirname(os.path.abspath(__file__))
CONST_PROJECT_DIRECTORY_LOCATION = str(Path(CONST_DIRECTORY_LOCATION).parent)

CONST_CONFIG_FILENAME = f"{CONST_DIRECTORY_LOCATION}\\config.json"

# The following refers to the jobs that are going to be processed
# The jobName is the name of the file that is going to be processed
# The FileName represents what will use to search for in file

MainFrameJobs = {
    "T40": {"JobName": "Assessment_T40", "FileName": "T40J003"},
}

# class EmailConfiguration:
#     """Email Configuration schema"""

#     def __init__(self, SMTPHost, SMTPPort):
#         self.SMTPHost = SMTPHost
#         self.SMTPPort = SMTPPort


# class EmailNotification:
#     """Email Notification schema"""

#     def __init__(
#         self,
#         IsEnabled: bool,
#         Sender: str,
#         Recipient: str,
#         Subject: str,
#         Configuration: EmailConfiguration,
#     ):
#         self.IsEnabled = IsEnabled
#         self.Sender = Sender
#         self.Recipient = Recipient
#         self.Subject = Subject
#         self.Configuration = Configuration


class MainConfiguration:
    """Main Configuration schema"""

    def __init__(
        self,
        ScriptLog: str,
        Source: str,
        Destination: str,
        DisableReportTextFile: bool,
       # EmailNotification: EmailNotification,
    ):
        
        self.ScriptLog = ScriptLog
        self.Source = Source
        self.Destination = Destination
        self.DisableReportTextFile = DisableReportTextFile
        #self.EmailNotification = EmailNotification


class Setting:
    """Setting class to handle configuration data"""

    def __init__(self):
        self.CONST_CONFIG_FILENAME = CONST_CONFIG_FILENAME
        self.CONST_CONFIG_DATA = setConfiguration()

    def getConfiguration(self) -> MainConfiguration:
        """Get the configuration data"""

        self.ScriptLog = CONST_PROJECT_DIRECTORY_LOCATION + self.CONST_CONFIG_DATA["ScriptLog"]  
        self.Source = CONST_PROJECT_DIRECTORY_LOCATION + self.CONST_CONFIG_DATA["Source"]
        self.Destination = CONST_PROJECT_DIRECTORY_LOCATION + self.CONST_CONFIG_DATA["Destination"]
        self.DisableReportTextFile = (
            True if self.CONST_CONFIG_DATA["DisableReportTextFile"] == "true" else False
        )

        #self.EmailNotification = EmailNotification(
        #    IsEnabled=(
        #        True
        #        if self.CONST_CONFIG_DATA["EmailNotification"]["IsEnabled"] == "true"
        #        else False
        #    ),
        #    Sender=self.CONST_CONFIG_DATA["EmailNotification"]["Sender"],
        #    Recipient=self.CONST_CONFIG_DATA["EmailNotification"]["Recipient"],
        #    Subject=self.CONST_CONFIG_DATA["EmailNotification"]["Subject"],
        #    Configuration=EmailConfiguration(
        #        SMTPHost=self.CONST_CONFIG_DATA["EmailNotification"]["configuration"][
        #            "SMTPHost"
        #        ],
        #        SMTPPort=self.CONST_CONFIG_DATA["EmailNotification"]["configuration"][
        #            "SMTPPort"
        #        ],
        #    ),
        #)

        # Return the configuration data
        return MainConfiguration(
            ScriptLog=self.ScriptLog,
            Source=self.Source,
            Destination=self.Destination,
            DisableReportTextFile=self.DisableReportTextFile,
            #EmailNotification=self.EmailNotification,
        )


class ElapseTime:

    def seconds_to_minutes(seconds) -> tuple[int, int]:
        """
        Converts seconds to minutes and remaining seconds."""
        td = timedelta(seconds=seconds)
        minutes = td.seconds // 60
        remaining_seconds = td.seconds % 60
        return minutes, remaining_seconds

    def GetElapseTime(timeSubtraction: float) -> str:
        """
        Returns the elapse time message taken to process the file
        """

        seconds = round(timeSubtraction, 2)

        if seconds > 1:
            minutes, remaining_seconds = ElapseTime.seconds_to_minutes(seconds)
            return (
                f"File was processed in {minutes} min(s) and {remaining_seconds} sec(s)."
                if minutes > 0
                else f"File was processed in {remaining_seconds} sec(s)."
            )
        else:
            return f"File was processed in: {math.floor((timeSubtraction) * 1000)} ms."


class Performance:
    def __init__(self):
        self.StartTime = time.time()

    def EndTime(self) -> None:
        t_sec = round(time.time() - self.StartTime)
        (t_min, t_sec) = divmod(t_sec, 60)
        (t_hour, t_min) = divmod(t_min, 60)
        # (t_sec, t_msecs) = divmod(t_sec, 1000) # Number of milliseconds in a second
        print(
            " \n\r |||| Time passed: {} hour(s):{} min(s):{} sec(s) |||".format(
                t_hour, t_min, t_sec
            )
        )


def setConfiguration():
    """Set the configuration data from the configuration file"""

    # Check if the configuration file exists
    try:
        with open(CONST_CONFIG_FILENAME, "r") as configFile:
            data = json.load(configFile)
            configFile.close()
            return data
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file '{CONST_CONFIG_FILENAME}' not found."
        )

    # Check if the configuration file is empty
    if not CONST_CONFIG_FILENAME:
        raise ValueError(f"Configuration file '{CONST_CONFIG_FILENAME}' is empty.")


# Get the configuration data
def returnConfiguration() -> MainConfiguration:
    """Returns the configuration file data"""
    configSetting = Setting()
    return configSetting.getConfiguration()


# Get the configuration data
CONST_CONFIG_DATA = returnConfiguration()

CONST_SCRIPT_LOG_FOLDER: str = CONST_CONFIG_DATA.ScriptLog
CONST_SOURCE_FOLDER: str = CONST_CONFIG_DATA.Source
CONST_DESTINATION_FOLDER: str = CONST_CONFIG_DATA.Destination
CONST_DISABLE_REPORT_TEXT_FILE: bool = CONST_CONFIG_DATA.DisableReportTextFile
#CONST_EMAIL_NOTIFICATION: EmailConfiguration = CONST_CONFIG_DATA.EmailNotification


