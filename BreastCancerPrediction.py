# Varun Thakkar
# Breast Cancer Prediction

# imports
import csv
import math
import statistics
import plotly.express as px


data = []
first = True
# opens dataset
with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        if first:
            first = False
        else:
            new_row = row[0].split(",")
            # creates row with classification, radius mean, smoothness value, and concavity value
            data.append([new_row[1], float(new_row[2]) / 100, float(new_row[6]), float(new_row[8])])

classifications = []
radii = []
smoothnesses = []
concavities = []
# adds all data to separate list for plotting purposes
for row in data:
    classifications.append(row[0])
    radii.append(row[1])
    smoothnesses.append(row[2])
    concavities.append(row[3])

# returns distance between two 3 dimensional points
def get_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

# returns all distances from each data value to specified point
def get_distances(data, point):
    # creates dictionary with two key-value pairs where values are lists
    distances = {}
    distances['classes'] = []
    distances['distances'] = []

    # assigns distances to each point with correct diagnosis
    for d in data:
        distances['classes'].append(d[0])
        distances['distances'].append(get_distance(d[1], d[2], d[3], point[0], point[1], point[2]))

    # returns distance dictionary
    return distances

# returns list of indexes of k nearest neighbors
def get_nearest_indexes(distances, k):
    indexes = []

    # makes new list of all distances
    new_distances = []
    for d in distances['distances']:
        new_distances.append(d)

    # while loop finds index of point with smallest distance k times
    while k > 0:
        index_of_min = new_distances.index(min(new_distances))
        indexes.append(index_of_min)
        # assigns arbitrary number to minimum indexes so indexes are not repeated
        new_distances[index_of_min] = 100
        k = k - 1

    return indexes

# predicts diagnosis of point based on nearest neighbors
def classify_point(distances, indexes):
    total = 0

    # goes through each nearest neighbor
    for index in indexes:
        # weights each neighbor based on diagnosis
        # closer points are weighted higher than others
        if distances['classes'][index] == 'B':
            total = total + (distances['distances'][index])
        elif distances['classes'][index] == 'M':
            total = total - (distances['distances'][index])

    # assess weights and make prediction
    if total > 0:
        return 'B'
    elif total < 0:
        return 'M'
    else:
        return 'Inconclusive'

# finds accuracy of predictions of all data values with k neighbors
def find_accuracy(data, k):
    index = 0
    total_correct = 0

    # for loop goes through each point
    for row in data:

        # data is prepared so evaluated point is not included in data
        new_data = []
        for row in data:
            new_data.append(row)
        new_row = new_data[index]
        classification = new_row[0]
        new_row = new_row[1:]
        new_data.pop(index)

        # makes prediction of point using k nearest neighbors
        distances = get_distances(new_data, new_row)
        indexes = get_nearest_indexes(distances, k)
        prediction = classify_point(distances, indexes)

        # checks accuracy
        # if correct, accumulate total correct and total
        if classification == prediction:
            total_correct = total_correct + 1
            index = index + 1
        # otherwise accumulate total
        else:
            index = index + 1

    # return accuracy
    return total_correct / index

# finds optimal k value for k nearest neighbors
def optimize_neighbors(data):
    accuracies = {}
    test_k = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # finds accuracy for all test values
    for k in test_k:
        accuracies[k] = find_accuracy(data, k)

    # finds highest accuracy k value
    highest = 0
    optimal = 0
    for k, acc in accuracies.items():
        if acc > highest:
            highest = acc
            optimal = k

    # returns optimal k value
    return optimal

# stores optimized k value
optimized_k = optimize_neighbors(data)
print("The optimized number of nearest neigbors is", optimized_k)

# user enters in all three parameters
radius = input("Please enter the average radius of the tumor (radius mean): ")
smoothness = input("Please enter the local variation in the radius lengths (smoothness): ")
concavity = input("Please enter the mean of the severity of concave portions of the contour (concavity): ")

# using k-NN algorithm, makes diagnosis prediction
point = [float(radius) / 100, float(smoothness), float(concavity)]
distances = get_distances(data, point)
indexes = get_nearest_indexes(distances, optimized_k)
classification = classify_point(distances, indexes)

# prints statement to summarize results
if classification == 'B':
    print("Tumor is predicted to be begign.")
elif classification == 'M':
    print("Tumor is predicted to be malignant")
else:
    print(classification)

# plots all values including user point
radii.append(point[0])
smoothnesses.append(point[1])
concavities.append(point[2])
classifications.append("Your point")

# reclassifies nearest neighbors for better visualization
for index in indexes:
    if distances['classes'][index] == 'M':
        classifications[index] = 'Malignant Neighbor'
    else:
        classifications[index] = 'Begign Neighbor'

labels = {"x": "Radius", "y": "Smoothness", "z": "Concavity", "color": "Classification"}
figure = px.scatter_3d(x=radii, y=smoothnesses, z=concavities, color=classifications, labels=labels, text=classifications)
figure.show()
