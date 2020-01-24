from hal_utils import grep_in_country, grep_from_to_year, stringify, grep_in_year
from hal_sql import HalSQL
from hal_utils import grep_leaves

class HalQueryTemplates:

    def __init__(self): 

        sql = HalSQL()
        self.categories = sql.get_categories()
        self.countries = sql.get_countries()

    def get_query_company(self, leaves, sql_tokens):

        _, adj, name, _, company, pos = grep_leaves(leaves, 'Det[]*Adj[]*N[]*P[]*N[]')
        if adj == "average" and name == "stock" and company:
            if self.get_query_average_stock(leaves, sql_tokens, company, pos):
                return True
            else:
                return False

        _, num, adj, name, pos = grep_leaves(leaves, 'Det[]*NUM[]*Adj[]*N[]')        
        if not num or not adj or not name:
            _, name, verb, pos = grep_leaves(leaves, 'Det[]*N[]*V[]')
            if "company" == name and "create" == verb:
                if self.get_query_company_event(leaves, sql_tokens, pos, "", 0):
                    return sql_tokens
        elif "company" == name:
            if self.get_query_company_event(leaves, sql_tokens, pos, adj, num):
                    return sql_tokens

        return False

    def get_query_average_stock(self, leaves, sql_tokens, company, startpos):

        sql_tokens.append('select avg(st.Value) from Stock as st')
        joins = []
        wheres = []

        joins.append('inner join Company as c on c.ID = st.CompanyID')
        wheres.append('c.Name = \"{0}\"'.format(company))

        year_intervals = grep_from_to_year(leaves, startpos)        
        if len(year_intervals):
            for (start, end) in year_intervals:                                
                wheres.append('st.Date >= {0} and st.Date <= {1}'.format(start, end))                    
        
        for j in joins:
            sql_tokens.append(j)

        sql_tokens.append("where")        
        for i in range(len(wheres)):
            sql_tokens.append(wheres[i])
            if i < len(wheres) - 1:
                sql_tokens.append("and")

        return True

    def get_query_company_event(self, leaves, sql_tokens, startpos, attribute, limit):

        sql_tokens.append('SELECT * from company as c')
        joins = []
        wheres = []
        orders = []

        if attribute in self.categories:
            joins.append('inner join {0} as ct on c.{1} = ct.id'.format("category", "CategoryID"))
            wheres.append('ct.{0}=\"{1}\"'.format("Type", attribute))
            
        elif attribute == "large": # Assume is number of employees
            orders.append('c.EmployeeCount desc')

        countries = grep_in_country(leaves, startpos, self.countries)
        year_intervals = grep_from_to_year(leaves, startpos)        
        if len(year_intervals):
            joins.append('inner join {0} as e on e.{1} = c.id'.format("event", "CompanyID"))
            wheres.append('e.{0}=\"{1}\"'.format("Type", "founded"))
            for (start, end) in year_intervals:                                
                wheres.append('e.Date >= {0} and e.Date <= {1}'.format(start, end))                    
        else:                
            years = grep_in_year(leaves, startpos)
            if years:
                joins.append('inner join {0} as e on e.{1} = c.id'.format("event", "CompanyID"))
                wheres.append('e.{0}=\"{1}\" and e.Date in ({2})'.format("Type", "founded", stringify(years)))

        if len(countries) != 0:
            wheres.append('c.Country in ({0})'.format(stringify(countries)))

        for j in joins:
            sql_tokens.append(j)

        sql_tokens.append("where")        
        for i in range(len(wheres)):
            sql_tokens.append(wheres[i])
            if i < len(wheres) - 1:
                sql_tokens.append("and")

        if orders:
            sql_tokens.append("order by")
            for i in range(len(orders)):
                sql_tokens.append(orders[i])
                if i < len(orders) - 1:
                    sql_tokens.append("and")

        if limit and int(limit) > 0:
            sql_tokens.append("limit {0}".format(limit))

        return True
