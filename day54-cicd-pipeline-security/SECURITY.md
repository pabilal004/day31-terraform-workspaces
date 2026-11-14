# Security policy

This repository is a learning lab. Do not add real passwords, API keys, tokens, private certificates, or production data.

If a credential is accidentally committed:
1. Revoke or rotate it immediately; deleting the file or commit is not enough.
2. Review repository access and relevant service logs.
3. Remove the exposed value from repository history where appropriate.
4. Store replacement credentials in GitHub Actions secrets or an approved secrets manager.

Report security issues privately to the repository maintainer rather than opening a public issue containing sensitive details.
