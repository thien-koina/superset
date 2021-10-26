from superset.security import SupersetSecurityManager
import logging

logger = logging.getLogger("google_login")


class CustomSsoSecurityManager(SupersetSecurityManager):
    def oauth_user_info(self, provider, response=None):
        logging.debug("Oauth2 provider: {0}.".format(provider))
        if provider == "google":
            res = self.appbuilder.sm.oauth_remotes[provider].get("userinfo")
            if res.status_code != 200:
                logger.error("Failed to obtain user info: %s", res.data)
                return

            me = res.json()
            logger.debug(" user_data: %s", me)

            username = me["email"].split("@")[0]
            return {
                "name": me["name"],
                "email": me["email"],
                "id": username,
                "username": username,
                "first_name": me["given_name"],
                "last_name": me["family_name"],
            }
