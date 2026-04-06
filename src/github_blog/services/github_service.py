import structlog
from github import Auth, Github
from github.Issue import Issue
from github.Repository import Repository
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger()


class GitHubService:
    def __init__(self, token: str):
        self.gh = self._login(token)

    def _login(self, token: str) -> Github:
        try:
            # Compatibility with different PyGithub versions
            if hasattr(Auth, "Token"):
                return Github(auth=Auth.Token(token))
            return Github(token)
        except Exception as e:
            logger.error("github_login_failed", error=str(e))
            raise

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def get_repo(self, repo_name: str) -> Repository:
        return self.gh.get_repo(repo_name)

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def get_user_issues(self, repo: Repository) -> list[Issue]:
        me = self.gh.get_user().login
        issues = repo.get_issues(creator=me)  # type: ignore
        return list(issues)
