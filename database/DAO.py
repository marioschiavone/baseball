from database.DB_connect import DBConnect
from model.teams import Team


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct (t.`year`) from teams t 
                    where t.`year` >= 1980
                    order by t.`year` desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from teams t 
                    where t.`year`=%s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsSalaries(year, idMap):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """select t.teamCode,t.ID, sum(s.salary) as totSalary
                    from teams t, salaries s, appearances a 
                    where t.`year`=s.`year` and a.`year` = t.`year` 
                    and s.`year` = %s
                    and s.playerID = a.playerID
                    and t.ID = a.teamID
                    group by t.teamCode"""

        cursor.execute(query, (year,))
        result={}
        for row in cursor:
            result[idMap[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return result
