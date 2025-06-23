# 🤝 Contributing to DeepRecon

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Improving The Documentation](#improving-the-documentation)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. By participating, you are expected to uphold this standard.

## I Have a Question

Before asking a question, it's best to search for existing [Issues](https://github.com/DeepPythonist/DeepRecon/issues) that might help you. If you have found a suitable issue and still need clarification, you can write your question in this issue.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/DeepPythonist/DeepRecon/issues/new)
- Provide as much context as you can about what you're running into
- Provide project and platform versions (Python, OS, etc.)

## I Want To Contribute

### Reporting Bugs

#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible:

- Make sure you are using the latest version
- Determine if your bug is really a bug and not an error on your side
- Check if other users have experienced the same issue
- Collect information about the bug

#### How Do I Submit a Good Bug Report?

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/DeepPythonist/DeepRecon/issues/new)
- Use our bug report template
- Explain the behavior you would expect and the actual behavior
- Please provide as much context as possible

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for DeepRecon, **including completely new features and minor improvements to existing functionality**.

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/DeepPythonist/DeepRecon/issues).

- Use our feature request template
- Use a **clear and descriptive title**
- Provide a **step-by-step description** of the suggested enhancement
- **Describe the current behavior** and **explain the behavior you expected**
- **Explain why this enhancement would be useful**

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Setting up the development environment

1. **Fork the repository**
   
   Click the "Fork" button at the top right of the repository page.

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/DeepRecon.git
   cd DeepRecon
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

5. **Install development dependencies**
   ```bash
   pip install pytest pytest-cov flake8 black isort
   ```

6. **Create a branch for your work**
   ```bash
   git checkout -b feature/amazing-feature
   ```

## Coding Guidelines

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 88 characters (Black default)

### Code Quality

- Write clear, readable code with meaningful variable names
- Add docstrings to all public functions and classes
- Include type hints where appropriate
- Handle errors gracefully
- No hardcoded values - use configuration

### Testing

- Write tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)

```python
def test_get_ip_valid_domain():
    # Arrange
    domain = "example.com"
    
    # Act
    result = get_ip(domain)
    
    # Assert
    assert result is not None
    assert isinstance(result, str)
```

### Documentation

- Update docstrings for any changed functions
- Update README.md if adding new features
- Add examples for new functionality
- Keep documentation clear and concise

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(dns): add support for AAAA records
fix(ssl): handle timeout errors gracefully
docs(readme): add installation instructions
test(resolve): add tests for invalid domains
```

## Pull Request Process

1. **Create a Pull Request**
   - Use a clear and descriptive title
   - Fill out the PR template completely
   - Link any related issues

2. **Code Review**
   - Address all review comments
   - Make sure CI passes
   - Keep the PR focused on a single feature/fix

3. **Before Merging**
   - Ensure all tests pass
   - Code coverage doesn't decrease
   - Documentation is updated
   - CHANGELOG.md is updated

### Pull Request Template

When creating a PR, include:

- **What**: Brief description of changes
- **Why**: Motivation and context
- **How**: Technical details if complex
- **Testing**: How you tested the changes
- **Checklist**: Use our PR checklist

## Questions?

Don't hesitate to ask questions if anything is unclear. You can:

- Open an issue for discussion
- Email the maintainer: mrasolesfandiari@gmail.com

Thank you for contributing to DeepRecon! 🚀 