---
phase: quick-260430-okr
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .venv/
  - .gitignore
  - README.md
autonomous: true
requirements: []

must_haves:
  truths:
    - Python virtual environment exists and can be activated
    - All project dependencies are installed in the virtual environment
    - Developer can run scripts using the venv Python interpreter
  artifacts:
    - path: ".venv/"
      provides: "uv-managed virtual environment"
      min_lines: 0
    - path: ".gitignore"
      provides: "venv exclusion"
      contains: ".venv"
    - path: "README.md"
      provides: "Updated setup instructions"
      contains: "uv venv"
  key_links:
    - from: "requirements.txt"
      to: ".venv/lib/python3.12/site-packages/"
      via: "uv pip install"
      pattern: "uv pip install -r requirements.txt"
---

<objective>
Set up a Python virtual environment using `uv` instead of the current conda-based approach.

Purpose: Modernize the development environment setup using the faster, more lightweight `uv` tool while maintaining compatibility with existing dependencies.
Output: A working `.venv/` directory with all dependencies installed, updated .gitignore, and revised README instructions.
</objective>

<execution_context>
@/home/mun/development/scipop/.opencode/get-shit-done/workflows/execute-plan.md
@/home/mun/development/scipop/.opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/STATE.md
@requirements.txt
@README.md
@.gitignore

Current setup uses conda with Python 3.12. The project has 17 dependencies in requirements.txt.
`uv` is already installed at version 0.11.7.
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create virtual environment and install dependencies</name>
  <files>.venv/, .gitignore</files>
  <action>
    1. Create a Python 3.12 virtual environment using uv: `uv venv --python 3.12`
    2. Activate the virtual environment and install all dependencies: `source .venv/bin/activate && uv pip install -r requirements.txt`
    3. Update .gitignore to exclude the virtual environment directory by adding `.venv/` to the file
    4. Verify all packages are installed correctly by listing installed packages: `uv pip list`
  </action>
  <verify>
    <automated>
      source .venv/bin/activate && python --version | grep "3.12" && uv pip list | grep -E "streamlit|bertopic|langchain" && grep -q "^\.venv" .gitignore
    </automated>
  </verify>
  <done>
    - .venv/ directory exists with Python 3.12
    - All 17 requirements.txt dependencies are installed
    - .gitignore contains .venv/ entry
    - uv pip list shows streamlit, bertopic, and langchain packages
  </done>
</task>

<task type="auto">
  <name>Task 2: Update README with uv-based setup instructions</name>
  <files>README.md</files>
  <action>
    Replace the conda-based "Environment setup" section in README.md with uv-based instructions:
    
    New section should include:
    1. Prerequisites: Install uv (link to https://docs.astral.sh/uv/getting-started/installation/)
    2. Create virtual environment: `uv venv --python 3.12`
    3. Activate environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
    4. Install dependencies: `uv pip install -r requirements.txt`
    5. Optional note: Original conda setup preserved in git history if needed
    
    Keep the same structure and tone as the existing README. Place this under the existing "# Environment setup" heading.
  </action>
  <verify>
    <automated>
      grep -q "uv venv" README.md && grep -q "uv pip install" README.md && ! grep -q "conda create" README.md
    </automated>
  </verify>
  <done>
    - README.md "Environment setup" section uses uv commands
    - No conda references remain in the setup instructions
    - Instructions are clear and follow the same structure as before
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Developer machine → PyPI | Downloading dependencies from public package registry |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-quick-01 | T (Tampering) | PyPI packages | accept | Trust PyPI's package signing; uv verifies package integrity via checksums |
| T-quick-02 | I (Information Disclosure) | keys.py exposure | mitigate | Already mitigated — keys.py excluded in .gitignore line 2; verify .venv/ also excluded |
</threat_model>

<verification>
After task completion:
1. Verify Python version: `source .venv/bin/activate && python --version`
2. Verify key dependencies: `uv pip list | grep -E "streamlit|bertopic|langchain|pypdf"`
3. Verify activation script exists: `ls .venv/bin/activate`
4. Verify README instructions are accurate by following them in a separate test directory (manual step for user if desired)
</verification>

<success_criteria>
- [ ] .venv/ directory created with Python 3.12 interpreter
- [ ] All 17 packages from requirements.txt installed successfully
- [ ] .gitignore includes .venv/ entry
- [ ] README.md updated with uv-based setup instructions
- [ ] No conda references in README setup section
- [ ] Virtual environment can be activated and Python scripts can run
</success_criteria>

<output>
After completion, create `.planning/quick/260430-okr-set-up-python-virtual-environment-using-/260430-okr-SUMMARY.md`
</output>
