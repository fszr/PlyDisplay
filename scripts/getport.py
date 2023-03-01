# %%
import os
import sys
import json
import subprocess

VCPKG_ROOT_DEFAULT = "D:/Dev/vcpkg"
THIRD_PARTY_CONFIG_FILE = "thirdparty.json"
BRANCH_NAME = "pcl"
VCPKG_JSON_FILE = "../vcpkg.json"
PROJECT_BASELINE_FILE = "baseline.json"


def printRed(content): print("\033[91m {}\033[00m" .format(content))
def printRed(content): print("\033[91m {}\033[00m" .format(content))
def printGreen(content): print("\033[92m {}\033[00m" .format(content))
def printYellow(content): print("\033[93m {}\033[00m" .format(content))
def printLightPurple(content): print("\033[94m {}\033[00m" .format(content))
def printPurple(content): print("\033[95m {}\033[00m" .format(content))
def printCyan(content): print("\033[96m {}\033[00m" .format(content))
def printLightGray(content): print("\033[97m {}\033[00m" .format(content))
def printBlack(content): print("\033[98m {}\033[00m" .format(content))


class Vcpkg_json_class(object):
    def __init__(self, name, versionsemver, dependencies, builtinbaseline, overrides):
        self.name = name
        self.versionsemver = versionsemver
        self.dependencies = dependencies
        self.builtinbaseline = builtinbaseline
        self.overrides = overrides

    def obj_json(self, obj_instance):
        return {
            'name': obj_instance.name,
            'version-semver': obj_instance.versionsemver,
            'dependencies': obj_instance.dependencies,
            'builtin-baseline': obj_instance.builtinbaseline,
            'overrides': obj_instance.overrides
        }


class vcpkg_checkout():
    def __init__(self, _vcpkgroot):
        self.vcpkgroot = _vcpkgroot

    def __enter__(self):
        output = subprocess.run(['git', 'checkout', '-b', BRANCH_NAME],
                                capture_output=True, encoding='utf-8', cwd=self.vcpkgroot)
        if 0 != output.returncode:
            output = subprocess.run(['git', 'checkout', BRANCH_NAME],
                                    capture_output=True, encoding='utf-8', cwd=self.vcpkgroot)

    def __exit__(self, exc_type, exc_val, exc_tb):
        output = subprocess.run(['git', 'checkout', 'master'],
                                capture_output=True, encoding='utf-8', cwd=self.vcpkgroot)


def get_vcpkg_root(argv):
    vcpkgroot = ""
    # try to read vcpkgroot from sys_argv
    if len(argv) > 1:
        vcpkgroot = sys.argv[len(argv)-1]
        if vcpkgroot and os.path.exists(vcpkgroot):
            print("read VCPKG_ROOT from argv, set VCPKG_ROOT: \'{}\'".format(vcpkgroot))
        else:
            vcpkgroot = ""

    # try to read vcpkgroot from environment variable
    if not vcpkgroot:
        vcpkgroot = os.getenv('VCPKG_ROOT')
        if vcpkgroot:
            if os.path.exists(vcpkgroot):
                print("read VCPKG_ROOT from environment variable, set VCPKG_ROOT: \'{}\'".format(
                    vcpkgroot))
            else:
                printYellow("read VCPKG_ROOT from environment variable but \'{}\' is not a directory".format(
                    vcpkgroot), file=sys.stderr)
                vcpkgroot = ""

    # no vcpkgroot specify, set default value, you can config VCPKG_ROOT_DEFAULT
    if not vcpkgroot:
        vcpkgroot = VCPKG_ROOT_DEFAULT
        if vcpkgroot and os.path.exists(vcpkgroot):
            print("set VCPKG_ROOT from default, VCPKG_ROOT = {}".format(vcpkgroot))
        else:
            printRed("Error: no available VCPKG_ROOT, exit.")
    return vcpkgroot


