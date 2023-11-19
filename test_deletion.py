# Script to delete events from the raw data in order to test the update script
import pandas as pd
import colors as c

fightInformation = pd.read_csv('Raw Data/fightInformation.csv')
fightRounds = pd.read_csv('Raw Data/fightRounds.csv')
fightTotals = pd.read_csv('Raw Data/fightTotals.csv')

def deleteEvents(events):
    if type(events) == str:
        events = [events]
    print(c.Color.RED + 'Deleting ' + str(len(events)) +' events: ' + str(events) + c.Color.RESET)
    print()
    print(c.Color.LIGHT_BLUE + 'Before:' + c.Color.RESET)
    fightInformationShape = fightInformation.shape
    fightRoundsShape = fightRounds.shape
    fightTotalsShape = fightTotals.shape
    print(fightInformationShape)
    print(fightRoundsShape)
    print(fightTotalsShape)
    for event in events:
        fightInformation.drop(fightInformation[fightInformation['Event'] == event].index, inplace = True)
        fightRounds.drop(fightRounds[fightRounds['Event'] == event].index, inplace = True)
        fightTotals.drop(fightTotals[fightTotals['Event'] == event].index, inplace = True)
    print()
    print(c.Color.LIGHT_BLUE + 'After:' + c.Color.RESET)
    print(fightInformation.shape)
    print(fightRounds.shape)
    print(fightTotals.shape)
    print()

    print(c.Color.CYAN + 'Deleted rows:' + c.Color.RESET)
    print('fightInformation: ' + format(fightInformationShape[0] - fightInformation.shape[0], ',d'))
    print('fightRounds: ' + format(fightRoundsShape[0] - fightRounds.shape[0], ',d'))
    print('fightTotals: ' + format(fightTotalsShape[0] - fightTotals.shape[0], ',d'))
    print()

    fightInformation.to_csv('Raw Data/fightInformation.csv', index = False)
    fightRounds.to_csv('Raw Data/fightRounds.csv', index = False)
    fightTotals.to_csv('Raw Data/fightTotals.csv', index = False)
    print(c.Color.GREEN + 'Data saved.' + c.Color.RESET)

eventsToRemove = ['UFC Fight Night: Allen vs. Craig']
deleteEvents(eventsToRemove)