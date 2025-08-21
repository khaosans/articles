# Contributing to AI/ML Roles and Workflows Documentation

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/ai-ml-roles-workflows.git
   cd ai-ml-roles-workflows
   ```
3. Install dependencies:
   ```bash
   make install-dev
   ```

## 📝 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Run Quality Checks
```bash
make all  # Runs all checks: clean, install-dev, format, lint, test, verify
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 🎨 Coding Standards

### Python Code
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused

### Mermaid Diagrams
- Use descriptive names for nodes
- Include comments for complex logic
- Test diagrams with the verification tools
- Use enhanced styling for better readability

### Documentation
- Write clear, concise documentation
- Include examples where appropriate
- Keep documentation up to date

## 🧪 Testing

### Running Tests
```bash
make test
```

### Adding Tests
- Add tests for new functionality
- Ensure all tests pass before submitting
- Use descriptive test names

## 📊 Diagram Guidelines

### Creating New Diagrams
1. Create the diagram in `/extracted_diagrams/`
2. Use descriptive filenames
3. Run enhancement script:
   ```bash
   make enhance
   ```
4. Verify the diagram:
   ```bash
   make verify
   ```

### Diagram Best Practices
- Use clear, descriptive labels
- Include emojis for visual hierarchy
- Use consistent color schemes
- Keep diagrams focused and readable

## 🔍 Code Review Process

1. **Automated Checks**: All PRs must pass CI checks
2. **Review**: At least one maintainer must approve
3. **Documentation**: Ensure documentation is updated
4. **Testing**: All tests must pass

## 📋 Pull Request Guidelines

### PR Title Format
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### PR Description
Include:
- Summary of changes
- Motivation for changes
- Testing performed
- Screenshots (if applicable)

## 🐛 Reporting Issues

### Bug Reports
Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment information

### Feature Requests
Include:
- Clear description of the feature
- Use cases
- Proposed implementation (if any)

## 📞 Getting Help

- Open an issue for questions or problems
- Join our community discussions
- Check existing documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
