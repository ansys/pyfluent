import datamodelgen
import print_fluent_version
import settingsgen
import tuigen

if __name__ == "__main__":
    print_fluent_version.generate()
    for mod in (tuigen, datamodelgen, settingsgen):
        try:
            mod.generate()
        except BaseException as ex:
            print("skipping generation of", str(mod), str(ex))
