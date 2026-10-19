"""Links oficiais das redes sociais da Conceito Prime."""

SOCIAL_FACEBOOK = "https://www.facebook.com/ConceitoPrimeSE/"
SOCIAL_INSTAGRAM = "https://www.instagram.com/conceitoprimese/"
SOCIAL_LINKEDIN = "https://www.linkedin.com/company/conceito-prime/"

_SOCIAL_ATTRS = 'target="_blank" rel="noopener noreferrer"'


def render_contact_social_rail():
    return f"""        <aside class="contact-social-rail" aria-label="Redes sociais">
          <a href="{SOCIAL_FACEBOOK}" {_SOCIAL_ATTRS} aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
          <a href="{SOCIAL_INSTAGRAM}" {_SOCIAL_ATTRS} aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          <a href="{SOCIAL_LINKEDIN}" {_SOCIAL_ATTRS} aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
        </aside>"""


def render_contact_social_mobile():
    return f"""          <div class="contact-social-mobile" aria-label="Redes sociais">
            <a href="{SOCIAL_FACEBOOK}" {_SOCIAL_ATTRS} aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="{SOCIAL_INSTAGRAM}" {_SOCIAL_ATTRS} aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="{SOCIAL_LINKEDIN}" {_SOCIAL_ATTRS} aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
          </div>"""


def render_footer_social():
    """Rodapé: só o Instagram, como @conceitoprimese (as redes não aparecem mais nos formulários)."""
    return f"""          <div class="flex">
            <a href="{SOCIAL_INSTAGRAM}" {_SOCIAL_ATTRS} class="footer-insta inline-flex items-center gap-3 text-white hover:text-gold-400 transition-colors duration-300"><span class="w-10 h-10 rounded-full border border-white/20 flex items-center justify-center"><i class="fab fa-instagram" aria-hidden="true"></i></span><span class="text-[15px] font-light">@conceitoprimese</span></a>
          </div>"""
