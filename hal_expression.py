from nltk.grammar import FeatStructNonterminal
from hal_treeparser import HalTreeParser
from functools import reduce
from hal_sql import HalSQL
from hal_utils import grep_leaves, grep_from_to_year, grep_in_country, grep_in_year
from hal_querytemplates import HalQueryTemplates

class HalExpression:

    def __init__(self, tree): 

        self.tree = tree
        self.table_metadata = {
            "shareholder_company": { 
                "id":"id", 
                "shareholder_id":"shareholder_id",
                "company_id":"company_id",
                "large": "participation" 
            },
            "shareholder": { "id":"id", "name":"name" },
            "company": { "id":"id", "name":"name" }
        }
        sql = HalSQL()
        self.companies = sql.get_companies()
        self.countries = sql.get_countries()
        self.categories = sql.get_categories()

    def gen_sql(self):

        if (len(self.tree) != 2 and
            all(isinstance(x, FeatStructNonterminal) for x in tree)):
            raise ValueError('Invalid sentence: a sentence is composed of VP and NP')

        sent_struct = [repr(self.tree[i].label()) for i in range(2)]
        sql_tokens = []
        if (['NP[]', 'VP[]'] == sent_struct):
            self.gen_npfirst_sent(self.tree[0], self.tree[1], sql_tokens)
        elif (['VP[]', 'NP[]'] == sent_struct):
            self.gen_vpfirst_sent(self.tree[0], self.tree[1], sql_tokens)
        else:
            raise ValueError('Invalid sentence structure: a sentence is a NP followed by VP or viceversa')
        
        return ' '.join(sql_tokens)


    def gen_npfirst_sent(self, np, vp, sql_tokens):
        
        template = HalQueryTemplates()
        leaves = self._get_annotated_leaves(np)
        _, attribute, company, _ = grep_leaves(leaves, '#WP#*(N[]|Adj[])*company')       
        if not company:
            attribute = ""
            _, company, _ = grep_leaves(leaves, '#WP#*company')                   
        if company:
            leaves = self._get_annotated_leaves(vp)
            verb1, part, pos = grep_leaves(leaves, 'V[]*(V[]|Adj[])')
            if ('be', 'create') == (verb1, part):
                # type of query -> what companies were created in netherlands in 1970
                if template.get_query_company_event(leaves, sql_tokens, pos, attribute, 0):            
                    return sql_tokens
            elif verb1 == 'be':
                if template.get_query_company_event(leaves, sql_tokens, pos, part, 0):            
                    return sql_tokens
            
        raise ValueError('Invalid sentence structure') 
    
    def gen_vpfirst_sent(self, vp, np, sql_tokens):
        
        leaves = vp.leaves()
        if (['#WDT#', 'be'] == leaves or ['give', '#PRP#'] == leaves or ['#WP#', 'be'] == leaves):            
            leaves = self._get_annotated_leaves(np)
            if self.get_query_type_1(leaves, sql_tokens):
                return sql_tokens            
            else:
                template = HalQueryTemplates()
                template.get_query_company(leaves, sql_tokens)
                return sql_tokens
            
        raise ValueError('Invalid sentence structure') 

    # type of query -> what are the 10 largest shareholders of sony
    def get_query_type_1(self, leaves, sql_tokens):

        num, adj, name1, _, name2, _ = grep_leaves(leaves, '(NUM[])*Adj[]*N[]*P[]*N[]')
        if not name1 or not name2:
            num, name1, _, name2 , _ = grep_leaves(leaves, '(NUM[])*N[]*P[]*N[]')
        if name1 and name2:
            if name1 == "shareholder" and name2 in self.companies:
                sql_tokens.append('SELECT')
                sql_tokens.append('n1.*, n2.Percent')
                sql_tokens.append('from {0} as n1'.format("company"))
                sql_tokens.append('inner join {0} as n2 on n2.{1} = n1.id'.format("links", "ParentID"))
                sql_tokens.append('inner join {0} as n3 on n3.id = n2.{1}'.format("company", "ChildID"))                
                sql_tokens.append("where n3.name = \"{0}\"".format(name2))  
                if adj:
                    sql_tokens.append("order by n2.{0} desc".format("Percent"))
                if num:
                    sql_tokens.append('limit {0}'.format(num))
                return True
        return False

    def _get_annotated_leaves(self, tree):        
        leaves = []
        for idx, leave in enumerate(tree.leaves()):
            tree_location = tree.leaf_treeposition(idx)
            non_terminal = tree[tree_location[:-1]]
            leaves.append((repr(non_terminal.label()), leave))
        return leaves
    
if __name__ == '__main__':   
    #how many electronics companies are in japan 
    #how many companies where created in japan in 2017
    #what companies were created in usa from 2017 to 2019
    #What were the sales of airbus in 2018
    #tree = HalTreeParser().get_tree(query = "give me the top 20 shipping companies in the world")                
    tree = HalTreeParser().get_tree(query = "what is the average stock of airbus between 2014 and 2019")    
    print (HalTreeParser().get_pprint(tree))
    expr = HalExpression(tree)
    print (expr.gen_sql())

