import matplotlib.pyplot as plt

classes_count = {}

with open('questions_test.txt', 'r') as train_file:
    lines = train_file.readlines()

    for line in lines:
        line_class = line.split(':')[0].encode('utf-8').decode('utf-8-sig')
        if line_class not in classes_count:
            classes_count[line_class] = 1
        else:
            classes_count[line_class] += 1

keys = list(classes_count.keys())


bars = range(len(keys))
bars_labels = keys
counts = [classes_count[key] for key in keys]

plt.bar(bars, counts, 0.2, align='center')
plt.xticks(bars, bars_labels)

plt.show()
