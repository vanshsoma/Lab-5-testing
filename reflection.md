**Q.1) Which issues were the easiest to fix, and which were the hardest? Why?**

Ans) The easiest issues to fix were the stylistic ones like naming conventions (C0103), unused imports (F401), and whitespace/newline errors (C0304, E302). These are mechanical changes that don't require deep logical analysis. The trickiest was the logging-fstring-interpolation (W1203) warning, not because the reason (lazy evaluation) is a subtle performance concept that isn't immediately obvious.

**Q.2) Did the static analysis tools report any false positives? If so, describe one example.**

Ans) There were no clear false positives, every issue flagged by the tools, including the security warning from Bandit (eval-used), the bug risks from Pylint (bare except), and the style issues from Flake8 (whitespace), pointed to a legitimate area for improvement in security, robustness, or adherence to Python best practices.

**Q.3) How would you integrate static analysis tools into your actual software development workflow**

Ans) I would integrate them at two key points. First, locally as a pre-commit hook using a tool like pre-commit. This would run Flake8 and Bandit on staged files, preventing bad code from ever entering the repository. Second, I would add them as a required check in the Continuous Integration (CI) pipeline to run Pylint, Bandit, and Flake8 on every pull request, ensuring no new issues are merged.

**Q.4) What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

Ans) The code is now more robust and professional. By removing eval() and the bare except, we eliminated a major security hole and a source of silent, hard-to-debug errors. Proper file handling with with open() prevents resource leaks. Finally, the addition of docstrings, input validation, and proper logging makes the code infinitely more readable, secure, and maintainable.
