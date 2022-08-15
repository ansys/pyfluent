import datamodelgen
import print_fluent_version
import settingsgen
import tuigen

if __name__ == "__main__":
    print_fluent_version.generate()
    tuigen.generate()
    datamodelgen.generate()
    settingsgen.generate()
