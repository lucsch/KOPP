#!/usr/bin/python

import argparse
import fileinput
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kopp.createversion import GitVersion

ACTIVE_PLATEFORM = ["Windows", "Linux", "OSX"]
ICON_BASE_NAME = "kopp_icon"

class CreateApp(object):
    def __init__(self, plateform="OSX"):
        if (plateform not in ACTIVE_PLATEFORM):
            raise ValueError(f"plateform must be one of {ACTIVE_PLATEFORM!r}.")

        self.basepath = os.path.join(os.path.dirname(__file__), "..")
        self.binpath = os.path.join(self.basepath, "bin")
        self.plateform = plateform
        self.iconfile = os.path.join(self.basepath, "art", self._get_icon())

    def _get_icon(self):
        """return the icon based on the plateform"""
        icon = f"{ICON_BASE_NAME}.icns"
        if self.plateform == ACTIVE_PLATEFORM[0]:  # Windows
            icon = f"{ICON_BASE_NAME}.ico"
        elif self.plateform == ACTIVE_PLATEFORM[1]:  # Linux
            icon = f"{ICON_BASE_NAME}.png"
        return icon

    def update_git_version(self):
        my_version = GitVersion()
        my_version.write_to_file(os.path.join(self.basepath, "kopp", "version.py"))
        self.m_commit_number = my_version.m_commit_number
        return True

    def modify_spec_file(self):
        """modifiy the spec file before building"""
        if self.plateform == ACTIVE_PLATEFORM[2]:  # OSX
            for line in fileinput.input(os.path.join(self.binpath, "kopp_{}.spec".format(self.m_commit_number)), inplace=1):
                if "bundle_identifier=None)" in line:
                    print("             bundle_identifier=None,")
                    print("             info_plist={")
                    print("                 'CFBundleShortVersionString': '1.1.{}',".format(self.m_commit_number))
                    print("                 'NSHumanReadableCopyright': '(c) 2026, Lucien SCHREIBER',")
                    print("                 'NSHighResolutionCapable': 'True'")
                    print("             })")
                else:
                    print(line[:-1])

    def create_exe(self):
        """run pyInstaller to create the exe"""
        if not os.path.exists(self.binpath):
            os.makedirs(self.binpath)

        # icon = os.path.join(self.basepath, "art", "pro.png")
        data_source = os.path.join(self.basepath, "kopp", "templates")
        data_dest = os.pathsep + "templates"
        mode = "--onefile"
        if self.plateform == ACTIVE_PLATEFORM[2]: ## OSX
            mode = "--onedir"
        command = [
            "pyi-makespec",
            mode,
            "--windowed",
            "--hidden-import=wx",
            "--hidden-import=pkg_resources.py2_warn",
            "-nkopp_{}".format(self.m_commit_number),
            "--icon={}".format(self.iconfile),
            f"--add-data={data_source}{data_dest}",
            os.path.join(self.basepath, "kopp", "__main__.py")]
        print(command)
        try:
            p = subprocess.Popen(command, cwd=self.binpath)
            p.wait()
        except subprocess.SubprocessError as e:
            print(f"Error running command: {' '.join(command)}")
            print(f"Error details: {e}")
            return False
        except FileNotFoundError as e:
            print(f"Command not found: {command[0]}")
            print(f"Error details: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error running command: {' '.join(command)}")
            print(f"Error details: {e}")
            return False

        self.modify_spec_file()

        # run pyinstaller with fipro.spec
        try:
            p = subprocess.Popen(
                ["pyinstaller", "kopp_{}.spec".format(self.m_commit_number), "-y"], cwd=self.binpath)
            p.wait()
        except subprocess.SubprocessError as e:
            print(f"Error running pyinstaller: {e}")
            return False
        except FileNotFoundError as e:
            print("PyInstaller not found. Please ensure it is installed and in your PATH.")
            print(f"Error details: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error running pyinstaller kopp_{self.m_commit_number}.spec")
            print(f"Error details: {e}")
            return False

##########################################################
# Main function, parse command line arguments
##########################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'plateform', help="choose a plateform. Supported values are : " + ", ".join(ACTIVE_PLATEFORM))
    args = parser.parse_args()

    myApp = CreateApp(plateform=args.plateform)
    myApp.update_git_version()
    myApp.create_exe()
