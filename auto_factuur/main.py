import os


TEST_DIRECTORY = "../test_dir/"


def main():
    if not os.path.exists(TEST_DIRECTORY):
        os.makedirs(TEST_DIRECTORY)

    os.chdir(TEST_DIRECTORY)


if __name__ == "__main__":
    main()
