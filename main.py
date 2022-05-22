import copy
import math
import random

CITIES_INPUT_DATA_FILE = 'ch130.tsp'
CITIES_OUTPUT_DATA_FILE = 'output.tsp'

""" 
    Inicjalne ładowanie danych miast
"""
def loadCitiesData(inputFile):
    lines = []
    with open(inputFile) as file:
        next(file)
        for line in file:
            l = line.split()
            lines.append([int(l[0]), float(l[1]), float(l[2])])
    return lines

"""
    Obliczenie długości euklidesowej między dwoma miastami
    Parametry: firstCity, secondCity
    [id, x, y],
"""
def calculateDistanceBetweenTwoCities(firstCity, secondCity):
    xCity1, yCity1, xCity2, yCity2 = firstCity[1], firstCity[2], secondCity[1], secondCity[2]
    return math.sqrt(math.pow(xCity2 - xCity1, 2) + math.pow(yCity2 - yCity1, 2))

"""
    Funkcja zwracająca tablicę tablic odległości danego miasta od wszystkich pozostałych miast
    :parameter allCities array
"""
def getAllDistances(allCities):
    distances = []
    for i in range(0, len(allCities)):
        temp = []
        for j in range(0, len(allCities)):
            temp.append(calculateDistanceBetweenTwoCities(allCities[j], allCities[i]))
        distances.append(temp)
    return distances

"""
    Losowanie początkowego miasta
"""
def calculateStartingCity(cities):
    return random.randint(0, len(cities) - 1)

"""
    Zwraca indeks najbliższego miasta i odległość od tego miasta
"""
def getNearestCityFromCity(cityDistances):
    shortestDistance = min(dist for dist in cityDistances if dist > 0)
    nextCityIndex = cityDistances.index(shortestDistance)
    cityDistances[nextCityIndex] = 0  # zabezpieczenie przed powrotem do miasta już odwiedzonego
    return nextCityIndex, shortestDistance

""" Zapis wyników do pliku """
def saveResultsToFile(file, costs, visitedCitiesIndexes):
    citiesCount = len(visitedCitiesIndexes)
    with open(file, 'w') as file:
        for i in range(0, len(visitedCitiesIndexes)):
            if i < citiesCount - 1:
                file.write(f"Way: {visitedCitiesIndexes[i]} - {visitedCitiesIndexes[i + 1]}, cost: {costs[i]}\n")
            elif i == citiesCount - 1:
                file.write(f"Way: {visitedCitiesIndexes[citiesCount - 1]} - {visitedCitiesIndexes[0]}, cost: {costs[citiesCount - 1]}\n")
        file.write(f"Total cost: {sum(costs)}")

""" Implementacja algorytmu zachłannego TSP
    :returns costs array, visitedCitiesIndexes array
 """
def greedyTravellerSalesmanAlgorithm():
    """ ładowanie danych"""
    cities = loadCitiesData(CITIES_INPUT_DATA_FILE)
    distances = getAllDistances(cities)
    [print(distance) for distance in distances]
    """ losowanie miasta startowego """
    startingCityIndex = calculateStartingCity(cities)
    print(f"\nStarting from city with index: {startingCityIndex}, {distances[startingCityIndex]}")

    """ Inicializacja """
    visitedCitiesIndexes = [startingCityIndex]
    costs = []
    unvisitedCities = []
    [unvisitedCities.append(i) for i in range(0, len(cities))]
    unvisitedCities.remove(startingCityIndex)

    """ obliczanie najlepszej drogi """
    lastVisitedCityIndex = startingCityIndex
    while len(unvisitedCities) > 0:
        nextCityToVisit, visitCost = getRandomCityFromNearestNCities(distances[lastVisitedCityIndex])
        if nextCityToVisit not in visitedCitiesIndexes:
            visitedCitiesIndexes.append(nextCityToVisit)
            unvisitedCities.remove(nextCityToVisit)
            lastVisitedCityIndex = nextCityToVisit
            costs.append(visitCost)
            print(f"next city index : {nextCityToVisit}, cost: {visitCost}, visitedCities: {visitedCitiesIndexes}, unvisitedCities: {unvisitedCities}")
    costs.append(distances[lastVisitedCityIndex][startingCityIndex])
    return costs, visitedCitiesIndexes

""" TODO
    Losuje najbliższe miasto spośrod n miast najbliżych miastu
    :parameter cityDistances - tablica odległości od miasta
    :parameter n = 5
"""
def getRandomCityFromNearestNCities(cityDistances, n=5):
    distancesToCalc = []
    copiedDistances = list(copy.deepcopy(cityDistances))
    for i in range(0, n):
        shortestDistance = min(dist for dist in copiedDistances if dist > 0)
        distancesToCalc.append(shortestDistance)
        copiedDistances.remove(shortestDistance)
    randomCityIdx = random.randint(0, n - 1)
    randomDistance = distancesToCalc[randomCityIdx]
    print(f"randomCityIdx: {randomCityIdx}, randomDistance: {randomDistance}")
    nextCityIndex = cityDistances.index(randomDistance)
    cityDistances[nextCityIndex] = 0  # zabezpieczenie przed powrotem do miasta już odwiedzonego
    return nextCityIndex, shortestDistance

if __name__ == "__main__":
    costs, visitedCitiesIndexes = greedyTravellerSalesmanAlgorithm()
    print("************** Result **************")
    saveResultsToFile(CITIES_OUTPUT_DATA_FILE, costs, visitedCitiesIndexes)
    print(f"Results saved in file '{CITIES_OUTPUT_DATA_FILE}'")