def main(argv):
    # first, get vcpkg_root
    vcpkgroot = get_vcpkg_root(argv)
    if not vcpkgroot:
        return

    vcpkgroot = vcpkgroot.replace('\\', '/')
    vcpkg_baseline_file = "{}/versions/baseline.json".format(vcpkgroot)
    print(vcpkg_baseline_file)
    with vcpkg_checkout(vcpkgroot):
        with open(THIRD_PARTY_CONFIG_FILE) as f:
            thirdparty_config = json.load(f)
        if not thirdparty_config:
            printRed("failed to open thirdparty.json, exit", file=sys.stderr)
            return

        with open(vcpkg_baseline_file, 'r') as f:
            vcpkg_baseline = json.load(f)
        if not vcpkg_baseline:
            printRed("failed to open \'{}\'".format(
                vcpkg_baseline_file), file=sys.stderr)
            return

        with open(PROJECT_BASELINE_FILE, 'r') as f:
            project_baseline = json.load(f)
        if not project_baseline:
            printRed("failed to open \'{}\'".format(
                PROJECT_BASELINE_FILE), file=sys.stderr)
            return

        for i in vcpkg_baseline['default']:
            if i not in project_baseline['default']:
                project_baseline['default'][i] = vcpkg_baseline['default'][i]

        modify_count = 0
        denp_list = []
        overrides_list = []
        for i in thirdparty_config.keys():
            if i in project_baseline['default']:
                print(i+":\tori:"+project_baseline['default'][i]
                      ['baseline']+"\tneed:"+thirdparty_config[i]['baseline'])
                if project_baseline['default'][i]['baseline'] != thirdparty_config[i]['baseline'] or project_baseline['default'][i]['port-version'] != thirdparty_config[i]['port-version']:
                    modify_count += 1
                    project_baseline['default'][i]['baseline'] = thirdparty_config[i]['baseline']
                    project_baseline['default'][i]['port-version'] = thirdparty_config[i]['port-version']
                denp = {"name": i,
                        "version>=": project_baseline['default'][i]['baseline']}
                if "features" in thirdparty_config[i].keys() and thirdparty_config[i]['features']:
                    features_item = {
                        "features": thirdparty_config[i]["features"]}
                    denp.update(features_item)
                denp_list.append(denp)
                overrides = {"name": i, "version-string": project_baseline['default'][i]
                             ['baseline'], "port-version": project_baseline['default'][i]['port-version']}
                overrides_list.append(overrides)
            else:
                print("waring: could not find \'{}\' in vcpkg_baseline.json".format(i))

        print("modify_count = {}".format(modify_count))

        with open(vcpkg_baseline_file, 'w') as f:
            json.dump(project_baseline, f, sort_keys=True,
                      indent=4, separators=(',', ':'))

        with open(PROJECT_BASELINE_FILE, 'w') as f:
            json.dump(project_baseline, f, sort_keys=True,
                      indent=4, separators=(',', ':'))
        print("baseline.json dump done")
        output = subprocess.run(['git', 'add', vcpkg_baseline_file],
                                capture_output=True, encoding='utf-8', cwd=vcpkgroot)
        output = subprocess.run(['git', 'commit', '-m', "modify dependency version"],
                                capture_output=True, encoding='utf-8', cwd=vcpkgroot)

        output = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                capture_output=True, encoding='utf-8', cwd=vcpkgroot)
        current_baseline = output.stdout.strip()
        my_cpkg_json_class = Vcpkg_json_class(
            'pcl-dependency', '1.0.0', denp_list, current_baseline, overrides_list)
        with open(VCPKG_JSON_FILE, 'w', encoding='utf8') as f:
            json.dump(my_cpkg_json_class, f, sort_keys=True, indent=4,
                      separators=(',', ':'), default=my_cpkg_json_class.obj_json)
            print("vcpkg.json dump done")


if __name__ == "__main__":
    main(sys.argv)
