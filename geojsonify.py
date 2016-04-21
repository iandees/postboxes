import json
import os

for root, dirs, files in os.walk('data'):
    for name in files:
        features = []
        filepath = os.path.join(root, name)

        with open(filepath) as f:
            # check to see if the first line is already geojson-ey
            first_line = f.readline()
            if first_line == '{"type": "FeatureCollection", "features": [\n':
                print "Skipping {} because it's already geojson-ey".format(name)
                break
            f.seek(0)

            for line in f:
                line = line.rstrip(',\n')
                features.append(json.loads(line))

        features = sorted(features, key=lambda f: f['properties']['id'])

        with open(filepath, 'w') as f:
            f.write('{"type": "FeatureCollection", "features": [\n')

            for feature in features:
                f.write(json.dumps(feature) + ',\n')

            f.seek(f.tell() - 2) # Chop off the last comma and newline
            f.write('\n]}\n')

