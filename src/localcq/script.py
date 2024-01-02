import shutil
import os
import argparse

quality_report_folder = "cq-report"


def run_command(command):
    os.system(command)


def move_files(source, destination):
    os.makedirs(destination, exist_ok=True)
    if os.path.exists(source):
        os.rename(source, os.path.join(destination, source))
        print(f"{source} moved to {destination}")


def main():
    package_directory = os.path.dirname(
        __file__
    )  # Get the directory of the current script
    index_path = os.path.join(package_directory, "templates", "index.html")

    parser = argparse.ArgumentParser(
        description="Generate reports for a Python project."
    )
    parser.add_argument("--source", help="Path to the source directory", required=True)
    parser.add_argument("--tests", help="Path to the tests directory", required=True)
    args = parser.parse_args()

    src_directory = args.source
    tests_directory = args.tests

    # Run pytest with specified arguments
    pytest_args = [
        "--junitxml=reports/junit/junit.xml",
        "--html=reports/junit/report.html",
        f"--cov={src_directory}",
        "--cov-report=html:reports/coverage/htmlcov",
        "--cov-report=xml:reports/coverage/coverage.xml",
        f"{tests_directory}",
    ]
    run_command(f"pytest {' '.join(pytest_args)}")

    run_command("genbadge coverage")
    run_command("genbadge tests")

    # Run Flake8 with specified arguments

    for folder, name in [
        (src_directory, "source"),
        (tests_directory, "tests"),
    ]:
        os.makedirs(f"reports/flake8/{name}", exist_ok=True)

        flake8_args = [
            "--exit-zero",
            "--statistics",
            f"--format=html --htmldir=reports/flake8/{name}/",
            "--tee --output-file=flake8stats.txt",
            f"{folder}",
        ]
        run_command(f"flake8 {' '.join(flake8_args)}")

        # Generate badges using genbadge
        run_command("genbadge flake8 -i - < flake8stats.txt")

        # Move flake8stats.txt to reports/flake8
        assert "flake8stats.txt" in os.listdir()

        shutil.move("flake8stats.txt", f"reports/flake8/{name}/")
        os.rename("flake8-badge.svg", f"flake8-badge-{name}.svg")

    # Move badges and reports to designated directories
    if not os.path.exists(quality_report_folder):
        os.makedirs(quality_report_folder)

    badges_to_move = [
        "coverage-badge.svg",
        "tests-badge.svg",
        "flake8-badge-source.svg",
        "flake8-badge-tests.svg",
    ]
    for badge in badges_to_move:
        if os.path.exists(badge):
            os.rename(badge, os.path.join(quality_report_folder, badge))
            print(f"{badge} moved to {quality_report_folder}")

    if os.path.exists(quality_report_folder + "/reports"):
        os.system(f"rm -rf {quality_report_folder}/reports")

    shutil.copy(index_path, quality_report_folder)

    os.rename("reports", quality_report_folder + "/reports")
    print(f"reports folder moved to {quality_report_folder}")

    # Add a .gitingore file to the quality_report_folder

    with open(f"{quality_report_folder}/.gitignore", "w") as f:
        f.write("*")

    import webbrowser
    webbrowser.open_new_tab(f"{quality_report_folder}/index.html")


if __name__ == "__main__":
    main()
