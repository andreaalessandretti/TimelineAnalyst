def plotActivitiesList(activitiesList):
    formatVisitTable = "{:<8} {:<8} {:<10} {:<20} {:<20}"
    print (formatVisitTable.format('id','userId','locationId','startTimeStr','stopTimeStr'))
    for i in range(len(activitiesList)):
         print (formatVisitTable.format(
            activitiesList[i]['id'],activitiesList[i]['userId'], activitiesList[i]['locationId'],
            activitiesList[i]['startTimeStr'],activitiesList[i]['stopTimeStr']))
