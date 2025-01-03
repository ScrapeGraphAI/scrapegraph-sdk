# Contributing to ScrapeGraphAI

Thank you for your interest in contributing to **ScrapeGraphAI**! We welcome contributions from the community to help improve and grow the project. This document outlines the guidelines and steps for contributing.

## Table of Contents

- [Getting Started](#getting-started)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [License](#license)

## Getting Started

### Development Setup

1. Fork the repository on GitHub **(FROM pre/beta branch)**.
2. Clone your forked repository:
   ```bash
   git clone https://github.com/ScrapeGraphAI/scrapegraph-sdk.git
   cd scrapegraph-sdk/scrapegraph-py
   ```

3. Install dependencies using uv (recommended):
   ```bash
   # Install uv if you haven't already
   pip install uv

   # Install dependencies
   uv sync

   # Install pre-commit hooks
   uv run pre-commit install
   ```

4. Run tests:
   ```bash
   # Run all tests
   uv run pytest

   # Run specific test file
   uv run pytest tests/test_client.py
   ```

4. Make your changes or additions.
5. Test your changes thoroughly.
6. Commit your changes with descriptive commit messages.
7. Push your changes to your forked repository.
8. Submit a pull request to the pre/beta branch.

N.B All the pull request to the main branch will be rejected!

## Contributing Guidelines

Please adhere to the following guidelines when contributing to ScrapeGraphAI:

- Follow the code style and formatting guidelines specified in the [Code Style](#code-style) section.
- Make sure your changes are well-documented and include any necessary updates to the project's documentation and requirements if needed.
- Write clear and concise commit messages that describe the purpose of your changes and the last commit before the pull request has to follow the following format:
  - `feat: Add new feature`
  - `fix: Correct issue with existing feature`
  - `docs: Update documentation`
  - `style: Improve formatting and style`
  - `refactor: Restructure code`
  - `test: Add or update tests`
  - `perf: Improve performance`
- Be respectful and considerate towards other contributors and maintainers.

## Code Style

Please make sure to format your code accordingly before submitting a pull request.

### Python

- [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/style/)
- [Pylint style of code for the documentation](https://pylint.pycqa.org/en/1.6.0/tutorial.html)

## Submitting a Pull Request

To submit your changes for review, please follow these steps:

1. Ensure that your changes are pushed to your forked repository.
2. Go to the main repository on GitHub and navigate to the "Pull Requests" tab.
3. Click on the "New Pull Request" button.
4. Select your forked repository and the branch containing your changes.
5. Provide a descriptive title and detailed description for your pull request.
6. Reviewers will provide feedback and discuss any necessary changes.
7. Once your pull request is approved, it will be merged into the pre/beta branch.

## Reporting Issues

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository. Provide a clear and detailed description of the problem or suggestion, along with any relevant information or steps to reproduce the issue.

## License

ScrapeGraphAI is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.
By contributing to this project, you agree to license your contributions under the same license.

ScrapeGraphAI uses code from the Langchain
frameworks. You find their original licenses below.

LANGCHAIN LICENSE
https://github.com/langchain-ai/langchain/blob/master/LICENSE

Can't wait to see your contributions! :smile:
