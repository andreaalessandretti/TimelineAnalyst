from timeManager import ms2str

def plotActivitiesList(activitiesList):
    formatVisitTable = "{:<8} {:<10} {:<20} {:<20}"
    retStr =  formatVisitTable.format('name','address','startTimeStr','stopTimeStr')+'\n\r'
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         retStr = retStr + formatVisitTable.format(
            activitiesList[i]['name'],activitiesList[i]['address'], activitiesList[i]['startTimeStr'],
            activitiesList[i]['stopTimeStr'])+'\n\r'
    return retStr

def plotInfectedActivitiesList(activitiesList):
    formatVisitTable = "{:<16} {:<16} {:<20} {:<40} {:<40}"
    retStr = formatVisitTable.format('vInfected.id','uInfected.id','vInfected.locationId','vInfected.startTime','vInfected.stopTime')+'\n\r'
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         retStr = retStr +formatVisitTable.format(
            activitiesList[i]['vInfected.id'],activitiesList[i]['uInfected.id'],activitiesList[i]['vInfected.locationId'],
            activitiesList[i]['vInfected.startTime'],
            activitiesList[i]['vInfected.stopTime'])+'\n\r'
    return retStr

def plotInfectedUserVisitList(activitiesList):
    formatVisitTable = "{:<16} {:<16}  {:<16}  {:<16} {:<40} {:<40}"
    retStr = '-'*(16+16+16+40+40) +'\n\r'
    retStr = retStr +formatVisitTable.format('vQuery.id', 'vInfectedId', 'vInfectedLocationId', 'uInfectedId', 'vInfectedstartTime', 'vInfectedstopTime' )+'\n\r'
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         retStr = retStr +formatVisitTable.format(
            activitiesList[i]['vQuery.id'],activitiesList[i]['vInfectedId'],activitiesList[i]['vInfectedLocationId'],
            activitiesList[i]['uInfectedId'],
            activitiesList[i]['vInfectedstartTime'],
            activitiesList[i]['vInfectedstopTime'])+'\n\r'
    return retStr

def plotInfectedUserVisitListShort(activitiesList):
    formatVisitTable = "{:<16} {:<16} {:<50} {:<100}"
    retStr ='-'*(16+16+40+40) +'\n\r'
    retStr = retStr +formatVisitTable.format('startTime', 'stopTime', 'name', 'address' )+'\n\r'
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         retStr = retStr +formatVisitTable.format(
            activitiesList[i]['vInfectedstartTime'],
            activitiesList[i]['vInfectedstopTime'],
            activitiesList[i]['name'],
            activitiesList[i]['address'].replace('\n', ' ').replace('\r', '')
            )+'\n\r'
    return retStr

def plotInputVisitListShort(activitiesList):
    formatVisitTable = "{:<16} {:<16} {:<50} {:<100}"
    retStr ='-'*(16+16+50+100) +'\n\r'
    retStr = retStr +formatVisitTable.format('startTime', 'stopTime', 'name', 'address' )+'\n\r'
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         retStr = retStr +formatVisitTable.format(
            ms2str(int(activitiesList[i]['startTime'])),
            ms2str(int(activitiesList[i]['stopTime'])),
            activitiesList[i]['name'],
            activitiesList[i]['address'].replace('\n', ' ').replace('\r', ''),
            )+'\n\r'
    return retStr

def plotCoundedInfectedLocation(locationList):

    formatTable = "{:<20} {:50} {:<100} "
    retStr='-'*(20+50+100) +'\n\r'
    retStr = retStr +formatTable.format('nPositiveVisits','name', 'address')+'\n\r'
    if locationList is None: return
    for i in range(len(locationList)):
         retStr = retStr +formatTable.format(
            locationList[i]['nPositiveVisits'],
            locationList[i]['name'],
            locationList[i]['address'].replace('\n', ' ').replace('\r', ''))+'\n\r'
    return retStr
