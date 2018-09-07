"""
Get Ready Related works class
"""

# sys
import pathlib
import sys
from abc import ABC
from typing import List
from argparse import ArgumentTypeError
import pymysql as mysql
# usr
from DBApps.DBAppArgs import DBAppArgs, DbArgNamespace
from DBApps.DBApp import DBApp
from DBApps.Writers import CSVWriter




class ReadyRelatedParser(DBAppArgs):
    """
    Parser for the Get Ready Related class
    Returns a structure containing fields:
    .drsDbConfig: str (from base class DBAppArgs
    .outline: bool
    .printmaster: bool
    .numResults: int
    .results: str (which will have to resolve to a pathlib.Path
    """

    def __init__(self, description: str, usage: str):
        """
        Constructor. Sets up the arguments
        """
        super().__init__(description, usage)
        group = self._parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-o', '--outline', action='store_true', help="Chooses works with outlines")
        group.add_argument('-p', '--printmaster', action='store_true', help="Chooses works with print masters")
        self._parser.add_argument('-n', '--numResults', help="maximum number to download",
                                  default=10, type=int)

        self._parser.add_argument("results",
                                  help='Output path name. May overwrite existing contents',
                                  type=DBAppArgs.writableExpandoFile)


class ReadyRelated(DBApp, ABC):
    """
    Gets related works
    """
    _options: DbArgNamespace

    @property
    def TypeString(self) -> str:
        """
        Map the option to a string. Calculated, readonly property
        Case sensitive, since this is used to build a call to a SPROC in a mySQL
        database, which has a mixed case namespace
        :return:
        """
        rs = None

        if self._options.outline:
            rs = "Outlines"
        if self._options.printmaster:
            rs = "printMasters"
        return rs

    def __init__(self, options: DbArgNamespace) -> None:
        """
        :param: self
        :param: options.
        :rtype: object
        """
        # drsDbConfig is a required
        super().__init__(options.drsDbConfig)
        self.ExpectedColumns = ['WorkName', 'HOLLIS', 'Volume']

        try:
            self.dbConfig = self._options.drsDbConfig
        except AttributeError:
            print("argument parsing error: drsDbConfig not found in args")
            sys.exit(1)

    def GetResults(self) -> list:
        """
        download the requested results
        :returns a list of dictionary items
        """
        self.start_connect(self.dbConfig)
        workCursor = self.connection.cursor(mysql.cursors.SSDictCursor)
        maxWorks = self._options.numResults

        rl: List[dict] = []

        with self.connection:
            print(f'Calling GetReadyRelated for n = {maxWorks} ')
            workCursor.callproc(f'GetReady{self.TypeString}', (maxWorks,))
            self.validateExpectedColumns(workCursor.description)

            hasNext: bool = True
            while hasNext:
                workVolumes = workCursor.fetchall_unbuffered()
                rl.extend(workVolumes)
                hasNext = workCursor.nextset()
        return rl

    def PutResults(self, fileName: str, results: list) -> None:
        """
        Public method to write results to file
        :param fileName: resulting path
        :param results: Data to output
        :param self:
        :return:
        """

        # Build the output path, resolving any ~ or .. references
        import os
        fPath = pathlib.Path(os.path.expanduser(fileName)).resolve()
        fPath.parent.mkdir(mode=0o755, parents=True, exist_ok=True)

        # and write
        CSVWriter(fileName).write_dict(results, self.ExpectedColumns)
        myCsv = CSVWriter(fileName)
        myCsv.write_dict(results, self.ExpectedColumns)




def _dumpToFile(outPath: pathlib.Path, data: list, columnNames: list) -> None:
    """
    Writes a list of dictionary to a csv.
    :param outPath: file destination for output
    :param data: list of dictionaries
    :param columnNames: list of columns to write (independent of result set)
    :return:
    """

    with outPath.open("w", newline=None) as fw:
        # Create the CSV writer. NOTE: multiple headers are written to the
        import csv
        csvwr = csv.DictWriter(fw, columnNames, lineterminator='\n')

        if len(data) > 0:
            csvwr.writeheader()
            for resultRow in data:
                down_row = {fieldName: resultRow[fieldName] for fieldName in columnNames}
                csvwr.writerow(down_row)
