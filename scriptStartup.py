#######################################################################################
### pdfCreator.py
#######################################################################################
### Purpose: Creates a pdf file
###
### Description :
###                - Page Styling
###                - Page Alignment
###                - Page separation → meaning some scripts will require that the document is
###                  created by grouping data or separate data every time there a header found on the document.
###                - Once the script finishes it prints (console) the path location of that newly created document.
###
### Usage: import pdfCreator

from logging import Logger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Clearing the Screen
os.system("cls || clear")

class HeaderLine:
    def __init__(self, HeaderKey: str, LinesPerHeader: int, Value: str):
        self.HeaderKey = HeaderKey
        self.LinesPerHeader = LinesPerHeader
        self.Value = Value

class PDF:
    def __init__(self, _LeftMargin=8):

        self._TextLineContinuationIndex = 0
        self._TextLineFont = "Courier"
        self._TextLineFontSize = 7.5
        self._TopMargin = 10
        self._LeftMargin = _LeftMargin
        self._PageOrientation = letter
        self._PageSize: tuple[float, float] = (650.0, 792.0)
        self._IsNextPage = False
        self._IsSearchNextPage = True
        self.RemittanceHeaders = list[
            HeaderLine
        ]  # provided by whoever consumes the class
        self.HeaderLines = []
        self.HeaderFoundIncrement = 0
        self.TextLineIncrement = 1
        self.AllowedLinesPerPage = 85

    def _AddTextLine(self, readLines: list[str], text: canvas.PDFTextObject):

        pageHeaders: list[HeaderLine] = []
        startRange = self._TextLineContinuationIndex
        lines = len(readLines)

        for rangeIndex in range(startRange, lines):

            self._TextLineContinuationIndex = rangeIndex

            if (
                self.IsRemittanceHeader(readLine=readLines[rangeIndex])
                and self._IsSearchNextPage
            ):

                if self.HeaderLines is not None and len(self.HeaderLines) > 0:
                    # fit at much header + content within a page

                    header = self.HeaderLines[self.HeaderFoundIncrement]

                    pageHeaders.append(header)

                    potentialContentLines = sum(
                        int(i.LinesPerHeader) for i in pageHeaders
                    )

                    self._IsSearchNextPage = True

                    if potentialContentLines < self.AllowedLinesPerPage:

                        text.textLine(readLines[rangeIndex].rstrip())
                    else:
                        pageHeaders = []
                        self._IsNextPage = True
                        self.TextLineIncrement = 0
                        break
                else:

                    if rangeIndex != 0:

                        self._IsNextPage = True
                        self._IsSearchNextPage = False
                        self.TextLineIncrement = 0
                        break
                    else:
                        text.textLine(readLines[rangeIndex].rstrip())

                self.HeaderFoundIncrement += 1
            else:
                self._IsSearchNextPage = True
                text.textLine(readLines[rangeIndex].rstrip())

            self.TextLineIncrement += 1

    def IsRemittanceHeader(self, readLine: str):

        for header in self.RemittanceHeaders:
            if not (header.lower() in readLine.lower()):
                return False

        return True

    def _AddNewPage(self, canvasObj: canvas.Canvas):
        """
        Close the current page and possibly start on a new page.
        """
        canvasObj.showPage()

    def _DrawText(self, canvasObj: canvas.Canvas, textObj: canvas.PDFTextObject):
        """
        Draw a text object
        """
        canvasObj.drawText(textObj)

    def Create(
        self,
        filePath: str,
        indexes: dict[str, list[str]],
        headerLines: list[HeaderLine] = None,
        readLines: list[str] = None,
        logger: Logger = None     
    ):
        """
        Creates a PDF file.
        """
        try:

            self.RemittanceHeaders = indexes
            self.HeaderLines = headerLines

            w, h = self._PageOrientation

            canvasFilePath = f"{filePath}"

            canvasObj = canvas.Canvas(canvasFilePath, pagesize=self._PageSize)
            readLinesLength = len(readLines)

            while self._TextLineContinuationIndex < readLinesLength - 1:
                self._IsNextPage = False
                pdfTextObject = canvasObj.beginText(
                    self._LeftMargin, h - self._TopMargin
                )
                pdfTextObject.setFont(self._TextLineFont, self._TextLineFontSize)

                self._AddTextLine(readLines, pdfTextObject)
                self._DrawText(canvasObj, pdfTextObject)

                if self._IsNextPage:
                    self._AddNewPage(canvasObj)
            canvasObj.save()  # method stores the file and closes the canvas.
            
            if logger is not None:
                logger.info(f"Created file: {canvasFilePath}")
        except Exception as e:
            print(f"Error type:  {type (e)} - {e}")
