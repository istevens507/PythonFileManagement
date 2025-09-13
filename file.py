#######################################################################################
### file.py
#######################################################################################
### Purpose: This file contains a class File which is used to create directories, files (.txt, .pdf),
###          and remove the source file and/or metadata ( sub folders name and file content) .
### Usage: import file

import logging
import os
import pdfCreator
import configuration
import sys

# File / PDF Creation, deletion, single file,
class File:

    def __init__(self, Path, Name, Data: list[str], DirectoryName=None):
        self.Path = Path
        self.Name = Name
        self.Data = Data
        self.DirectoryName = DirectoryName

    def CreateTextFile(self, extension=".txt", logger: logging.Logger = None) -> None:
        """
        Creates a file with default extension as '.txt'
        or pass extension as parameter.
        """
        try:

            filePath = (
                f"{self.Path}/{self.DirectoryName}/{self.Name}{extension}"
                if self.DirectoryName is not None
                else f"{self.Path}/{self.Name}{extension}"
            )

            with open(filePath, "w") as file:
                # Perform operations on the file
                file.writelines(self.Data)
                file.close()

        except Exception as e:

            if logger is not None:
                logger.exception(f"Error type:  {type(e)} - {e}")
            else:
                print(f"Error type:  {type(e)} - {e}")

            sys.exit(
                1
            )  # Exit the program if an error occurs, using code 1 to indicate an error

    def CreatePDF(
        self,
        indexes: dict[str, list[str]],
        headerLines: list[pdfCreator.HeaderLine] = None,
        leftMargin: int = None,
        readLines: list[str] = None,
        logger: logging.Logger = None,
    ):
        """
        Creates a PDF file.
        """

        filePath = (
            f"{self.Path}/{self.Name}.pdf"
            if self.DirectoryName is None
            else f"{self.Path}/{self.DirectoryName}/{self.Name}.pdf"
        )

        pdfObj = (
            pdfCreator.PDF(_LeftMargin=leftMargin)
            if leftMargin is not None
            else pdfCreator.PDF()
        )

        pdfObj.Create(
            filePath=filePath,
            indexes=indexes,
            headerLines=headerLines,
            readLines=readLines,
            logger=logger,
        )


def CreateDirectory(
    folderPath: str,
    directoryName: str = None,
    isSubFolder: bool = False,
    logger: logging.Logger = None,
) -> None:
    """
    Create a Directory.
    """
    if isSubFolder:
        folderPath = f"{folderPath}/{directoryName}"

    if not os.path.exists(folderPath):
        os.makedirs(folderPath, exist_ok=True)

        if logger is not None:
            logger.info(f"Created directory: {folderPath}")


def Remove(
    filename: str, isMetadata: bool = False, logger: logging.Logger = None
) -> None:
    """
    Removes a file.
    """
    try:
        filePath = (
            filename
            if isMetadata
            else f"{configuration.CONST_SOURCE_FOLDER}/{filename}"
        )
        os.remove(filePath)

        if logger is not None:
            logger.info(f"File Deleted - {filePath}")
        else:
            print(f"File Deleted - {filePath}")
    except Exception as e:
        if logger is not None:
            logger.exception(f"Error type:  {type (e)} - {e}")
        else:
            print(f"Error type:  {type (e)} - {e}")
        sys.exit(
            1
        )  # Exit the program if an error occurs, using code 1 to indicate an error
