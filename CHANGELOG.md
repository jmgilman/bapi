# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `/directive/id/{id}` endpoint for getting a directive by ID
- `/file` endpoint for getting the entire ledger contents
- `filter` query parameter for filtering results with JMESPath
- `search` query parameter for performing full-text searches
- In-depth documentation
- Support for Redis as a storage backend
- Background task for invalidating the cache automatically

### Changed

- Refactored codebase to make use of `bdantic`
- Tests now use raw JSON dumps for validation
- Docstrings expanded and updated
- Integration support for various auth/storage backends was improved
- Most routes changed to be asynchronous

## [0.2.0] - 2022-01-24

### Added

- Adds endpoint for querying Beancount data using BQL queries
- Adds endpoints for generating Beancount directive syntax

### Changed

- Custom directive updated to be more explicit about what types it accepts

## [0.1.0] - 2022-01-23

### Added

- Initial release

[unreleased]: https://github.com/jmgilman/bapi/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/jmgilman/bapi/releases/tag/v0.2.0
[0.1.0]: https://github.com/jmgilman/bapi/releases/tag/v0.1.0
