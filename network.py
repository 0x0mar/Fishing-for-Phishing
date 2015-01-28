import networkx as nx
import matplotlib.pyplot as plt
import MySQLdb

G=nx.MultiDiGraph()
db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
cursor = db.cursor()
execString = ("SELECT DISTINCT Domain FROM Content;" % ()) 
cursor.execute(execString)
nodes = cursor.fetchall()

execString = ("SELECT DISTINCT Domain, domainTo FROM outboundLinks;" % ()) 
cursor.execute(execString)
edges = cursor.fetchall()

G.add_nodes_from(nodes)
G.add_nodes_from(edges)

nx.draw(G, with_labels=False)
plt.savefig("simple_path2.png") # save as png
plt.show() # display
