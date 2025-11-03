# Contributing Guide
How to set up, code, test, review, and release so contributions meet our Definition
of Done.
## Code of Conduct
All contributors must follow the Oregon State University Student Code of Conduct and the team’s charter agreement.
* Treat all collaborators with respect and proffessionalism.
* Provide decent participation during meetings and reviews.
* Raise the issue privately with the team first.
* Issues of academic or ethical concern should be reported directly to the instructor.
* Report any inappropriate or unprofessional behavior to the TA, instructor or project manager.
  
**Owner**: Bradley Rule 
**Next Rewiew**:  11/26/25

## Getting Started
* ### Prerequisites
  * Python 3.10 +
  * pip installed
  * Access to GitHub repository
* ### Setup Instructions
```
    git clone https://github.com/marknovak/FracFeedExtractor.git
    cd FracFeedExtractor
    python -m venv venv
    source venv/bin/activate   
    # Windows: venv\Scripts\activate
    pip install -r requirements.txt
```
* ### Running the application
```
    python src/main.py
```
* ### Enviorment Variables
    * Sensitive information such as API keys will be stored in a local .env file which will be excluded by .gitignore.
    * Never hardcode secrets
  
**Owner**: Raymond Cen
**Next Rewiew**:  11/26/25

## Branching & Workflow
We will use the feature-branch workflow with all merges handled through PRs.
* Default branch: ```main```
* Branch naming template:
  * ```feature/short-name```
  * ```bugfix/short-name```
* Rebase your working branch with main, and often, before submitting a PR (simpler conflict resolution)
## Issues & Planning
Issue titles should start with the following tags to designate intent:
- `FEAT:` New feature request.
  - Include problem and feature description within issue description field.
  - Include note of requirement ID where applicable (ex: `Requirement ID: REQ-005`).
- `BUG:`  Bug report.
  - Include problem description.
- `DOC:`  Documentation changes.
  - Brief description of what needs to be changed or added.

Example:
```
FEAT: Example Issue

Requirement ID: REQ-XXX

Problem Desciption:
- Brief explanation of why this is important

Feature Description:
- Brief explanation of expected implementation 
```

**Owner**: Zahra Zahir Ahmed Alsulaimawi
**Next Rewiew**:  11/26/25

## Commit Messages
We will use the [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) format for clarity and traceability

```
<type>(scope): short summary [issue number if applicable]

[optional body]
[optional footer]
```
**Examples:**
```
feat(parser): implement CSV input parsing 
fix(ci): update pytest command in workflow [#42]
docs(readme): add setup section
```
**Owner**: Raymond Cen
**Next Rewiew**:  11/26/25

## Code Style, Linting & Formatting
We use Black for automatic code formatting and Flake8 for linting to maintain consistent style and prevent common Python errors.

* ### Formatter: Black
  - Config file: `pyproject.toml`
  - Install `pip install black`
  - Local usage:
  ```bash
  # Check formatting without changing files
  black --check src tests

  # Automatically reformat code
  black src tests
  ```

* ### Formatter: Black
  - Config file: `pyproject.toml`
  - Install `pip install flake8`
  - Local usage:
  ```bash
  flake8 src/ tests/
  ```
  - Configured to ignore line length violations (E501) and other minor style differences.
  - 
**Owner**: Sean Clayton
**Next Rewiew**:  11/26/25


## Testing
* ### Test framework
  - `pytest`

* ### Running tests locally
  ```bash
  # Run all tests
  pytest tests/

  # Run tests with coverage
  coverage run -m pytest tests/
  coverage report -m
  coverage html
  ```

* ### Expectations
    - New features must include unit or integration tests.
    - Coverage thresholds: aim for >80% for core modules; all critical paths must be tested.
    - Tests must pass locally before creating a PR.

## Pull Requests & Reviews
* ### PR requirements
  - Keep PRs focused and small (**<300 lines changed** if possible).
  - Include related issue references in the PR description.
  - Clearly describe what the PR changes and why.

* ### Review process
  - At least one approving review is required for non-trivial changes.
  - Reviewers check code quality, tests, CI status, and adherence to style guides.
  - Ensure all linting and formatting checks pass.

