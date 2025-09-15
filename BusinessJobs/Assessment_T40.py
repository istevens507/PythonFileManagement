#######################################################################################
### Assessment_T40.py
#######################################################################################
### Purpose:
###
### Description:
###
### Example: python Assessment_T40.py -fileName 'filename.txt'

import sys
import os
import argparse
import concurrent.futures
import time
import logging
from datetime import datetime
from pathlib import Path

#special built-in variable that holds the pathname of the file from which the module was loaded. 
mainDirectory = Path(__file__).resolve().parent.parent

# set system path to where helpers directory 
sys.path.insert(0, f'{mainDirectory}\\Helpers')

import file as fileManagement
import dataManagement
import configuration

# Clearing the Screen
os.system("cls || clear")

# region Initialize

jobs = configuration.MainFrameJobs

documentStatements: list[dataManagement.Document] = [
    dataManagement.Document(
        JobName= jobs["T40"]["JobName"],
        Name= jobs["T40"]["FileName"],
        Description="MEDICAL SERVICES PLAN OF B. COLUMBIA",
        Indexes={"Header": ["CLAIMT40J003", "MEDICAL SERVICES PLAN"]},
    ),
]

ap = argparse.ArgumentParser()
ap.add_argument("-fileName", "--foperand", required=True, help="first operand")
args = vars(ap.parse_args())
jobFileName = (args["foperand"]).replace("'", "")
jobFileName = None if jobFileName == "" else jobFileName
# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s : %(levelname)s - %(message)s")
scriptsLogDirectoryPath = Path(configuration.CONST_SCRIPT_LOG_FOLDER)
# Create the ScriptsLog directory if it does not exist
if not os.path.exists(scriptsLogDirectoryPath):
    os.makedirs(scriptsLogDirectoryPath, exist_ok=True)
