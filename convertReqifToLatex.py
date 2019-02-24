import os
import Requirements
from Requirements.TReqz import reqif_req_if
import utils
import string
import time

def convertReqifToLatex(reqifFile:str = "input.reqif", latexFile:str = "output.tex", width:str = "15cm", include_images=False):
    reqif = Requirements.TReqz.reqif(reqifFile)
    documentIds = reqif.getAllDocumentIds()
    specTypeIds = reqif.getAllSpecObjectTypeIds()

    target = open(latexFile, 'w')

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

    def handleReq(reqif, requirement:str, level='', childId=1):
        reqif.handledReqs+=1
        utils.commandlinePrint(utils.fillLeftWithZeros(str(reqif.handledReqs), len(str(len(allRequirements))))+"/"+str(len(allRequirements)))
        
        values = reqif.getRequirementValues(requirement)
        res=""

        results = []
        isChapter=False
        for attribute in attributes:
            value = values.get(attribute)

            if attribute == 'ReqIF.Text':
                if chapterExists and (value == None or value == ''):
                    value = values.get('ReqIF.ChapterName')
                    if value != None and value != '':
                        isChapter=True

            if value != None and value != '':

                if reqif.checkAttributeIsXhtmlByLongName(typeId, attribute):
                    value=htmlToText(value)
                    value=utils.cleanXhtml(value)
                    value=utils.tex_escape(value)
                    value:str = value.strip("\n")
                    value = value.split("\n")
                    newValue=[]
                    for v in value:
                        normalizedValue = v.strip()
                        normalizedValue = normalizedValue.strip("\t")
                        if normalizedValue!='' and normalizedValue!="\n":
                            newValue.append(normalizedValue)

                    value = "\n".join(newValue)

                    value:str = value.replace("\n", "\\newline \n")
                    if isChapter:
                        if level=='':
                            level=str(childId)
                        else:
                            level+='.'+str(childId)
                        value = "\\textcolor{red}{\\textbf{"+level+' '+value+"}}"
                    value = '\\begin{minipage}{'+width+'}'+value+'\\end{minipage}'
                else:
                    if reqif.checkAttributeIsEnumerationByLongName(typeId, attribute):
                        attributeType = reqif.findAttributeTypeByLongName(typeId, attribute)
                        valueMap = attributeType.getValueMap()
                        newValue = []
                        for v in value:
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

                results.append(value)
            else:
                if reqif.checkAttributeIsEnumerationByLongName(typeId, attribute):
                    elem=reqif.convertEnumerationValuesByLongName(typeId, attribute, value)
                    if elem!=[]:
                        value = ', '.join(elem)
                        results.append(value)
                    else:
                        results.append(' ')
                else:
                    results.append(' ')

        res+= ("&".join(results))+"\\\\\n\\hline\n"

        childs = reqif.getRequirementChilds(documentId, requirement)

        res = ''.join(x for x in res if x in string.printable)
        target.write(res)

        if childs==None:
            raise RuntimeError

        i=1
        for child in childs:
            wasChapter = handleReq(reqif, child, level, i)
            if wasChapter:
                i+=1

        if isChapter:
            return True
        return False

    res="\\documentclass[10pt,a4paper,final,landscape]{scrartcl}\n"
    res+="\\usepackage{longtable}\n"
    res+="\\usepackage{tabu}\n"
    res+="\\usepackage{xcolor}\n"
    res+="\\usepackage[utf8]{inputenc}\n"
    res+="\\usepackage{lmodern}\n"
    res+="\\usepackage[babel, german=guillemets]{csquotes}\n"
    res+="\\usepackage[ngerman]{babel}\n"
    res+="\\usepackage{textcomp}\n"
    res+="\\usepackage[left=1cm,right=1cm, bottom=1cm, top=1cm]{geometry}\n"
    res+="\\begin{document}\n"
    res+="\\setlength{\\tabulinesep}{3pt}\\begin{center}\\begin{longtabu} to \\textwidth {|p{"+width+"}|"+"l|"*(len(attributes)-1)+"}\n"
    
    attributeNames = []
    for attribute in attributes:
        attributeNames.append(utils.tex_escape(attribute))
    res+=" & ".join(attributeNames)+"\\\\\n"
    res+="\\hline\n"
    target.write(res)

    utils.startCommandlinePrint(utils.fillLeftWithZeros(str(reqif.handledReqs), len(str(len(allRequirements))))+"/"+str(len(allRequirements)))
    i=1
    for requirement in rootReqs:
        wasChapter = handleReq(reqif, requirement, '', i)
        if wasChapter:
            i+=1

    res="\\end{longtabu}\\end{center}\n"
    res+="\\end{document}"
    target.write(res)

    target.close()
    utils.endCommandlinePrint()