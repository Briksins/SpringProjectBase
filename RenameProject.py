#!/usr/bin/env python
import os
import sys


conf = {}


def start():
    read_args()
    if len(conf) != 5:
        ask_project_info()
    rename_the_project()


# Example: package=com.company
def read_args():
    path_split = os.path.dirname(os.path.abspath(__file__)).split(os.sep)
    project_dir = path_split[len(path_split) - 1]
    if project_dir == "SpringProjectBase":
        print("Please Rename Project Root Folder")
        sys.exit(1)
    conf["project_name"] = project_dir
    conf["project_name_lower"] = conf["project_name"].lower()

    for arg in sys.argv[1:]:
        print("Argument: {0}".format(arg))
        try:
            if arg.startswith("package="):
                package_split = arg.split("=")[1].lower().split(".")
                if len(package_split) != 2:
                    print("Unexpected Package Name: {0}".format(arg.split("=")[1]))
                    sys.exit(1)
                else:
                    conf["package_pref"] = package_split[0]
                    conf["package_comp"] = package_split[1]
                    conf["full_pkg_name"] = conf["package_pref"] + "." + conf["package_comp"] + "." + conf["project_name_lower"]
            else:
                print("Unsupported argument: {0}, Exit...".format(arg))
                sys.exit(1)
        except Exception as e:
            print("Unable to parse argument {0}. Exception: {1}".format(arg, str(e)))
            sys.exit(1)


def ask_project_info():
    while True:
        package_split = get_user_input("Please Enter Your Package Name", "Example: com.company").lower().split(".")
        if len(package_split) != 2:
            print("Unexpected Package Name, Expected: <???>.<??????> Pattern")
        else:
            conf["package_pref"] = package_split[0]
            conf["package_comp"] = package_split[1]
            conf["full_pkg_name"] = conf["package_pref"] + "." + conf["package_comp"] + "." + conf["project_name_lower"]
            break


def get_user_input(question, example):
    user_input = None
    while user_input is None:
        try:
            print(question)
            print(example)
            user_input = input("Your Input: ")
            if len(user_input) < 3:
                user_input = None
                print("Invalid User Input, Please Try Again")
            print("")
        except Exception as e:
            print("Invalid Input! Please Try Again. Exception: {0}".format(str(e)))
    return user_input


def rename_the_project():
    print("Current Configuration:")
    for key in conf:
        print("{0} = {1}".format(key, conf[key]))
    
    rename_folders_and_files()
    fix_files_content()


def rename_folders_and_files():
    try:
        if conf["project_name"] is not "SpringProjectBase":
            os.rename("src/main/java/com/company/springprojectbase/SpringProjectBaseApplication.java",
                      "src/main/java/com/company/springprojectbase/" + conf["project_name"] + "Application.java")
            os.rename("src/main/java/com/company/springprojectbase",
                      "src/main/java/com/company/" + conf["project_name_lower"])

            os.rename("src/test/java/com/company/springprojectbase/SpringProjectBaseApplicationTests.java",
                      "src/test/java/com/company/springprojectbase/" + conf["project_name"] + "ApplicationTests.java")
            os.rename("src/test/java/com/company/springprojectbase",
                      "src/test/java/com/company/" + conf["project_name_lower"])

        if conf["package_comp"] is not "company":
            os.rename("src/main/java/com/company", "src/main/java/com/" + conf["package_comp"])
            os.rename("src/test/java/com/company", "src/test/java/com/" + conf["package_comp"])

        if conf["package_pref"] is not "com":
            os.rename("src/main/java/com", "src/main/java/" + conf["package_pref"])
            os.rename("src/test/java/com", "src/test/java/" + conf["package_pref"])
    except Exception as e:
        print("Failed to rename directories and files. Exception: {0}".format(str(e)))


def fix_files_content():
    # Docker File
    replace_in_file("deployment/build/Dockerfile", {"SpringProjectBase": conf["project_name"]})

    # Java Files
    replace_in_file("src/main/java/" + conf["full_pkg_name"].replace('.', '/') + "/" + conf["project_name"] + "Application.java",
                    {
                        "com.company.springprojectbase": conf["full_pkg_name"],
                        "SpringProjectBaseApplication": conf["project_name"] + "Application"
                    })
    replace_in_file("src/test/java/" + conf["full_pkg_name"].replace('.', '/') + "/" + conf["project_name"] + "ApplicationTests.java",
                    {
                        "com.company.springprojectbase": conf["full_pkg_name"],
                        "SpringProjectBaseApplicationTests": conf["project_name"] + "ApplicationTests"
                    })

    other_java_files = get_all_java_files(ignore="Application")
    for java_file in other_java_files:
        replace_in_file(java_file, {"com.company.springprojectbase": conf["full_pkg_name"]})

    # Gradle
    replace_in_file("settings.gradle", {"SpringProjectBase": conf["project_name_lower"]})
    replace_in_file("build.gradle", {"com.company": conf["package_pref"]+ "." + conf["package_comp"]})

    # Scripts
    replace_in_file("gradle_build.ps1", {"SpringProjectBase": conf["project_name"]})
    replace_in_file("gradle_build.sh", {"SpringProjectBase": conf["project_name"]})
    replace_in_file("clean_dockers.ps1", {"springprojectbase": conf["project_name_lower"]})
    replace_in_file("clean_dockers.sh", {"springprojectbase": conf["project_name_lower"]})


def replace_in_file(file_path, map_of_values):
    print("Replacing Content for: {0}".format(file_path))
    try:
        f = open(file_path, "r")
        file_content = f.read()
        f.close()

        for key in map_of_values:
            file_content = file_content.replace(key, map_of_values[key])

        f = open(file_path, "w")
        f.write(file_content)
        f.close()

    except Exception as e:
        print("Failed to replace content in file: {0}. Exception: {1}".format(file_path, str(e)))


def get_all_java_files(path="src", ignore=None):
    files_list = []
    items = os.listdir(path)
    for item in items:
        full_item_path = path + "/" + item
        if os.path.isdir(full_item_path):
            files_list += get_all_java_files(full_item_path, ignore)
            continue
        if item.endswith(".java"):
            if ignore and ignore not in item:
                files_list.append(full_item_path)
    return files_list


if __name__ == "__main__":
    start()
