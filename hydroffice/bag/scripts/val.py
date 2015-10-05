from lxml import etree
from lxml import isoschematron

doc_tree = etree.parse("./metadata.xml")
#print(etree.tostring(doc_tree, pretty_print=True))

#schema_doc = etree.parse("./ISO19139/gmi/metadataEntitySet.xsd")
schema_doc = etree.parse("./ISO19139/bag/bag.xsd")
#schema_doc = etree.parse("http://www.opennavsurf.org/schema/bag/bag.xsd")
schema = etree.XMLSchema(schema_doc)
try:
    schema.assertValid(doc_tree)
except etree.DocumentInvalid as e:
    print(e)

for i in schema.error_log:
    print(i)

schematron_doc = etree.parse("./bag_metadata_profile.sch")
schematron = isoschematron.Schematron(schematron_doc, store_report=True)
print(schematron.validate(doc_tree))


for i in schematron.error_log:
    print(i)

#report = schematron.validation_report
#print(report)




