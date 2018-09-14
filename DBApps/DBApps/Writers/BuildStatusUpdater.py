"""
DBApp class to update Build Status

"""
import sys

from DBApps.DBApp import DBApp
from DBApps.DBAppArgs import DBAppArgs, DbArgNamespace, writableExpandoFile


class updateBuildStatusParser(DBAppArgs):
    """
    Specifies arguments for get ready works
    """

    def __init__(self, description: str, usage: str):
        super().__init__(description, usage)
        self._parser.add_argument('-n', '--numWorks',
                                  help='how many works to fetch',
                                  default=10, type=int)
        self._parser.add_argument('resultsPath',
                                  help='Output path name. May overwrite existing contents',
                                  type=writableExpandoFile)


class GetReadyWorks(DBApp):
    """
    Fetch all ready works
    """

    def __init__(self, options: DbArgNamespace) -> None:
        """
        :param: self
        :param: options
        :rtype: object
        """
        # drsDbConfig is required
        try:
            super().__init__(options.drsDbConfig)
        except AttributeError:
            print("argument parsing error: drsDbConfig not found in args")
            sys.exit(1)

        self._options = options
        self.ExpectedColumns = ['WorkName', 'HOLLIS', 'Volume', 'OutlineUrn', 'PrintMasterUrn']