* ### Approval rules
  - CI must pass all mandatory jobs before merging.
  - PRs should be rebased on the latest `main` branch before merge if there are conflicts.
  - 
**Owner**: Sean Clayton
**Next Rewiew**:  11/26/25

## CI/CD
Continuous integration ensures all contributions meet quality standards automatically.

* ### Pipeline
  - GitHub Actions workflow: `.github/workflows/pdf_extraction_ci.yml`

* ### Mandatory jobs
  - Install dependencies
  - Code style checks: Black & Flake8
  - Unit tests & coverage
  - Functional validation: PDF extraction tests

* ### Viewing logs
  - Navigate to the **Actions** tab in GitHub.
  - Select the workflow run and expand individual jobs to see logs.

* ### Before merge
  - All jobs must complete successfully.
  - Any failing test, linter, or formatting check blocks the merge.
  - Artifacts (e.g., coverage reports) are uploaded automatically and can be reviewed.

**Owner**: Sean Clayton
**Next Rewiew**:  11/26/25

## Security & Secrets
State how to report vulnerabilities, prohibited patterns (hard-coded secrets),
dependency update policy, and scanning tools.

* Never commit sensitive credentials, tokens, or API keys.
* Secrets are stored locally in .env files and excluded via .gitignore.
* Dependencies are managed in requirements.txt.
* Use pip-audit monthly to check for vulnerabilities.
* Security issues or potential breaches should be reported privately to the Project Manager and TA.

**Owner**: Raymond Cen
**Next Rewiew**:  11/26/25

## Documentation Expectations

- `README.md`: Provides an overview of the project and its goals. It should also detail where to find information and contact individuals.
- `documentation/`: This directory will store all documentation for the program and its features including standards and usage information. 
- `Comments`: 
  - General comments should be kept short and to the point.
  - Functions should contain a docstring as the first statement within a function providing a brief explanation of the function and a quick explanation of parameters and return values.
  - Inline comments should be reserved for places where the function of code is difficult to understand or infer.

**Owner**: Zahra Zahir Ahmed Alsulaimawi
**Next Rewiew**:  11/26/25

## Release Process
### Versioning Scheme
- We follow **semantic versioning****: `MAJOR.MINOR.PATCH`
  - **MAJOR**: breaking changes
  - **MINOR**: new features, backwards-compatible
  - **PATCH**: bug fixes, minor improvements
- Example: `1.2.0` → `1.2.1` (patch), `1.3.0` (minor), `2.0.0` (major)

### Tagging
- Each release must be tagged in Git using the version number:

```bash
git tag -a v1.2.0 -m "Release v1.2.0: <short description>"
git push origin v1.2.0
```
**Owner**: Bradley Rule 
**Next Rewiew**:  11/26/25
### Changelog Generation
* For each release, include:

  * Added: new features
  * Changed: updates or improvements
  * Fixed: bug fixes

Example entry:
```
## [1.2.0] - 2025-11-10
### Added
- New feed extraction method
### Fixed
- Timeout handling in API fetch
```

### Packaging and Publishing
* Before publishing, ensure all CI/CD pipelines pass.
* Prepare the release branch or merge main into it.
* Include updated documentation and changelog.

### Rollback Process
* In case of a faulty release
  1) Revert the release tag in Git:
    ```
    git tag -d v1.2.0
    git push origin :refs/tags/v1.2.0
    ```
  2) Revert the merge commit on the main branch:
    ```
    git revert -m 1 <merge-commit-hash>
    git push origin main
    ```
  3) Update CHANGELOG to reflect the rollback.
  4) Notify the team and project partner of the rollback.

**Owner**: Bradley Rule 
**Next Rewiew**:  11/26/25
## Support & Contact
* **Primaty Communciations**: Slack and Teams
* **Meetings**: Fridays 1 PM PST
* **Project Partner**: Mark Novak, Fridays 8:30AM PST (biweekly check-ins) 
* **TA Meetings**: Thursdays 1:30PM PST

**Owner**: Zahra Zahir Ahmed Alsulaimawi
**Next Rewiew**:  11/26/25