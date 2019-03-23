import os
import Requirements
from Requirements.TReqz import reqif_req_if
import utils
import string
import time
import csv

def convertReqifToCsv(reqifFile:str = "input.reqif", csvFile:str = "requirements.csv", idAttribute='ID', typeAttribute='Typ'):
    reqif = Requirements.TReqz.reqif(reqifFile)
    documentIds = reqif.getAllDocumentIds()
    specTypeIds = reqif.getAllSpecObjectTypeIds()

    targetHandle = open(csvFile, 'w', newline='')
    target = csv.DictWriter(targetHandle, fieldnames=['REQ_ID', 'TEXT', 'TYPE'])

    documentId = documentIds[0]
    typeId = specTypeIds[0]

    rootReqs = reqif.getAllDocumentRootRequirements(documentId)
    attributes = reqif.getAllAttributeTypeLongNames(typeId)
    chapterExists = False

    allRequirements = reqif.getAllDocumentRequirementIds(documentId)
    reqif.handledReqs=0

    for attribute in attributes:
        if attribute == 'ReqIF.ChapterName':
            chapterExists=True
            attributes.remove('ReqIF.ChapterName')
            break

    attributes.remove('ReqIF.Text')
    attributes.insert(0, 'ReqIF.Text')

    def htmlToText(text:str):
        newtext = text.replace("<br />", "\n")
        newtext = newtext.replace("</div>", "</div> ")
        newtext = newtext.replace("\n\n", "\n")
        return newtext

    def handleReq(reqif, requirement:str):
        reqif.handledReqs+=1
        utils.commandlinePrint(utils.fillLeftWithZeros(str(reqif.handledReqs), len(str(len(allRequirements))))+"/"+str(len(allRequirements)))
        
        values = reqif.getRequirementValues(requirement)
        res=""

        results = {'REQ_ID': '', 'TEXT': '', 'TYPE': ''}
        for attribute in attributes:
            value = values.get(attribute)

            if not attribute in ['ReqIF.Text', idAttribute, typeAttribute]:
                continue

            if attribute == 'ReqIF.Text':
                if chapterExists and (value == None or value == ''):
                    value = values.get('ReqIF.ChapterName')

            if value != None and value != '':

                if reqif.checkAttributeIsXhtmlByLongName(typeId, attribute):
                    value=htmlToText(value)
                    value=utils.cleanXhtml(value)
                    value:str = value.strip("\n")
                    value = value.split("\n")
                    newValue=[]
                    for v in value:
                        normalizedValue = v.strip()
                        normalizedValue = normalizedValue.strip("\t")
                        if normalizedValue!='' and normalizedValue!="\n":
                            newValue.append(normalizedValue)

                    value = "\n".join(newValue)
                else:
                    if reqif.checkAttributeIsEnumerationByLongName(typeId, attribute):
                        attributeType = reqif.findAttributeTypeByLongName(typeId, attribute)
                        valueMap = attributeType.getValueMap()
                        newValue = []
                        for v in value:
                            if v != [] and v != None:
                                newValue.append(valueMap.get(v))
                        value = newValue
                    else:
                        pass

                if isinstance(value, str):
                    pass
                elif isinstance(value, list):
                    value = ', '.join(value)
                else:
                    raise RuntimeError("unsupported type: "+str(type(value)))
            else:
                if reqif.checkAttributeIsEnumerationByLongName(typeId, attribute):
                    elem=reqif.convertEnumerationValuesByLongName(typeId, attribute, value)
                    if elem!=[]:
                        value = ', '.join(elem)
                    else:
                        value = ' '
                else:
                    value = ' '

            if attribute == 'ReqIF.Text':
                results['TEXT'] = value
            elif attribute == idAttribute:
                results['REQ_ID'] = value
            elif attribute == typeAttribute:
                results['TYPE'] = value

        childs = reqif.getRequirementChilds(documentId, requirement)

        res = ''.join(x for x in res if x in string.printable)
        target.writerow(results)

        if childs==None:
            raise RuntimeError

        for child in childs:
            handleReq(reqif, child)
    
    target.writeheader()
    utils.startCommandlinePrint(utils.fillLeftWithZeros(str(reqif.handledReqs), len(str(len(allRequirements))))+"/"+str(len(allRequirements)))
    for requirement in rootReqs:
        handleReq(reqif, requirement)

    targetHandle.close()
    utils.endCommandlinePrint()