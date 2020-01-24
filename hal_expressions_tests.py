import unittest
from nltk import Tree
from hal_treeparser import HalTreeParser
from hal_expression import HalExpression

class HalExpressionsTests(unittest.TestCase):

    def test_expressions_1(self):
        query = "what are the 10 shareholders of sony"
        expected_sql = "SELECT n1.*, n2.Percent from company as n1 " \
                "inner join links as n2 on n2.ParentID = n1.id " \
                "inner join company as n3 on n3.id = n2.ChildID " \
                "where n3.name = \"sony\" " \
                "limit 10"
        self.validate_sql(query, expected_sql)

    def test_expressions_2(self):
        query = "what are the 10 largest shareholders of sony"
        expected_sql = "SELECT n1.*, n2.Percent from company as n1 " \
                "inner join links as n2 on n2.ParentID = n1.id " \
                "inner join company as n3 on n3.id = n2.ChildID " \
                "where n3.name = \"sony\" " \
                "order by n2.Percent desc " \
                "limit 10"
        self.validate_sql(query, expected_sql)

    def test_expressions_3(self):
        query1 = "what companies were created in netherlands in 1970"
        query2 = "what companies were created in the netherlands in 1970"        
        expected_sql = "SELECT * from company as c " \
                "inner join event as e on e.CompanyID = c.id " \
                "where e.Type=\"founded\" " \
                "and e.Date in ('1970') " \
                "and c.Country in ('netherlands')"
        self.validate_sql(query1, expected_sql)
        self.validate_sql(query2, expected_sql)

    def test_expressions_4(self):
        query1 = "what companies were created in 1946"
        query2 = "what are the companies created in 1946"
        query3 = "what companies were created in the world in 1946"
        expected_sql = "SELECT * from company as c " \
                "inner join event as e on e.CompanyID = c.id " \
                "where e.Type=\"founded\" " \
                "and e.Date in ('1946')"
        self.validate_sql(query1, expected_sql)
        self.validate_sql(query2, expected_sql)
        self.validate_sql(query3, expected_sql)

    def test_expressions_5(self):
        query1 = "what companies were created in usa from 1946 to 1970"
        query2 = "what companies were created in usa between 1946 and 1970"
        expected_sql = "SELECT * from company as c " \
                "inner join event as e on e.CompanyID = c.id " \
                "where e.Type=\"founded\" " \
                "and e.Date >= 1946 and e.Date <= 1970 " \
                "and c.Country in ('usa')"
        self.validate_sql(query1, expected_sql)
        self.validate_sql(query2, expected_sql)
    
    def test_expressions_6(self):
        query = "what electronic companies were created in {0}"
        expected_sql = "SELECT * from company as c " \
                "inner join category as ct on c.CategoryID = ct.id " \
                "inner join event as e on e.CompanyID = c.id " \
                "where ct.Type=\"electronic\" and " \
                "e.Type=\"founded\" and " \
                "e.Date in ('{0}')"                 
        self.validate_sql(query.format(1970), expected_sql.format(1970))
        self.validate_sql(query.format(1946), expected_sql.format(1946))

    def test_expressions_7(self):
        query = "what are the 10 largest companies of japan"
        expected_sql = "SELECT * from company as c " \
                "where c.Country in ('japan') " \
                "order by c.EmployeeCount desc limit 10"
        self.validate_sql(query, expected_sql)

    def test_expressions_8(self):
        query = "what companies are chocolatier"
        expected_sql = "SELECT * from company as c " \
                "inner join category as ct on c.CategoryID = ct.id " \
                "where ct.Type=\"chocolatier\""
        self.validate_sql(query, expected_sql)     

    def test_expressions_9(self):
        query = "what are the shareholders of sony"
        expected_sql = "SELECT n1.*, n2.Percent from company as n1 " \
                "inner join links as n2 on n2.ParentID = n1.id " \
                "inner join company as n3 on n3.id = n2.ChildID " \
                "where n3.name = \"sony\""
        self.validate_sql(query, expected_sql)   

    def test_expressions_10(self):
        query = "what is the largest shareholder of sony"
        expected_sql = "SELECT n1.*, n2.Percent from company as n1 " \
                "inner join links as n2 on n2.ParentID = n1.id " \
                "inner join company as n3 on n3.id = n2.ChildID " \
                "where n3.name = \"sony\" " \
                "order by n2.Percent desc"
        self.validate_sql(query, expected_sql)   

    def test_expressions_11(self):
        query = "what is the average stock of airbus between 2014 and 2019"
        expected_sql = "select avg(st.Value) from Stock as st " \
                "inner join Company as c on c.ID = st.CompanyID " \
                "where c.Name = \"airbus\" " \
                "and st.Date >= 2014 and st.Date <= 2019"
        self.validate_sql(query, expected_sql)   

    def validate_sql(self, query, expected_sql):
        parser = HalTreeParser()
        tree = parser.get_tree(query)
        expr = HalExpression(tree)
        gen_sql = expr.gen_sql()
        print ('query:        \"' + query + "\"")
        print ('expected sql: \"' + expected_sql + "\"")
        print ('gen sql:      \"' + gen_sql + "\"")
        self.assertEqual(expected_sql, gen_sql, "Invalid sql")

if __name__ == '__main__':
    unittest.main()
    #t = HalExpressionsTests()
    #t.setUp()
    #t.test_expressions_11()
