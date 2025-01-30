# Contributing to FHIR2SQL

Thank you for your interest in contributing to **FHIR2SQL**! Contributions are welcomed and appreciated. This document outlines the basic process for contributing, from reporting bugs to submitting pull requests.

---

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Workflow](#development-workflow)
- [Coding and Style Guidelines](#coding-and-style-guidelines)
- [License](#license)

---

## Code of Conduct
Please review our [Code of Conduct](CODE_OF_CONDUCT.md) (if present) before contributing. We expect all contributors to abide by the standards set out there to help maintain a welcoming, respectful community.

---

## How Can I Contribute?

### Reporting Bugs
1. Search [existing issues](../../issues) to see if the problem has already been reported.  
2. If not, open a new issue. Provide:
   - **Description** of the bug
   - **Steps to Reproduce**
   - **Expected vs. Actual Behavior**
   - Any **error messages** or **logs** (redacted of sensitive info)

### Suggesting Enhancements
1. Check [existing issues](../../issues) to see if someone else has made a similar request.  
2. Open a new **Feature Request** issue. Include:
   - A **clear description** of the feature
   - **Use cases** or examples
   - Potential **benefits** or **impacts** to current workflow

### Pull Requests
1. **Fork** the repository.  
2. **Create** a new branch from `main` (e.g., `feature/my-cool-feature`).  
3. Write your code, docs, or fixes.  
4. **Commit** and push your changes to your branch.  
5. **Open** a pull request (PR) against `main`. Fill in the PR template if provided.  
6. One or more maintainers will review your PR. Please address any feedback or requested changes.

---

## Development Workflow
If you’re making larger changes or new features:

1. **Discuss** with maintainers:  
   - Open an issue or add a comment to an existing issue.  
   - Outline your approach or a proof-of-concept.

2. **Set Up** a local environment:  
   - Clone your fork.  
   - Install dependencies (e.g., `pip install -r requirements.txt`).  
   - Copy `.env.example` to `.env` and configure as needed.

3. **Implement** your changes:  
   - Use a topic branch (not `main`) to keep changes organized.  
   - Write or update tests if applicable.  
   - Ensure no sensitive data is committed (API keys, PHI, etc.).

4. **Run Tests** and lint checks:  
   - E.g., `pytest` for Python or whichever test command is used.  
   - Address any failing tests or lint warnings.

5. **Submit a Pull Request**:  
   - Indicate what the change does.  
   - Reference any relevant issues (e.g., “Closes #123”).

---

## Coding and Style Guidelines
1. **Python Version**: Typically Python 3.