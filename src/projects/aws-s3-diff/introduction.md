# AWS S3 Diff

## Table of contents

- [Introduction](#introduction)
- [How to run the program. Practical example](#how-to-run-the-program.-practical-example)
  - [Requirements installation](#requirements-installation)
  - [Configuration files](#configuration-files)
    - [s3-uris-to-analyze.csv](#s3-uris-to-analyze.csv)
    - [analysis.csv](#analysis.csv)
  - [Run the program](#run-the-program)
- [FAQ](#faq)
- [Development](#development)
- [Testing](#testing)
  - [Run all tests](#run-all-tests)
  - [Run local S3 server to make requests](#run-local-s3-server-to-make-requests)
- [Resources](#resources)

## Introduction

Thank you for reading this documentation!

The objective of this program is to compare files between AWS S3 URIs.

In a configuration file the user specifies the URIs to compare (they can be in different AWS accounts and buckets) and the program will retrieve their information (name, date time, size and hash) and export to a csv file where the user can compare them in a easy way.

Some analysis columns will be added too to the final result file. For example, a column that indicates if the files are the same in each compared URI.

Note. Despite AWS S3 uses the term `prefix` instead of `path` and `folder`, I won't use `prefix` because I think that the explanation will be easier to understand :).

## How to run the program. Practical example

### Requirements installation

The dependencies are managed with [Poetry](https://python-poetry.org/docs/), so the first step is to [install it](https://python-poetry.org/docs/#installation).

Now the dependencies can be installed running `poetry install`.

Before execute the program, the configuration files must be updated.

### Configuration files

In order to tell the program what to analyze, two files must be updated.

These files are in the `config` folder.

#### s3-uris-to-analyze.csv

The first row of this csv file specifies how to group the results. The other rows are the URIs to analyze, so the first row indicates the AWS account where the URIs are.

Each row contains the URIs to compare between the AWS accounts.

Example file:

```bash
pro,relase,dev
s3://cars/europe/,s3://cars/europe/,s3://cars-dev/europe-dev
s3://pets/dogs/big-size,s3://pets/dogs/big-size,s3://pets-dev/dogs-dev/big-size-dev
```

The firs row of previous file shows that three accounts will be analyzed: pro, release and dev.

From the second row, the S3 URIs to analyze are set; there is no limit in the number of URIs to compare. In the previous example, the files of the `s3://pets/dogs/big-size` URI in the pro account will be compared against the `s3://pets/dogs/big-size` URI of the release account and the `s3://pets-dev/dogs-dev/big-size-dev` URI of the dev account, in the final results file, these URIs will be shown grouped together.

#### analysis.csv

This file indicates what extra information will the program generate by analyzing the data obtained from S3.

The current possibilities are:

- Add a summary column that shows with a boolean if the files in each URI are the same or not.
- A new column to indicate if the file can exist in the account. For example, if we want the release account to have the same files of the pro account, a `False` value will be set if a file in the realise URI does not exist in the pro URI.

### Run the program

Now that the configuration file are ready, let's run the program!

The program will guide you over the required steps, but we will see a detailed execution example in order to understand them better.

Before run it, we need to authenticate to the first AWS account specified in the `s3-uris-to-analyze.csv.` file. If you don't execute the authentication commands, the program won't be able to request AWS information and the program will exit with an error message.

## FAQ

- How many accounts can the program work with?

Minimum two accounts. There isn't a maximum number of accounts.

- Can I compare paths in the same AWS account?

Sure, but you can't repeat the same AWS account name in the first line of the `s3-uris-to-analyze.csv` file. It can be solved with a prefix, for example `pro,pro-b`.

- Can I specify an URI more than once in the `s3-uris-to-analyze.csv` file in the same AWS account?

It is not possible, each URI must be unique per AWS account. The current version of the program cannot manage a duplicated URI.

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

- The URIS between accounts must match?

No. For example, we can compare the `s3://pets/dogs/` URI in account 1 with the `s3://puppies` URI in account 2.

- Can the S3 URI contain folders?

No, the current version of the program cannot manage folders, it only compares files.

If the S3 URI contains any folder, the program will end with an error.

- Can be empty values in the `s3-uris-to-analyze.csv` file?

No, the program will raise an exception if any account name or S3 URI is empty.

- How can I extract the S3 data of an already managed AWS account?

You have to remove the result files of that account and all the accounts that follow it. After that, authenticate to the account and run the program.

For example, if four accounts are configured and the last extracted data was of the third one, to extract the second account values again, delete the files with S3 data of the second and third accounts.

## Development

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

After that, you can:

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
