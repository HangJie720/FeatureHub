from featurefactory.problems import commands
dataset = commands.get_sample_dataset()

import __main__
if hasattr(__main__, "__file__"):
    def example_feature(dataset):
        1+1
        return dataset["users"][["age"]].fillna(0)

    def example_feature2(dataset):
        1+2
        return dataset["users"][["age"]].fillna(0)
else:
    import sys
    import os
    import shutil
    if os.path.exists("/tmp/test"):
        shutil.rmtree("/tmp/test")
    os.mkdir("/tmp/test")
    with open("/tmp/test/example_feature.py", "w") as f:
        f.write("""\
    def example_feature(dataset):
        1+1
        return dataset["users"][["age"]].fillna(0)

    def example_feature2(dataset):
        1+2
        return dataset["users"][["age"]].fillna(0)""")
    sys.path.insert(0, "/tmp/test")
    from example_feature import example_feature
    sys.path.pop(0)

# test evaluation
print("Re-registering existing feature (should fail)...")
print("executing 'commands.evaluate(example_feature)'")
commands.evaluate(example_feature)
description="Age"
print("executing 'commands.register_feature(example_feature, description=description)'")
commands.register_feature(example_feature, description=description)
print("Re-registering existing feature (should fail)...done")

print("Registering new feature (should succeed)...")
print("executing 'commands.evaluate(example_feature2)'")
commands.evaluate(example_feature2)
description="Age"
print("executing 'commands.register_feature(example_feature2, description=description)'")
commands.register_feature(example_feature2, description=description)
print("Registering new feature (should succeed)...done")

# test feature discovery
print("executing 'commands.discover_features()'")
commands.discover_features()
print("executing 'commands.print_my_features()'")
commands.print_my_features()