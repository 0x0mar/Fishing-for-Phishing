import networkx as nx
import matplotlib.pyplot as plt
import MySQLdb

G=nx.Graph()
db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
cursor = db.cursor()
execString = ("SELECT Domain FROM Content;" % ()) 
cursor.execute(execString)
nodes = cursor.fetchall()

G.add_nodes_from(nodes)

nx.draw(G)
plt.savefig("simple_path.png") # save as png
plt.show() # display
