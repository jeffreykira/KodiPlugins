#!/usr/bin/env python
import os
import zipfile

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

import xml.dom.minidom as dom

class XML:
    def __init__(self, path=None, string=None):
        if string:
            self.root = dom.parseString(string)
        elif path:
            self.root = dom.parse(path)
        else:
            self.root = dom.Document()

    def add_element(self, elementname, parent=None):
        element = self.root.createElement(elementname)
        if parent:
            parent.appendChild(element)
        else:
            self.root.appendChild(element)
        return element

    def add_data(self, text, parent):
        data = self.root.createTextNode(text)
        parent.appendChild(data)

    def get_xmlstring(self):
        return self.root.toprettyxml("\t", "\n").replace('\t','  ')

    def get_root(self):
        return self.root

    def get_children(self, parent=None):
        if parent:

            return parent.childNodes
        else:
            return self.root.childNodes

    def get_data(self,node):

        if node.nodeValue:

            return node.nodeValue
        else:
            return node.nodeName

    def is_root(self, node):

        try:
            node.tagName
            return False
        except:
            return True

    def is_data(self, node):
        if node.nodeValue:
            return True
        else:
            return False

    def write_xml(self, path):
        xml_file = open(path, 'wb')
        xml_file.write(self.get_xmlstring().encode(encoding))
        xml_file.close()

    def write_xml_with_dom(self, path, indent="  ",addindent="  ", newl=""):
        xml_file = open(path, 'wb')
        self.root.writexml(xml_file, indent=indent,addindent=addindent, newl=newl)
        xml_file.close()

def count_version_up(verion):
    versionint = int(version.replace('.',''))
    versionint += 1
    newversionstr = str(versionint)
    if len(newversionstr) == 1:
        return '0.0.%s'%newversionstr
    if len(newversionstr) == 2:
        return '0.%s.%s'%(newversionstr[0],newversionstr[1])
    if len(newversionstr) == 3:
        return '%s.%s.%s'%(newversionstr[0],newversionstr[1],newversionstr[2])

if __name__ == '__main__':


    plugin = 'script.mvg.departures'

    sourcefolder = './%s'%plugin
    try:
        os.makedirs(sourcefolder)
    except:
        pass
    addon_xml_file = os.path.join(sourcefolder,'addon.xml')
    print 'Updating: %s'%addon_xml_file
    xml = XML(path=addon_xml_file)

    node = xml.get_children()[0]

    assert xml.get_data(node) == 'addon',xml.get_data(node)

    version = node.getAttribute('version')
    newversion = count_version_up(version)
    print version,'-->',newversion
    node.setAttribute('version',newversion)

    xml.write_xml_with_dom(addon_xml_file)



    list_xml_file = 'addons.xml'
    print 'Updating: %s'%list_xml_file
    xml = XML(path=list_xml_file)
    node = xml.get_children()[0]

    addon_list = xml.get_children(node)
    for addon in addon_list:
        if not isinstance(addon, dom.Text):
            if addon.getAttribute('id') == plugin:
                addon.setAttribute('version',newversion)

    xml.write_xml_with_dom(list_xml_file)
    try:
        os.makedirs('./releases/%s'%plugin)
    except:
        pass
    zippath = './releases/%s/service.zfs-%s.zip'%(plugin,newversion)
    print 'Creating: %s'%zippath
    zipf = zipfile.ZipFile(zippath, 'w')
    zipdir(sourcefolder, zipf)
    zipf.close()