file_hander = logging.FileHandler(
    f"{configuration.CONST_SCRIPT_LOG_FOLDER}/T40_{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)
file_hander.setFormatter(formatter)
logger.addHandler(file_hander)
# endregion

# region Classes
class MedicalCareStatement:
    def __init__(
        self,
        ProvinceName: str,
        BeginIndex: int,
        EndIndex: int = -1,
    ):
        self.ProvinceName = ProvinceName
        self.BeginIndex = BeginIndex
        self.EndIndex = EndIndex
    def __repr__(self):
        """Helps with printing the MedicalCareStatement instance and see all populated attributes"""
        return (
            "MedicalCareStatement: { ProvinceName:%s, BeginIndex:%s, EndIndex:%s }"
            % (self.ProvinceName, self.BeginIndex, self.EndIndex)
        )
# endregion

# region Methods
def GetMedicalCareLines(beginIndex: int, endIndex: int, mainSourceReadLines: list[str]):
    readLinesText = mainSourceReadLines[beginIndex:endIndex + 1] # add + 1 Extract characters end begining to end
    return readLinesText
def GetMedicalCareReceivedTapes(
    filePath: str, document: dataManagement.Document
) -> None:
    try:
        medicalCareStatements: list[MedicalCareStatement] = []
        logger.info("Attempting to open/read file")

        with open(filePath, "r", encoding="utf-8", errors="ignore") as f:
            readLines = f.readlines()
            f.close()
            numberOfLines = len(readLines)
            logger.info(f"Processing file with {numberOfLines} line(s) ...")
            mainDirectory = configuration.CONST_DESTINATION_FOLDER
            processedClaimJobNameDirectory = f"{mainDirectory}\\{document.JobName}"
            # Create main folder
            fileManagement.CreateDirectory(
                folderPath=processedClaimJobNameDirectory, logger=logger
            )
                   
            currentProvinceName: str = None
            for rangeIndex in range(numberOfLines):
                readLine = readLines[rangeIndex]
                if document.IsRemittanceHeader(readLine):
                    _residentByIndex = (
                        readLines[rangeIndex + 2].lower().find("residents by")
                    )
                    _provinceName = readLines[rangeIndex + 2][
                        _residentByIndex + 13 : _residentByIndex + 50
                    ]
                    _provinceName = _provinceName.strip()
                    if _provinceName in [
                        "ALBERTA",
                        "MANITOBA",
                        "NEWFOUNDLAND",
                        "ONTARIO",
                        "SASKATCHEWAN",
                        "NEW BRUNSWICK",
                        "NOVA SCOTIA",
                    ]:
                        if currentProvinceName != _provinceName:
                                                 
                            provinceIsExists = any(item.ProvinceName == currentProvinceName for item in medicalCareStatements)
                            if (provinceIsExists):
                                name = currentProvinceName if currentProvinceName is not None else _provinceName
                                index = next((i for i, item in enumerate(medicalCareStatements) if item.ProvinceName == name), -1)
                                # Update "EndIndex" attribute for previous item on the collection
                                medicalCareStatements[index].EndIndex = rangeIndex - 1
                              
                                #Province doesn't exist yet, so we a record needs to be added
                                # add new item to the collection
                                medicalCareStatements.append(
                                    MedicalCareStatement(
                                        ProvinceName=_provinceName, BeginIndex=rangeIndex
                                    )
                                )
                              
                            else:
                                #province doesn't exist yet, so we a record needs to be added
                                # add new item to the collection
                                medicalCareStatements.append(
                                    MedicalCareStatement(
                                        ProvinceName=_provinceName, BeginIndex=rangeIndex
                                    )
                                )
                                
                        currentProvinceName = _provinceName
                else:
                    if rangeIndex == numberOfLines - 1:
                       index = next((i for i, item in enumerate(medicalCareStatements) if item.ProvinceName == currentProvinceName), -1)
                       medicalCareStatements[index].EndIndex = rangeIndex                       
            return medicalCareStatements, readLines 
    except Exception as e:
        logger.exception(f"Error Type: {type (e)} - {e}")
        os.system("cls || clear")
        print(
            f"An error occurred while processing the file: {filePath} - for more details see log file '{file_hander.baseFilename}'"
        )
        sys.exit(1)
# -----------
def MedicalCareStatementFileManagement(
    statementJobPath: str,
    medicalCareItem: MedicalCareStatement,
    mainSourceReadLines: list[str],
):
    """
    Manages the file creation for Medical Care Statement for Tapes Received.
    """
    readLines = GetMedicalCareLines(
        medicalCareItem.BeginIndex, medicalCareItem.EndIndex, mainSourceReadLines
    )
    fileName = f"{medicalCareItem.ProvinceName}_{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}"
    fileObj = fileManagement.File(Path=statementJobPath, Name=fileName, Data=readLines)
    disableReportTextFile: bool = configuration.CONST_DISABLE_REPORT_TEXT_FILE
    if not disableReportTextFile:
        fileObj.CreateTextFile(logger=logger)
    fileObj.CreatePDF(
        indexes=document.Indexes["Header"],
        readLines=readLines,
        logger=logger
    )
def ProcessFile(filePath: str, document: dataManagement.Document):
    if document is not None:
        filenameToRemove = filePath
        currenDate = datetime.now()
        medicalCareStatements, readLines = GetMedicalCareReceivedTapes(
            f"{configuration.CONST_SOURCE_FOLDER}\\{filePath}",
            document,
        )
        SourceFolder = document.JobName
        statementJobPath = (
            f"{configuration.CONST_DESTINATION_FOLDER}\\{SourceFolder}"
        )
        # Create the job folder if it does not exist
        fileManagement.CreateDirectory(
            folderPath=statementJobPath,
            logger=logger,
        )
        # Year
        currenYear = currenDate.year
        fileManagement.CreateDirectory(
            folderPath=statementJobPath,
            directoryName=currenYear,
            isSubFolder=True,
            logger=logger,
        )
        # Month
        statementJobPath = f"{statementJobPath}//{currenYear}"
        currenMonthName = currenDate.strftime("%B")
        fileManagement.CreateDirectory(
            folderPath=statementJobPath,
            directoryName=currenMonthName,
            isSubFolder=True,
            logger=logger,
        )
        statementJobPath = f"{statementJobPath}//{currenMonthName}"
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            results = [
                executor.submit(
                    MedicalCareStatementFileManagement,
                    statementJobPath,
                    medicalCareStatement,
                    readLines,
                )
                for medicalCareStatement in medicalCareStatements
            ]
            for f in concurrent.futures.as_completed(results):
                if f is not None:
                    result = f.result()
                    if result is not None:
                        print(f.result())
        # Remove file
        fileManagement.Remove(filenameToRemove)
        logger.info(f"File to Remove: {filenameToRemove}")
        os.system("cls || clear")
        print(
            f"=== DONE === For more details see log file '{file_hander.baseFilename}'"
        )
def GetStatements(directory):
    try:
        performance = configuration.Performance()
        files = os.listdir(directory)
        for file in files:
            filename, extension = os.path.splitext(file)
            if extension.lower() == ".txt":
                document = next(
                    (x for x in documentStatements if x.Name in filename), None
                )
                ProcessFile(file, document)
        performance.EndTime()
    except Exception as e:
        logger.exception(f"Error Type: {type (e)} - {e}")
        os.system("cls || clear")
        print(
            f"An error occurred while processing the file: {file} - for more details see log file '{file_hander.baseFilename}'"
        )
        sys.exit(1)
# endregion
# region - Script Execution
directory_path = f"{configuration.CONST_SOURCE_FOLDER}"
start = time.perf_counter()
if jobFileName is None:
    GetStatements(directory_path)
else:
    document = next((x for x in documentStatements if x.Name in jobFileName), None)
    ProcessFile(jobFileName, document)
finish = time.perf_counter()
logger.info(configuration.ElapseTime.GetElapseTime(finish - start))
# endregion
