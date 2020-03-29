def plotActivitiesList(activitiesList):
    formatVisitTable = "{:<8} {:<8} {:<10} {:<20} {:<20}"
    print (formatVisitTable.format('id','userId','locationId','startTimeStr','stopTimeStr'))
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         print (formatVisitTable.format(
            activitiesList[i]['id'],activitiesList[i]['userId'], activitiesList[i]['locationId'],
            activitiesList[i]['startTimeStr'],activitiesList[i]['stopTimeStr']))

def plotInfectedActivitiesList(activitiesList):
    formatVisitTable = "{:<16} {:<16} {:<20} {:<40} {:<40}"
    print (formatVisitTable.format('vInfected.id','uInfected.id','vInfected.locationId','vInfected.startTime','vInfected.stopTime'))
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         print (formatVisitTable.format(
            activitiesList[i]['vInfected.id'],activitiesList[i]['uInfected.id'],activitiesList[i]['vInfected.locationId'],
            activitiesList[i]['vInfected.startTime'],
            activitiesList[i]['vInfected.stopTime']))

def plotInfectedUserVisitList(activitiesList):
    formatVisitTable = "{:<16} {:<16}  {:<16}  {:<16} {:<40} {:<40}"
    print('-'*(16+16+16+40+40) )
    print (formatVisitTable.format('vQuery.id', 'vInfectedId', 'vInfectedLocationId', 'uInfectedId', 'vInfectedstartTime', 'vInfectedstopTime' ))
    if activitiesList is None: return
    for i in range(len(activitiesList)):
         print (formatVisitTable.format(
            activitiesList[i]['vQuery.id'],activitiesList[i]['vInfectedId'],activitiesList[i]['vInfectedLocationId'],
            activitiesList[i]['uInfectedId'],
            activitiesList[i]['vInfectedstartTime'],
            activitiesList[i]['vInfectedstopTime']))
