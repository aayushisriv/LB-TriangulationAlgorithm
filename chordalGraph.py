import random
import numpy as np

import itertools
import copy

import networkx as nx
import matplotlib.pyplot as plt

class ChordalGraph:
	"""This class turns arbitrary graph into chordal graph."""

	def __init__(self, noNodes, noEdges):
		"""function to initialize the variables in the instance of a WeaklyChordalGraph"""
		self.noNodes = noNodes
		self.noEdges = noEdges
		self.vertexList = []
		self.GEdgeList = []
		self.HEdgeList = []
		self.minSepList = []
		self.minSepListRec = []
		self.G = {}
		self.H = {}
		
	def createAG(self): 
		"""function to create arbitrary graph"""
		self.G = nx.dense_gnm_random_graph(self.noNodes, self.noEdges)
		#self.G = {0: [1, 3], # a=0, b=1, c=2, d=3
				  #1: [0, 2],
				  #2: [1, 3],
				  #3: [0, 2]}
	
		#self.G = {0: [1, 2, 3], # a=0, b=1, c=2, d=3
				  #1: [0, 2],
				  #2: [0, 1, 3],
				  #3: [0, 2]}
	
		#self.G = {0: [1, 2, 3], # a=0, b=1, c=2, d=3
				#1: [0, 2, 3],
				#2: [0, 1, 3],
				#3: [0, 1, 2]}
				
		#self.G = {0: [1, 2, 3, 4], # a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, i=8
				  #1: [0, 5, 7],
				  #2: [0, 6],
				  #3: [0, 7],
				  #4: [0, 8],
				  #5: [1, 6],
				  #6: [2, 5],`
				  #7: [1, 3, 8],
				  #8: [4, 7]}
				  
		self.G = {0: [15], 1: [8, 2, 3, 10], 2: [1, 10, 5, 6], 3: [1, 15], 4: [5], 5: [2, 4, 6, 15], 6: [9, 2, 12, 5], 7: [8, 11, 13], 8: [1, 14, 7], 9: [10, 6, 15], 10: [1, 2, 12, 13, 9], 11: [7], 12: [10, 13, 6], 13: [10, 15, 12, 7], 14: [8, 15], 15: [0, 3, 5, 9, 13, 14]}
		

		if type(self.G) is not dict:
			self.G = nx.to_dict_of_lists(self.G)
				
		for i in range(0, self.noNodes):
			self.vertexList.append(i)
		for key, value in self.G.iteritems():
			for v in value:
				if key<v:
					e = []
					e.append(key)
					e.append(v)
					self.GEdgeList.append(e)
		
		self.G = nx.Graph(self.G)
		connComp = sorted(nx.connected_components(self.G))
		self.G = nx.to_dict_of_lists(self.G)
		
		connComp = list(connComp)
		noOFConnComp = len(connComp)
		if noOFConnComp > 1:
			print "Here we are"
			print connComp
			self.plotGraph(self.G, "Arbitrary Graph (before splitting)")
			j = 0
			while j < noOFConnComp - 1:
				u = random.choice(list(connComp[j%noOFConnComp]))
				v = random.choice(list(connComp[(j+1)%noOFConnComp]))
				self.addAnEdge(self.G, self.GEdgeList, u, v)
				j = j + 1

	def addAnEdge(self, graphToAdd, edgeListToAdd, v1, v2):
		"""function to add an edge in the graph"""
		graphToAdd[v1].append(v2)
		graphToAdd[v2].append(v1)
		e = []
		e.append(v1)
		e.append(v2)
		edgeListToAdd.append(e)
	
	def createAuxGraph(self, graph, auxNodes):
		"""function to create induced graph on the set of vertices"""
		auxGraph = {}
		for i in auxNodes:
			if i in graph:
				auxGraph[i] = list(set(graph[i]).intersection(set(auxNodes)))
		return auxGraph
	
	def createCompleteGraph(self, vertexList):
		"""function to create complete graph on the set of vertices"""
		eCounter = 0
		for pair in itertools.combinations(vertexList, 2):
			v1 = pair[0]
			v2 = pair[1]
			if [v1, v2] not in self.HEdgeList and [v2, v1] not in self.HEdgeList:
				self.addAnEdge(self.H, self.HEdgeList, v1, v2)
				print "\nAdded edge between: "+str(v1)+" and "+str(v2)
				eCounter = eCounter + 1
		return eCounter
		
	def createCG(self):
		"""function to create Chordal Graph"""
		self.HEdgeList = copy.deepcopy(self.GEdgeList)
		self.H = copy.deepcopy(self.G)
		
		print "START~~~~~~~~~Turning the AG to CG~~~~~~~~~START"
		self.LB_Triang(self.vertexList, self.HEdgeList, self.H)
		print "END=========Turning the AG to CG=========END"
			
		return True
		
	def LB_Triang(self, vertexList, edgeList, graphToRecognize):
		"""This function is implemented based on the algorithm LB-Triang from the paper "A WIDE-RANGE EFFICIENT ALGORITHM FOR 
		MINIMAL TRIANGULATION" by Anne Berry for recognition chordal graphs and add edges (if necessary) by making each vertex 
		LB-simplicial.""" 

		#graphToRecognize = {0: [1, 4], 1:[0, 2], 2:[1, 3], 3:[2, 4], 4:[0, 3]}
		#vertexList, edgeList = self.createEdgeList(graphToRecognize)
		
		#random.shuffle(vertexList)
		vertexVisibility = [0]*len(vertexList)
		isChordal = False
		for v in vertexList:
			print "The vertex "+str(vertexList.index(v))+"-"+str(v)+" is verifying..."
			openNeighbors = graphToRecognize[v]
			print "My openNeighbors is;", openNeighbors
			closedNeighbors = copy.deepcopy(openNeighbors)
			closedNeighbors.append(v)
			print "Closed Neighb:", closedNeighbors
			cNMinusE = list(set(vertexList).difference(set(closedNeighbors))) #V-S
			print "cNMinusE:",cNMinusE
			eAddedCount = 0
			if cNMinusE:
				VMinusSGraph = self.createAuxGraph(graphToRecognize, cNMinusE) #G(V-S)
				componentsOri = sorted(nx.connected_components(nx.Graph(VMinusSGraph)))
				print "Component(s) in the graph: "+str(componentsOri)
				componentsCompAll = []
				for co in componentsOri:
					openNCO = []
					for v1 in co:
						openNV1 = graphToRecognize[v1]
						print "openNV1",openNV1
						openNCO = openNCO+openNV1
						print "pehle wala openNCO",openNCO
					openNCO = list(set(openNCO).difference(co))
					print "Baad wala openNCO:",openNCO
					eCounter = self.createCompleteGraph(openNCO)
					#if eCounter >= 1:
					#    self.plotGraph(self.H, str(eCounter)+" edge(s) added.")
					#    print "================================================"
					#else:
					#    print "================================================"
			else:
				print "The vertex "+str(v)+" does not generate any minimal separator."
				print "================================================"
			
		###For recognition, if the generated graph is a chordal graph or not.
		graph = nx.Graph(self.H)
		if nx.is_chordal(graph):
			print("*********After adding edges the generated graph is Chordal graph.*********")
		else:
			print("*********After adding edges the generated graph is NOT Chordal graph.*********")
		
	def plotGraph(self, graphToDraw, graphName):
		"""function to plot graphs"""
		edges = 0
		for node, degree in graphToDraw.iteritems():
			edges += len(degree)           
		
		GD = nx.Graph(graphToDraw)
		pos = nx.spring_layout(GD)
		
		plt.figure()
		if graphName == 1:
			print "\nArbitrary Graph: "+str(self.G)
			print "\nNo. of edges in the Arbitrary Graph: "+ str(edges/2)
			plt.title("Arbitrary Graph")
			nx.draw_networkx(GD, pos, True)
		else:
			H_set = set(map(tuple, self.HEdgeList))
			G_set = set(map(tuple, self.GEdgeList))
			
			newEdgeList = list(H_set.difference(G_set))
			newVertexList = list(set(x for l in newEdgeList for x in l))
			oldVertexList = list(set(self.vertexList).difference(set(newVertexList)))
			
		
			nx.draw_networkx_nodes(GD, pos, nodelist=newVertexList, node_color='blue', node_size=500, alpha=0.8)
			nx.draw_networkx_nodes(GD, pos, nodelist=oldVertexList, node_color='r', node_size=500, alpha=0.8)
			
			nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
			nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList, width=8, alpha=0.5, edge_color='blue')
			if newEdgeList:
				if graphName == 2:
					print "\nChordal Graph: "+str(self.H)
					print "\nNo. of edges in the CG: "+ str(edges/2)
					plt.title("Chordal Graph")
				else:
					plt.title(graphName)
				nx.draw_networkx_labels(GD, pos, font_size=16)
			else:
				if graphName == 2:
					print "\nChordal Graph: "+str(self.H)
					print "\nNo. of edges in the CG: "+ str(edges/2)
					plt.title("Chordal Graph")
					
				else:                
					plt.title(graphName)
				nx.draw_networkx(GD, pos, True)
		plt.show(block = False)