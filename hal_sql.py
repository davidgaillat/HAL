
import sqlite3

class HalSQL:

    def ExecuteQuery(self, query):
        connection = sqlite3.connect('hal_database.db')
        cursor = connection.execute(query)
        items = []
        to_remove = []
        columns = [description[0] for description in cursor.description if not description[0].endswith('ID')]
        columns = [w.replace("EmployeeCount", "Number of employees") for w in columns]
        columns = [w.replace("Percent", "Total percent") for w in columns]
        columns = [w.replace("avg(st.Value)", "Stock average") for w in columns]

        for i, item in enumerate(cursor.description):
            if(item[0].endswith('ID')):
                to_remove.append(i)
        for row in (cursor):          
            r = [w for i, w in enumerate(row) if i not in to_remove]  
            items.append(r)
        
        connection.close()    
        return (items, columns)

    def get_companies(self):
        connection = sqlite3.connect('hal_database.db')
        cursor = connection.execute("select Name from Company")
        results = []

        for row in cursor:
            results.append(row[0])

        connection.close()    
        return results

    def get_countries(self):
        connection = sqlite3.connect('hal_database.db')
        cursor = connection.execute("select Country from Company")
        results = []

        for row in cursor:
            results.append(row[0])

        connection.close()    
        return results

    def get_categories(self):
        connection = sqlite3.connect('hal_database.db')
        cursor = connection.execute("select Type from Category")
        results = []

        for row in cursor:
            results.append(row[0])

        connection.close()    
        return results

if __name__ == "__main__":
    f = HalSQL
    results = HalSQL().ExecuteQuery("SELECT * from company as n1 inner join links as n2 on n2.ParentID = n1.id inner join company as n3 on n3.id = n2.ChildID where n3.name = \"sony\" limit 10")
    #results = HalSQL().ExecuteQuery('select Country from Company')
    for result in results:
        print(result)
