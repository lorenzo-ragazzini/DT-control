# define communicator of dvs to other machine
# define high-level actuator translating dvs into MES input
from typing import List
from DTPPC.implementation.local.dbConnect import DBConnection
import pyodbc

class Actuator(DBConnection):
    def act(self,dvs):
        pass
    def sort_table(self,table_name, index_column):
        fetch_query = (
            f"SELECT * FROM {table_name} "
        )
        self.cursor.execute(fetch_query)
        rows_to_update = self.cursor.fetchall()

        # Filter out rows where 'Start' is not empty
        non_empty_start_rows = [row for row in rows_to_update if row.Start != '']

        # Sort rows where 'Start' is empty based on the provided triplet
        sorted_empty_start_rows = sorted(
            [row for row in rows_to_update if row.Start == ''],
            key=lambda row: (row[triplet[0]], row[triplet[1]], row[triplet[2]])
        )

        # Update the positions of sorted rows where 'Start' is empty in the original table
        for idx, row in enumerate(sorted_empty_start_rows):
            update_query = (
                f"UPDATE {table_name} "
                f"SET [ONo]='{row[0]}', [OPos]='{row[1]}' "
                f"WHERE PrimaryKey='{row.PrimaryKey}';"
            )
            cursor.execute(update_query)

        except pyodbc.Error as e:
            print(f"Error executing the query: {e}")
        except Exception as e:
            print(f"Error executing the query: {e}")
    def order(self,order:str)->List:
        return [int(i) for i in order.split(" - ")]




    def run(self):
        pass
    async def run_async(self):
        pass
    def process(self):
        pass
