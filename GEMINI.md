# Flask CRM Application

## Purpose

This is a Flask-based Customer Relationship Management (CRM) application specifically designed for managing donors and their donations.

## Guiding Principles (TIGER Style)

This project adheres to the TIGER style of development, which emphasizes the following:

*   **Lean:** Keep the codebase concise and avoid unnecessary complexity.
*   **Efficient:** Write performant code and be mindful of resource management (e.g., database connections).
*   **Modern:** Use modern Python features and libraries (e.g., `factory-boy` for tests, proper timezone handling).
*   **Strictly Organized:** Maintain a clear and logical project structure, separating concerns into blueprints, services, and forms.
*   **Aggressively Refactored:** Continuously improve the code by eliminating redundancy and improving clarity.

## Development Workflow

*   **Testing:** All new features must be accompanied by thorough unit tests. The goal is to maintain 100% test coverage.
*   **Dependency Management:** Runtime and development dependencies are kept in separate `requirements.txt` and `requirements-dev.txt` files, respectively, with versions pinned.
*   **Commits:** Changes are not autocommitted. Commits are made manually after verification and user approval.
