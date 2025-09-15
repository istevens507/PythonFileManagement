#######################################################################################
### dataManagement.py
#######################################################################################
### Purpose: This file contains a class Document which 2 defined function.
###         - IsRemittanceHeader: Checks if read line text contains all header items, returns a bool response.
###         - ReturnMainHeaderLines: Return 4 rows down, "will be assume is the main
###           header of the document", returns a list on strings .
### Usage: import dataManagement

class Document:
    """
    Document Statement Class, holds all Jobs, Files names and Header indexes
    """

    def __init__(
        self, JobName: str, Name: str, Description: str, Indexes: dict[str, list[str]]
    ):
        self.Name = Name
        self.JobName = JobName
        self.Description = Description
        self.Indexes = Indexes

    def IsRemittanceHeader(self, readLine: str, indexName: str = "Header"):
        """
        Checks if read line text contains all header items.
        """
        if not any(x == indexName for x in self.Indexes):
            return False

        for item in self.Indexes[indexName]:
            if not (item.lower() in readLine.lower()):
                return False

        return True

    def ReturnMainHeaderLines(self, readLines: list[str], indexName: str, rangeIndex: int = 0) :
        """
        Return 4 rows down, "will be assume is the main
        header of the document".
        """
        counter = rangeIndex
        headerReadlines: list[str] = []

        for itemReadLine in readLines:
            isRemittanceHeader = self.IsRemittanceHeader(
                readLine=itemReadLine, indexName=indexName
            )

            if isRemittanceHeader:
                headerReadlines.append(readLines[counter])
                headerReadlines.append(readLines[counter + 1])
                headerReadlines.append(readLines[counter + 2])
                headerReadlines.append(readLines[counter + 3])
                headerReadlines.append("")

                break

            counter += 1

        return headerReadlines
