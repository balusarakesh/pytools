import rdflib
from rdflib import BNode
from rdflib import Literal
def get_mozilla_package(rdf_file):
    graph = rdflib.Graph()
    graph.parse(rdf_file)
    triplets = []
    val = 'rak'
    for subject, predicate, object in graph:
        
#         if u'N916980c7bb924a20ba919426268b45f2' in unicode(triplet[0].n3()):
        if unicode(subject) == 'urn:mozilla:install-manifest':
            print unicode(subject) + ' : '  + predicate + ' : ' + object.toPython()
        else:
            print type(subject).__name__
get_mozilla_package('/home/rakesh/Documents/tempr/test/bountysource-0.0.14-fx.xpi-extract/install.rdf')