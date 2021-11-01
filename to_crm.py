from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import SKOS, RDF, RDFS
import textbase
import uuid
from rich.progress import track

"""
A first cut at making a conversion of the DPD data to a CIDOC-CRM vocabulary
Thanks to Athanasios Velos for the extensive explanation and pointers to get started.
This is not done, but needs to be reviewed and completed.
"""

graph = Graph()
CRM = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
graph.bind('crm', CRM)
DPD_URI = 'http://dutchprintersdevices.com/'
DPD = Namespace(DPD_URI)
graph.bind('dpd', DPD_URI)


for obj in track(textbase.parse('printerinfo.dmp')):
    new_uuid = URIRef(str(uuid.uuid4()), DPD_URI)
    graph.add((new_uuid, RDF.type, CRM["E7_Activity"]))
    
    person_uuid = URIRef(str(uuid.uuid4()), DPD_URI)
    graph.add((new_uuid, CRM["P14_carried_out_by"], person_uuid))
    bspr_uuid = URIRef(str(uuid.uuid4()), DPD_URI)
    graph.add((person_uuid, CRM["P1_is_identified_by"], bspr_uuid))
    graph.add((bspr_uuid, RDF.type, CRM["E42_Identifier"]))
    graph.add((bspr_uuid, RDFS.label, Literal(obj["ID"][0])))

    

    pa = obj.get("PLACE.ACTIVE", [None])[0]
    if pa:
        placename = pa.split(" ")[0]
        paa = pa.split("@RANGE")
        if len(paa) > 1:
            paa = paa[1]
            paa_date = paa.split("-")            
            timespan_uuid = URIRef(str(uuid.uuid4()), DPD_URI)
            graph.add((new_uuid, CRM["P4_has_time-span"], timespan_uuid))
            graph.add((timespan_uuid, CRM["P89a_begin_of_the_begin"], Literal(paa_date[0].strip())))
            if len(paa_date) == 2:
                graph.add((timespan_uuid, CRM["P90a_end_of_the_end"], Literal(paa_date[1].strip())))

graph.serialize(destination='printerinfo.ttl', format='turtle', encoding="utf-8")

