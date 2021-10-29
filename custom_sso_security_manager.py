import logging
from typing import Optional

from werkzeug.wrappers import Response as WerkzeugResponse
import jwt
from flask import flash, g, redirect, request, session, url_for
from flask_appbuilder import expose
from flask_appbuilder.security.views import AuthOAuthView
from flask_appbuilder._compat import as_unicode
from superset.security import SupersetSecurityManager


logger = logging.getLogger("google_login")


class CustomAuthOAuthView(AuthOAuthView):
    @expose("/login/")
    @expose("/login/<provider>")
    @expose("/login/<provider>/<register>")
    def login(
        self, provider: Optional[str] = None, register: Optional[str] = None
    ) -> WerkzeugResponse:
        logger.debug("Provider: {0}".format(provider))
        if g.user is not None and g.user.is_authenticated:
            logger.debug("Already authenticated {0}".format(g.user))
            return redirect(self.appbuilder.get_url_for_index)

        if provider is None:
            return self.render_template(
                self.login_template,
                providers=self.appbuilder.sm.oauth_providers,
                title=self.title,
                appbuilder=self.appbuilder,
            )

        logger.debug("Going to call authorize for: {0}".format(provider))
        state = jwt.encode(
            request.args.to_dict(flat=False),
            self.appbuilder.app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        try:
            if register:
                logger.debug("Login to Register")
                session["register"] = True
            if provider == "twitter":
                return self.appbuilder.sm.oauth_remotes[provider].authorize_redirect(
                    redirect_uri=url_for(
                        ".oauth_authorized",
                        provider=provider,
                        _external=True,
                        state=state,
                    )
                )
            else:
                return self.appbuilder.sm.oauth_remotes[provider].authorize_redirect(
                    redirect_uri=url_for(
                        ".oauth_authorized", provider=provider, _external=True
                    ),
                    state=state.decode("ascii") if isinstance(state, bytes) else state,
                )
        except Exception as e:
            logger.error("Error on OAuth authorize: {0}".format(e))
            flash(as_unicode(self.invalid_login_message), "warning")
            return redirect(self.appbuilder.get_url_for_index)


class CustomSsoSecurityManager(SupersetSecurityManager):
    authoauthview = CustomAuthOAuthView

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
