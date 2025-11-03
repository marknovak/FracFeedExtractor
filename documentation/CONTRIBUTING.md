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
  
## Branching & Workflow
We will use the feature-branch workflow with all merges handled through PRs.
* Default branch: ```main```
* Branch naming template:
  * ```feature/short-name```
  * ```bugfix/short-name```
* Rebase your working branch with main, and often, before submitting a PR (simpler conflict resolution)
## Issues & Planning
Explain how to file issues, required templates/labels, estimation, and
triage/assignment practices.
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
  
## Security & Secrets
State how to report vulnerabilities, prohibited patterns (hard-coded secrets),
dependency update policy, and scanning tools.
## Documentation Expectations
Specify what must be updated (README, docs/, API refs, CHANGELOG) and
docstring/comment standards.
## Release Process
Describe versioning scheme, tagging, changelog generation, packaging/publishing
steps, and rollback process.
## Support & Contact
Provide maintainer contact channel, expected response windows, and where to ask
questions.