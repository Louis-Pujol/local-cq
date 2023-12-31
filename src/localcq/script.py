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
    package_directory = os.path.dirname(__file__)  # Get the directory of the current script
    index_path = os.path.join(package_directory, "templates", "index.html")

    parser = argparse.ArgumentParser(description='Generate reports for a Python project.')
    parser.add_argument('--source', help='Path to the source directory', required=True)
    parser.add_argument('--tests', help='Path to the tests directory', required=True)
    args = parser.parse_args()

    src_directory = args.source
    tests_directory = args.tests

    # Run pytest with specified arguments
    pytest_args = [
        f"--junitxml=reports/junit/junit.xml",
        f"--html=reports/junit/report.html",
        f"--cov={src_directory}",
        f"{tests_directory}"
    ]
    run_command(f"pytest {' '.join(pytest_args)}")

    # Generate coverage report
    run_command("coverage report")
    run_command("coverage xml")
    run_command("coverage html")

    print(os.listdir("."))

    # Move coverage files to designated directory
    os.makedirs("reports/coverage", exist_ok=True)
    os.rename("coverage.xml", "reports/coverage/coverage.xml")
    if os.path.exists("reports/coverage/htmlcov"):
        shutil.rmtree("reports/coverage/htmlcov")
    os.rename("htmlcov", "reports/coverage/htmlcov")
    run_command("rm -f reports/coverage/htmlcov/.gitignore")

    # Run Flake8 with specified arguments
    run_command(f"flake8 {src_directory} --exit-zero --statistics --format=html --htmldir ./reports/flake8 --tee --output-file flake8stats.txt")

    # Generate badges using genbadge
    run_command("genbadge coverage")
    run_command("genbadge tests")
    run_command("genbadge flake8 -i - < flake8stats.txt")

    # Move flake8stats.txt to reports/flake8
    os.rename("flake8stats.txt", "reports/flake8/flake8stats.txt")

    # Move badges and reports to designated directories
    if not os.path.exists(quality_report_folder):
        os.makedirs(quality_report_folder)

    badges_to_move = ["coverage-badge.svg", "tests-badge.svg", "flake8-badge.svg"]
    for badge in badges_to_move:
        if os.path.exists(badge):
            os.rename(badge, os.path.join(quality_report_folder, badge))
            print(f"{badge} moved to {quality_report_folder}")

    if os.path.exists(quality_report_folder + "/reports"):
        os.system(f"rm -rf {quality_report_folder}/reports")

    shutil.copy(index_path, quality_report_folder)

    os.rename("reports", quality_report_folder + "/reports")
    print(f"reports folder moved to {quality_report_folder}")

if __name__ == "__main__":
    main()
