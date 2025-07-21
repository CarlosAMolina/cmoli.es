# AWS S3 Diff

## Table of contents

- [Introduction](#introduction)
- [Example results](#example-results)
- [How to run the program. Practical example](#how-to-run-the-program.-practical-example)
  - [Requirements installation](#requirements-installation)
  - [Configuration files](#configuration-files)
    - [s3-uris-to-analyze.csv](#s3-uris-to-analyze.csv)
    - [analysis-config.json](#analysis-config.json)
  - [Run the program](#run-the-program)
- [FAQ](#faq)
- [Develop](#develop)
- [Testing](#testing)
  - [Run all tests](#run-all-tests)
  - [Run local S3 server to make requests](#run-local-s3-server-to-make-requests)
- [Resources](#resources)

## Introduction

Thanks for your interest in this project!

The purpose of the program is to compare files between AWS S3 URIs.

In a configuration file the user specifies the URIs to analyze, they can be in different AWS accounts and buckets. The program will retrieve the files information (name, date time, size and hash) and export it to a CSV file where a comparison can be made easily.

Some analysis columns can be added to the final CSV file. For example, a column that indicates if the files have the same hash in each compared URI.

Note. Despite AWS S3 uses the term `prefix` instead of `path` and `folder`, I won't use `prefix` because I think the explanation will be easier to understand.

## Example results

Example of a CSV [results file](https://github.com/CarlosAMolina/aws-s3-diff/blob/main/tests/expected-results/if-queries-with-results/analysis.csv).

Example of the CLI output if two accounts have been analyzed:

```bash
$ awsume pro

$ make run
poetry run python run.py
[INFO] Welcome to the AWS S3 Diff tool!
[DEBUG] Checking if the URIs to analyze configuration file is correct
[INFO] AWS accounts configured to be analyzed:
1. pro
2. dev
[DEBUG] Creating the directory: /home/user/Software/aws-s3-diff/s3-results/20250519224348
[INFO] Analyzing the AWS account 'pro'
[INFO] Analyzing S3 URI 1/2: s3://pets/dogs/
[INFO] Analyzing S3 URI 2/2: s3://pets/cats/
[INFO] Exporting /home/user/Software/aws-s3-diff/s3-results/20250519224348/pro.csv
[INFO] The next account to be analyzed is 'dev'. Authenticate and run the program again

$ awsume dev

$ make run
poetry run python run.py
[INFO] Welcome to the AWS S3 Diff tool!
[DEBUG] Checking if the URIs to analyze configuration file is correct
[INFO] AWS accounts configured to be analyzed:
1. pro
2. dev
[INFO] Analyzing the AWS account 'dev'
[INFO] Analyzing S3 URI 1/2: s3://pets-dev/doggies/
[INFO] Analyzing S3 URI 2/2: s3://pets-dev/kitties/
[INFO] Exporting /home/user/Software/aws-s3-diff/s3-results/20250519224348/dev.csv
[INFO] Exporting /home/user/Software/aws-s3-diff/s3-results/20250519224348/s3-files-all-accounts.csv
[INFO] Analyzing if files of the account 'pro' have the same hash as in account 'dev'
[INFO] Analyzing if files in account 'dev' can exist, compared to account 'pro'
[INFO] Exporting /home/user/Software/aws-s3-diff/s3-results/20250519224348/analysis.csv
[DEBUG] Removing: /home/user/Software/aws-s3-diff/s3-results/analysis_date_time.txt
```

## How to run the program. Practical example

### Requirements installation

The dependencies are managed with [Poetry](https://python-poetry.org/docs/), so the first step is to [install it](https://python-poetry.org/docs/#installation).

Now the dependencies can be installed running `poetry install`.

After that, we need to edit some configuration files. Once it is done, execute `make run` and follow the instructions.

### Configuration files

In order to tell the program what to analyze, two files must be updated.

These files are in the [config](https://github.com/CarlosAMolina/aws-s3-diff/tree/main/config) folder.

#### s3-uris-to-analyze.csv

The file with the AWS information to analyze [is here](https://github.com/CarlosAMolina/aws-s3-diff/blob/main/config/s3-uris-to-analyze.csv).

File structure:

- It is a `.csv` file that uses `,` as separator.
- Each column represents an AWS account configuration.
- The first row is special, is where the account names are specified. This information will be used in the CLI outputs and in the result files to organize the data.
- The other rows are the S3 URIs to be analyzed. Each row contains the URIs to compare between the AWS accounts.

The order in which the AWS accounts are specified is the order in which they will be analyzed.

Example file:

```bash
pro,relase,dev
s3://cars/europe/,s3://cars/europe/,s3://cars-dev/europe-dev
s3://pets/dogs/big-size,s3://pets/dogs/big-size,s3://pets-dev/dogs-dev/big-size-dev
```

The firs row of previous file shows that three accounts will be analyzed: pro, release and dev.

From the second row, the S3 URIs to analyze are set and there is no limit in the number of URIs to compare. In the previous example, the files of the `s3://pets/dogs/big-size` URI of the pro account will be compared against the `s3://pets/dogs/big-size` URI of the release account and the `s3://pets-dev/dogs-dev/big-size-dev` URI of the dev account, in the final results file, these URIs will be shown grouped together.

#### analysis-config.json

This file indicates what extra information will the program generate by analyzing the data obtained from S3.

File path: [here](https://github.com/CarlosAMolina/aws-s3-diff/blob/main/config/analysis-config.json).

You can configure the values of the following keys (do not modify the keys, only the values):

Key                   | Type of the value | What is it?
----------------------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------
run_analysis          | Boolean           | If the analysis should be executed.
origin                | String            | The benchmark account against which to compare other accounts.
can_the_file_exist_in | Array of strings  | If the file does not exist in the origin account, it cannot exist in the specified accounts. This is useful when checking synchronization between accounts.
is_hash_the_same_in   | Array of strings  | Checks if the files in the specified accounts have the same hash as in the origin account.

For example, if we want the release account to have the same files as the pro account, we set `"can_the_file_exist_in": ["release"]` and a `False` value will be set if a file in the release URI does not exist in the pro URI.

### Run the program

Now that the configuration files are ready, let's run the program!

The program will guide you over the required steps, but we will see a detailed execution example in order to understand them better.

Before run it, authenticate in the terminal to the first AWS account specified in the `s3-uris-to-analyze.csv` file that will be analyzed. If you don't execute the authentication command, the program won't be able to request AWS information and the program will exit with an error message. For example:

```bash
awsume pro
```

After that, execute:

```bash
make run
```

Now, we have the results for the buckets of the first account ([file example](https://github.com/CarlosAMolina/aws-s3-diff/blob/main/tests/expected-results/if-queries-with-results/pro.csv)). Let's create the second AWS account results!

We authenticate in the terminal to the second AWS account and run `make run` again. The script will detect that the first account results exist and will analyze the second account.

We repeat the previous steps per each configured AWS account:

1. Authenticate in the terminal to the AWS account to request information.
2. Execute `make run`.

The results are stored in the [s3-results](https://github.com/CarlosAMolina/aws-s3-diff/tree/main/s3-results) folder, a folder with the current analysis timestamp is created and all the accounts results are stored in that folder.

When the last account data is retrieved, the program starts the analysis phase. First, all accounts information is joined and exported to the `s3-files-all-accounts.csv` file. Then the final `analysis.csv` file is created with all results and analysis, you can open and examine that file ([example](https://github.com/CarlosAMolina/aws-s3-diff/blob/main/tests/expected-results/if-queries-with-results/analysis.csv)).

## FAQ

- How many accounts can the program work with?

Minimum two accounts. There isn't a maximum number of accounts.

- Can I compare paths for the same account?

Yes, instead of managing each `s3-uris-to-analyze.csv` column as a different account, configure them using the desired paths of the target AWS account.

You can't repeat the same AWS account name in the first line of the `s3-uris-to-analyze.csv` file. It can be solved with a prefix, for example `pro,pro-b`.

- Can I specify an URI more than once in the `s3-uris-to-analyze.csv` file in the same AWS account?

It is not possible, each URI must be unique per AWS account. The current version of the program cannot manage duplicated URIs.

For example, if you want to analyze this:

```bash
pro,relase
s3://pets/dogs/big,s3://pets/dogs
s3://pets/dogs/small,s3://pets/dogs
```

The program detects that the `s3://pets/dogs` is duplicated for the release account and will raise an exception.

You need to run the program twice two create different result folders, first run this configuration:

```bash
pro,relase
s3://pets/dogs/big,s3://pets/dogs
```

And finally run the program with this configuration:

```bash
pro,relase
s3://pets/dogs/small,s3://pets/dogs
```

- Must the URIS between accounts match?

No. For example, we can compare the `s3://pets/dogs/` URI in account 1 with the `s3://puppies` URI in account 2.

- Can the S3 URI contain folders?

No, the current version of the program cannot manage folders. The analyzed paths must contain only files, not folders.

If the S3 URI contains any folder, the program will end with an error.

- Can a S3 URI without prefix be analyzed?

No, the program currently only manages S3 URIs with bucket and prefix. For example, `s3://cars` cannot be analyzed.

- Can be empty values in the `s3-uris-to-analyze.csv` file?

No, the program will raise an exception if any account name or S3 URI is empty.

- How can I extract the S3 data of an already managed AWS account?

You have to remove the result file of that account and all the accounts that follow it. After that, authenticate to the account and run the program.

For example, if four accounts are configured and the last extracted data was from the third one, to extract the second account values again, in the results folder delete the files with S3 data of the second and third accounts.

## Develop

Run:

```bash
poetry install --all-extras
poetry run pre-commit install
```

## Testing

### Run all tests

```bash
make test
```

### Run local S3 server to make requests

Start the local server:

```bash
make start-local-s3-server
```

After that, in a new terminal you can:

- List files:

    ```bash
    make awscli-local-s3-ls
    ```

- Run the CLI:

    ```bash
    make run-using-local-s3-server
    ```

## Resources

- [GitHub code](https://github.com/CarlosAMolina/aws-s3-diff).
