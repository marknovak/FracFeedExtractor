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
Name the formatter/linter, config file locations, and the exact commands to
check/fix locally.
## Testing
Define required test types, how to run tests, expected coverage thresholds, and
when new/updated tests are mandatory.
## Pull Requests & Reviews
Outline PR requirements (template, checklist, size limits), reviewer expectations,
approval rules, and required status checks.
## CI/CD
Link to pipeline definitions, list mandatory jobs, how to view logs/re-run jobs,
and what must pass before merge/release.
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