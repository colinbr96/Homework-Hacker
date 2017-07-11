################################################################################
# Imports

from collections import OrderedDict


################################################################################
# Classes

class DataReport:
    """ Represents a collection of data pulled from a database. DataReport is
        used to generate ascii-representations of the provided data (used to
        send formatted replies to Slack). The ascii-representation can either
        be a "report" or a table.

        The inputted data is broken into 2 parts: titles and entries. Titles
        are akin to the labels on the columns of a table, whereas entries are
        akin to the contents of the rows of that table.
    """
    def __init__(self, titles: [tuple], entries: [dict]):
        """ Args:
            titles (list of 2-tuple):
                Each 2-tuple is formatted as such: (label, key)
                The label is used to describe the data that the key accesses
                from an entry dict.

                    For example, if the entry dict is:
                        {"usr_first": "Peter", "usr_last": "Anteater"}
                    Then you could specify title as:
                        ("First Name", "usr_first")
                    And the output would be:
                        First Name: Peter

                To concatenate two or more entry fields into one title,
                separate the keys with a "|".

                    For example, if the entry dict is:
                        {"usr_first": "Peter", "usr_last": "Anteater"}
                    Then you could specify title as:
                        ("Name", "usr_first|usr_last")
                    And the output would be:
                        Name: Peter Anteater

                To pass the entry through a function for formatting purposes,
                the key will become a 3-tuple formatted as such:
                    (function_name, entry_params, static_params)
                - The function_name points to a function where the entry_params
                  and static_params are passed.
                - entry_params is a dict where the keys are the parameter names
                  passed to function_name and values are keys to the entry dict
                  provided in "entries".
                - static_params is a dict where the keys are the parameter names
                  passed to function_name and the values are static variables
                  (passed as is).

                    For example, if the entry dict is:
                        {"usr_first": "Peter", "usr_last": "Anteater"}
                    And a function specified above is:
                        def indent(s:str, size:int) -> str:
                    Then you could specify title as:
                        ("Name", (indent, {"s": "usr_first|usr_last"}, {"size": 4}))
                    And the output would be:
                        ....Name: Peter Anteater

            entries (list of dict):
                A list of JSON dicts returned by the database call where each
                entry in the list has the same keys.

                    For example, entries can be:
                    [
                        {
                            "usr_id" : "00001",
                            "first_name" : "Peter",
                            "last_name" : "Anteater"
                        },
                        {
                            "usr_id" : "00002",
                            "first_name" : "Mike",
                            "last_name" : "Caban"
                        }
                    ]
        """
        self.__titles = OrderedDict(titles)
        self.__entries = entries

    #-------------------------------------------------------------------------
    #
    # Private Helpers

    def _get_entry_str(self, entry_key, entry: dict):
        """ Returns the resulting entry string. This takes into account if the
            entry_key is a tuple with a function in it. It also uses '|' to
            concatenate two or more fields
        """
        if isinstance(entry_key, tuple) and callable(entry_key[0]):
            combined_dict = self._get_combined_dict_with_values(
                entry_key, entry)
            entry_str = entry_key[0](**combined_dict)

        else:
            if "|" in entry_key:
                entry_str = " ".join(entry[e] for e in entry_key.split('|'))

            elif "." in entry_key:
                temp_entry = entry
                for entry_key_part in entry_key.split("."):
                    temp_entry = temp_entry[entry_key_part]
                entry_str = temp_entry
            else:
                entry_str = entry[entry_key]

        return str(entry_str).strip()


    def _get_combined_dict_with_values(self, entry_key, entry: dict):
        """ Combines the first and second dictionaries in a tuple ([1][2]) and
            substitutes in the values from entry dict into dict 1
        """
        combined_dict = {}

        for x, y in entry_key[1].items():
            if "|" in y:
                result_str = " ".join(entry[e] for e in y.split('|'))
                combined_dict[x] = result_str
            elif "." in y:
                temp_entry = entry
                for entry_key_part in y.split("."):
                    temp_entry = temp_entry[entry_key_part]
                combined_dict[x] = temp_entry
            else:
                combined_dict[x] = entry[y]

        combined_dict.update(entry_key[2])
        return combined_dict

    #-------------------------------------------------------------------------
    #
    # Utility

    def ascii_table(self, monospaced: bool=True, indent_len: int=0) -> str:
        """ Returns the str representation of self's titles and entries as a table
            The table is ascii formatted and ready to post to Slack

            Example output:

            UCInetID | MAC Address  | Blocked | Registered On       | Comments
            ---------+--------------+---------+---------------------+---------------------
            colin    | 97285b1182c2 | False   | 2016-05-20 12:22:40 | MacBook Pro Ethernet
            colin    | 0fa2d35e4d0d | False   | 2016-08-02 12:22:35 | HTC 10
            colin    | 2b98951ac93d | False   | 2014-10-02 11:00:39 | MacBook Pro Wi-Fi
        """


        max_column_width = [len(t) for t in self.__titles]

        table = [[t for t in self.__titles]]


        for _ in range(len(self.__entries)):
            table.append([])


        # Constructing list of lists (2D array) of table contents
        for row, e in enumerate(self.__entries):
            for col, t in enumerate(self.__titles.values()):
                try:
                    s = self._get_entry_str(t, e)

                    width = len(s)
                    if s and s[0] == "<" and s[-1] == ">":
                        width = len(s.split("|")[1].strip())

                    if width > max_column_width[col]:
                        max_column_width[col] = width

                    table[row + 1].append(s)

                except KeyError:
                    table[row + 1].append("")

        # Constructing str result
        result = ""
        right_most_column = len(self.__titles) - 1

        for row in range(len(table)):
            for col, s in enumerate(table[row]):
                if col == right_most_column:
                    result += " "
                    result += s
                else:
                    if col == 0:
                        result += " " * indent_len
                    else:
                        result += " "

                    result += s

                    len_to_subtract = len(s)
                    if s and s[0] == "<" and s[-1] == ">":
                        len_to_subtract = len(s.split("|")[1].strip()) - 1

                    for _ in range(max_column_width[col] - len_to_subtract):
                        result += " "

                    result += " |"

            result += "\r\n"

            if row == 0:
                for col in range(right_most_column + 1):
                    if col == 0:
                        result += " " * indent_len
                        result += "-" * (max_column_width[col] + 1)

                    elif col == right_most_column:
                        result += "+"
                        result += "-" * (max_column_width[col] + 1)

                    else:
                        result += "+"
                        result += "-" * (max_column_width[col] + 2)

                result += "\r\n"

        return result[0: len(result) - 2]  # Removing trailing \r\n
